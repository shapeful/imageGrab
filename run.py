import os
import requests
from PIL import Image
from PIL.ExifTags import TAGS
import json
import re

# Directories to save images and JSON files
save_dir = "downloaded_images"
json_dir = "exif_data"
os.makedirs(save_dir, exist_ok=True)
os.makedirs(json_dir, exist_ok=True)

# Base URL for images
base_url = "https://projectskydrop.com/cameras/archiveA/"

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {image_url} to {save_path}")
        return True
    elif response.status_code == 404:
        print(f"Image not found: {image_url} (404 error)")
        return False
    else:
        print(f"Failed to download {image_url} with status code {response.status_code}")
        return False

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif() or {}
        exif = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif[tag_name] = convert_to_serializable(value)
        return exif
    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
        return {}

def convert_to_serializable(value):
    """Convert EXIF data into JSON-serializable format."""
    if isinstance(value, bytes):
        return value.decode(errors='ignore')  # Convert bytes to string
    elif isinstance(value, tuple):
        return tuple(convert_to_serializable(v) for v in value)  # Recursively handle tuples
    elif isinstance(value, (int, float, str)):
        return value  # Return JSON-serializable basic types
    elif isinstance(value, list):
        return [convert_to_serializable(v) for v in value]  # Recursively handle lists
    else:
        # Convert non-serializable objects like IFDRational to string
        return str(value)

def save_exif_to_json(exif_data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(exif_data, json_file, indent=4)
    print(f"Saved EXIF data to {json_path}")

def find_last_downloaded_image():
    """Find the last downloaded image in the directory."""
    files = [f for f in os.listdir(save_dir) if re.match(r'\d{6}\.jpg', f)]
    if files:
        numbers = [int(re.findall(r'(\d{6})\.jpg', f)[0]) for f in files]
        return max(numbers)
    return 0

def main():
    # Find the last downloaded image
    last_downloaded = find_last_downloaded_image()
    start_image = last_downloaded + 1

    image_num = start_image
    while True:
        image_id = f"{image_num:06}.jpg"  # Format the number as a 6-digit string
        image_url = base_url + image_id
        image_path = os.path.join(save_dir, image_id)

        # Download image
        if not download_image(image_url, image_path):
            break  # Stop when a 404 error occurs

        # Extract EXIF data
        exif_data = get_exif_data(image_path)

        # Save EXIF data as JSON in the json_dir
        json_path = os.path.join(json_dir, f"{os.path.splitext(image_id)[0]}.json")
        save_exif_to_json(exif_data, json_path)

        image_num += 1

if __name__ == "__main__":
    main()