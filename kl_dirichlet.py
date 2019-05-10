# Requires:
# import numpy as np
# from scipy import special


def divergence(alpha1, beta1, alpha2, beta2):
    import numpy as np
    from scipy import special
        
    # KL divergence between two Dirichlet densities
    # KL(d1||d2)

    # Liu et al. 2006
    #d = np.log(special.beta(alpha2, beta2)/special.beta(alpha1, beta1))
    #d = d+(alpha1-alpha2)*(special.psi(alpha1)-special.psi(alpha1+beta1))
    #d = d+(beta1-beta2)*(special.psi(beta1)-special.psi(alpha1+beta1))
    
    # Wikipedia https://en.wikipedia.org/wiki/Beta_distribution
    d = np.log(special.beta(alpha2, beta2)/special.beta(alpha1, beta1))
    d = d+(alpha1-alpha2)*special.psi(alpha1)
    d = d+(beta1-beta2)*special.psi(beta1)
    d = d+(alpha2-alpha1+beta2-beta1)*special.psi(alpha1+beta1)
    
    return d