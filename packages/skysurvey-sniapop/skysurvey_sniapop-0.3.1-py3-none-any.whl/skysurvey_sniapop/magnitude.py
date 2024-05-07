import numpy as np
from astropy.cosmology import Planck18

def standardisation_step(x1, c, isup,
                          mabs=-19.3, alpha=-0.15, beta=3.15, gamma=0.1,
                          sigmaint=0.10):
    """ """
    mabs = np.random.normal(loc=mabs, scale=sigmaint, size=len(x1))

    # Standardisation
    # - color
    color_corr = c * beta
    
    # - stretch
    stretch_corr = x1 * alpha
    
    # - astro
    astro_corr = isup * gamma

    mabs_notstandard = mabs + (color_corr + stretch_corr + astro_corr)
    return mabs_notstandard

def standardisation_brokenalpha( x1, c, isup, x1mode,
                                    mabs=-19.3, sigmaint=0.10,
                                    alpha_low=-0.2, alpha_high=-0.07, 
                                    beta=3.15, gamma=0.1,
                                    x1ref=-0.05):
    """ 
    Parameters
    ----------
    
    x1ref: float
        x1 value where the two model are crossing.
    """
    mabs = np.random.normal(loc=mabs, scale=sigmaint, size=len(x1))

    # Standardisation
    # - color
    color_corr = c * beta
    
    # - astro
    astro_corr = isup * gamma

    # - stretch
    flag_mode_h = (x1mode==1) # flag mode high
    stretch_corr = np.zeros( len(x1) )*np.NaN # empty
    stretch_corr[flag_mode_h] = (x1[flag_mode_h]-x1ref) * alpha_high # flag mode high
    stretch_corr[~flag_mode_h] = (x1[~flag_mode_h]-x1ref) * alpha_low # flag mode high
    
    mabs_notstandard = mabs + (stretch_corr + color_corr + astro_corr)
    return mabs_notstandard

def magobs_to_magres(magobs, z, magabs=-19.3, cosmology=Planck18, c=0, x1=0, beta=0, alpha=0):
    """ """
    standardisation = (beta*c + alpha*x1)
    mag = magobs - (cosmology.distmod(z).value + magabs) - standardisation
    return mag
