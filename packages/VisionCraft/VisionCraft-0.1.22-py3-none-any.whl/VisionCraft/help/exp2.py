# -*- coding: utf-8 -*-
"""
# **Utils**
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

def imShow(title: str = "",
           image: np.ndarray = None,
           subplot: bool = False,
           row: int = 0, col: int = 0, num: int = 0) -> None:

    if subplot:
        plt.subplot(row, col, num)
        plt.imshow(image, cmap="gray")
        plt.title(title)
        plt.axis('off')
    else:
        plt.imshow(image, cmap="gray")
        plt.title(title)
        plt.axis('off')
        plt.show()

"""# **Exp1**"""

# Import Libaries
import cv2
import matplotlib.pyplot as plt
import numpy as np

print("OpenCV Version: ",cv2.__version__)

# Reading an Image
print("Image")
img = cv2.imread("/content/drive/MyDrive/dip_Images/Fig0354(a)(einstein_orig).tif")
plt.imshow(img)
plt.axis("off")
plt.show()

# Resizing an Image

print("Before")
plt.imshow(img)
plt.axis("off")
plt.show()
print("After")
img_resize = cv2.resize(img,(287,133))
plt.imshow(img_resize)
plt.axis("off")
plt.show()

# Rotating an Image
img_rotate = cv2.rotate(img, cv2.ROTATE_180)
print("Rotated 180")
plt.imshow(img_rotate)
plt.axis("off")
plt.show()

# Adding two Images

img2 = cv2.imread("/content/drive/MyDrive/dip_Images/Fig0327(a)(tungsten_original).tif")
img2 = cv2.resize(img2, (img.shape[1], img.shape[0]))
img_add = cv2.add(img, img2)
print("IMG1")
plt.imshow(img)
plt.axis("off")
plt.show()
print("IMG2")
plt.imshow(img2)
plt.axis("off")
plt.show()
print("IMG1+IMG2")
plt.imshow(img_add)
plt.axis("off")
plt.show()

# Get Histogram for color channels
r_hist = cv2.calcHist(img, channels=[0], mask=None, histSize=[256], ranges=[0, 256])
g_hist = cv2.calcHist(img, channels=[1], mask=None, histSize=[256], ranges=[0, 256])
b_hist = cv2.calcHist(img, channels=[2], mask=None, histSize=[256], ranges=[0, 256])

plt.figure(figsize=(15,5))
plt.plot(r_hist, color='red', label='Red Channel')
plt.plot(g_hist, color='green', label='Green Channel')
plt.plot(b_hist, color='blue', label='Blue Channel')

plt.xlabel('Pixel Value')
plt.ylabel('Intensity')
plt.title('RGB Histogram')
plt.legend()

plt.show()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print("BW Image")
plt.imshow(img_gray)
plt.axis("off")
plt.show()
print("HLS Image")
img_HLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
plt.imshow(img_HLS)
plt.axis("off")
plt.show()

_, img_thres = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
plt.imshow(img_thres)
plt.axis("off")
plt.show()

_, img_thres = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
plt.imshow(img_thres)
plt.axis("off")
plt.show()

_, img_thres = cv2.threshold(img, 150, 255, cv2.THRESH_TRUNC)
plt.imshow(img_thres)
plt.axis("off")
plt.show()

_, img_thres = cv2.threshold(img, 150, 255, cv2.THRESH_TOZERO)
plt.imshow(img_thres)
plt.axis("off")
plt.show()

_, img_thres = cv2.threshold(img, 150, 255, cv2.THRESH_TOZERO_INV)
plt.imshow(img_thres)
plt.axis("off")
plt.show()

print("Before")
plt.imshow(img)
plt.axis("off")
plt.show()
print()
noise = np.zeros_like(img, dtype=np.float32)
cv2.randn(noise, 0, 10)
noisy_img = cv2.add(img, noise.astype(np.uint8))
print("After")
plt.imshow(noisy_img)
plt.axis("off")
plt.show()

"""# **Exp 2**"""

# Image Negative
img = cv2.imread("/content/drive/MyDrive/dip_Images/Fig0327(a)(tungsten_original).tif",cv2.COLOR_BGR2GRAY)
imShow("Original Image",img, subplot=True, row=1, col=2, num=1)
img_negative = 255 - img
imShow("Image Negation",img_negative, subplot=True, row=1, col=2, num=2)

