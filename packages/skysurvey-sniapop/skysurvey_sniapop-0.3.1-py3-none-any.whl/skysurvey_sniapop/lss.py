from scipy import stats, special
import numpy as np

def get_cluster_radius(size,
                        logprob=stats.genlogistic(c=0.33, loc=1.585, scale=0.13), 
                        as_log=False):
    """ """
    r_sample = logprob.rvs(size)
    if not as_log:
        r_sample = 10**r_sample
        
    return r_sample


def get_cluster_prompt(radius, redshift, r0=2, gamma=4, k=0.87):
    """ """
    prompt_cluster = special.expit(np.log10(radius/r0)*gamma)
    #prompt_cluster = (1- (1+radius/r0)**(-gamma))
    prompt = prompt_cluster * delta_z(redshift, k=k)
    return prompt
