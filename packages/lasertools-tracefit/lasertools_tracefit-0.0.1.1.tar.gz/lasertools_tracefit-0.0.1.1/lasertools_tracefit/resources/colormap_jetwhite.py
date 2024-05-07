"""Module to create colormap"""
import matplotlib as mpl
import numpy as np


def create_colormap():
    """Create the colormap"""
    upper_cmap = mpl.cm.jet(np.arange(256))
    lower_cmap = np.ones((int(64), 4))
    for i in range(3):
        lower_cmap[:, i] = np.linspace(
            1, upper_cmap[0, i], lower_cmap.shape[0]
        )
    cmap_rgbs = np.vstack((lower_cmap, upper_cmap))
    cmap = mpl.colors.ListedColormap(
        cmap_rgbs, name="modifiedJet", N=cmap_rgbs.shape[0]
    )
    return cmap
