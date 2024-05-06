def generate_outliers(num_samples, num_features, num_outliers, outlier_strength=10, seed=None):
    """
    Generate synthetic outliers in a dataset.

    Parameters:
    - num_samples (int): Number of samples in the dataset.
    - num_features (int): Number of numerical features.
    - num_outliers (int): Number of outliers to generate.
    - outlier_strength (float, optional): Strength of the outliers. Default is 10.
    - seed (int or None, optional): Seed for random number generation. Default is None.

    Returns:
    - df (pandas.DataFrame): Synthetic dataset with outliers.
    """
    # Set seed for reproducibility
    np.random.seed(seed)
    
    # Generate synthetic dataset
    df = generate_unsupervised_numerical_dataframe(num_samples, num_features, seed=seed)
    
    # Generate random indices for outliers
    outlier_indices = np.random.choice(num_samples, num_outliers, replace=False)
    
    # Generate outliers
    for i in range(num_features):
        df.iloc[outlier_indices, i] += np.random.randn(num_outliers) * outlier_strength
    
    return df