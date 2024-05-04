import os
import glob
import inspect
import time

import yaml

import numpy as np
import matplotlib.pyplot as plt

import scipy.ndimage as nd
from scipy.special import huber

import astropy.io.fits as pyfits

import jwst.datamodels

from grizli import utils
import msaexp.utils as msautils

utils.LOGFILE = "/tmp/msaexp_slit_combine.log.txt"

# Cross-dispersion pixel scale computed from one of the fixed slits
PIX_SCALE = 0.10544

# Default MSA nod offset
MSA_NOD_ARCSEC = 0.529

EVAL_COUNT = 0
CHI2_MASK = None
SKIP_COUNT = 10000
CENTER_WIDTH = 0.1
CENTER_PRIOR = 0.0
SIGMA_PRIOR = 0.6

HUBER_ALPHA = 7

PRISM_MAX_VALID = 10000
PRISM_MIN_VALID_SN = -3
SPLINE_BAR_GRATINGS = [
    "PRISM",
    "G395M",
    "G235M",
    "G140M",
    "G395H",
    "G235H",
    "G140H",
]

WING_SIGMA = 2.0
SCALE_FWHM = 1.0
DEFAULT_WINGS = None
WINGS_XOFF = None


def split_visit_groups(
    files, join=[0, 3], gratings=["PRISM"], split_uncover=True, verbose=True
):
    """
    Compute groupings of `SlitModel` files based on exposure, visit, detector,
    slit_id

    Parameters
    ----------
    files : list
        List of `SlitModel` files

    join : list
        Indices of ``files[i].split('[._]') + GRATING`` to join as a group

    gratings : list
        List of NIRSpec gratings to consider

    Returns
    -------
    groups : dict
        File groups

    """
    keys = []
    all_files = []
    for file in files:
        with pyfits.open(file) as im:
            if im[0].header["GRATING"] not in gratings:
                continue

            fk = "_".join(
                [
                    os.path.basename(file).replace(".", "_").split("_")[i]
                    for i in join
                ]
            )

            key = f"{fk}-{im[0].header['GRATING']}"

            keys.append(key.lower())
            all_files.append(file)

    keys = np.array(keys)
    un = utils.Unique(keys, verbose=False)
    groups = {}
    for k in np.unique(keys):
        if split_uncover & (un[k].sum() % 6 == 0) & ("jw02561" in files[0]):
            msg = "split_visit_groups: split UNCOVER sub groups "
            msg += f"{k} N={un[k].sum()}"
            utils.log_comment(utils.LOGFILE, msg, verbose=verbose)

            ksp = k.split("-")

            groups[ksp[0] + "a-" + ksp[1]] = np.array(all_files)[un[k]][
                0::2
            ].tolist()

            groups[ksp[0] + "b-" + ksp[1]] = np.array(all_files)[un[k]][
                1::2
            ].tolist()
        else:
            groups[k] = np.array(all_files)[un[k]].tolist()

    return groups


def slit_prf_fraction(
    wave,
    sigma=0.0,
    x_pos=0.0,
    slit_width=0.2,
    pixel_scale=PIX_SCALE,
    verbose=True,
):
    """
    Rough slit-loss correction given derived source width and x_offset shutter centering

    Parameters
    ----------
    sigma : float
        Derived source width (pixels) in quadtrature with the tabulated intrinsic PSF
        width from ``msaexp.utils.get_nirspec_psf_fwhm``

    wave : array-like, float
        Spectrum wavelengths, microns

    x_pos : float
        Shutter-normalized source center in range (-0.5, 0.5) (``source_xpos`` in slit
        metadata)

    slit_width : float
        Slit/shutter width, arcsec

    pixel_scale : float
        NIRSpec pixel scale, arcsec/pix

    Returns
    -------
    prf_frac : array-like
        Wavelength-dependent flux fraction within the shutter

    """
    from msaexp.resample_numba import pixel_integrated_gaussian_numba as PRF

    global SCALE_FWHM

    # Tabulated PSF FWHM, pix
    psf_fw = msautils.get_nirspec_psf_fwhm(wave) * SCALE_FWHM

    pix_center = np.zeros_like(wave)
    pix_mu = x_pos * slit_width / pixel_scale
    pix_sigma = np.sqrt((psf_fw / 2.35) ** 2 + sigma**2)

    msg = f"slit_prf_fraction: mu = {pix_mu:.2f}, sigma = {sigma:.1f} pix"
    utils.log_comment(utils.LOGFILE, msg, verbose=verbose)

    dxpix = slit_width / pixel_scale
    prf_frac = (
        PRF(pix_center, pix_mu, pix_sigma, dx=dxpix, normalization=1) * dxpix
    )

    return prf_frac


def objfun_prof_trace(
    theta,
    base_coeffs,
    wave,
    xpix,
    ypix,
    yslit0,
    diff,
    vdiff,
    mask,
    ipos,
    ineg,
    sh,
    fix_sigma,
    force_positive,
    verbose,
    ret,
):
    """ """
    from msaexp.resample_numba import pixel_integrated_gaussian_numba as PRF

    global EVAL_COUNT
    global CHI2_MASK
    global SKIP_COUNT
    global CENTER_WIDTH
    global CENTER_PRIOR
    global SIGMA_PRIOR
    global SCALE_FWHM
    global WING_SIGMA
    global DEFAULT_WINGS
    global WINGS_XOFF

    EVAL_COUNT += 1

    wings = DEFAULT_WINGS

    if fix_sigma > 0:
        sigma = fix_sigma / 10.0
        i0 = 0
    elif WINGS_XOFF is not None:
        sigma = theta[0] / 10.0
        wings = theta[1 : len(WINGS_XOFF) + 1]
        i0 = len(WINGS_XOFF) + 1

    elif len(theta) == 4:
        sigma = WING_SIGMA / 10
        wings = np.append(theta[:2], 0)  # [theta[1], 3.]
        i0 = 2
        if DEFAULT_WINGS is not None:
            sigma = theta[0] / 10.0
            wings = DEFAULT_WINGS
            i0 = 1

    elif len(theta) >= 5:
        sigma = WING_SIGMA / 10
        wings = theta[:3]
        i0 = 3

        if DEFAULT_WINGS is not None:
            sigma = theta[0] / 10.0
            wings = DEFAULT_WINGS
            i0 = 1

    else:
        if DEFAULT_WINGS is not None:
            sigma = theta[0] / 10.0
            wings = DEFAULT_WINGS

        sigma = theta[0] / 10.0
        i0 = 1

    # print('xxx', sigma, wings, theta[i0:])
    yslit = yslit0 * 1.0
    for j in np.where(ipos)[0]:
        xj = (xpix[j, :] - sh[1] / 2) / sh[1]
        _ytr = np.polyval(theta[i0:], xj)
        _ytr += np.polyval(base_coeffs, xj)
        yslit[j, :] = ypix[j, :] - _ytr

    psf_fw = msautils.get_nirspec_psf_fwhm(wave) * SCALE_FWHM

    # sig2 = np.sqrt((psf_fw / 2.35)**2 + sigma**2)
    sig2 = np.sqrt((psf_fw / 2.35) ** 2 + sigma**2)

    # wings = (0.05, 2)

    ppos = PRF(yslit[ipos, :].flatten(), 0.0, sig2[ipos, :].flatten(), dx=1)
    if WINGS_XOFF is not None:
        for wx, wn in zip(WINGS_XOFF, wings):
            ppos += wn * PRF(
                yslit[ipos, :].flatten() + wx,
                0.0,
                sig2[ipos, :].flatten(),
                dx=1,
            )

    elif wings is not None:
        ppos += wings[0] * PRF(
            yslit[ipos, :].flatten() + wings[2],
            0.0,
            sig2[ipos, :].flatten() * wings[1],
            dx=1,
        )

    ppos = ppos.reshape(yslit[ipos, :].shape)

    if ineg.sum() > 0:
        pneg = PRF(
            yslit[ineg, :].flatten(), 0.0, sig2[ineg, :].flatten(), dx=1
        )
        if WINGS_XOFF is not None:
            for wx, wn in zip(WINGS_XOFF, wings):
                pneg += wn * PRF(
                    yslit[ineg, :].flatten() + wx,
                    0.0,
                    sig2[ineg, :].flatten(),
                    dx=1,
                )
        elif wings is not None:
            pneg += wings[0] * PRF(
                yslit[ineg, :].flatten() + wings[2],
                0.0,
                sig2[ineg, :].flatten() * wings[1],
                dx=1,
            )

        pneg = pneg.reshape(yslit[ineg, :].shape)
    else:
        pneg = np.zeros_like(ppos)

    if 0:
        ppos = np.nansum(ppos, axis=0) / ipos.sum()
        if ineg.sum() > 0:
            pneg = np.nansum(pneg, axis=0) / ineg.sum()
        else:
            pneg = np.zeros_like(ppos)
    else:
        ppos = np.nansum(ppos, axis=0) / np.nansum(mask[ipos, :], axis=0)
        if ineg.sum() > 0:
            pneg = np.nansum(pneg, axis=0) / np.nansum(mask[ineg, :], axis=0)
        else:
            pneg = np.zeros_like(ppos)

    pdiff = ppos - pneg

    if (pneg.sum() == 0) & (len(theta) == 1000):
        bkg = theta[2] / 10.0
    else:
        bkg = 0.0

    if force_positive:
        pdiff *= pdiff > 0

    # Remove any masked pixels
    pmask = mask.sum(axis=0) == mask.shape[0]

    snum = np.nansum(
        ((diff - bkg) * pdiff / vdiff * pmask).reshape(sh), axis=0
    )
    sden = np.nansum((pdiff**2 / vdiff * pmask).reshape(sh), axis=0)
    smod = snum / sden * pdiff.reshape(sh)

    chi = (diff - (smod + bkg).flatten()) / np.sqrt(vdiff)

    if 0:
        # two-sided
        # CHI2_MASK = (chi < 40) & (chi > -10)
        # CHI2_MASK &= ((smod+bkg).flatten()/np.sqrt(vdiff) > -10)
        CHI2_MASK = diff / np.sqrt(vdiff) > -10

    elif 0:
        # absolute value
        CHI2_MASK = chi**2 < 40**2
    else:
        # no mask
        CHI2_MASK = np.isfinite(diff)

    ok = np.isfinite(chi)
    chi2 = np.nansum(huber(HUBER_ALPHA, chi[CHI2_MASK & ok]))

    # "prior" on sigma with logistic bounds
    peak = 10000
    chi2 += peak / (1 + np.exp(-10 * (sigma - 1.8)))  # right
    chi2 += peak - peak / (1 + np.exp(-30 * (sigma - 0)))  # left
    chi2 += (sigma - SIGMA_PRIOR) ** 2 / 2 / PIX_SCALE**2
    chi2 += (
        (np.array(theta[i0:]) - CENTER_PRIOR) ** 2 / 2 / CENTER_WIDTH**2
    ).sum()

    if (EVAL_COUNT % SKIP_COUNT == 0) | (ret == 1):
        tval = " ".join([f"{t:6.3f}" for t in theta[i0:]])
        tfix = "*" if i0 == 0 else " "
        msg = f"{EVAL_COUNT:>8} {tfix}sigma={sigma*10:.2f}{tfix}"
        msg += f" [{tval}]  {chi2:.1f}"
        utils.log_comment(utils.LOGFILE, msg, verbose=verbose)

    if ret == 1:
        trace_coeffs = theta[i0:]
        return snum, sden, smod, sigma, trace_coeffs, chi2
    else:
        return chi2


