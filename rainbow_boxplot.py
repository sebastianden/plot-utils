import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import colorsys


def rand_data(num_classes,num_samples,std):
    # Create a placeholder vector
    data = np.empty((0,num_samples))
    # Create num_classes samples
    for i in range(num_classes):
        # Choose mean by quadratic function
        x = i-(num_classes*0.5)+0.5
        # Create one sample with std and num_samples points
        sample=np.random.normal(loc=-0.5*x*x,scale=std,size=(1,num_samples))
        # Append to placeholder
        data = np.append(data,sample,axis=0)
    # Transpose (for seaborne visualisation)
    data = data.T
    # Save as pandas dataframe
    df = pd.DataFrame(data)
    return df


# Take a RGB color and lighten it by a given factor
def lighten_color(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        c = color
    # Convert RGB to HLS
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    # Reduce saturation by amount
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


if __name__ == "__main__":
    
    data = rand_data(30,100,3)  # Create random data in shape of a rainbow

    # Define outlier properties
    flierprops = dict(marker='o', markersize=3)
    # Set the style to only horizontal lines
    sns.set_style("whitegrid")
    # Set up the figure
    fig, ax = plt.subplots(figsize=(12,6))
    # Delete the frame of the figure
    sns.despine(left=True,ax=ax)

    sns.boxplot(palette="husl", data=data, saturation=1, flierprops=flierprops, ax=ax)

    for i,artist in enumerate(ax.artists):
        # Get the fill color
        col_edge = lighten_color(artist.get_facecolor(), 1.0)
        # Set edge color to the fill color
        artist.set_edgecolor(col_edge)
        # Lighten the fill color by a faktor of 0.5 and set it
        col_face = lighten_color(artist.get_facecolor(), 0.5)
        artist.set_facecolor(col_face)
        #artist.set_facecolor((1,1,1))  # delete fill

        # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
        # Loop over them here, and use the same colour as above
        for j in range(i*6,i*6+6):
            line = ax.lines[j]
            line.set_color(col_edge)
            line.set_mfc(col_edge)
            line.set_mec(col_edge)
            line.set_linewidth(1.5)
    plt.savefig("rainbow.png", dpi=300)
    plt.show()