c = 255 / np.log(1 + np.max(np.array(img)))
img_log = np.round(c * np.log(1 + np.array(img)))
imShow("Original Image", img, subplot=True, row=1, col=2, num=1)
imShow("Logarithmic Transfored Image", img_log, subplot=True, row=1, col=2, num=2)

img_light = cv2.imread("/content/drive/MyDrive/dip_Images/Fig0309(a)(washed_out_aerial_image).tif",cv2.COLOR_BGR2GRAY)
plt.figure(figsize=(15,12))
gammas = [0.04, 0.1, 0.2, 0.4, 0.67, 1 , 1.5, 2.5, 5, 10, 25, 30]
img_no = 1
for gamma in gammas:
    img_pl = 255*(img_light/255)**gamma
    if img_no == 1:
        imShow("Original Image",img_light, subplot=True, row=3, col=4, num=1)
    else:
        imShow(f"Gamma {gamma}",img_pl, subplot=True, row=3, col=4, num=img_no)
    img_no += 1

plt.figure(figsize=(15,12))
img_dollar = cv2.imread("/content/drive/MyDrive/dip_Images/Fig0314(a)(100-dollars).tif",cv2.COLOR_BGR2GRAY)
imShow("Original Image",img_dollar, subplot=True, row=1, col=3, num=1)

img_flip_v = cv2.flip(img_dollar, 0)
imShow("Vertical Flip",img_flip_v, subplot=True, row=1, col=3, num=2)

img_flip_h = cv2.flip(img_dollar, 1)
imShow("Horizontal Flip",img_flip_h, subplot=True, row=1, col=3, num=3)

"""# **Exp 3**"""

def gray_level_slicing(path, lower, upper, bg = False, THRESHOLD = 256):
    image = cv2.imread(path,cv2.COLOR_BGR2GRAY)
    rows, cols = image.shape
    for row in range(rows):
        for col in range(cols):
            if lower <= image[row][col] <= upper:
                image[row][col] = THRESHOLD-1
            else:
                if bg:
                    pass
                else:
                    image[row][col] = 0
    return image

plt.figure(figsize=(10,5))
path = "/content/drive/MyDrive/dip_Images/Fig0308(a)(fractured_spine).tif"
img_sliced_nbg = gray_level_slicing(path, 100, 200)
img_sliced_bg = gray_level_slicing(path, 100, 200, bg = True)
img = cv2.imread(path, cv2.COLOR_BGR2GRAY)
imShow("Original Image", img, subplot=True, row=1, col=3, num=1)
imShow("Grey Level Slicing Without BG", img_sliced_nbg, subplot=True, row=1, col=3, num=2)
imShow("Grey Level Slicing With BG", img_sliced_bg, subplot=True, row=1, col=3, num=3)

def bit_plane_slicing(path):
    for bit in range(8):
        img = cv2.imread(path,0)
        plane=np.zeros_like(img)
        plane[img&(1<<bit)!=0]=255
        imShow(f"Bit Plane {bit}", plane, subplot=True, row = 2, col = 4, num=bit+1)
plt.figure(figsize=(15,4))
bit_plane_slicing(path="/content/drive/MyDrive/dip_Images/Fig0314(a)(100-dollars).tif")

def contrast_stretching(path=None, s1=30, s2 = 150, r1=80, r2=150, L=255):
    img = cv2.imread(path,cv2.COLOR_BGR2GRAY)
    imShow("Original Image", img, subplot=True, row = 2, col = 2, num=1)
    plt.subplot(2,2,3)
    plt.title("Original Histogram")
    plt.hist(img.ravel(), 256, [0,256])

    a = s1/r1
    b = (s2-s1)/(r2-r1)
    g = (L-s2)/(L-r2)

    rows, cols = img.shape
    for row in range(rows):
        for col in range(cols):
            if img[row][col] <= r1:
                img[row][col] = a*img[row][col]
            elif img[row][col] >r1 and img[row][col] <=r2:
                r = img[row][col]
                img[row][col] = b*(r-r1) + s1
            else:
                r = img[row][col]
                img[row][col] = g*(r-r2) + s2
    imShow("Contrast Stretching Image", img, subplot=True, row = 2, col = 2, num=2)
    plt.subplot(2,2,4)
    plt.title("Contrasted Histogram")
    plt.hist(img.ravel(),256,[0,256])
plt.figure(figsize=(12,6))
path = "/content/drive/MyDrive/dip_Images/Fig0316(2)(2nd_from_top).tif"
contrast_stretching(path = path)

"""# **Exp 4**"""

