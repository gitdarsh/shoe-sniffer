from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import requests
import io
import pandas as pd

# Read data from CSV file
df = pd.read_csv("sneaker_data.csv")

# Function to load and preprocess images using requests and PIL
def load_and_preprocess_image(image_url):
    try:
        # Skip images with specific parameters in the URL
        if "fit=fill" in image_url or "trim=color" in image_url:
            print(f"Skipping image with specific parameters - URL: {image_url}")
            return None

        response = requests.get(image_url)
        response.raise_for_status()  # Check for HTTP errors
        img = Image.open(io.BytesIO(response.content))

        # Check if the image is readable
        img.verify()

        img = img.convert("RGB")  # Convert to RGB mode
        img = img.resize((224, 224))
        img_array = np.array(img)
        img_array = img_array / 255.0
        return img_array
    except Exception as e:
        print(f"Error processing image: {str(e)} - URL: {image_url}")
        return None

# Load images and use 'name' column as labels
X = []
y = []

for index, row in df.iterrows():
    image_url = row['image_url']
    label = row['name']  # Use 'name' column as labels
    img_array = load_and_preprocess_image(image_url)
    if img_array is not None:
        X.append(img_array)
        y.append(label)

# Convert lists to numpy arrays
X = np.array(X)
y = np.array(y)

# Rest of your code (e.g., data augmentation, training the model) goes here

# Create an ImageDataGenerator for data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Visualize a few augmented images
fig, ax = plt.subplots(2, 5, figsize=(12, 6))
ax = ax.flatten()

for batch in datagen.flow(X, batch_size=1, shuffle=False):
    ax[0].imshow(X[0])
    ax[0].set_title('Original')
    ax[0].axis('off')

    ax[1].imshow(batch[0])
    ax[1].set_title('Augmented')
    ax[1].axis('off')

    break  # Stop the loop after one batch to avoid an infinite loop

plt.tight_layout()
plt.show()
