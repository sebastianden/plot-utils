import numpy as np
import pandas as pd
from rainbow_boxplot import rainbow_boxplot


def rand_data(num_classes, num_samples, std):
    # Create a placeholder vector
    data = np.empty((0, num_samples))
    # Create num_classes samples
    for i in range(num_classes):
        # Choose mean by quadratic function
        x = i - (num_classes * 0.5) + 0.5
        # Create one sample with std and num_samples points
        sample = np.random.normal(loc=-0.5 * x * x, scale=std, size=(1, num_samples))
        # Append to placeholder
        data = np.append(data, sample, axis=0)
    # Transpose (for seaborne visualisation)
    data = data.T
    # Save as pandas dataframe
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":

    data = rand_data(30, 100, 3)  # Create random data in shape of a rainbow
    rainbow_boxplot(data, "./img/rainbow_boxplot.png")  # Create rainbow boxplot
