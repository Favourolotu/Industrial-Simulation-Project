import numpy as np


def expo_inverse_cdf(p_value, lambda_value):
    """
        Calculate the inverse cumulative distribution function of the Exponential distribution given 
        a p-value lambda.
    """
    # Lambda = 1 / sample_mean
    return (-np.log(1-p_value))/lambda_value