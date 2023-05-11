# Import the required functions
from sobel import sobel_filter

import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------------
# SELECT INPUT VIDEO

path = 'D:/FAU/Studies/Research Project/Video Sequences/Input - Original/'          #Set path to the video sequences

# Take input from user
print('Please select a video sequence and press Enter:\n')
print('1 = Campfire Party')
print('2 = Fountains')
print('3 = Marathon')
print('4 = Runners')
print('5 = Rush Hour')
print('6 = Tall Buildings')
print('7 = Traffic Flow')
print('8 = Wood\n')
user_input = input()

while True:
    if (user_input == '1'):
        video = 'Campfire Party.yuv'
        break
    elif (user_input == '2'):
        video = 'Fountains.yuv'
        break
    elif (user_input == '3'):
        video = 'Marathon.yuv'
        break
    elif (user_input == '4'):
        video = 'Runners.yuv'
        break
    elif (user_input == '5'):
        video = 'Rush Hour.yuv'
        break
    elif (user_input == '6'):
        video = 'Tall Buildings.yuv'
        break
    elif (user_input == '7'):
        video = 'Traffic Flow.yuv'
        break
    elif (user_input == '8'):
        video = 'Wood.yuv'
        break
    else:
        print('\nError: Wrong number pressed. Please try again.')
        user_input = input()

# Get path to the video sequence
vid_path = path  + video
print('\nSelected video sequence:', video)

# Video sequence details
height = 2160
width = 3840
frames = 130          # Number of frames to be encoded
fps = 30
fr_size = int(width * height * 1.5)          # Size of each frame in bytes

# Print video details
print('\nVideo sequence details:\n')
print('Color format: YUV')
print('Resolution:', width, 'x', height)
print('Subsampling method: (4:2:0)')
print('Number of frames:', frames)
print('FPS:', fps)

# -----------------------------------------------------------------------------------
# YUV VIDEO SEQUENCE (READ & STORE)

with open(vid_path, 'rb') as file:
    # Create an empty numpy array to store video frames
    vid_arr = np.empty((frames, height, width), dtype=np.uint8)

    # Loop over the frames in the video and read them one by one
    for i in range(frames):
        # Read the YUV data for the current frame
        yuv_data = file.read(fr_size)

        # Convert YUV data to a numpy array
        yuv_arr = np.frombuffer(yuv_data, dtype=np.uint8)

        # Reshape the array to YUV frame shape
        yuv_fr = yuv_arr.reshape((int(height * 1.5), width))

        # Extract Y component from the YUV frame
        y_fr = yuv_fr[:height, :]

        # Store Y component in the video array
        vid_arr[i, :, :] = y_fr

# -----------------------------------------------------------------------------------
# SPATIAL INFORMATION

# Wait for key press
input("\nPress Enter to continue and start calculating Spatial Information ...\n")

# Create empty arrays
sobel_arr = np.empty((frames, height, width), dtype=np.uint8)
std_si_arr = np.empty(frames)
img_sobel = np.empty((height, width), dtype=np.uint8)

# Apply Sobel filter and calculate standard deviation
for i in range(frames):
    sobel_arr[i, :, :] = sobel_filter(vid_arr[i, :, :])
    std_si_arr[i] = np.std(sobel_arr[i, :, :])
    print('Standard Deviation of Sobel-filtered frame', (i + 1), ': ', std_si_arr[i])

    # Remove these comments to display Sobel-filtered images one by one
    #img_sobel = sobel_arr[i, :, :]
    #plt.imshow(img_sobel, cmap = 'gray')
    #plt.show()

# Plot SD over all frames
plt.plot(std_si_arr, color ='red')
plt.title('Spatial Information', fontweight = 'bold')
plt.xlabel('Frame #', color = 'green', fontstyle = 'italic')
plt.ylabel('Standard Deviation', color = 'green', fontstyle = 'italic')
plt.show()

# Calculate SI by averaging the SD of all frames
si = np.mean(std_si_arr)
print('\nSI of the video sequence: ', si, '\n')

# -----------------------------------------------------------------------------------
# TEMPORAL INFORMATION

# Wait for key press
input('Press Enter to continue and start calculating Temporal Information ...\n')

# Create empty arrays
diff_arr = np.empty((frames - 1, height, width), dtype=np.uint8)
std_ti_arr = np.empty(frames - 1)
img_diff = np.empty((frames, width), dtype=np.uint8)

# Find the difference between two consecutive frames and calculate standard deviation
for i in range(frames - 1):
    diff_arr[i, :, :] = vid_arr[i + 1, :, :] - vid_arr[i, :, :]
    std_ti_arr[i] = np.std(diff_arr[i, :, :])
    print('Standard Deviation of difference frame', (i + 1), ': ', std_ti_arr[i])

    # Remove these comments to display difference images one by one
    #img_diff = diff_arr[i, :, :]
    #plt.imshow(img_diff, cmap = 'gray')
    #plt.show()

# Plot TI over all frames
plt.plot(std_ti_arr, color = 'red')
plt.title('Temporal Information', fontweight = 'bold')
plt.xlabel('Frame #', color = 'green', fontstyle = 'italic')
plt.ylabel('Standard Deviation', color = 'green', fontstyle = 'italic')
plt.show()

# Calculate TI by averaging the SD of all difference frames
ti = np.mean(std_ti_arr)
print('\nTI of the video sequence: ', ti, '\n')

# -----------------------------------------------------------------------------------
#THE END