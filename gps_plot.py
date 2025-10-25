import gpxpy
import matplotlib.pyplot as plt
import tilemapbase


def load_gps_data(path: str | list[str]) -> list[tuple[float, float]]:
    """Loads GPS data from GPX file or list of GPX files.

    Args:
        path (str | list(str)): Path to single GPX file or list of GPX files.

    Returns:
        list(tuple(float, float)): List of tuples containing longitude and latitude.
    """

    if isinstance(path, str):
        path = [path]

    coordinates = []
    for p in path:
        with open(p, "r") as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        coordinates.append((point.longitude, point.latitude))
    return coordinates


def gps_plot(
    coordinates: list[tuple[float, float]],
    filename: str,
    frame: float = 0.25,
    color: str = "r",
    linestyle: str = "dashed",
    dpi: int = 300,
) -> None:
    """Creates a map plot from GPS coordinates.

    Args:
        coordinates (list(tuple(float, float))): List of tuples containing longitude and latitude.
        filename (str): Output filename for the saved plot.
        frame (float, optional): Frame around the path as a fraction of the path size. Defaults to 0.25.
        color (str, optional): Color of the path. Defaults to "r".
        linestyle (str, optional): Line style of the path. Defaults to "dashed".
        dpi (int, optional): Dots per inch for the saved plot. Defaults to 300.
    """
    lon, lat = zip(*coordinates)
    path = [tilemapbase.project(x, y) for x, y in zip(lon, lat)]
    edges = (min(lon), max(lon), min(lat), max(lat))
    lon_range, lat_range = edges[1] - edges[0], edges[3] - edges[2]
    edges = (
        edges[0] - frame * lon_range,
        edges[1] + frame * lon_range,
        edges[2] - frame * lat_range,
        edges[3] + frame * lat_range,
    )
    x, y = zip(*path)

    tilemapbase.init(create=True)
    t = tilemapbase.tiles.build_OSM()
    extent = tilemapbase.Extent.from_lonlat(*edges)
    extent = extent.to_aspect(1.0, False)
    _, ax = plt.subplots(figsize=(8, 8), dpi=300)
    plotter = tilemapbase.Plotter(extent, t, width=500)
    plotter.plot(ax, t)
    ax.plot(x, y, color=color, linestyle=linestyle)
    plt.savefig(filename, dpi=dpi)
