import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import matplotlib.pyplot as plt
import os
import time

# Ensure the image path is correct relative to the working directory
image_path = 'sample_file.png'

# Check if image file exists
if not os.path.exists(image_path):
    print(f"Error: Image file '{image_path}' not found.")
else:
    # Loading and preparation
    image = Image.open(image_path)

    start_time = time.time()

    # Compression begins
    image = image.convert("RGB")
    image_np = np.array(image)

    # Reshaping the image to a list of RGB pixels
    pixels = image_np.reshape(-1, 3)

    # Defining the number of colors to use in compression
    num_colors = 10

    # KMeans clustering to reduce colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Assigning the nearest cluster center to each pixel
    compressed_pixels = kmeans.cluster_centers_[kmeans.labels_]
    compressed_pixels = np.clip(compressed_pixels.astype('uint8'), 0, 255)

    # Reshape the compressed pixels back to the original image shape
    compressed_image_np = compressed_pixels.reshape(image_np.shape)

    compressed_image = Image.fromarray(compressed_image_np)
    end_time = time.time()
    execution_time = end_time - start_time
    # Compression ends

    # Saving original and compressed images
    original_image_path = 'original_image.jpg'
    compressed_image_path = 'compressed_image.jpg'

    # Saving the images
    image.save(original_image_path)
    compressed_image.save(compressed_image_path)

    # Calculating the compression statistics
    original_size = os.path.getsize(image_path)
    compressed_size = os.path.getsize(compressed_image_path)

    compression_ratio = original_size / compressed_size
    compression_percentage = 100 * (1 - (compressed_size / original_size))

    # Displaying the images and statistics
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.title(f"Original Image\nSize: {original_size / 1024:.2f} KB")
    plt.imshow(image)

    plt.subplot(1, 2, 2)
    plt.title(f"Compressed Image with {num_colors} colors\nSize: {compressed_size / 1024:.2f} KB")
    plt.imshow(compressed_image)

    plt.show()

    # Printing the compression results and execution time
    print(f"Original Image Size: {original_size / 1024:.2f} KB")
    print(f"Compressed Image Size: {compressed_size / 1024:.2f} KB")
    print(f"Compression Ratio: {compression_ratio:.2f}")
    print(f"Compression Percentage: {compression_percentage:.2f}%")
    print(f"Execution Time: {execution_time:.2f} seconds")
