# Image Downloader and Video Stitcher

This project downloads sequential images from a specified URL, extracts EXIF data from the images, and stitches them together into a video file.

## Features
1. **Download Images**: Automatically download a sequence of images until a 404 error is encountered.
2. **EXIF Data Extraction**: Extract EXIF metadata from each image and store it in JSON format.
3. **Create a Video**: Stitch the downloaded images together into a video file.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>

   
2. install deps:
   ```bash
   pip install -r requirements.txt
   ```

Usage
Step 1: Download Images and Extract EXIF Data
Use the download_images.py script to download images and extract EXIF data.

```bash
python download_images.py
```
The images will be saved in the downloaded_images directory.
The EXIF data for each image will be saved in the exif_data directory as JSON files.
Step 2: Stitch Images into a Video
Once the images have been downloaded, use the stitch_images_to_video.py script to stitch them into a video file.

```bash

python stitch_images_to_video.py
```
The video will be saved as stitched_video.mp4.