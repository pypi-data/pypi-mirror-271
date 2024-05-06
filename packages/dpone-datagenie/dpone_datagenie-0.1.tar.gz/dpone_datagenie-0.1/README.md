# Synthetic: A Python Library for Synthetic Data Generation

Synthetic is a Python library designed to facilitate the generation of synthetic datasets for machine learning and artificial intelligence applications. It provides functions to create synthetic dataframes with various features, including numerical and categorical variables, and offers utilities for visualization and data augmentation. With Synthetic, users can quickly generate synthetic datasets tailored to their specific needs, whether for model training, testing, or exploration.

## Features

- **Supervised Data Generation**: Generate synthetic datasets with labeled data for supervised learning tasks.
- **Numerical and Categorical Features**: Create synthetic dataframes with both numerical and categorical features.
- **Visualization Tools**: Visualize correlations and distributions of features within the synthetic datasets.
- **Data Augmentation**: Apply techniques such as SMOTE (Synthetic Minority Over-sampling Technique) to address class imbalance in the datasets.

## Installation

You can install Synthetic using pip:

```bash
pip install synthetic
```

## Usage

### 1. Generating Synthetic Dataframes

```python
import synthetic.generate as synthetic

# Generate a supervised numerical dataframe
numerical_df = synthetic.generate_supervised_numerical_dataframe(num_samples=1000, num_features=5)

# Generate a supervised dataframe with mixed numerical and categorical features
mixed_df = synthetic.generate_supervised_mixed_dataframe(num_samples=1000, num_numerical_features=3, num_categorical_features=2)

# Display the first few rows of the generated dataframes
print("Numerical DataFrame:")
print(numerical_df.head())

print("\nMixed DataFrame:")
print(mixed_df.head())
```

### 2. Visualization

```python
import synthetic

# Plot correlation heatmap
synthetic.plot_correlation(mixed_df)

# Plot distribution of features
synthetic.plot_distribution(mixed_df)
```

### 3. Data Augmentation

```python
import synthetic

# Apply SMOTE for data augmentation
augmented_df = synthetic.apply_smote(mixed_df, target_column='label')

# Display the first few rows of the augmented dataframe
print("Augmented DataFrame:")
print(augmented_df.head())
```

## Examples

For more examples and detailed usage instructions, please refer to the [Examples](./examples) directory in the repository.

## Contributing

We welcome contributions from the community. If you encounter any issues, have suggestions for improvements, or would like to contribute code, please feel free to open an issue or pull request on our [GitHub repository](https://github.com/your_username/synthetic).

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