plt.figure(figsize=(15,15))

image_paths = [
    "/content/drive/MyDrive/dip_Images/Fig0320(4)(bottom_left).tif",     # Dark img
    "/content/drive/MyDrive/dip_Images/Fig0320(1)(top_left).tif",        # Light img
    "/content/drive/MyDrive/dip_Images/Fig0316(3)(third_from_top).tif",  # High contrast img
    "/content/drive/MyDrive/dip_Images/Fig0316(2)(2nd_from_top).tif"     # low contrast img
]

img_type = [
    "Dark Image",
    "Light Image",
    "High Contrast Image",
    "Low Contrast Image"
]

subplot_count = 0
for index in range(len(image_paths)):
    img = cv2.imread(image_paths[index], 1)
    imShow(title=img_type[index], image= img, subplot=True, row=4,col=2,num=2*index+1)
    plt.subplot(4,2,2*index+2)
    plt.hist(img.ravel(),256,[0,256])
plt.show()

def Histogram_Equilization(path:str):
    plt.figure(figsize=(14,10))
    img = cv2.imread(path,1)
    imShow("Original Image", img, subplot=True, row=2, col=2, num=1)
    plt.subplot(2,2,2)
    plt.hist(img.ravel(),256,[0,256])
    img = cv2.imread(path,0) # Reading again in zero mode to avoid an error of CV_8UC1
    img = cv2.equalizeHist(img)
    imShow("Histogram Equilization", img, row=2, col=2, num=3, subplot=True)
    plt.subplot(2,2,4)
    plt.hist(img.ravel(),256,[0,256])

Histogram_Equilization("/content/drive/MyDrive/dip_Images/Fig0316(2)(2nd_from_top).tif")
plt.show()

"""# **Exp 5**"""

img = cv2.imread("/content/drive/MyDrive/dip_Images/Fig0333(a)(test_pattern_blurring_orig).tif", 0)

def box_filter(filter_size, img, CONSTANT=255):
    rows, cols = img.shape
    img1 = np.pad(img, pad_width=int(np.floor(filter_size/2)), mode='constant', constant_values=CONSTANT)
    filtered_img = np.zeros_like(img)
    for row in range(rows):
        for col in range(cols):
            replace = np.round(np.sum(img1[row:row+filter_size, col:col+filter_size])/(filter_size*filter_size))
            filtered_img[row,col]=  replace

    plt.figure(figsize=(5, 3))
    imShow("Original Image",img, subplot=True, row=1,col=2, num=1)
    imShow(f"{filter_size} x {filter_size} Box Filter",filtered_img,subplot=True, row=1,col=2, num=2)
    plt.show()

# 3 x 3 Filter
box_filter(3,img)
# 5 x 5 Filter
box_filter(5,img)

def weighted_filter(filter, img):
    if filter == 3:
        kernel = np.array([[1,2,1],
                           [2,4,2],
                           [1,2,1]]) / 16
    elif filter == 5:
        kernel = np.array([[1, 4, 6, 4, 1],
                           [4,16,24,16, 4],
                           [6,24,36,24, 6],
                           [4,16,24,16, 4],
                           [1, 4, 6, 4, 1]]) / 256
    img = cv2.filter2D(img,-1,kernel)
    return img
img = cv2.imread("/content/drive/MyDrive/dip_Images/Fig0333(a)(test_pattern_blurring_orig).tif", 0)
imShow("Original Image", img, subplot=True, row=1, col=3, num=1)
imShow("3x3 Image", weighted_filter(3,img), subplot=True, row=1, col=3, num=2)
imShow("5x5 Image", weighted_filter(5,img), subplot=True, row=1, col=3, num=3)

filter_size = 3

rows, cols = img.shape
img1 = np.pad(img, pad_width=int(np.floor(filter_size/2)), mode='constant', constant_values=255)
filtered_img = np.zeros_like(img)
for row in range(rows):
    for col in range(cols):
        replace = np.median(img1[row:row+filter_size, col:col+filter_size])
        filtered_img[row,col]=  replace

plt.figure(figsize=(5, 3))
imShow("Original Image",img, subplot=True, row=1,col=2, num=1)
imShow("Median Filter",filtered_img,subplot=True, row=1, col=2, num=2)
plt.show()

rows, cols = img.shape
img1 = np.pad(img, pad_width=int(np.floor(filter_size/2)), mode='constant', constant_values=255)
filtered_img = np.zeros_like(img)
for row in range(rows):
    for col in range(cols):
        replace = np.min(img1[row:row+filter_size, col:col+filter_size])
        filtered_img[row,col]=  replace

