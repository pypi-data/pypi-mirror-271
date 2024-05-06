import matplotlib.pyplot as plt
import seaborn as sns

def plot_correlation(df):
    """
    Plot correlation heatmap for the features in the dataframe.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing the features.

    Returns:
    - None
    """
    # Compute correlation matrix
    corr_matrix = df.corr()
    
    # Plot heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Plot')
    plt.show()

def plot_distribution(df):
    """
    Plot distribution of each feature in the dataframe.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing the features.

    Returns:
    - None
    """
    # Plot distribution
    plt.figure(figsize=(15, 10))
    for column in df.columns:
        if column != 'label':  # Exclude label column from distribution plot
            sns.histplot(df[column], kde=True, label=column, alpha=0.5)
    plt.title('Distribution Plot')
    plt.legend()
    plt.show()
