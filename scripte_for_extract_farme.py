import cv2
import os

# Specify the path to your video file
video_path = r'C:\Users\ARABI\Desktop\mobile net v2\WIN_20240914_09_58_16_Pro.mp4'

# Create a folder to save the extracted frames
output_folder = 'empty'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Open the video file
video = cv2.VideoCapture(video_path)

# Get the frames per second (FPS) of the video
fps = video.get(cv2.CAP_PROP_FPS)

# Initialize frame count
frame_count = 0

# Loop through the video frames
while True:
    success, frame = video.read()
    
    if not success:
        break  # Exit if the video is finished

    # Calculate the current second in the video
    current_second = int(frame_count / fps)
    
    # Save one frame per second
    if frame_count % int(fps) == 0:
        frame_filename = os.path.join(output_folder, f"frame_{current_second}.jpg")
        cv2.imwrite(frame_filename, frame)
        print(f"Saved {frame_filename}")

    # Increment the frame count
    frame_count += 1

# Release the video capture object
video.release()

print("Frame extraction completed.")