plt.figure(figsize=(5, 3))
imShow("Original Image",img, subplot=True, row=1,col=2, num=1)
imShow("Min Filter",filtered_img,subplot=True, row=1,col=2, num=2)
plt.show()

rows, cols = img.shape
img1 = np.pad(img, pad_width=int(np.floor(filter_size/2)), mode='constant', constant_values=255)
filtered_img = np.zeros_like(img)
for row in range(rows):
    for col in range(cols):
        replace = np.max(img1[row:row+filter_size, col:col+filter_size])
        filtered_img[row,col]=  replace

plt.figure(figsize=(5, 3))
imShow("Original Image",img, subplot=True, row=1,col=2, num=1)
imShow("Max Filter",filtered_img,subplot=True, row=1,col=2, num=2)
plt.show()

"""# **Exp 6**"""

T = 150
img = cv2.imread("/content/drive/MyDrive/dip_Images/Fig0305(a)(DFT_no_log).tif",0)
rows, cols = img.shape
img1 = np.pad(img, pad_width=1, mode='constant', constant_values=255)
filtered_img = np.zeros_like(img)
mask = np.array([[-1,-1,-1],
                 [-1, 8,-1],
                 [-1,-1,-1]])
for row in range(rows):
    for col in range(cols):
        replace = np.sum(img1[row:row+3, col:col+3] * mask)
        if replace > T:
            filtered_img[row,col]=  255
        else:
            filtered_img[row,col]=  0

plt.figure(figsize=(10, 8))
imShow("Original Image",img, subplot=True, row=1,col=2, num=1)
imShow("Point Detection Image",filtered_img,subplot=True, row=1, col=2, num=2)
plt.show()

T = 70

rows, cols = img.shape
img1 = np.pad(img, pad_width=1, mode='constant', constant_values=255)
filtered_img = np.zeros_like(img)

horizontal_mask = np.array([[-1,-1,-1],
                            [ 2, 2, 2],
                            [-1,-1,-1]])

vertical_mask = np.array([[-1, 2,-1],
                          [-1, 2,-1],
                          [-1, 2,-1]])
# +45*
deg45_mask = np.array([[-1,-1, 2],
                       [-1, 2,-1],
                       [ 2,-1,-1]])

# -45*
degn45_mask = np.array([[ 2,-1,-1],
                        [-1, 2,-1],
                        [-1,-1, 2]])
masks = [horizontal_mask, vertical_mask, deg45_mask, degn45_mask]
merged_img = np.zeros_like(img)
output  = []

for mask in masks:
    filtered_img = np.zeros_like(img)
    for row in range(rows):
        for col in range(cols):
            replace = np.sum(img1[row:row+3, col:col+3] * mask)
            if replace > T:
                filtered_img[row,col]=  255
                merged_img[row,col] = 255
            else:
                filtered_img[row,col] =  0
    output.append(filtered_img)

plt.figure(figsize=(10, 8))
imShow("Original Image",img, subplot=True, row=2,col=3, num=1)
imShow("Horizontal Detection Image",output[0],subplot=True, row=2, col=3, num=2)
imShow("Vertical Detection Image",output[1],subplot=True, row=2, col=3, num=3)
imShow("+45 degree Detection Image",output[2],subplot=True, row=2, col=3, num=4)
imShow("-45 degree Detection Image",output[3],subplot=True, row=2, col=3, num=5)
imShow("Mixed Detection Image",merged_img,subplot=True, row=2, col=3, num=6)
plt.show()

img = cv2.imread('/content/drive/MyDrive/dip_Images/Fig0354(a)(einstein_orig).tif',0)
imShow("Original Image", image=img, subplot=True, row=1, col=2, num=1)
delta = 3
Tnew = np.min(img)+1
while abs(T-Tnew) >= delta:
    T = Tnew
    rows, cols = img.shape
    totalCells = rows*cols

    G1 = []
    G2 = []
    for row in range(rows):
        for col in range(cols):
            if img[row][col] > T:
                G1.append(img[row][col])
            else:
                G2.append(img[row][col])
    m1 = np.mean(G1)
    m2 = np.mean(G2)

    Tnew = (m1+m2)/2
for row in range(rows):
    for col in range(cols):
        if img[row][col] > T:
            img[row][col] = 255
        else:
            img[row][col] = 0