class SlitGroup:
    def __init__(
        self,
        files,
        name,
        position_key="position_number",
        diffs=True,
        stuck_threshold=0.5,
        bad_shutter_names=None,
        undo_barshadow=False,
        sky_arrays=None,
        undo_pathloss=True,
        trace_with_xpos=False,
        trace_with_ypos=True,
        trace_from_yoffset=False,
        nod_offset=None,
        pad_border=2,
        reference_exposure="auto",
        **kwargs,
    ):
        """
        Container for a list of 2D extracted ``SlitModel`` files

        Parameters
        ----------
        files : list
            List of `SlitModel` files

        name : str
            Label for the group

        position_key : str
            Column in the ``info`` table to define the nod positions

        diffs : bool
            Compute nod differences

        stuck_threshold : float
            Parameter for identifying stuck-closed shutters in prism spectra in
            `~msaexp.slit_combine.SlitGroup.mask_stuck_closed_shutters`

        bad_shutter_names : list, None
            List of integer shutter indices (e.g., among ``[-1, 0, 1]`` for a
            3-shutter slitlet) to mask as bad, e.g., from stuck shutters

        undo_barshadow : bool
            Undo the ``BarShadow`` correction if an extension found in the
            slit model files

        sky_arrays : array-like
            Optional sky data (in progress)

        undo_pathloss : bool
            Remove the pathloss correction if the extensions found in the slit
            model files

        trace_with_ypos : bool
            Compute traces including the predicted source center

        nod_offset : float, None
            Nod offset size (pixels) to use if the slit model traces don't
            already account for it, e.g., in background-indicated slits
            without explicit catalog sources.  If not provided (None), then set
            to `MSA_NOD_ARCSEC / slit_pixel_scale`.

        reference_exposure : int, 'auto'
            Define a reference nod position. If ``'auto'``, then will use the
            exposure in the middle of the nod offset distribution

        pad_border : int
            Grow mask around edges of 2D cutouts

        Attributes
        ----------
        sh : (int, int)
            Dimensions of the 2D slit data

        sci : array-like (float)
            Science data with dimensions ``(N, sh[0]*sh[1])``

        dq : array-like (int)
            DQ bit flags

        mask : array-like (bool)
            Valid data

        var : array-like (float)
            Variance data

        var_flat: array-like (float)
            VAR_FLAT variance data

        xslit : array-like (float)
            Array of x slit coordinates

        yslit: array-like (float)
            Array of cross-dispersion coordinates. Should be zero along the
            expected center of the (curved) trace

        yslit_orig : array-like (float)
            Copy of ``yslit``, which may be updated with new trace coefficients

        ypix : array-like (float)
            y pixel coordinates

        wave : array-like (float)
            2D wavelengths

        bar : array-like (float)
            The BarShadow correction if found in the `SlitModel` files

        xtr : array-like (float)
            1D x pixel along trace

        ytr : array-like (float)
            1D y trace position

        wtr : array-like (float)
            Wavelength along the trace

        """
        self.name = name

        self.slits = []
        keep_files = []

        self.sky_arrays = sky_arrays

        # kwargs to meta dictionary
        self.meta = {
            "diffs": diffs,
            "trace_with_xpos": trace_with_xpos,
            "trace_with_ypos": trace_with_ypos,
            "trace_from_yoffset": trace_from_yoffset,
            "stuck_threshold": stuck_threshold,
            "bad_shutter_names": bad_shutter_names,
            "undo_barshadow": undo_barshadow,
            "wrapped_barshadow": False,
            "own_barshadow": False,
            "nod_offset": nod_offset,
            "undo_pathloss": undo_pathloss,
            "reference_exposure": reference_exposure,
            "pad_border": pad_border,
            "position_key": position_key,
        }

        # Comments on meta for header keywords
        self.meta_comment = {
            "diffs": "Calculated with exposure differences",
            "trace_with_xpos": "Trace includes x offset in shutter",
            "trace_with_ypos": "Trace includes y offset in shutter",
            "trace_from_yoffset": "Trace derived from yoffsets",
            "stuck_threshold": "Stuck shutter threshold",
            # 'bad_shutter_names': bad_shutter_names,
            "undo_barshadow": "Bar shadow update behavior",
            "wrapped_barshadow": "Bar shadow was wrapped for central shutter",
            "own_barshadow": "Internal bar shadow correction applied",
            "nod_offset": "Nod offset size, pixels",
            "undo_pathloss": "Remove pipeline pathloss correction",
            "reference_exposure": "Reference exposure argument",
            "pad_border": "Border padding",
            "position_key": "Method for determining offset groups",
        }

        self.shapes = []

        for i, file in enumerate(files):
            slit = jwst.datamodels.open(file)

            self.slits.append(slit)
            keep_files.append(file)
            self.shapes.append(slit.data.shape)

        self.files = keep_files
        self.info = self.parse_metadata()
        self.sh = np.min(np.array(self.shapes), axis=0)

        self.parse_data()

    @property
    def N(self):
        """
        Number of individual SlitModel components
        """
        return len(self.slits)

    @property
    def grating(self):
        """
        Grating used
        """
        return self.info["grating"][0]

    @property
    def filter(self):
        """
        Grating used
        """
        return self.info["filter"][0]

    @property
    def unp(self):
        """
        `grizli.utils.Unique` object for the different nod positions
        """
        return utils.Unique(
            self.info[self.meta["position_key"]], verbose=False
        )

    @property
    def calc_reference_exposure(self):
        """
        Define a reference exposure, usually middle of three nods
        """
        # if reference_exposure in ['auto']:
        #     reference_exposure = 1 if obj.N == 1 else 2 - ('bluejay' in root)
        if self.meta["reference_exposure"] in ["auto"]:
            if self.N < 3:
                ix = 0
            else:
                ix = np.nanargmin(np.abs(self.relative_nod_offset))

            ref_exp = self.info[self.meta["position_key"]][ix]
        else:
            ref_exp = self.meta["reference_exposure"]

        return ref_exp

    @property
    def source_ypixel_position(self):
        """
        Expected relative y pixel location of the source
        """
        for j, slit in enumerate(self.slits[:1]):

            _res = msautils.slit_trace_center(
                slit, with_source_ypos=False, index_offset=0.0
            )

            _xtr, _ytr0, _wtr0, slit_ra, slit_dec = _res

            _res = msautils.slit_trace_center(
                slit, with_source_ypos=True, index_offset=0.0
            )

            _xtr, _ytr1, _wtr1, slit_ra, slit_dec = _res

            # plt.plot(_ytr1 - _ytr0)
            trace_yoffset = np.nanmedian(_ytr1 - _ytr0)
            break

        return trace_yoffset

    @property
    def slit_pixel_scale(self):
        """
        Compute cross dispersion pixel scale from slit WCS

        Returns
        -------
        pix_scale : float
            Cross-dispersion pixel scale ``arcsec / pixel``

        """

        sl = self.slits[0]
        wcs = sl.meta.wcs
        d2s = wcs.get_transform("detector", "world")

        x0 = d2s(self.sh[1] // 2, self.sh[0] // 2)
        x1 = d2s(self.sh[1] // 2, self.sh[0] // 2 + 1)

        dx = np.array(x1) - np.array(x0)
        cosd = np.cos(x0[1] / 180 * np.pi)
        pix_scale = np.sqrt((dx[0] * cosd) ** 2 + dx[1] ** 2) * 3600.0

        return pix_scale

    @property
    def relative_nod_offset(self):
        """
        Compute relative nod offsets from the trace polynomial
        """
        if self.N == 1:
            return np.array([0])

        y0 = np.array([c[-1] for c in self.base_coeffs])
        return y0 - np.median(y0)

    @property
    def fixed_yshutter(self):
        """
        Fixed cross-dispersion shutter coordinates
        """
        if self.meta["position_key"] == "manual_position":
            shutter_y = (self.yshutter + self.source_ypixel_position - 1.0) / 5
        else:
            shutter_y = (self.yshutter + self.source_ypixel_position) / 5

        return shutter_y

    def slit_metadata(self):
        """
        Make a table of the slit metadata
        """
        rows = []
        pscale = self.slit_pixel_scale * 1
        source_ypixel_position = self.source_ypixel_position * 1

        for i, sl in enumerate(self.slits):
            row = {
                "filename": sl.meta.filename,
                "nx": self.sh[1],
                "ny": self.sh[0],
            }

            for j in range(3):
                row[f"trace_c{j}"] = self.base_coeffs[i][j]

            row["slit_pixel_scale"] = pscale
            row["source_ypixel_position"] = source_ypixel_position

            for att in [
                "is_extended",
                "source_id",
                "source_name",
                "source_ra",
                "source_dec",
                "source_type",
                "source_xpos",
                "source_ypos",
                "shutter_state",
                "shutter_id",
                "slitlet_id",
                "slit_ymin",
                "slit_ymax",
                "quadrant",
                "xcen",
                "ycen",
                "xstart",
                "xsize",
                "ystart",
                "ysize",
            ]:
                row[att] = sl.__getattr__(att)

            inst = sl.meta.instrument.instance
            for k in [
                "detector",
                "grating",
                "filter",
                "msa_metadata_file",
                "msa_configuration_id",
                "msa_metadata_id",
            ]:
                if k in inst:
                    row[k] = inst[k]

            _exp = sl.meta.exposure.instance
            for k in [
                "exposure_time",
                "nframes",
                "ngroups",
                "nints",
                "readpatt",
                "start_time",
            ]:
                if k in _exp:
                    row[k] = _exp[k]

            _point = sl.meta.pointing.instance
            for k in _point:
                row[k] = _point[k]

            _dith = sl.meta.dither.instance
            for k in _dith:
                row[k] = _dith[k]

            rows.append(row)

        tab = utils.GTable(rows)
        return tab

    def parse_metadata(self, verbose=True):
        """
        Generate the `info` metadata attribute from the `slits` data

        Returns
        -------
        info : `~astropy.table.Table`
            Metadata table

        """
        rows = []
        for i, slit in enumerate(self.slits):
            msg = f"{i:>2} {slit.meta.filename} {slit.data.shape}"
            utils.log_comment(utils.LOGFILE, msg, verbose=True)

            md = slit.meta.dither.instance
            mi = slit.meta.instrument.instance
            rows.append(
                [
                    slit.meta.filename,
                    slit.meta.filename.split("_")[0],
                    slit.data.shape,
                ]
                + [md[k] for k in md]
                + [mi[k] for k in mi]
            )

        names = (
            ["filename", "visit", "shape"] + [k for k in md] + [k for k in mi]
        )

        info = utils.GTable(names=names, rows=rows)
        info["x_position"] = np.round(info["x_offset"] * 10) / 10.0
        info["y_position"] = np.round(info["y_offset"] * 10) / 10.0
        info["y_index"] = (
            utils.Unique(info["y_position"], verbose=False).indices + 1
        )

        return info

    def parse_data(self, verbose=True):
        """
        Read science, variance and trace data from the ``slits`` SlitModel
        files
        """
        import scipy.ndimage as nd

        global PRISM_MAX_VALID, PRISM_MIN_VALID_SN

        slits = self.slits

        if self.meta["nod_offset"] is None:
            self.meta["nod_offset"] = MSA_NOD_ARCSEC / self.slit_pixel_scale

        sl = (slice(0, self.sh[0]), slice(0, self.sh[1]))

        sci = np.array([slit.data[sl].flatten() * 1 for slit in slits])
        try:
            bar = np.array(
                [slit.barshadow[sl].flatten() * 1 for slit in slits]
            )
        except:
            bar = np.ones_like(sci)

        dq = np.array([slit.dq[sl].flatten() * 1 for slit in slits])
        var = np.array(
            [
                (slit.var_poisson + slit.var_rnoise)[sl].flatten()
                for slit in slits
            ]
        )
        var_flat = np.array(
            [slit.var_flat[sl].flatten() * 1 for slit in slits]
        )

        bad = sci == 0
        sci[bad] = np.nan
        var[bad] = np.nan
        var_flat[bad] = np.nan
        dq[bad] = 1
        if bar is not None:
            bar[bad] = np.nan

        sh = slits[0].data.shape
        yp, xp = np.indices(sh)

        # 2D
        xslit = []
        ypix = []
        yslit = []
        wave = []

        # 1D
        xtr = []
        ytr = []
        wtr = []

        attr_keys = [
            "source_ra",
            "source_dec",
            "source_xpos",
            "source_ypos",
            "shutter_state",
            "slitlet_id",
        ]

        self.info["shutter_state"] = "xxxxxxxx"

        for k in attr_keys:
            if k not in self.info.colnames:
                self.info[k] = 0.0

        for j, slit in enumerate(slits):

            _res = msautils.slit_trace_center(
                slit,
                with_source_xpos=False,
                with_source_ypos=self.meta["trace_with_ypos"],
                index_offset=0.0,
            )

            _xtr, _ytr, _wtr, slit_ra, slit_dec = _res

            xslit.append(xp[sl].flatten())
            yslit.append((yp[sl] - (_ytr[sl[1]])).flatten())
            ypix.append(yp[sl].flatten())

            wcs = slit.meta.wcs
            d2w = wcs.get_transform("detector", "world")

            _ypi, _xpi = np.indices(slit.data.shape)
            _ras, _des, _wave = d2w(_xpi, _ypi)

            if self.meta["trace_with_xpos"] & (slit.source_xpos is not None):
                _xres = msautils.slit_trace_center(
                    slit,
                    with_source_xpos=True,
                    with_source_ypos=self.meta["trace_with_ypos"],
                    index_offset=0.0,
                )
                _xwtr = _xres[2]
                dwave = _xwtr - _wtr
                dwave_step = np.nanpercentile(
                    dwave / np.gradient(_wtr), [5, 50, 95]
                )

                # Signs of source_xpos and dwave_step should be opposite
                sign = slit.source_xpos * dwave_step[1]
                if sign > 0:
                    dwave *= -1
                    dwave_step *= -1
                    _note = "(flipped)"
                else:
                    _note = ""

                msg = (
                    "  Apply wavelength correction for "
                    f"source_xpos = {slit.source_xpos:.2f}: {_note}"
                    f"dx = {dwave_step[0]:.2f} to {dwave_step[2]:.2f} pixels"
                )

                utils.log_comment(utils.LOGFILE, msg, verbose=verbose)

                _wave += np.interp(_xpi, _xtr, dwave)
                _wtr = _xwtr

            xtr.append(_xtr[sl[1]])
            ytr.append(_ytr[sl[1]])
            wtr.append(_wtr[sl[1]])

            wave.append(_wave[sl].flatten())

            for k in attr_keys:
                self.info[k][j] = getattr(slit, k)

        xslit = np.array(xslit)
        yslit = np.array(yslit)
        ypix = np.array(ypix)
        wave = np.array(wave)

        xtr = np.array(xtr)
        ytr = np.array(ytr)
        wtr = np.array(wtr)

        bad = (dq & 1025) > 0
        bad |= ~np.isfinite(sci) | (sci == 0)

        if self.grating in ["PRISM"]:
            bad |= sci > PRISM_MAX_VALID
            bad |= sci < PRISM_MIN_VALID_SN * np.sqrt(var)

        if self.meta["pad_border"] > 0:
            # grow mask around edges
            for i in range(len(slits)):
                ysl_i = wave[i, :].reshape(self.sh)
                msk = nd.binary_dilation(
                    ~np.isfinite(ysl_i), iterations=self.meta["pad_border"]
                )
                bad[i, :] |= (msk).flatten()

        sci[bad] = np.nan
        mask = np.isfinite(sci)
        var[~mask] = np.nan

        self.sci = sci
        self.dq = dq
        self.mask = mask & True
        self.bkg_mask = mask & True
        self.var = var
        self.var_flat = var_flat

        for j, slit in enumerate(slits):
            phot_scl = slit.meta.photometry.pixelarea_steradians * 1.0e12
            # phot_scl *= (slit.pathloss_uniform / slit.pathloss_point)[sl].flatten()
            # Remove pathloss correction
            if self.meta["undo_pathloss"]:
                if slit.source_type is None:
                    pl_ext = "PATHLOSS_UN"
                else:
                    pl_ext = "PATHLOSS_PS"

                with pyfits.open(self.files[j]) as sim:
                    if pl_ext in sim:
                        if verbose:
                            msg = f"   {self.files[j]} source_type={slit.source_type} "
                            msg += pl_ext
                            utils.log_comment(utils.LOGFILE, msg, verbose=True)

                        phot_scl *= (
                            sim[pl_ext].data.astype(sci.dtype)[sl].flatten()
                        )
                        self.meta["removed_pathloss"] = pl_ext

            self.sci[j, :] *= phot_scl
            self.var[j, :] *= phot_scl**2
            self.var_flat[j, :] *= phot_scl**2

        self.xslit = xslit
        self.yslit = yslit
        self.yslit_orig = yslit * 1
        self.ypix = ypix
        self.wave = wave

        self.bar = bar

        self.xtr = xtr
        self.ytr = ytr
        self.wtr = wtr

        if (self.info["source_ra"] < 0.0001).sum() == self.N:
            if self.N == -3:
                msg = "Seems to be a background slit.  "
                msg += "Force [0, {0}, -{0}]".format(self.meta["nod_offset"])
                msg += "pix offsets"
                utils.log_comment(utils.LOGFILE, msg, verbose=verbose)

                self.ytr[0, :] -= 1.0
                self.ytr[1, :] += -1 + self.meta["nod_offset"]
                self.ytr[2, :] -= 1 + self.meta["nod_offset"]

                self.info["manual_position"] = [2, 3, 1]
                self.meta["position_key"] = "manual_position"
            else:

                # offsets = self.info["y_position"] - self.info["y_position"][0]
                offsets = self.info["y_offset"] - self.info["y_offset"][0]
                offsets /= self.slit_pixel_scale

                # offsets = np.round(offsets / 5) * 5

                offstr = ", ".join(
                    [f"{_off:5.1f}" for _off in np.unique(offsets)]
                )

                msg = "Seems to be a background slit.  "
                msg += f"Force {offstr} pix offsets"
                utils.log_comment(utils.LOGFILE, msg, verbose=verbose)

                self.info["manual_position"] = offsets
                self.meta["position_key"] = "manual_position"

                for i, _off in enumerate(offsets):
                    self.ytr[i, :] += _off - 1

        elif (self.info["lamp_mode"][0] == "FIXEDSLIT") & (1):

            _dy = self.info["y_offset"] - np.median(
                self.info["y_offset"]
            )  # [0])
            _dy /= self.slit_pixel_scale

            msg = " Fixed slit: "
            _dystr = ", ".join([f"{_dyi:5.2f}" for _dyi in _dy])

            msg += f"force [{_dystr}] pix offsets"
            utils.log_comment(utils.LOGFILE, msg, verbose=verbose)

            for i, _dyi in enumerate(_dy):
                self.ytr[i, :] += 1 + _dyi

        elif self.meta["trace_from_yoffset"]:

            _dy = self.info["y_offset"] - self.info["y_offset"][0]
            _dy /= self.slit_pixel_scale

            msg = " Recomputed offsets slit: "
            _dystr = ", ".join([f"{_dyi:5.2f}" for _dyi in _dy])

            msg += f"force [{_dystr}] pix offsets"
            utils.log_comment(utils.LOGFILE, msg, verbose=verbose)

            for i, _dyi in enumerate(_dy):
                self.ytr[i, :] = self.ytr[0, :] + _dyi

        self.set_trace_coeffs(degree=2)

        if self.meta["undo_barshadow"] == 2:
            self.apply_spline_bar_correction()
            self.meta["undo_barshadow"] = False

        if self.meta["bad_shutter_names"] is None:
            self.mask_stuck_closed_shutters()
        else:
            self._apply_bad_shutter_mask()

    def set_trace_coeffs(self, degree=2):
        """
        Fit a polynomial to the trace

        Parameters
        ----------
        degree : int
            Polynomial degree of fit to the traces in the ``ytr`` attribute

        Sets the ``base_coeffs`` attribute and initializes ``trace_coeffs``
        with zeros

        """
        coeffs = []
        for i in range(self.N):
            xi = (self.xtr[i, :] - self.sh[1] / 2) / self.sh[1]
            yi = self.ytr[i, :]
            oki = np.isfinite(xi + yi)
            coeffs.append(np.polyfit(xi[oki], yi[oki], degree))

        self.base_coeffs = coeffs
        self.trace_coeffs = [c * 0.0 for c in coeffs]
        self.update_trace_from_coeffs()

    def update_trace_from_coeffs(self):
        """
        Update the ``yslit`` attribute based on the polynomial coefficients in
        the ``base_coeffs`` and ``trace_coeffs`` attributes

        """
        yslit = []
        yshutter = []

        for i in range(self.N):
            xi = (self.xtr[i, :] - self.sh[1] / 2) / self.sh[1]
            _ytr = np.polyval(self.base_coeffs[i], xi)
            if i == 0:
                _ytr0 = _ytr * 1.0

            _ytr += np.polyval(self.trace_coeffs[i], xi)
            yslit.append((self.ypix[i, :].reshape(self.sh) - _ytr).flatten())

            yshutter.append(
                (self.ypix[i, :].reshape(self.sh) - _ytr0).flatten()
            )

        self.yslit = np.array(yslit)
        self.yshutter = np.array(yshutter)

    def apply_spline_bar_correction(self, verbose=True):
        """
        Own bar shadow correction for PRISM derived from empty background shutters
        and implemented as a flexible bspline

        See `msaexp.utils.get_prism_bar_correction`.

        Parameters
        ----------
        verbose : bool
            Messaging

        Returns
        -------
        Rescales the ``sci`` data array and updates the ``mask``
        """
        global SPLINE_BAR_GRATINGS
        if self.grating.upper() not in SPLINE_BAR_GRATINGS:
            utils.log_comment(
                utils.LOGFILE,
                (
                    " apply_spline_bar_correction: "
                    + f" grating {self.grating.upper()} not in {SPLINE_BAR_GRATINGS}"
                ),
                verbose=verbose,
            )
            return None

        utils.log_comment(
            utils.LOGFILE,
            f" Run apply_spline_bar_correction",
            verbose=verbose,
        )

        bar, bar_wrapped = msautils.get_prism_bar_correction(
            self.fixed_yshutter,
            wrap="auto",
        )
        self.meta["wrapped_barshadow"] = bar_wrapped
        self.meta["own_barshadow"] = True

        self.sci *= self.bar / bar
        self.var *= 1.0 / bar**2
        self.orig_bar = self.bar * 1
        self.bar = bar * 1
        self.mask &= np.isfinite(self.sci)

    def mask_stuck_closed_shutters(self, stuck_threshold=0.3, min_bar=0.6):
        """
        Identify stuck-closed shutters in prism spectra

        Parameters
        ----------
        stuck_threshold : float
            1. Compute the median S/N of all pixels in each shutter of the slitlet
            2. If the slitlet is more than one shutter, mask shutters where
               ``sn_shutter < stuck_threshold * max(sn_shutters)``
            3. If the slitlet is a single shutter, mask the shutter if the absolute
               S/N is less than ``bad_shutter_names``

        min_bar : float
            Minimum value of the bar shadow mask to treat as valid pixels within a
            shutter

        Returns
        -------
        Updates ``bad_shutter_names`` attribute and runs
        `~msaexp.slit_combine.SlitGroup._apply_bad_shutter_mask`

        """
        if self.grating.upper() != "PRISM":
            self.meta["bad_shutter_names"] = []
            return None

        shutter_y = self.fixed_yshutter

        sn = self.sci / np.sqrt(self.var)

        bar_mask = self.mask & (self.bar > min_bar)
        if bar_mask.sum() == 0:
            self.meta["bad_shutter_names"] = []
            return None

        un = utils.Unique(
            np.cast[int](np.round(shutter_y[bar_mask])), verbose=False
        )
        sn_shutters = np.zeros(un.N, dtype=float)
        for i, v in enumerate(un.values):
            sn_shutters[i] = np.nanmedian(sn[bar_mask][un[v]])

        if un.N == 1:
            bad_shutter = sn_shutters < stuck_threshold
        else:
            bad_shutter = sn_shutters < stuck_threshold * sn_shutters.max()

        if bad_shutter.sum() > 0:
            bad_list = [un.values[i] for i in np.where(bad_shutter)[0]]

            self.meta["bad_shutter_names"] = bad_list
        else:
            self.meta["bad_shutter_names"] = []

        self._apply_bad_shutter_mask()

    def _apply_bad_shutter_mask(self, verbose=True):
        """
        Mask ``sci`` array for ``bad_shutter_names`` shutters
        """
        if len(self.meta["bad_shutter_names"]) == 0:
            return None

        utils.log_comment(
            utils.LOGFILE,
            f""" PRISM: stuck bad shutters {self.meta["bad_shutter_names"]}""",
            verbose=verbose,
        )

        for i in self.meta["bad_shutter_names"]:
            shutter_mask = np.abs(self.fixed_yshutter - i) < 0.5
            self.sci[shutter_mask] = np.nan
            self.mask &= np.isfinite(self.sci)

    @property
    def sky_background(self):
        """
        Optional sky-background data computed from the ``sky_arrays`` attribute

        Returns
        -------
        sky : array-like
            Sky data with dimensions ``(N, sh[0]*sh[1])``

        """
        if self.sky_arrays is not None:
            sky = np.interp(self.wave, *self.sky_arrays, left=-1, right=-1)
            sky[sky < 0] = np.nan
        else:
            sky = 0.0

        return sky

    @property
    def data(self):
        """
        Evaluate the ``sci`` data including optional ``sky_background`` and
        ``bar`` barshadow attributes

        Returns
        -------
        sci : array-like
            science data with dimensions ``(N, sh[0]*sh[1])``
        """
        sky = self.sky_background

        if self.meta["undo_barshadow"]:
            return (self.sci - sky) * self.bar
        else:
            return self.sci - sky

    def make_diff_image(self, exp=1):
        """
        Make a difference image for an individual exposure group

        Parameters
        ----------
        exp : int
            Exposure group

        Returns
        -------
        ipos : array-like
            Array indices of the "positive" exposures

        ineg : array-like
            Array indices of the "negative" exposures at the other nod
            positions

        diff : array-like
            Flattened difference image

        vdiff : array-like
            Flattened variance image

        """
        ipos = self.unp[exp]

        pos = np.nansum(self.data[ipos, :], axis=0) / np.nansum(
            self.mask[ipos, :], axis=0
        )

        vpos = (
            np.nansum(self.var[ipos, :], axis=0)
            / np.nansum(self.mask[ipos, :], axis=0) ** 2
        )
        #
        if self.meta["diffs"]:
            ineg = ~self.unp[exp]
            neg = np.nansum(self.data[ineg, :], axis=0) / np.nansum(
                self.bkg_mask[ineg, :], axis=0
            )
            vneg = (
                np.nansum(self.var[ineg, :], axis=0)
                / np.nansum(self.bkg_mask[ineg, :], axis=0) ** 2
            )
        else:
            ineg = np.zeros(self.N, dtype=bool)
            neg = np.zeros_like(pos)
            vneg = np.zeros_like(vpos)

        diff = pos - neg
        vdiff = vpos + vneg

        return ipos, ineg, diff, vdiff

    def plot_2d_differences(
        self,
        fit=None,
        clip_sigma=3,
        kws=dict(cmap="Blues", interpolation="hanning"),
        figsize=(6, 2),
    ):
        """ """
        Ny = self.unp.N
        if fit is None:
            Nx = 1
        else:
            Nx = 3

        fig, axes = plt.subplots(
            Ny,
            Nx,
            figsize=(figsize[0] * Nx, figsize[1] * Ny),
            sharex=True,
            sharey=True,
        )

        if Ny == Nx == 1:
            axes = [[axes]]

        ref_exp = self.calc_reference_exposure
        nods = self.relative_nod_offset

        for i, exp in enumerate(self.unp.values):
            ipos, ineg, diff, vdiff = self.make_diff_image(exp=exp)

            if fit is not None:
                model = fit[exp]["smod"]
            else:
                model = None

            vmax = clip_sigma * np.nanpercentile(np.sqrt(vdiff), 50)

            kws["vmin"] = -1 * vmax
            kws["vmax"] = 1.5 * vmax

            ax = axes[i][0]
            ax.imshow(
                diff.reshape(self.sh), aspect="auto", origin="lower", **kws
            )
            if i == 0:
                ax.text(
                    0.05,
                    0.95,
                    f"{self.name}",
                    ha="left",
                    va="top",
                    fontsize=10,
                    transform=ax.transAxes,
                    bbox={
                        "fc": "w",
                        "alpha": 0.1,
                        "ec": "None",
                    },
                )

            star = "*" if exp == ref_exp else " "
            spacer = " " * 5
            msg = f"exp={exp}{star}  nod={nods[ipos][0]:5.1f}"
            msg += f"{spacer}Npos = {ipos.sum()} {spacer}Nneg = {ineg.sum()}"

            ax.text(
                0.05,
                0.05,
                msg,
                ha="left",
                va="bottom",
                fontsize=8,
                transform=ax.transAxes,
                bbox={
                    "fc": "w",
                    "alpha": 0.1,
                    "ec": "None",
                },
            )

            if model is not None:
                axes[i][1].imshow(model, aspect="auto", origin="lower", **kws)
                axes[i][2].imshow(
                    diff.reshape(self.sh) - model,
                    aspect="auto",
                    origin="lower",
                    **kws,
                )

            for ax in axes[i]:
                for j in np.where(ipos)[0]:
                    xj = (self.xtr[j, :] - self.sh[1] / 2) / self.sh[1]
                    _ytr = np.polyval(self.trace_coeffs[j], xj)
                    _ytr += np.polyval(self.base_coeffs[j], xj)
                    _ = ax.plot(_ytr, color="tomato", alpha=0.3, lw=2)

                for j in np.where(ineg)[0]:
                    xj = (self.xtr[j, :] - self.sh[1] / 2) / self.sh[1]
                    _ytr = np.polyval(self.trace_coeffs[j], xj)
                    _ytr += np.polyval(self.base_coeffs[j], xj)
                    _ = ax.plot(_ytr, color="wheat", alpha=0.3, lw=2)

                # ax.grid()

        fig.tight_layout(pad=1)
        return fig

    def fit_all_traces(
        self, niter=3, dchi_threshold=-25, ref_exp=2, verbose=True, **kwargs
    ):
        """
        Fit all traces in the group
        """
        tfits = {}

        if ref_exp is None:
            exp_groups = self.unp.values
        else:
            exp_groups = [ref_exp]
            for p in self.unp.values:
                if p not in exp_groups:
                    exp_groups.append(p)

        if "evaluate" in kwargs:
            force_evaluate = kwargs["evaluate"]
        else:
            force_evaluate = None

        for k in range(niter):
            utils.log_comment(
                utils.LOGFILE, f"   fit_all_traces, iter {k}", verbose=verbose
            )

            for i, exp in enumerate(exp_groups):

                if k > 0:
                    kwargs["x0"] = tfits[exp]["theta"]

                if ref_exp is not None:
                    if exp != ref_exp:
                        kwargs["evaluate"] = True
                        kwargs["x0"] = tfits[ref_exp]["theta"]
                    else:
                        kwargs["evaluate"] = False
                else:
                    kwargs["evaluate"] = False

                if force_evaluate is not None:
                    kwargs["evaluate"] = force_evaluate

                tfits[exp] = self.fit_single_trace(exp=exp, **kwargs)
                dchi = tfits[exp]["chi2_fit"] - tfits[exp]["chi2_init"]

                msg = f"     Exposure group {exp}   dchi2 = {dchi:9.1f}"

                if (dchi < dchi_threshold) | (kwargs["evaluate"]):
                    msg += "\n"
                    for j in np.where(tfits[exp]["ipos"])[0]:
                        self.trace_coeffs[j] = tfits[exp]["trace_coeffs"]
                else:
                    msg += "*\n"

                utils.log_comment(utils.LOGFILE, msg, verbose=verbose)

            if ref_exp is not None:
                # Match all fits
                for i, exp in enumerate(exp_groups):
                    tfits[exp]["theta"] = tfits[ref_exp]["theta"]
                    tfits[exp]["trace_coeffs"] = tfits[ref_exp]["trace_coeffs"]
                    for j in np.where(tfits[exp]["ipos"])[0]:
                        self.trace_coeffs[j] = tfits[exp]["trace_coeffs"]

            self.update_trace_from_coeffs()

        return tfits

    def fit_single_trace(
        self,
        x0=None,
        initial_sigma=3.0,
        exp=1,
        force_positive=True,
        method="powell",
        tol=1.0e-6,
        evaluate=False,
        degree=2,
        sigma_bounds=(1, 20),
        trace_bounds=(-1, 1),
        fix_sigma=-1,
        with_bounds=True,
        verbose=True,
        **kwargs,
    ):
        """
        Fit profile width and trace offset polynomial to one of the nod traces

        Parameters
        ----------
        x0 : array-like, None
            Initial parameter guess

        initial_sigma : float
            Initial profile sigma to use (pixels*10)

        exp : int
            Exposure index (see ``unp``)

        force_positive : bool
            Don't consider the negative subtracted parts of the difference
            image

        method, tol : str, float
            Optimization parameters

        evaluate : bool
            Don't fit, just evaluate with given parameters

        degree : int
            Trace offset polynomial degree

        sigma_bounds : (float, float)
            Bounds on profile width

        trace_bounds : (float, float)
            Bounds on trace offset coefficients

        fix_sigma : float
            If ``fix_sigma > 0``, don't fit for the profile width but fix to
            this value

        with_bounds : bool
            Use ``sigma_bounds`` and ``trace_bounds`` in optimization

        Returns
        -------
        fit : dict
            Fit results

        """
        from scipy.optimize import minimize

        global EVAL_COUNT
        ipos, ineg, diff, vdiff = self.make_diff_image(exp=exp)

        base_coeffs = self.base_coeffs[np.where(ipos)[0][0]]

        args = (
            base_coeffs,
            self.wave,
            self.xslit,
            self.ypix,
            self.yslit,
            diff,
            vdiff,
            self.mask,
            ipos,
            ineg,
            self.sh,
            fix_sigma,
            force_positive,
            verbose,
            0,
        )
        xargs = (
            base_coeffs,
            self.wave,
            self.xslit,
            self.ypix,
            self.yslit,
            diff,
            vdiff,
            self.mask,
            ipos,
            ineg,
            self.sh,
            fix_sigma,
            force_positive,
            verbose,
            1,
        )

        if x0 is None:
            if fix_sigma > 0:
                x0 = np.zeros(degree + 1)
            else:
                x0 = np.append([initial_sigma], np.zeros(degree + 1))

        if with_bounds:
            if fix_sigma > 0:
                bounds = [trace_bounds] * (len(x0))
            else:
                bounds = [sigma_bounds] + [trace_bounds] * (len(x0) - 1)
        else:
            bounds = None

        if evaluate:
            theta = x0
        else:
            EVAL_COUNT = 0

            _res = minimize(
                objfun_prof_trace,
                x0,
                args=args,
                method=method,
                tol=tol,
                bounds=bounds,
            )

            theta = _res.x

        # Initial values
        _ = objfun_prof_trace(x0, *xargs)
        snum, sden, smod, sigma, trace_coeffs, chi2_init = _

        # Evaluated
        _ = objfun_prof_trace(theta, *xargs)
        snum, sden, smod, sigma, trace_coeffs, chi2_fit = _

        out = {
            "theta": theta,
            "sigma": sigma,
            "trace_coeffs": trace_coeffs,
            "chi2_init": chi2_init,
            "chi2_fit": chi2_fit,
            "ipos": ipos,
            "ineg": ineg,
            "diff": diff,
            "vdiff": vdiff,
            "snum": snum,
            "sden": sden,
            "smod": smod,
            "force_positive": force_positive,
            "bounds": bounds,
            "method": method,
            "tol": tol,
        }

        return out

    def get_trace_sn(
        self,
        exposure_position="auto",
        theta=[4.0, 0],
        force_positive=True,
        **kwargs,
    ):
        """
        Compute spectrum S/N along the trace

        Parameters
        ----------
        exposure_position : int, 'auto'
            Reference exposure position to use

        theta : array-like
            Default trace profile parameters

        force_positive : bool
            Parameter on `msaexp.slit_combine.fit_single_trace`

        Returns
        -------
        tfit : dict
            Output from `msaexp.slit_combine.fit_single_trace` with an
            additional ``sn`` item

        """
        ref_exp = (
            self.calc_reference_exposure
            if exposure_position in ["auto"]
            else exposure_position
        )

        if ref_exp is None:
            ref_exp = self.unp.values[0]

        tfit = self.fit_single_trace(
            exp=ref_exp,
            x0=np.array(theta),
            fix_sigma=-1,
            evaluate=True,
            force_positive=force_positive,
            verbose=False,
        )

        tfit["sn"] = tfit["snum"] / np.sqrt(tfit["sden"])

        return tfit

    def fit_params_by_sn(
        self,
        sn_percentile=80,
        sigma_threshold=5,
        degree_sn=[[-1000], [0]],
        verbose=True,
        **kwargs,
    ):
        """
        Compute trace offset polynomial degree and whether or not to fix the
        profile sigma width as a function of S/N

        Parameters
        ----------
        sn_percentile : float
            Percentile of the 1D S/N array extracted along the trace

        sigma_threshold : float
            Threshold below which the profile width is fixed (``fix_sigma =
            True``)

        degree_sn : [array-like, array-like]
            The two arrays/lists ``x_sn, y_degree = degree_sn`` define the S/N
            thresholds ``x_sn`` below which a polynomial degree ``y_degree``
            is used

        kwargs : dict
            Keyword arguments passed to the ``get_trace_sn`` method

        Returns
        -------
        sn : array-like
            1D S/N along the dispersion axis

        sn_value : float
            ``sn_percentile`` of ``sn`` array

        fix_sigma : bool
            Test whether SN percentile is below ``sigma_threshold``

        interp_degree : int
            The derived polynomial degree given the estimated SN percentile
            ``interp_degree = np.interp(SN[sn_percentile], x_sn, y_degree)``

        """
        tfit = self.get_trace_sn(**kwargs)
        sn_value = np.nanpercentile(tfit["sn"], sn_percentile)

        if not np.isfinite(sn_value):
            return tfit["sn"], sn_value, True, degree_sn[1][0]

        interp_degree = int(
            np.interp(
                sn_value,
                *degree_sn,
                left=degree_sn[1][0],
                right=degree_sn[1][-1],
            )
        )

        fix_sigma = sn_value < sigma_threshold

        msg = (
            f"fit_params_by_sn: {self.name}"  # {degree_sn[0]} {degree_sn[1]}'
        )
        msg += f"  SN({sn_percentile:.0f}%) = {sn_value:.1f}  fix_sigma={fix_sigma}"
        msg += f"  degree={interp_degree} "
        utils.log_comment(utils.LOGFILE, msg, verbose=verbose)

        return tfit["sn"], sn_value, fix_sigma, interp_degree

    def plot_profile(self, exp=1, ax=None, fit_result=None, ymax=0.2):
        """
        Make a plot of cross-dispersion profile
        """
        ipos, ineg, diff, vdiff = self.make_diff_image(exp=exp)
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))

        ax.scatter(self.yslit[0, :], diff, alpha=0.1, color="0.5")
        if fit_result is not None:
            _smod = fit_result["smod"]
            ymax = np.nanpercentile(_smod[_smod], 98) * 2.0

            ax.scatter(self.yslit[0, :], _smod, alpha=0.1, color="r")
            ax.vlines(
                fit_result["sigma"], -ymax, ymax, linestyle=":", color="r"
            )

        ax.set_ylim(-0.5 * ymax, ymax)
        ax.grid()
        fig.tight_layout(pad=1)

        return fig


