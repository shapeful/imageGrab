import os
import cv2

# Directory containing the images
image_dir = "downloaded_imagesB"
output_video = "stitched_videoB.mp4"

# Set the desired frames per second (fps) for the video
fps = 24  # You can adjust this based on the desired speed of the video

def get_image_files(image_dir):
    """Get a sorted list of image file paths from the directory."""
    files = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]
    files.sort()  # Sorting by image number (assuming filenames are sequential)
    return [os.path.join(image_dir, f) for f in files]

def stitch_images_to_video(image_dir, output_video, fps):
    image_files = get_image_files(image_dir)

    if not image_files:
        print("No images found in the directory.")
        return

    # Read the first image to get video dimensions
    first_image = cv2.imread(image_files[0])
    height, width, _ = first_image.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 video
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # Iterate through all the image files and write them to the video
    for image_file in image_files:
        img = cv2.imread(image_file)
        video_writer.write(img)

    # Release the VideoWriter
    video_writer.release()
    print(f"Video saved as {output_video}")

if __name__ == "__main__":
    stitch_images_to_video(image_dir, output_video, fps)