imShow("Global Thresholding",image=img, subplot=True, row=1, col=2, num=2)

"""# **Exp 7**"""

img = cv2.imread("/content/cameraman.png",0)
rows, cols = img.shape
img1 = np.pad(img, pad_width=1, mode='constant', constant_values=0)

dGx = np.array([[ 1, 0],
                [ 0,-1]])
dGy = np.array([[ 0,-1],
                [ 1, 0]])

Gx = np.zeros_like(img)
Gy = np.zeros_like(img)
robertImg = np.zeros_like(img)

for row in range(rows):
    for col in range(cols):
        r1 = np.sum(img1[row:row+2, col:col+2] * dGx)
        r2 = np.sum(img1[row:row+2, col:col+2] * dGy)
        robertImg[row][col] = abs(r1) + abs(r2)
        Gx[row][col] = r1
        Gy[row][col] = r2

plt.figure(figsize=(10, 8))
imShow("Original Image",img, subplot=True, row=2,col=2, num=1)
imShow("Robert Operator (Gx)", robertImg, subplot=True, row=2, col=2, num=2)
imShow("Robert Operator (Gy)", robertImg, subplot=True, row=2, col=2, num=3)
imShow("Robert Operator (Gx+Gy)", robertImg, subplot=True, row=2, col=2, num=4)
plt.show()

rows, cols = img.shape
img1 = np.pad(img, pad_width=1, mode='constant', constant_values=0)

dGx = np.array([[-1,-1,-1],
                [ 0, 0, 0],
                [ 1, 1, 1]])
dGy = np.array([[-1, 0, 1],
                [-1, 0, 1],
                [-1, 0, 1]])

prewittImg = np.zeros_like(img)
Gx = np.zeros_like(img)
Gy = np.zeros_like(img)

for row in range(rows):
    for col in range(cols):
        r1 = np.sum(img1[row:row+3, col:col+3] * dGx)
        r2 = np.sum(img1[row:row+3, col:col+3] * dGy)
        prewittImg[row][col] = abs(r1) + abs(r2)
        Gx[row][col] = abs(r1)
        Gy[row][col] = abs(r2)

plt.figure(figsize=(10, 8))
imShow("Original Image",img, subplot=True, row=2,col=2, num=1)
imShow("Prewitt Operator (Gx)", Gx, subplot=True, row=2, col=2, num=2)
imShow("Prewitt Operator (Gy)", Gy, subplot=True, row=2, col=2, num=3)
imShow("Prewitt Operator (Gx+Gy)", prewittImg, subplot=True, row=2, col=2, num=4)
plt.show()

rows, cols = img.shape
img1 = np.pad(img, pad_width=1, mode='constant', constant_values=0)

dGx = np.array([[-1,-2,-1],
                [ 0, 0, 0],
                [ 1, 2, 1]])
dGy = np.array([[-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1]])
Gx = np.zeros_like(img)
Gy = np.zeros_like(img)
sobelImg = np.zeros_like(img)

for row in range(rows):
    for col in range(cols):
        r1 = np.sum(img1[row:row+3, col:col+3] * dGx)
        r2 = np.sum(img1[row:row+3, col:col+3] * dGy)
        sobelImg[row][col] = abs(r1) + abs(r2)
        Gx[row][col] = abs(r1)
        Gy[row][col] = abs(r2)

plt.figure(figsize=(10, 8))
imShow("Original Image",img, subplot=True, row=2,col=2, num=1)
imShow("Sobel Operator (Gx)", Gx, subplot=True, row=2, col=2, num=2)
imShow("Sobel Operator (Gy)", Gy, subplot=True, row=2, col=2, num=3)
imShow("Sobel Operator", sobelImg, subplot=True, row=2, col=2, num=4)
plt.show()

"""# **Exp 8**"""

img = cv2.imread("/content/cameraman.png",0)
height, width = img.shape
new_height = height - (height % 8)
new_width = width - (width % 8)
imShow(title=f"Original Image ({height} x {width})", image=img, subplot=True, row=1, col=2, num=1)
img = img[:new_height, :new_width]
imShow(title=f"New Image ({new_height} x {new_width})", image=img, subplot=True, row=1, col=2, num=2)