# grid for oversampling cross-dispersion
xstep_func = (
    lambda x, pf: (np.linspace(1.0 / x, 2 + 1.0 / x, x + 1)[:-1] - 1) * pf
)


def pseudo_drizzle(
    xpix, ypix, data, wht, xbin, ybin, arrays=None, oversample=4, pixfrac=1
):
    """
    2D histogram analogous to drizzle with pixfrac=0
    """
    from scipy.stats import binned_statistic_2d

    xs = xstep_func(oversample, pixfrac)

    if arrays is None:
        num = np.zeros((len(ybin) - 1, len(xbin) - 1))
        den = num * 0.0
    else:
        num, den = arrays

    dx = 0
    for dy in xs:
        # for dy in xs:
        res = binned_statistic_2d(
            ypix + dy,
            xpix + dx,
            (data * wht / oversample),
            statistic="sum",
            bins=(ybin, xbin),
        )

        ok = np.isfinite(res.statistic)

        num[ok] += res.statistic[ok]
        res = binned_statistic_2d(
            ypix + dy,
            xpix + dx,
            (wht / oversample),
            statistic="sum",
            bins=(ybin, xbin),
        )

        den[ok] += res.statistic[ok]

    return (num, den)


def obj_header(obj):
    """
    Generate a header from a `msaexp.slit_combine.SlitGroup` object

    Parameters
    ----------
    obj : `msaexp.slit_combine.SlitGroup`
        Data group

    Returns
    -------
    header : `astropy.io.fits.Header`
        Merged FITS header from the ``slits`` of ``obj``

    """

    header = pyfits.Header()
    with pyfits.open(obj.files[0]) as im:
        for ext in [0, "SCI"]:
            for k in im[ext].header:
                if k in ("", "COMMENT", "HISTORY"):
                    continue

                header[k] = (im[ext].header[k], im[ext].header.comments[k])

    files = []
    header["EXPTIME"] = 0.0
    header["NCOMBINE"] = 0
    header["BUNIT"] = "microJansky"

    header["WAVECORR"] = (
        obj.meta["trace_with_xpos"],
        "Wavelength corrected for xpos",
    )

    header["YPIXTRA"] = (
        obj.source_ypixel_position,
        "Y pixel position in 2D cutouts",
    )
    header["YPIXSCL"] = (
        obj.slit_pixel_scale,
        "Cross dispersion pixel scale, arcsec",
    )
    header["CALCREF"] = (
        obj.calc_reference_exposure,
        "Derived reference exposure",
    )

    for k in obj.meta:
        if k == "bad_shutter_names":
            header["NBADSHUT"] = (
                len(obj.meta[k]),
                "Number of flagged bad shutters",
            )
            for i, ki in enumerate(obj.meta[k]):
                header[f"BADSHUT{i}"] = ki, "Bad shutter name"
        else:
            if k in obj.meta_comment:
                key = (obj.meta[k], obj.meta_comment[k])
            else:
                key = obj.meta[k]

            header[k.upper()] = key

    for i, sl in enumerate(obj.slits):
        fbase = sl.meta.filename.split("_nrs")[0]
        if fbase in files:
            continue

        files.append(fbase)
        header["EXPTIME"] += sl.meta.exposure.effective_exposure_time
        header["NCOMBINE"] += 1

    return header


