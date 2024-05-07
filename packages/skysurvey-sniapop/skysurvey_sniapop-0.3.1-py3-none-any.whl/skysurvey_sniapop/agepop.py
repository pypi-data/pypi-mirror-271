import numpy as np
from scipy import stats

# ----------- #
#   Prompt    #
# ----------- #
def psi_z(redshift, k=0.87, phi=2.8):
    """ fraction of delayed SNeIa as a function of redshift 
    (Rigault et al. 2020)
    """
    return (k * (1+redshift)**(phi) + 1)**(-1)

def delta_z(redshift, k=0.87, phi=2.8):
    """ reciprocate of psi_z """
    return 1 - psi_z(redshift, k=k, phi=phi)

def get_promptpdf(redshift, xx=[0,1], k=0.87, phi=2.8):
    """ get the pdf of the probability to be prompt or delayed as a function of redshift. """
    xx = np.asarray(xx)
    delayed_cut = psi_z(np.atleast_1d(redshift), phi=phi, k=k)
    return xx, np.asarray([delayed_cut, 1-delayed_cut]).T

# ----------- #
#  Stretch    #
# ----------- #
def get_stretchmode(fprompt, xx=[0, 1], ratio_old=0.35):
    """ """
    if len(np.atleast_1d(fprompt)) > 1:
        fprompt = np.asarray(fprompt)[:,None]

    pdf_young = np.asarray([0, 1])
    pdf_old = np.asarray([1-ratio_old, ratio_old])
    
    return xx, pdf_young * fprompt + pdf_old * (1-fprompt)

def x1mode_to_stretch(pmode_h, mass,
                      xx="-4:4:0.005", 
                      muh=0.3, sigmah=0.55, 
                      mul=-1.3, sigmal=0.63,
                      mass_coefs=-0.32):
    """ """
    from scipy.stats import norm
    if type(xx) == str: # assumed r_ input
        xx = eval(f"np.r_[{xx}]") # (M,)

    pmode_h = np.atleast_1d(pmode_h)[:,None]          # (N,1)
    mass_offset = (np.atleast_1d(mass) - 10)[:, None] # (N, 1)
    
    model_h = norm.pdf(xx, loc=muh + mass_offset*mass_coefs, scale=sigmah) # (N, M)
    model_l = norm.pdf(xx, loc=mul + mass_offset*mass_coefs, scale=sigmal) # (N, M)

    stretch_pdf = pmode_h * model_h  +  (1-pmode_h) * model_l
    return xx, np.squeeze(stretch_pdf)

# ------------- #
#  Environment  #
# ------------- #
def get_localcolor(fprompt, 
                    xx="-0.5:2.5:300j", 
                    blue_dist = stats.norm(loc=0.8, scale=0.19),
                    red_dist = stats.norm(loc=1.37, scale=0.205),
                    ):
    """ """
    if type(xx) == str: # assumed r_ input
        xx = eval(f"np.r_[{xx}]")

    
    p_y = blue_dist.pdf(xx)
    p_o = red_dist.pdf(xx)
    
    if type(fprompt) is not float: 
        fprompt = np.asarray(fprompt)[:,None]
        
    pdf = fprompt*p_y + (1-fprompt)*p_o
    return xx, pdf

def hostmass_to_color(fprompt, mass,
                      xx="-0.5:3:300j",
                      blue_dist={"loc":0.85, "scale":0.16},
                      red_dist={"loc":1.32, "scale":0.19},
                      blue_coef = 0.15, 
                      red_coef = 0.15, 
                     ):
    """ """
    # M: number of steps in xx
    # N: number of targets
    # 2: env cases, blue or red
    
    if type(xx) == str: # assumed r_ input
        xx = eval(f"np.r_[{xx}]") # (M,)

    
    mass_offset = (np.atleast_1d(mass) - 10)[:, None] # (N, 1)
    fprompt = np.atleast_1d(fprompt)[:,None] # (N,1)
    # (N, M)
    localcolor_prompts = stats.norm.pdf(xx, loc=blue_dist["loc"] + mass_offset * blue_coef, scale=blue_dist["scale"])
    localcolor_delayed = stats.norm.pdf(xx, loc=red_dist["loc"] + mass_offset * red_coef, scale=red_dist["scale"])

    pdf_localcolor = fprompt * localcolor_prompts + (1-fprompt) * localcolor_delayed
    return xx, np.squeeze(pdf_localcolor)


def get_hostmass_pdf(redshift, fprompt, xx="6:12:300j", sfr_gamma=0.8, **kwargs):
    """ get the host stellar mass distribution.

    The derivation of the host stellar mass PDF is computed as:
    hostmass = stellar_mass_function * star_formation_rate
    
    The stellar mass functions (SMF) comes from reference literature (Davidzon et al. 2017, 
    see hostmass.get_stellar_mass_function documentation). The SMF parameter (double Schechter) 
    depend on redshift and exist for active star-forming, passive, or all galaxies.
    - for prompts, this uses the active star-forming galaxy SMF
    - for delayed, this uses the passive galaxy SMF.

    Then, prompts' rate is proportional to the SFR, so Mass_pdf = SFR * SMR_blue
    and delayeds' rate is proportional to the Mass, so Mass_pdf = Mass * SMR_red

    SFR comes from 10**(Mass-10)**sfr_gamma.
    
    Parameters
    ----------
    redshift: float, array
        redshift of the mass distribution. 
        If array, same size (N) as fprompt.

    fprompt: float, array
        fraction of prompt in the sample
        If array, same size (N) as redshift.

    xx: str, array
        binning of the pdf (size M), log(mass)

    sfr_gamma: float
        exponent relation connecting mass to sfr.

    **kwargs goes to hostmass.get_stellar_mass_function documentation

    Returns
    -------
    array, array
        - xx (M)
        - pdf (M,) or (N, M) see redshift and fprompt.
    
    """
    # M, number of mass bin
    # N, sample size
    from . import hostmass
    if type(xx) == str: # assumed r_ input
        xx = eval(f"np.r_[{xx}]")

    fprompt = np.atleast_1d(fprompt)[:,None] # (N, 1)
    redshift = np.atleast_1d(redshift)[:,None] # (N, 1)
    
    # Stellar Mass Function | (N, M)
    _, smf_blue = hostmass.get_stellar_mass_function(redshift=redshift, which="blue", xx=xx, **kwargs)
    _, smf_red = hostmass.get_stellar_mass_function(redshift=redshift, which="red", xx=xx, **kwargs)

    # Stellar Mass
    stellar_mass = 10**xx                        # stellar_mass (N,)

    # Star Formation Rate
    sfr_mass = (10**(xx-10))**sfr_gamma          # SFR = stellar_mass ** gamma (N,)

    # Mass PDF
    # rates: prompt \propto SFR
    mass_pdf_prompt = smf_blue * sfr_mass                      # (N, M)
    mass_pdf_prompt /= np.trapz(mass_pdf_prompt, x=xx)[:,None] # normalize
    
    # rates: delayed \propto stellar mass
    mass_pdf_delayed = smf_red * stellar_mass                    # (N, M)
    mass_pdf_delayed /= np.trapz(mass_pdf_delayed, x=xx)[:,None] # normalize

    
    full_pdf = mass_pdf_prompt * fprompt + mass_pdf_delayed * (1-fprompt)
    return xx, np.squeeze(full_pdf)