def dct2D(block, N = 8):
    DCT_matrix = np.zeros((N, N))
    for u in range(N):
        for v in range(N):
            au = (1/(N))**0.5 if u == 0 else (2/(N))**0.5
            av = (1/(N))**0.5 if v == 0 else (2/(N))**0.5
            dct_sum = 0
            for x in range(N):
                for y in range(N):
                    dct_sum += block[x, y] * np.cos(((2 * x + 1) * u * np.pi) / (2 * N)) * np.cos(((2 * y + 1) * v * np.pi) / (2 * N))
            DCT_matrix[u, v] = au * av * dct_sum
    return DCT_matrix


blocks = [img[i:i+8, j:j+8] for i in range(0, new_height, 8) for j in range(0, new_width, 8)]


dct_blocks = [dct2D(block) for block in blocks]

new_img = np.zeros((new_height, new_width))
idx = 0
for i in range(0, new_height, 8):
    for j in range(0, new_width, 8):
        new_img[i:i+8, j:j+8] = dct_blocks[idx]
        idx += 1


new_img = np.round(new_img)

imShow(image=new_img)

def idct2D(block, N = 8):
    IDCT_matrix = np.zeros((N, N))
    for u in range(N):
        for v in range(N):
            au = (1/(N))**0.5 if u == 0 else (2/(N))**0.5
            av = (1/(N))**0.5 if v == 0 else (2/(N))**0.5
            idct_sum = 0
            for x in range(N):
                for y in range(N):
                    idct_sum += block[x, y] * np.cos(((2 * x + 1) * u * np.pi) / (2 * N)) * np.cos(((2 * y + 1) * v * np.pi) / (2 * N))
            IDCT_matrix[u, v] = au * av * idct_sum
    return IDCT_matrix


blocks = [new_img[i:i+8, j:j+8] for i in range(0, new_height, 8) for j in range(0, new_width, 8)]

idct_blocks = [dct2D(block) for block in blocks]

og_img = np.zeros((new_height, new_width))
idx = 0
for i in range(0, new_height, 8):
    for j in range(0, new_width, 8):
        og_img[i:i+8, j:j+8] = idct_blocks[idx]
        idx += 1


og_img = np.round(og_img)

imShow(image=og_img)

thresh = 0.1
img_thresh = new_img * (np.absolute(new_img) > thresh*np.max(np.absolute(new_img)))
frac_nonzero = np.sum(img_thresh != 0.0)/img.size
print("Keeping %.2f%% of DCT coefficients"%(100*frac_nonzero))
print('Compression ratio: %.1f:1'%(1/frac_nonzero))

MSE = np.sum((img-og_img)**2)/img.size
PSNR = 10*np.log10(np.max(img)**2/MSE)
print(f'PSNR: {round(PSNR)} db')

"""# **Exp 9**"""

import math
x = ['A','B', 'C', 'D', 'E', 'F']
freq = [40,30,10,10,6,4]

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.nodes = []

freq_node = {}
for i in range(len(x)):
    n = Node()
    n.nodes.append(x[i])
    freq_node[n] = [freq[i],0]


def get_smallest():
    sorted_dict = sorted(freq_node.items(), key=lambda x: (x[1][0], -x[1][1]))

    return sorted_dict[:2]

while len(freq_node)!=1:
    ns1, ns2 = get_smallest()
    n1 = list(ns1)[0]
    n2 = list(ns2)[0]
    v1 = list(ns1)[1][0]
    v2 = list(ns2)[1][0]
    n = Node()
    n.left = n1
    n.right = n2
    n1.parent = n
    n2.parent = n
    n.nodes.extend(n1.nodes)
    n.nodes.extend(n2.nodes)
    del freq_node[n1]
    del freq_node[n2]
    freq_node[n] = [v1+v2, len(n.nodes)]
huffman_codes = {}
for char in x:
    code = ""
    temp = n
    while temp.left or temp.right:
        if char in temp.left.nodes:
            code += "1"

            temp = temp.left
        else:

            temp = temp.right
            code += "0"
    huffman_codes[char] = code
    print(char, "->", code)


def calculate_metrics(freq, huffman_codes):
    total = sum(freq)
    prob = [round(f/total,2) for f in freq]
    len_codes = [len(code) for code in huffman_codes.values()]
    Lavg = 0
    for i in range(len(prob)):
        Lavg += prob[i]*len_codes[i]
    print("--------------------")
    print("Average CodeWord Length: ", Lavg)

    entropy = 0
    for p in prob:
        entropy -= p*math.log2(p)
    print("Entropy: ", entropy)
    print("Efficiency: ", entropy*100/Lavg, "%")
    print("Redundancy:", 1-entropy/Lavg)

calculate_metrics(freq, huffman_codes)