DRIZZLE_KWS = dict(
    step=1,
    with_pathloss=True,
    wave_sample=1.05,
    ny=13,
    dkws=dict(oversample=16, pixfrac=0.8),
)


def combine_grating_group(
    xobj, grating_keys, drizzle_kws=DRIZZLE_KWS, extract_kws={}, verbose=True
):
    """
    Make pseudo-drizzled outputs from a set of `msaexp.slit_combine.SlitGroup`
    objects

    Parameters
    ----------
    xobj : dict
        Set of `msaexp.slit_combine.SlitGroup` objects

    grating_keys : list
        List of keys of ``xobj`` to combine

    drizzle_kws : dict
        Keyword arguments passed to `msaexp.slit_combine.drizzle_grating_group`

    extract_kws : dict
        Not used

    Returns
    -------
    hdul : `astropy.io.fits.HDUList`
        FITS HDU list generated from `msaexp.drizzle.make_optimal_extraction`

    """

    import astropy.units as u
    import grizli.utils
    import msaexp.drizzle

    _ = drizzle_grating_group(xobj, grating_keys, **drizzle_kws)
    wave_bin, xbin, ybin, header, slit_info, arrays, parrays = _

    num, den = arrays
    mnum, mden = parrays

    sci2d = num / den
    wht2d = den * 1

    pmask = mnum / den > 0
    snum = np.nansum((num / den) * mnum * pmask, axis=0)
    sden = np.nansum(mnum**2 / den * pmask, axis=0)

    smsk = nd.binary_erosion(np.isfinite(snum / sden), iterations=2) * 1.0
    smsk[smsk < 1] = np.nan
    snum *= smsk

    snmask = snum / sden * np.sqrt(sden) > 3
    if snmask.sum() < 10:
        snmask = snum / sden * np.sqrt(sden) > 1

    pdata = np.nansum((num / den) * snmask * den, axis=1)
    pdata /= np.nansum(snmask * den, axis=1)

    pmod = np.nansum(mnum / den * snum / sden * snmask * den, axis=1)
    pmod /= np.nansum(snmask * den, axis=1)

    kwargs = {}

    for k in xobj:
        bkg_offset = int(np.round(xobj[k]["obj"].meta["nod_offset"]))
        break

    _data = msaexp.drizzle.make_optimal_extraction(
        wave_bin,
        sci2d,
        wht2d,
        profile_slice=None,
        prf_center=0.0,
        prf_sigma=header["SIGMA"],
        sigma_bounds=(0.5, 2.5),
        center_limit=0.001,
        fit_prf=False,
        fix_center=False,
        fix_sigma=True,
        trim=0,
        bkg_offset=bkg_offset,
        bkg_parity=[1, -1],
        offset_for_chi2=1.0,
        max_wht_percentile=None,
        max_med_wht_factor=10,
        verbose=True,
        find_line_kws={},
        ap_radius=None,
        ap_center=None,
        **kwargs,
    )

    _sci2d, _wht2d, profile2d, spec, prof = _data

    spec["flux"] = snum / sden
    spec["err"] = 1.0 / np.sqrt(sden)
    spec["flux"].unit = u.microJansky
    spec["err"].unit = u.microJansky
    spec["wave"].unit = u.micron

    # Add path_corr column
    average_path_loss(spec, header=header)

    for c in list(spec.colnames):
        if "aper" in c:
            spec.remove_column(c)

    # spec['flux'][~np.isfinite(smsk)] = 0
    # spec['err'][~np.isfinite(smsk)] = 0

    profile2d = mnum / den  # *snum/sden
    profile2d[~np.isfinite(profile2d)] = 0

    prof["profile"] = pdata
    prof["pfit"] = pmod

    for k in spec.meta:
        header[k] = spec.meta[k]

    msg = "msaexp.drizzle.extract_from_hdul:  Output center = "
    msg += f" {header['PROFCEN']:6.2f}, sigma = {header['PROFSIG']:6.2f}"
    grizli.utils.log_comment(
        grizli.utils.LOGFILE, msg, verbose=verbose, show_date=False
    )

    hdul = pyfits.HDUList()

    hdul.append(pyfits.BinTableHDU(data=spec, name="SPEC1D"))
    hdul.append(pyfits.ImageHDU(data=sci2d, header=header, name="SCI"))
    hdul.append(pyfits.ImageHDU(data=wht2d, header=header, name="WHT"))
    hdul.append(pyfits.ImageHDU(data=profile2d, header=header, name="PROFILE"))
    hdul.append(pyfits.BinTableHDU(data=prof, name="PROF1D"))
    if slit_info is not None:
        hdul.append(pyfits.BinTableHDU(data=slit_info, name="SLITS"))

    for k in hdul["SCI"].header:
        if k not in hdul["SPEC1D"].header:
            hdul["SPEC1D"].header[k] = (
                hdul["SCI"].header[k],
                hdul["SCI"].header.comments[k],
            )

    return hdul


