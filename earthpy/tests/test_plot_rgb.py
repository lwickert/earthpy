"""Tests for plot_rgb function"""

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import pytest
import rasterio as rio
from rasterio.plot import plotting_extent
from earthpy.plot import plot_rgb
from earthpy.io import path_to_example

plt.show = lambda: None


@pytest.fixture
def rgb_image():
    """Fixture holding an RGB image for plotting"""
    with rio.open(path_to_example("rmnp-rgb.tif")) as src:
        rgb = src.read()
        ext = plotting_extent(src)
    return rgb, ext


def test_rgb_extent(rgb_image):
    """Test to ensure that when the extent is provided, plot_rgb stretches
     the image or applies the proper x and y lims. Also ensure that the
     correct bands are plotted an in the correct order when the rgb
     param is called and defined. Finally test that a provided title and
     figsize created a plot with the correct title and figsize"""
    a_rgb_image, ext = rgb_image
    f, ax = plot_rgb(
        a_rgb_image,
        extent=ext,
        rgb=(1, 2, 0),
        title="My Title",
        figsize=(5, 5),
    )
    # Get x and y lims to test extent
    plt_ext = ax.get_xlim() + ax.get_ylim()

    plt_array = ax.get_images()[0].get_array()

    assert f.bbox_inches.bounds[2:4] == (5, 5)
    assert ax.get_title() == "My Title"
    assert np.array_equal(plt_array[0], a_rgb_image.transpose([1, 2, 0])[1])
    assert ext == plt_ext


def test_1band(rgb_image):
    """Test to ensure the input image has 3 bands to support rgb plotting.
    If fewer than 3 bands are provided, fail gracefully."""
    a_rgb_image, _ = rgb_image

    with pytest.raises(
        ValueError,
        match="""Input needs to be 3 dimensions and in rasterio
                           order with bands first""",
    ):
        plot_rgb(a_rgb_image[1])


def test_ax_provided(rgb_image):
    """Test to ensure the plot works when an explicit axis is provided"""
    rgb_image, _ = rgb_image
    _, ax1 = plt.subplots()
    f, ax = plot_rgb(rgb_image, ax=ax1)

    rgb_im_shape = rgb_image.transpose([1, 2, 0]).shape
    the_plot_im_shape = ax.get_images()[0].get_array().shape
    assert rgb_im_shape == the_plot_im_shape
    plt.close(f)


def test_ax_not_provided(rgb_image):
    """Test plot_rgb produces an output image when an axis object is
    not provided."""

    rgb_image, _ = rgb_image
    f, ax = plot_rgb(rgb_image)
    rgb_im_shape = rgb_image.transpose([1, 2, 0]).shape
    the_plot_im_shape = ax.get_images()[0].get_array().shape
    assert rgb_im_shape == the_plot_im_shape


def test_stretch_image(rgb_image):
    """Test that running stretch actually stretches the data
    to a max value of 255."""

    im, _ = rgb_image
    np.place(im, im > 150, [0])

    f, ax = plot_rgb(im, stretch=True)
    max_val = ax.get_images()[0].get_array().max()
    assert max_val == 255
    plt.close(f)


def test_stretch_image_clip(rgb_image):
    """Test that if you run clip with a different stretch than the default,
     you get a different mean value given the change in the range of values
     stretched."""

    im, _ = rgb_image
    np.place(im, im > 150, [0])

    f, ax = plot_rgb(im, stretch=True, str_clip=1)
    mean_val = ax.get_images()[0].get_array().mean()
    assert mean_val == 110.23530766608626
    plt.close(f)


im, _ = rgb_image
stretch_vals = list(range(10))
axs = [plot_rgb(im, stretch=True, str_clip=v)[1] for v in stretch_vals]
means = np.array([ax.get_images()[0].get_array().mean() for ax in axs])
n_unique_means = np.unique(mean_vals).shape[0]
assert n_unique_means == len(stretch_clip_vals)


def test_masked_im(rgb_image):
    """Test that a masked image will be plotted using an alpha channel.
    Thus it should return an array that has a 4th dimension representing
    the alpha channel."""

    im, _ = rgb_image
    im_ma = ma.masked_where(im > 140, im)

    f, ax = plot_rgb(im_ma)
    im_plot = ax.get_images()[0].get_array()
    assert im_plot.shape[2] == 4
    plt.close(f)


def test_ticks_off(rgb_image):
    """Test that the output plot has ticks turned off. The ticks
    array should be empty (length == 0)."""

    im, _ = rgb_image

    f, ax = plot_rgb(im)
    assert len(ax.get_xticks()) == 0
    assert len(ax.get_yticks()) == 0
    plt.close(f)