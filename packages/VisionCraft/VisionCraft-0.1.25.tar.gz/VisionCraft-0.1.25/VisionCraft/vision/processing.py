"""
processing.py - Module for image processing operations.

This module provides functions for various image processing operations, such as image negation.

Author: Prem Gaikwad
Date: Feb 2024

"""

import numpy as np
from typing import Tuple, Union
import matplotlib.pyplot as plt
from VisionCraft.vision.utils import imShow, imRead


def imgNegative(img : np.ndarray = None, 
                path : str = "",
                show : bool = False,
                height : int = 8, 
                width : int = 10) -> Union[np.ndarray,None]:
    """
    Creates the negative of an input image.

    Parameters:
    - img (np.ndarray, Required is path not given): Input image as a NumPy array. If not provided,
                                   and 'path' is specified, the image will be loaded
                                   from the given path using OpenCV.
    - path (str, Required if img not given): Path to the image file. If provided, 'img' parameter is ignored.
    - show (bool, optional): If True, displays the original and negated images using Matplotlib.
    - height (int, optional): Height of the Matplotlib figure when 'show' is True.
    - width (int, optional): Width of the Matplotlib figure when 'show' is True.

    Returns:
    - np.ndarray: The negated image as a NumPy array.

    Note:
    - If 'path' is provided but the image is not found, a message is printed, and None is returned.
    """
    if img is None:
        img = imRead(path)
        if img is None:
            return img
        
    img_negative = 255 - img
    if show:
        plt.figure(figsize=(width, height))
        imShow("Original Image", img, subplot=True, row=1, col=2, num=1)
        imShow("Image Negation",img_negative, subplot=True, row=1, col=2, num=2)
        plt.show()   
    return img_negative
    

def imgLog(img : np.ndarray = None, 
           path : str = "", 
           show : bool = False,
           height : int = 8, 
           width : int = 10) -> Union[np.ndarray,None]:
    """
    Applies a logarithmic transformation to the input image.

    Parameters:
    - img (np.ndarray, Required is path not given): Input image as a NumPy array. If not provided,
                                   and 'path' is specified, the image will be loaded
                                   from the given path using OpenCV.
    - path (str, Required if img not given): Path to the image file. If provided, 'img' parameter is ignored.
    - show (bool, optional): If True, displays the original and transformed images using Matplotlib.
    - height (int, optional): Height of the Matplotlib figure when 'show' is True.
    - width (int, optional): Width of the Matplotlib figure when 'show' is True.

    Returns:
    - np.ndarray: The transformed image as a NumPy array.

    Note:
    - If 'path' is provided but the image is not found, a message is printed, and None is returned.
    """
    if img is None:
        img = imRead(path)
        if img is None:
            return img
        
    c = 255 / np.log(1 + np.max(np.array(img)))
    img_log = c * np.log(1 + np.array(img))    
    if show:
        plt.figure(figsize=(width, height))
        imShow("Original Image",img, subplot=True, row=1, col=2, num=1)
        imShow("Logarithmic Transformation",img_log, subplot=True, row=1, col=2, num=2)
        plt.show()
    return img_log
        
def powerLaw(img : np.ndarray = None, 
             path : str = "", 
             height : int = 8, 
             width : int = 10, 
             show : bool = False, 
             gamma : float = 1.0) -> Union[np.ndarray,None]:
    """
    Applies a power-law transformation to the input image.

    Parameters:
    - img (np.ndarray, Required is path not given): Input image as a NumPy array. If not provided,
                                   and 'path' is specified, the image will be loaded
                                   from the given path using OpenCV.
    - path (str, Required if img not given): Path to the image file. If provided, 'img' parameter is ignored.
    - height (int, optional): Height of the Matplotlib figure when 'show' is True.
    - width (int, optional): Width of the Matplotlib figure when 'show' is True.
    - show (bool, optional): If True, displays the original and transformed images using Matplotlib.
    - gamma (float, optional): Gamma parameter for the power-law transformation.

    Returns:
    - np.ndarray: The transformed image as a NumPy array.

    Note:
    - If 'path' is provided but the image is not found, a message is printed, and None is returned.
    """
    if img is None:
        img = imRead(path)
        if img is None:
            return img
        
    plt.figure(figsize=(width, height))
    img_pl = 255*(img/255)**gamma
    if show:
        imShow("Original Image",img, subplot=True, row=1, col=2, num=1)
        imShow(f"Gamma {gamma}",img_pl, subplot=True, row=1, col=2, num=2)
        plt.show()
    return img_pl

def flipImg(img : np.ndarray = None, 
            path : bool = False, 
            show : bool = False,
            height : int = 8, 
            width : int = 10) -> Union[None, Tuple[np.ndarray, np.ndarray] ]:
    """
    Flips the input image vertically and horizontally.

    Parameters:
    - img (np.ndarray, Required is path not given): Input image as a NumPy array. If not provided,
                                   and 'path' is specified, the image will be loaded
                                   from the given path using OpenCV.
    - path (str, Required if img not given): Path to the image file. If provided, 'img' parameter is ignored.
    - show (bool, optional): If True, displays the original and flipped images using Matplotlib.
    - height (int, optional): Height of the Matplotlib figure when 'show' is True.
    - width (int, optional): Width of the Matplotlib figure when 'show' is True.

    Returns:
    - Tuple[np.ndarray, np.ndarray]: Tuple containing horizontally and vertically flipped images as NumPy arrays.

    Note:
    - If 'path' is provided but the image is not found, a message is printed, and None is returned.
    """
    if img is None:
        img = imRead(path)
        if img is None:
            return img
        
    img_flip_v = img[::-1]
    img_flip_h = np.array([row[::-1] for row in img])
    if show:
        plt.figure(figsize=(width, height))
        imShow("Original Image",img, subplot=True, row=1, col=3, num=1)           
        imShow("Vertical Flip",img_flip_v, subplot=True, row=1, col=3, num=2)
        imShow("Horizontal Flip",img_flip_h, subplot=True, row=1, col=3, num=3)
        plt.show()
    return img_flip_h, img_flip_v
        
