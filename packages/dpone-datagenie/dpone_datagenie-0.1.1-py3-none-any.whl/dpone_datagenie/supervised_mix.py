
import numpy as np
import pandas as pd

def generate_supervised_mixed_dataframe(num_samples, num_numerical_features, num_categorical_features, num_categories_per_feature=3, numerical_mean=0, numerical_std=1, seed=None):
    """
    Generate a synthetic supervised dataframe with mixed numerical and categorical features.

    Parameters:
    - num_samples (int): Number of samples in the dataframe.
    - num_numerical_features (int): Number of numerical features in the dataframe.
    - num_categorical_features (int): Number of categorical features in the dataframe.
    - num_categories_per_feature (int, optional): Number of categories per categorical feature. Default is 3.
    - numerical_mean (float or array-like, optional): Mean of the normal distribution for numerical features. Default is 0.
    - numerical_std (float or array-like, optional): Standard deviation of the normal distribution for numerical features. Default is 1.
    - seed (int or None, optional): Seed for random number generation. Default is None.

    Returns:
    - df (pandas.DataFrame): Synthetic dataframe with mixed numerical and categorical features and labels.
    """
    # Validate input parameters
    if not isinstance(num_samples, int) or num_samples <= 0:
        raise ValueError("num_samples must be a positive integer.")
    if not isinstance(num_numerical_features, int) or num_numerical_features <= 0:
        raise ValueError("num_numerical_features must be a positive integer.")
    if not isinstance(num_categorical_features, int) or num_categorical_features <= 0:
        raise ValueError("num_categorical_features must be a positive integer.")
    if not isinstance(num_categories_per_feature, int) or num_categories_per_feature <= 0:
        raise ValueError("num_categories_per_feature must be a positive integer.")
    if not isinstance(numerical_mean, (int, float)) and not isinstance(numerical_mean, (list, np.ndarray)):
        raise ValueError("numerical_mean must be a single value or an array-like object.")
    if not isinstance(numerical_std, (int, float)) and not isinstance(numerical_std, (list, np.ndarray)):
        raise ValueError("numerical_std must be a single value or an array-like object.")

    # Set seed for reproducibility
    np.random.seed(seed)
    
    # Generate synthetic numerical features
    numerical_features_data = np.random.normal(loc=numerical_mean, scale=numerical_std, size=(num_samples, num_numerical_features))
    
    # Generate synthetic categorical features
    categorical_features_data = np.random.randint(num_categories_per_feature, size=(num_samples, num_categorical_features))
    
    # Combine numerical and categorical features
    features_data = np.concatenate((numerical_features_data, categorical_features_data), axis=1)
    
    # Generate synthetic labels/targets
    labels = np.random.randint(2, size=num_samples)  # Binary classification labels (0 or 1)
    
    # Create dataframe
    numerical_column_names = [f"numerical_feature_{i+1}" for i in range(num_numerical_features)]
    categorical_column_names = [f"categorical_feature_{i+1}" for i in range(num_categorical_features)]
    column_names = numerical_column_names + categorical_column_names + ["label"]
    df = pd.DataFrame(np.column_stack([features_data, labels]), columns=column_names)
    
    return df