def drizzle_grating_group(
    xobj,
    grating_keys,
    step=1,
    with_pathloss=True,
    wave_sample=1.05,
    ny=13,
    dkws=dict(oversample=16, pixfrac=0.8),
    **kwargs,
):
    """
    Run the pseudo-drizzled sampling from a set of
    `msaexp.slit_combine.SlitGroup` objects

    Parameters
    ----------
    xobj : dict
        Set of `msaexp.slit_combine.SlitGroup` objects

    grating_keys : list
        List of keys of ``xobj`` to combine

    step : float
        Cross dispersion step size in units of original pixels

    with_pathloss : bool
        Compute a pathloss correction for each spectrum based on the fitted
        profile width and the (planned) intra-shutter position of a particular
        source

    wave_sample : float
        Wavelength sampling relative to the default grid for a particular
        grating provided by `msaexp.utils.get_standard_wavelength_grid`

    ny : int
        Half-width in pixels of the output grid in the cross-dispersion axis

    dkws : dict
        keyword args passed to `msaexp.slit_combine.pseudo_drizzle`


    Returns
    -------
    wave_bin : array-like
        1D wavelength sample points

    xbin : array-like
        2D x (wavelength) sample points

    ybin : array-like
        2D cross-dispersion sample points

    header : `~astropy.io.fits.Header`
        Header for the combination

    slit_info : `~astropy.table.Table`
        Table of slit metadata

    arrays : (array-like, array-like)
        2D `sci2d` and `wht2d` arrays of the resampled data

    parrays : (array-like, array-like)
        2D `prof2d` and `prof_wht2d` arrays of the profile model resampled
        like the data

    """

    import astropy.io.fits as pyfits
    import astropy.table

    obj = xobj[grating_keys[0]]["obj"]

    header = pyfits.Header()

    wave_bin = msautils.get_standard_wavelength_grid(
        obj.grating, sample=wave_sample
    )

    dw = np.diff(wave_bin)
    xbin = np.hstack(
        [
            wave_bin[0] - dw[0] / 2,
            wave_bin[:-1] + dw / 2.0,
            wave_bin[-1] + dw[-1] / 2.0,
        ]
    )

    ybin = np.arange(-ny, ny + step * 1.01, step) - 0.5

    arrays = None
    parrays = None

    header = None
    slit_info = []

    for k in grating_keys:
        obj = xobj[k]["obj"]
        if header is None:
            header = obj_header(obj)
        else:
            hi = obj_header(obj)
            header["NCOMBINE"] += hi["NCOMBINE"]
            header["EXPTIME"] += hi["EXPTIME"]

        try:
            fit = xobj[k]["fit"]
            for e in fit:
                sigma = fit[e]["sigma"]
                trace_coeffs = fit[e]["trace_coeffs"]
                break
        except:
            fit = None
            sigma = 1.0
            trace_coeffs = [0]

        header["SIGMA"] = (sigma, "Profile width, pixels")
        header["TRACEDEG"] = (
            len(trace_coeffs) - 1,
            "Trace offset polynomial degree",
        )
        for i, val in enumerate(trace_coeffs):
            header[f"TRACEC{i}"] = (val, "Trace offset polynomial coefficient")

        exp_ids = obj.unp.values

        header["WITHPTH"] = (with_pathloss, "Internal path loss correction")

        for ii, exp in enumerate(exp_ids):
            ipos, ineg, diff, vdiff = obj.make_diff_image(exp=exp)
            wht = 1.0 / vdiff
            ip = np.where(ipos)[0][0]
            ok = np.isfinite(diff + wht + obj.yslit[ip, :])
            if fit is not None:
                ok &= np.isfinite(fit[exp]["smod"].flatten())

            ok &= vdiff > 0
            if ok.sum() == 0:
                continue

            ysl = (obj.yslit[ip, :].reshape(obj.sh) + 0.0).flatten()[ok]

            xsl = obj.xslit[ip, :][ok]
            xsl = obj.wave[ip, :][ok]

            # path loss
            if with_pathloss:
                header[f"PTHEXP{ii}"] = (exp, "Exposure group name")
                header[f"PTHSIG{ii}"] = (
                    fit[exp]["sigma"],
                    f"Sigma of group {exp}",
                )
                header[f"PTHXPO{ii}"] = (
                    obj.slits[ip].source_xpos,
                    f"source_xpos of grup {exp}",
                )

                # print('With PRF pathloss correction')
                prf_i = slit_prf_fraction(
                    obj.wave[ip, :][ok],
                    sigma=fit[exp]["sigma"],
                    x_pos=obj.slits[ip].source_xpos,
                    slit_width=0.2,
                    pixel_scale=PIX_SCALE,
                    verbose=False,
                )

                prf_0 = slit_prf_fraction(
                    obj.wave[ip, :][ok],
                    sigma=0.01,
                    x_pos=0.0,
                    slit_width=0.2,
                    pixel_scale=PIX_SCALE,
                    verbose=False,
                )
                prf_i /= prf_0

            else:
                # print('WithOUT PRF pathloss')
                prf_i = 1.0

            arrays = pseudo_drizzle(
                xsl,
                ysl,
                diff[ok] / prf_i,
                wht[ok] * prf_i**2,
                xbin,
                ybin,
                arrays=arrays,
                **dkws,
            )

            if fit is not None:
                mod = (
                    fit[exp]["smod"] / (fit[exp]["snum"] / fit[exp]["sden"])
                ).flatten()

                parrays = pseudo_drizzle(
                    xsl,
                    ysl,
                    mod[ok],
                    wht[ok] * prf_i**2,
                    xbin,
                    ybin,
                    arrays=parrays,
                    **dkws,
                )

        _meta = obj.slit_metadata()
        _meta_nlines = len(_meta)
        for c in list(_meta.colnames):
            if np.isin(_meta[c], [None]).sum() == _meta_nlines:
                _meta.remove_column(c)

        slit_info.append(_meta)

    if len(slit_info) > 0:
        slit_info = astropy.table.vstack(slit_info)
    else:
        slit_info = None

    return wave_bin, xbin, ybin, header, slit_info, arrays, parrays


