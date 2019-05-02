# Requires:
# import numpy as np
# from scipy import special


def kl_dirichlet(lambda_q,lambda_p):
    import numpy as np
    from scipy import special
        
    # KL divergence between two Dirichlet densities
    #
    # Calculate KL (Q||P) = <log Q/P> where avg is wrt Q
    # between two Dirichlet densities Q and P
    #
    # lambda_q      Parameter vector of first density (as list or numpy array)
    # lambda_p      Parameter vector of second density (as list or numpy array)
    # log_tilde_pi  <log (pi)> where avg is over Q. If this argument
    #               isn't passed the routine will calculate it
    #______________________________________________________________

    # Translated into Python from
    # $Id: spm_kl_dirichlet.m 2696 2009-02-05 20:29:48Z guillaume $
    # Copyright (C) 2008 Wellcome Trust Centre for Neuroimaging
    
    lambda_q = np.array(lambda_q)
    lambda_p = np.array(lambda_p)
    
    m           = len(lambda_q)
    lambda_tot  = sum(lambda_q)
    dglt        = special.psi(lambda_tot)
    log_tilde_pi = np.array([])
    for s in range(0, m):
        log_tilde_pi = np.append(log_tilde_pi, special.psi(lambda_q[s])-dglt)
    
    d = special.gammaln(sum(lambda_q))
    d = d+sum((lambda_q-lambda_p)*log_tilde_pi)
    d = d-sum(special.gammaln(lambda_q))
    d = d-special.gammaln(sum(lambda_p))
    d = d+sum(special.gammaln(lambda_p))
    
    return d