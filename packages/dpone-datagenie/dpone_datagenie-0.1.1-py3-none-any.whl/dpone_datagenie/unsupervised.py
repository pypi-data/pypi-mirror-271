def generate_unsupervised_numerical_dataframe(num_samples, num_features, mean=0, std=1, seed=None):
    """
    Generate a synthetic unsupervised numerical dataframe.

    Parameters:
    - num_samples (int): Number of samples in the dataframe.
    - num_features (int): Number of numerical features in the dataframe.
    - mean (float or array-like, optional): Mean of the normal distribution. Default is 0.
    - std (float or array-like, optional): Standard deviation of the normal distribution. Default is 1.
    - seed (int or None, optional): Seed for random number generation. Default is None.

    Returns:
    - df (pandas.DataFrame): Synthetic dataframe with numerical features.
    """
    # Set seed for reproducibility
    np.random.seed(seed)
    
    # Generate synthetic numerical features
    features_data = np.random.normal(loc=mean, scale=std, size=(num_samples, num_features))
    
    # Create dataframe
    column_names = [f"feature_{i+1}" for i in range(num_features)]
    df = pd.DataFrame(features_data, columns=column_names)
    
    return df
