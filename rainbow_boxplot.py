import colorsys
import matplotlib.colors as mc
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def lighten_color(
    color: str | tuple, amount: float = 0.5
) -> tuple[float, float, float]:
    """
     Lightens the given color by multiplying (1-luminosity) by the given amount.

    Args:
        color (str or tuple): Matplotlib color string, hex string, or RGB tuple.
        amount (float): Factor by which to lighten the color. 0 returns black, 1 returns the original color.

    Returns:
        tuple: Lightened RGB color tuple.
    """
    try:
        c = mc.cnames[color]
    except:
        c = color
    # Convert RGB to HLS
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    # Reduce saturation by amount
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def rainbow_boxplot(data: pd.DataFrame, filename: str, dpi: int = 300):
    """
    Creates a rainbow-colored boxplot from the given data.

    Args:
        data (DataFrame): Pandas DataFrame containing the data to plot.
        filename (str): The filename to save the plot to.
        dpi (int): The resolution in dots per inch for the saved figure.
    """

    # Define outlier properties
    flierprops = dict(marker="o", markersize=3)
    # Set the style to only horizontal lines
    sns.set_style("whitegrid")
    # Set up the figure
    fig, ax = plt.subplots(figsize=(12, 6))
    # Delete the frame of the figure
    sns.despine(left=True, ax=ax)

    sns.boxplot(palette="husl", data=data, saturation=1, flierprops=flierprops, ax=ax)

    # Prefer patches (Rectangle boxes). If empty, fall back to artists for older Matplotlib versions.
    containers = ax.patches if len(ax.patches) else ax.artists

    for i, artist in enumerate(containers):
        # Get the fill color (use only RGB part if RGBA is returned)
        face = artist.get_facecolor()
        if hasattr(face, "__len__") and len(face) >= 3:
            face_rgb = tuple(face[:3])
        else:
            face_rgb = face

        col_edge = lighten_color(face_rgb, 1.0)
        # Set edge color to the fill color
        artist.set_edgecolor(col_edge)
        # Set edge linewidth for the box/patch
        try:
            artist.set_linewidth(1.5)
        except Exception:
            # Not all artist types expose set_linewidth; ignore if unavailable
            pass

        # Lighten the fill color by a factor of 0.5 and set it
        col_face = lighten_color(face_rgb, 0.5)
        artist.set_facecolor(col_face)

        # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
        # Loop over them here, and use the same colour as above
        for j in range(i * 6, i * 6 + 6):
            line = ax.lines[j]
            line.set_color(col_edge)
            line.set_mfc(col_edge)
            line.set_mec(col_edge)
            line.set_linewidth(1.5)

    plt.savefig(filename, dpi=dpi)