FIT_PARAMS_SN_KWARGS = dict(
    sn_percentile=80,
    sigma_threshold=5,
    # degree_sn=[[-10000,10,100000], [0,1,2]],
    degree_sn=[[-10000], [0]],
    verbose=True,
)


def average_path_loss(spec, header=None):
    """
    Get average pathloss correction from spectrum metadata

    Parameters
    ----------
    spec : Table
        Table with metadata including pathloss parameters used above

    header : `~astropy.io.fits.Header`
        Optional FITS header to use instead of ``spec.meta``

    Returns
    -------
    path_corr : Column
        Adds a ``path_corr`` column to ``spec`` that represents the average
        path-loss correction determined from the profile width and x_pos
        centering parameters using `msaexp.slit_combine.slit_prf_fraction`

    """
    if header is None:
        header = spec.meta

    if "WITHPTH" not in header:
        print("WITHPTH keyword not found")
        return False

    if not header["WITHPTH"]:
        print("WITHPTH = False")
        return False

    prf_list = []
    for i in range(100):
        if f"PTHSIG{i}" in header:
            sigma = header[f"PTHSIG{i}"]
            x_pos = header[f"PTHXPO{i}"]

            prf_i = slit_prf_fraction(
                spec["wave"].astype(float),
                sigma=sigma,
                x_pos=x_pos,
                slit_width=0.2,
                pixel_scale=PIX_SCALE,
                verbose=False,
            )

            # Path loss is relative to a centered point source
            prf_0 = slit_prf_fraction(
                spec["wave"].astype(float),
                sigma=0.01,
                x_pos=0.0,
                slit_width=0.2,
                pixel_scale=PIX_SCALE,
                verbose=False,
            )

            prf_list.append(prf_i / prf_0)

    if len(prf_list) > 0:
        print("Added path_corr column to spec")
        spec["path_corr"] = 1.0 / np.nanmean(np.array(prf_list), axis=0)
        spec["path_corr"].format = ".2f"
        spec["path_corr"].description = (
            "Average path loss correction already applied"
        )


