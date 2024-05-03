import pandas as pd

def get_functions():
    r = {
        'sample': 'get_sample_size'
    }
    return r

def get_sample_size(population_size, population_deviation, margin_of_error = 0.01):
    Z = 1.96  # 95% confidence level's z-score
    N = population_size
    sigma = population_deviation
    E = margin_of_error
    sample_size = ((Z**2) * (sigma**2) * N) / (((Z**2) * (sigma**2)) + ((N - 1) * (E**2)))
    return sample_size