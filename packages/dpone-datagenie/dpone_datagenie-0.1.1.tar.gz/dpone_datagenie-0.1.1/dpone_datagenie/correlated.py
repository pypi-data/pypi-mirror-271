import numpy as np
import matplotlib.pyplot as plt 
def generate_correlated_features(num_samples, num_features, correlation_strength=0.5, seed=None):
    """
    Generate synthetic correlated numerical features.

    Parameters:
    - num_samples (int): Number of samples in the dataset.
    - num_features (int): Number of numerical features.
    - correlation_strength (float, optional): Strength of correlation between features (between -1 and 1). Default is 0.5.
    - seed (int or None, optional): Seed for random number generation. Default is None.

    Returns:
    - features (numpy.ndarray): Synthetic numerical features with correlation.
    """
    # Validate input parameters
    if not isinstance(num_samples, int) or num_samples <= 0:
        raise ValueError("num_samples must be a positive integer.")
    if not isinstance(num_features, int) or num_features <= 0:
        raise ValueError("num_features must be a positive integer.")
    if not -1 <= correlation_strength <= 1:
        raise ValueError("correlation_strength must be between -1 and 1.")

    # Set seed for reproducibility
    np.random.seed(seed)
    
    # Generate synthetic correlated features
    features = np.random.randn(num_samples, num_features)
    
    # Implement correlation
    if correlation_strength != 0:
        correlation_matrix = np.eye(num_features) + correlation_strength * np.ones((num_features, num_features))
        cholesky_matrix = np.linalg.cholesky(correlation_matrix)
        features = features @ cholesky_matrix
    
    
    df = pd.DataFrame(features)
    return df 