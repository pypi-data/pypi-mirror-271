from scipy import stats
import numpy as np

def apply_noise_convolution(pdf, noise=0.1, keep_norm=True):
    """ """
    norm_noise = stats.norm.pdf( np.linspace(-3, 3, len(pdf)), loc=0, scale=noise)
    pdf_noisy = np.convolve(pdf, norm_noise, mode="same")
    if keep_norm:
        coefs = np.sum(pdf)/np.sum(pdf_noisy) 
    else:
        coefs = 1
        
    return pdf_noisy*coefs