def get_spectrum_path_loss(spec):
    """
    Calculate the path loss correction that was applied to a spectrum

    Parameters
    ----------
    spec : Table
        Table with metadata including ``SRCXPOS`` (intra-shutter position,
        arcsec) and ``SIGMA`` (source gaussian width, pixels) keywords

    Returns
    -------
    path_corr : array-like
        Wavelength-dependent path loss correction

    """
    path_loss = slit_prf_fraction(
        spec["wave"].astype(float),
        sigma=spec.meta["SIGMA"],
        x_pos=spec.meta["SRCXPOS"],
        slit_width=0.2,
        pixel_scale=PIX_SCALE,
        verbose=False,
    )

    path_loss_ref = slit_prf_fraction(
        spec["wave"].astype(float),
        sigma=0.01,
        x_pos=0.0,
        slit_width=0.2,
        pixel_scale=PIX_SCALE,
        verbose=False,
    )

    path_loss /= path_loss_ref
    return 1.0 / path_loss


def extract_spectra(
    target="1208_5110240",
    root="nirspec",
    path_to_files="./",
    files=None,
    do_gratings=["PRISM", "G395H", "G395M", "G235M", "G140M"],
    join=[0, 3, 5],
    split_uncover=True,
    stuck_threshold=0.0,
    pad_border=2,
    sort_by_sn=False,
    position_key="y_index",
    mask_cross_dispersion=None,
    cross_dispersion_mask_type="trace",
    trace_from_yoffset=False,
    reference_exposure="auto",
    trace_niter=4,
    offset_degree=0,
    degree_kwargs={},
    recenter_all=False,
    nod_offset=None,
    initial_sigma=7,
    fit_type=1,
    initial_theta=None,
    fix_params=False,
    input_fix_sigma=None,
    fit_params_kwargs=None,
    diffs=True,
    undo_pathloss=True,
    undo_barshadow=False,
    drizzle_kws=DRIZZLE_KWS,
    get_xobj=False,
    trace_with_xpos=False,
    trace_with_ypos="auto",
    get_background=False,
    make_2d_plots=True,
    **kwargs,
):
    """
    Spectral combination workflow

    Parameters
    ----------
    target : str
        Target name. If no ``files`` specified, will search for the 2D slit
        cutout files with names like ``*phot*{target}.fits``

    root : str
        Output file rootname

    path_to_files : str
        Directory path containing the ``phot`` files

    files : list, None
        Optional explicit list of ``phot`` files to combine

    do_gratings : list
        Gratings to consider

    join : list
        Indices of ``files[i].split('[._]') + GRATING`` to join as a group

    split_uncover : bool
        Split sub-pixel dithers from UNCOVER when defining exposure groups

    stuck_threshold, pad_border, position_key:
        See `msaexp.slit_combine.SlitGroup`

    sort_by_sn : bool
        Try to process groups in order of decreasing S/N, i.e., to derive the
        trace offsets in the prism where it will be best defined and propagate
        to other groups with the gratings

    mask_cross_dispersion : None or [int, int]
        Optional cross-dispersion masking, e.g., for stuck-closed shutters or
        multiple sources within a slitlet. The specified values are integer
        indices of the pixel range to mask. See ``cross_dispersion_mask_type``.

    cross_dispersion_mask_type : str
        Type of cross dispersion mask to apply. With ``'trace'``, the masked
        pixels are calculated relative to the (expected) center of the trace,
        and, e.g., ``mask_cross_dispersion = [5,100]`` will mask all pixels 5
        pixels "above" the center of the trace (100 is an arbitrarily large
        number to include all pixels). The mask will shift along with the nod
        offsets.

        With ``fixed``, the mask indices are relative to the trace *in the
        first exposure* and won't shift with the nod offsets. So
        ``mask_cross_dispersion = [-3,3]`` would mask roughly the central
        shutter in all exposures that will contain the source in some
        exposures and not in others. This can be used to try to mitigate some
        stuck-closed shutters, though the how effective it is is still under
        investigation.

    trace_from_yoffset, reference_exposure :
        See `msaexp.slit_combine.SlitGroup`

    """
    global CENTER_WIDTH, CENTER_PRIOR, SIGMA_PRIOR, MSA_NOD_ARCSEC
    frame = inspect.currentframe()

    # Log function arguments
    utils.LOGFILE = f"{root}_{target}.extract.log"
    args = utils.log_function_arguments(
        utils.LOGFILE, frame, "slit_combine.extract_spectra"
    )
    if isinstance(args, dict):
        with open(f"{root}_{target}.extract.yml", "w") as fp:
            fp.write(f"# {time.ctime()}\n# {os.getcwd()}\n")
            yaml.dump(args, stream=fp, Dumper=yaml.Dumper)

    if files is None:
        files = glob.glob(os.path.join(path_to_files, f"*phot*{target}.fits"))

    for i in range(len(files))[::-1]:
        if "jw04246003001_03101_00001_nrs2" in files[i]:
            utils.log_comment(
                utils.LOGFILE, f"Exclude {files[i]}", verbose=True
            )
            files.pop(i)
        elif (target == "1210_9849") & ("jw01210001001" in files[i]):
            utils.log_comment(
                utils.LOGFILE, f"Exclude {files[i]}", verbose=True
            )
            files.pop(i)

    files.sort()

    utils.log_comment(
        utils.LOGFILE,
        f"{root}   target: {target}   Files: {len(files)}",
        verbose=True,
    )

    groups = split_visit_groups(
        files, join=join, gratings=do_gratings, split_uncover=split_uncover
    )

    xobj = {}
    for ig, g in enumerate(groups):
        if "xxxprism" in g:
            continue

        if ig == -100:
            continue

        if "jw02561002001" in g:
            continue

        msg = f"\n* Group {g}   "
        msg += f"N={len(groups[g])}\n"
        msg += "=================================="
        utils.log_comment(utils.LOGFILE, msg, verbose=True)

        if nod_offset is None:
            if ("glazebrook" in root) | ("suspense" in root):
                # nod_offset = 10
                MSA_NOD_ARCSEC = 0.529 * 2
            else:
                MSA_NOD_ARCSEC = 0.529 * 1

        if trace_with_ypos in ["auto"]:
            trace_with_ypos = ("b" not in target) & (not get_background)

        if root.startswith("glazebrook-v"):
            utils.log_comment(
                utils.LOGFILE, "  ! Auto glazebrook", verbose=True
            )
            trace_from_yoffset = True

        elif "maseda" in root:
            utils.log_comment(utils.LOGFILE, "  ! Auto maseda", verbose=True)
            trace_from_yoffset = True

        elif "smacs0723-ero-v" in root:
            utils.log_comment(
                utils.LOGFILE, "  ! Auto SMACS0723", verbose=True
            )
            trace_from_yoffset = True

        obj = SlitGroup(
            groups[g],
            g,
            position_key=position_key,
            diffs=diffs,  # (True & (~isinstance(id, str))),
            stuck_threshold=stuck_threshold,
            undo_barshadow=undo_barshadow,
            undo_pathloss=undo_pathloss,
            # sky_arrays=(wsky, fsky),
            trace_with_xpos=trace_with_xpos,
            trace_with_ypos=trace_with_ypos,
            trace_from_yoffset=trace_from_yoffset,
            nod_offset=nod_offset,
            reference_exposure=reference_exposure,
            pad_border=pad_border,
        )

        if 0:
            if (obj.grating not in do_gratings) | (
                obj.sh[1] < 83 * 2 ** (obj.grating not in ["PRISM"])
            ):
                msg = f"\n    skip shape=({obj.sh}) {obj.grating}\n"
                utils.log_comment(utils.LOGFILE, msg, verbose=True)
                continue

        if obj.meta["diffs"]:
            valid_frac = obj.mask.sum() / obj.mask.size

            if obj.N == 1:
                utils.log_comment(
                    utils.LOGFILE,
                    f"\n    skip N=1 {obj.grating}\n",
                    verbose=True,
                )
                continue

            elif len(obj.meta["bad_shutter_names"]) == obj.N:
                utils.log_comment(
                    utils.LOGFILE,
                    f"\n    skip all bad {obj.grating}\n",
                    verbose=True,
                )
                continue

            elif (len(obj.unp.values) == 1) & (obj.meta["diffs"]):
                utils.log_comment(
                    utils.LOGFILE,
                    f"\n    one position {obj.grating}\n",
                    verbose=True,
                )
                continue

            elif os.path.basename(obj.files[0]).startswith("jw02561002001"):
                utils.log_comment(
                    utils.LOGFILE,
                    f"\n    uncover {obj.files[0]}\n",
                    verbose=True,
                )
                continue

            elif valid_frac < 0.2:
                utils.log_comment(
                    utils.LOGFILE,
                    f"\n    masked pixels {valid_frac:.2f}\n",
                    verbose=True,
                )
                continue

            elif ("b" in target) & (
                (obj.info["shutter_state"] == "x").sum() > 0
            ):
                utils.log_comment(
                    utils.LOGFILE,
                    "\n    single background shutter\n",
                    verbose=True,
                )
                continue

        ind = None

        if ind is not None:
            obj.xslit = obj.xslit[ind, :]
            obj.yslit = obj.yslit[ind, :]
            obj.ypix = obj.ypix[ind, :]

            obj.xtr = obj.xtr[ind, :]
            obj.ytr = obj.ytr[ind, :]
            obj.wtr = obj.wtr[ind, :]

            obj.wave = obj.wave[ind, :]
            obj.bar = obj.bar[ind, :]

            obj.base_coeffs = [obj.base_coeffs[j] for j in ind]

        xobj[g] = {"obj": obj}

        # if not obj.trace_with_ypos:
        #     CENTER_WIDTH = 2

    if len(xobj) == 0:
        utils.log_comment(utils.LOGFILE, "No valid spectra", verbose=True)
        return None

    if ("macs0417" in root) & (target == "1208_234"):
        for k in xobj:
            obj = xobj[k]["obj"]
            for j in range(obj.N):
                obj.sci[j, (obj.yslit[j, :] < -8)] = np.nan

            obj.mask &= np.isfinite(obj.sci)

    elif target == "4233_945401":
        for k in xobj:
            obj = xobj[k]["obj"]
            for j in range(obj.N):
                obj.sci[j, (obj.yslit[j, :] > 6)] = np.nan

            obj.mask &= np.isfinite(obj.sci)

    if mask_cross_dispersion is not None:
        msg = f"slit_combine: mask_cross_dispersion {mask_cross_dispersion}"
        msg += f"  cross_dispersion_mask_type={cross_dispersion_mask_type}"
        utils.log_comment(utils.LOGFILE, msg, verbose=True)

        for k in xobj:
            obj = xobj[k]["obj"]
            for j in range(obj.N):
                cross_mask = obj.yslit[j, :] > mask_cross_dispersion[0]
                cross_mask &= obj.yslit[j, :] < mask_cross_dispersion[1]

                if cross_dispersion_mask_type == "bkg":
                    # Just mask background when doing the differences
                    obj.bkg_mask[j, cross_mask] = False

                elif cross_dispersion_mask_type == "fixed":
                    # Relative to first trace
                    cross_mask = obj.yshutter[j, :] > mask_cross_dispersion[0]
                    cross_mask &= obj.yshutter[j, :] < mask_cross_dispersion[1]
                    obj.sci[j, cross_mask] = np.nan

                else:
                    # Mask out all pixels, source and background
                    obj.sci[j, cross_mask] = np.nan

            obj.mask &= np.isfinite(obj.sci)
            obj.bkg_mask &= np.isfinite(obj.sci)

    # Sort by grating
    okeys = []
    xkeys = []
    for k in list(xobj.keys()):
        obj = xobj[k]["obj"]
        okeys.append(f"{k.split('-')[-1]}-{obj.sh[1]}")
        xkeys.append(k)

    if sort_by_sn:
        # Sort in order of decreasing S/N
        sn_keys = []

        for k in xkeys:
            obj = xobj[k]["obj"]

            _sn, sn_val, _, _ = obj.fit_params_by_sn(**fit_params_kwargs)
            if "prism" in k:
                sn_val *= 2

            if not np.isfinite(sn_val):
                sn_keys.append(-1)
            else:
                sn_keys.append(sn_val)

        so = np.argsort(sn_keys)[::-1]

    else:
        # Sort by the keys favoring largest arrays in the reddest gratings
        so = np.argsort(okeys)[::-1]

    keys = [xkeys[j] for j in so]

    utils.log_comment(utils.LOGFILE, f"\nkeys: {keys}", verbose=True)

    if fit_params_kwargs is not None:
        obj0 = xobj[keys[0]]["obj"]
        _ = obj0.fit_params_by_sn(**fit_params_kwargs)
        _sn, sn_val, do_fix_sigma, offset_degree = _

        if do_fix_sigma:
            # input_fix_sigma = initial_sigma*1
            recenter_all = False
            fix_params = True
            initial_theta = np.array([initial_sigma, 0])

    if initial_theta is not None:
        CENTER_PRIOR = initial_theta[-1]
        SIGMA_PRIOR = initial_theta[0] / 10.0
    else:
        CENTER_PRIOR = 0
        SIGMA_PRIOR = 0.6

    # fix_sigma = None
    if input_fix_sigma is None:
        fix_sigma_across_groups = True
        fix_sigma = -1
    else:
        if input_fix_sigma < 0:
            fix_sigma_across_groups = False
            fix_sigma = -1
        else:
            fix_sigma_across_groups = True
            fix_sigma = input_fix_sigma

    for i, k in enumerate(keys):
        msg = f"\n##### Group #{i+1} / {len(xobj)}: {k} ####\n"
        utils.log_comment(utils.LOGFILE, msg, verbose=True)

        obj = xobj[k]["obj"]

        kws = dict(
            niter=trace_niter,
            force_positive=(fit_type == 0),
            degree=offset_degree,
            ref_exp=obj.calc_reference_exposure,
            sigma_bounds=(3, 12),
            with_bounds=False,
            trace_bounds=(-1.0, 1.0),
            initial_sigma=initial_sigma,
            x0=initial_theta,
            # evaluate=fix_params,
            method="powell",
            tol=1.0e-8,
        )

        if fix_params:
            kws["evaluate"] = True

        if (i == 0) | (recenter_all):

            if fix_sigma > 0:
                kws["fix_sigma"] = fix_sigma

            tfit = obj.fit_all_traces(**kws)

            theta = tfit[obj.unp.values[0]]["theta"]

            if i == 0:
                if "fix_sigma" in kws:
                    if kws["fix_sigma"] > 0:
                        fix_sigma = kws["fix_sigma"]
                    else:
                        fix_sigma = tfit[obj.unp.values[0]]["sigma"] * 10
                elif fix_sigma_across_groups:
                    theta = theta[1:]
                    fix_sigma = tfit[obj.unp.values[0]]["sigma"] * 10

        else:
            kws["x0"] = theta
            kws["with_bounds"] = False
            kws["evaluate"] = True
            kws["fix_sigma"] = fix_sigma

            tfit = obj.fit_all_traces(**kws)

        xobj[k] = {"obj": obj, "fit": tfit}

    ######
    # Fit plots
    if make_2d_plots:
        for k in keys:
            obj = xobj[k]["obj"]
            if "fit" in xobj[k]:
                fit = xobj[k]["fit"]
            else:
                fit = None

            fig2d = obj.plot_2d_differences(fit=fit)
            fileroot = f"{root}_{obj.grating}-{obj.filter}_{target}".lower()
            fig2d.savefig(f"{fileroot}.d2d.png")

    for k in xobj:
        xobj[k]["obj"].sky_arrays = None

    gratings = {}
    for k in keys:
        gr = k.split("-")[-1]
        if gr in gratings:
            gratings[gr].append(k)
        else:
            gratings[gr] = [k]

    utils.log_comment(utils.LOGFILE, f"\ngratings: {gratings}", verbose=True)

    hdul = {}
    for g in gratings:
        hdul[g] = combine_grating_group(
            xobj, gratings[g], drizzle_kws=drizzle_kws
        )

        _head = hdul[g][1].header

        specfile = f"{root}_{_head['GRATING']}-{_head['FILTER']}".lower()
        specfile += f"_{_head['SRCNAME']}.spec.fits".lower().replace(
            "background_", "b"
        )

        utils.log_comment(utils.LOGFILE, specfile, verbose=True)
        hdul[g].writeto(specfile, overwrite=True)

        fig = msautils.drizzled_hdu_figure(hdul[g])
        fig.savefig(specfile.replace(".spec.fits", ".fnu.png"))

        fig = msautils.drizzled_hdu_figure(hdul[g], unit="flam")
        fig.savefig(specfile.replace(".spec.fits", ".flam.png"))

    # Cleanup
    for k in xobj:
        obj = xobj[k]["obj"]
        for sl in obj.slits:
            sl.close()

    if get_xobj:
        return hdul, xobj
    else:
        del xobj
        return hdul
