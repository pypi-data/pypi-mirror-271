# Host 

import numpy as np


# =============== #
#                 #
#  Mass & SFR     #
#                 #
# =============== #
def get_sfr_as_function_of_mass_and_redshift(mass, redshift, power=0.8):
    """ equation A.7 from Childress et al. 2014, used in Wiseman et al. 2021.
    We use power of 0.8 rather than the default 0.7 as it fits better our data given the SMF we use.

    0.8 is in agreement with Vilella-Rojo et al. (2021) literature summary table 
    (https://ui.adsabs.harvard.edu/abs/2021A%26A...650A..68V/abstract)
    """
    ampl = (10**(mass)/10**10)**power    

    fraction = np.exp(1.9*redshift)/ (np.exp(1.7* (redshift-2)) + np.exp(0.2* (redshift-2)))
    
    return  ampl * fraction

def get_schechterpdf(mass, mstar, alpha, phi, alpha2=None, phi2=None):
    """ """
    delta_logmass = mass-mstar
    # single schechter
    if alpha2 is None or phi2 is None: 
        return np.log(10)* np.exp(-10**(delta_logmass)) *  phi * ( 10**(delta_logmass*(1+alpha)) )

    # double schechter
    return np.log(10)* np.exp(-10**(delta_logmass)) * 10**(delta_logmass) * (phi*10**(delta_logmass*alpha) + 
                                                                    phi2*10**(delta_logmass*alpha2))
def get_stellar_mass_function(redshift, which="all", xx="6:12:100j",
                             offset=0.5):
    """ get the stellar mass function at the given redshift
    SMF froml Davidzon et al. 2017 (COSMO2015, https://www.aanda.org/articles/aa/pdf/2017/09/aa30419-17.pdf)
    They are close to Weaver et al. 2023 (COSMO2020, https://www.aanda.org/articles/aa/pdf/2023/09/aa45581-22.pdf)

    = Redshift ignored so far = 
    """
    if type(xx) == str: # assumed r_ input
        xx = eval(f"np.r_[{xx}]")

    # Davidzon et al. 2017
    prop = {(0., 0.5):
               {"all": {"mstar":10.78, "alpha":-1.38, "phi":1.19*1e-3,  "alpha2":-0.43, "phi2":1.92*1e-3},
                "blue":{"mstar":10.26, "alpha":-1.29, "phi":2.40*1e-3,  "alpha2":+1.01, "phi2":1.30*1e-3},
                "red": {"mstar":10.83, "alpha":-1.30, "phi":0.098*1e-3, "alpha2":-0.39, "phi2":1.58*1e-3}
               },
            (0.5, 0.8):
               {"all": {"mstar":10.77, "alpha":-1.36, "phi":1.07*1e-3,  "alpha2":+0.03, "phi2":1.68*1e-3},
                "blue":{"mstar":10.40, "alpha":-1.32, "phi":1.66*1e-3,  "alpha2":+0.84, "phi2":0.86*1e-3},
                "red": {"mstar":10.83, "alpha":-1.46, "phi":0.012*1e-3, "alpha2":-0.21, "phi2":1.33*1e-3}
               },
            (0.8, 1.1):
               {"all": {"mstar":10.56, "alpha":-1.31, "phi":1.43*1e-3,  "alpha2":+0.51, "phi2":2.19*1e-3},
                "blue":{"mstar":10.35, "alpha":-1.29, "phi":1.74*1e-3,  "alpha2":+0.81, "phi2":0.95*1e-3},
                "red": {"mstar":10.75, "alpha":-0.07, "phi":1.72*1e-3} # single Schechter for passive
               },
            (1.1, 1.5):
               {"all": {"mstar":10.62, "alpha":-1.28, "phi":1.07*1e-3,  "alpha2":+0.29, "phi2":1.21*1e-3},
                "blue":{"mstar":10.42, "alpha":-1.21, "phi":1.54*1e-3,  "alpha2":+1.11, "phi2":0.49*1e-3},
                "red": {"mstar":10.56, "alpha":+0.53, "phi":0.76*1e-3} # single Schechter for passive
               },

            (1.5, 2.0):
               {"all": {"mstar":10.51, "alpha":-1.28, "phi":0.97*1e-3,  "alpha2":+0.82, "phi2":0.64*1e-3},
                "blue":{"mstar":10.40, "alpha":-1.24, "phi":1.16*1e-3,  "alpha2":+0.90, "phi2":0.46*1e-3},
                "red": {"mstar":10.54, "alpha":+0.93, "phi":0.25*1e-3} # single Schechter for passive
               },
            (2., 2.5):
               {"all": {"mstar":10.60, "alpha":-1.57, "phi":0.30*1e-3,  "alpha2":+0.07, "phi2":0.45*1e-3},
                "blue":{"mstar":10.45, "alpha":-1.50, "phi":0.44*1e-3,  "alpha2":+0.59, "phi2":0.38*1e-3},
                "red": {"mstar":10.69, "alpha":+0.17, "phi":0.07*1e-3} # single Schechter for passive
               },
           }
    
    redshift = np.atleast_1d(redshift)
    if len(redshift)==1:
        redshift_ = redshift[0]
        for k,prop_ in prop.items():
            if redshift_>k[0] and redshift_<k[1]:
                break
            
        pdf = get_schechterpdf(xx+offset, **prop_[which])
        
    else:
        pdf = []
        for redshift_ in redshift:
            for k,prop_ in prop.items():
                if redshift_>k[0] and redshift_<k[1]:
                    break
                
            pdf.append(get_schechterpdf(xx+offset, **prop_[which]))
            
    return xx, np.asarray(pdf)
