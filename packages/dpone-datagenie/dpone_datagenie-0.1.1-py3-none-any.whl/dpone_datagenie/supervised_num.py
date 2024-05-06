import numpy as np
from imblearn.over_sampling import SMOTE
from collections import Counter
import pandas as pd

def generate_supervised_numerical_dataframe(num_samples, num_features, mean=0, std=1, seed=None):
    """
    Generate a synthetic supervised numerical dataframe.

    Parameters:
    - num_samples (int): Number of samples in the dataframe.
    - num_features (int): Number of numerical features in the dataframe.
    - mean (float or array-like, optional): Mean of the normal distribution. Default is 0.
    - std (float or array-like, optional): Standard deviation of the normal distribution. Default is 1.
    - seed (int or None, optional): Seed for random number generation. Default is None.

    Returns:
    - df (pandas.DataFrame): Synthetic dataframe with numerical features and labels.
    """
    # Validate input parameters
    if not isinstance(num_samples, int) or num_samples <= 0:
        raise ValueError("num_samples must be a positive integer.")
    if not isinstance(num_features, int) or num_features <= 0:
        raise ValueError("num_features must be a positive integer.")
    if not isinstance(mean, (int, float)) and not isinstance(mean, (list, np.ndarray)):
        raise ValueError("mean must be a single value or an array-like object.")
    if not isinstance(std, (int, float)) and not isinstance(std, (list, np.ndarray)):
        raise ValueError("std must be a single value or an array-like object.")

    # Set seed for reproducibility
    np.random.seed(seed)
    
    # Generate synthetic numerical features
    features_data = np.random.normal(loc=mean, scale=std, size=(num_samples, num_features))
    
    # Generate synthetic labels/targets
    labels = np.random.randint(2, size=num_samples)  # Binary classification labels (0 or 1)
    
    # Create dataframe
    column_names = [f"feature_{i+1}" for i in range(num_features)]
    column_names.append("label")
    df = pd.DataFrame(np.column_stack([features_data, labels]), columns=column_names)
    
    return df



def apply_smote(df, target_column):
    """
    Apply SMOTE (Synthetic Minority Over-sampling Technique) to the dataframe to address class imbalance.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing features and labels.
    - target_column (str): Name of the column containing the target variable.

    Returns:
    - augmented_df (pandas.DataFrame or None): DataFrame with augmented samples, or None if the dataset is too small.
    """
    # Separate features and target variable
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Check if the dataset is large enough for SMOTE
    if len(X) < 6:
        print("Dataset is too small for SMOTE. Returning original dataframe.")
        return None
    
    # Apply SMOTE
    smote = SMOTE()
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    # Combine resampled features and target variable
    augmented_df = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled, name=target_column)], axis=1)
    
    return augmented_df