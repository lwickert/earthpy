""" Tests for the mask module. """

import numpy as np
from earthpy.mask import mask_pixels
import pytest


@pytest.fixture
def im():
    """Create image arr for masking"""
    return np.random.randint(10, size=(4, 5))


@pytest.fixture
def im_mask():
    """Create image mask"""
    return np.random.randint(5, size=(4, 5))


def test_arr_provided(im, im_mask):
    """ Test for arrays provided as image and/or mask input. """

    an_arr_tup = (2, 3)
    with pytest.raises(
        AttributeError, match="Input arr should be a numpy array."
    ):
        mask_pixels(an_arr_tup, mask_arr=im_mask, vals=[0, 4])
    with pytest.raises(
        AttributeError, match="Input arr should be a numpy array."
    ):
        mask_pixels(im, mask_arr=an_arr_tup, vals=[0, 4])


def test_masked_arr_returned(im, im_mask):
    """ Test for return of masked_array type. """

    masked = mask_pixels(im, im_mask, vals=[0, 4])
    assert np.ma.is_masked(masked)


# This is not doing what i would expect it to do.
# This test doesn't make sense as is.
# def test_val_list_provided(im, im_mask):
#    """ Provide a singular value to the vals keyword to raise AttributeError"""

#    with pytest.raises(ValueError):
#        mask_pixels(im, mask_arr=im_mask, vals=0)


def test_mask_vals_in_arr(im, im_mask):
    """If vals are not found in mask_arr, fail gracefully"""

    im_mask_no_ones = im_mask * 0
    with pytest.raises(
        ValueError,
        match="""List of values provided for the mask does 
                             not exist in your mask array.""",
    ):
        mask_pixels(im, im_mask_no_ones, [3, 4])

    # def test_boolean_mask_provided(im, im_mask):
    """If a boolean arr is provided, mask returns masked arr"""

    # im_with_mask = np.ma.masked_where(im_mask < 2, im)
    # im_result = mask_pixels(im, im_mask)
    # assert np.ma.is_masked(im_result)


def test_boolean_mask(im, im_mask):

    im_mask[im_mask > 1] = 1

    assert np.ma.is_masked(mask_pixels(im, im_mask))


def test_user_mask_arr(im, im_mask):
    """Test to see if user is passing in their own masked array
    instead of a pixel QA layer and values to mask."""

    with pytest.raises(
        ValueError,
        match="""You have provided a mask_array with no values to mask""",
    ):
        mask_pixels(im, im_mask)
