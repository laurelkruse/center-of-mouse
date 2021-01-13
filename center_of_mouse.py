# Import modules
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from tqdm import tqdm
from scipy import ndimage
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--video',
                    help="input video for tracking")
parser.add_argument('--image_path', default='frames',
                    help="directory for image export")
parser.add_argument('--output', default='output',
                    help="directory for tracked frame export")
parser.add_argument('--fps', default=1, type=float,
                    help="frame rate for image extraction")

args = parser.parse_args()

# Load video and convert it to a series of images
def video_to_images(video_path, image_path, fps):
    # Define the relative path to the video, and the relative path where the frames should be stored

    # Check if the output directory exists.
    # If it exists already, delete the directory to remove old frames

    if os.path.exists(image_path):
        shutil.rmtree(image_path)

    os.mkdir(image_path)

    # Run the command for ffmpeg to convert the video
    os.system("ffmpeg -i \"{0}\" -vf fps={1} -f image2 {2}/frame%05d.png".format(video_path, fps, image_path))

def get_bounding_box(img):
    plt.figure(figsize=(12,8))
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.tight_layout()
    #plt.axis('off', bbox_inches='tight')
    plt.title("Please select the four corners of the floor of the enclosure\n Start from the top right and move clockwise")
    corners = np.array(plt.ginput(4), dtype=int)
    plt.close()
    return(corners)


def extract_rect(img, corners):
    rect = cv2.minAreaRect(corners)
    # the order of the box points: bottom left, top left, top right, bottom right
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # get width and height of the detected rectangle
    width = int(rect[1][0])
    height = int(rect[1][1])

    src_pts = box.astype("float32")
    # corrdinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    warped = np.rot90(cv2.warpPerspective(img, M, (width, height)))
    warped_norm = np.zeros(np.shape(warped))

    warped_norm =  cv2.normalize(warped, warped_norm, 1, 0, cv2.NORM_MINMAX)

    return(warped)

def get_mouse_color(patch):
    # Get mouse color to extract threshold
    plt.figure(figsize=(12,8))
    plt.imshow(patch, cmap='gray')
    plt.colorbar()
    plt.title("Place 3 points on the subject to be tracked")
    mouse_coord = np.array(plt.ginput(3), dtype=int)
    mouse_color = np.mean([patch[position[1], position[0]] for position in mouse_coord])
    plt.close()
    return(mouse_color)

def get_zone(x_val, y_val):
    """
    This function converts a normalized x, y coordinate pair into the appropriate zone in a 3x3 grid.
    1 starts in the bottom left corner, followed by 9 in the top right
    """
    if x_val <= 1/3:
        if y_val >= 2/3:
            zone = 1
        if y_val > 1/3 and y_val < 2/3:
            zone = 4
        if y_val <= 1/3:
            zone = 7
    elif x_val < 2/3 and x_val > 1/3:
        if y_val >= 2/3:
            zone = 2
        if y_val > 1/3 and y_val < 2/3:
            zone = 5
        if y_val <= 1/3:
            zone = 8
    elif x_val >= 2/3:
        if y_val >= 2/3:
            zone = 3
        if y_val > 1/3 and y_val < 2/3:
            zone = 6
        if y_val <= 1/3:
            zone = 9
    else:
        zone = 0
    return(int(zone))

def find_mouse(patch, color):
    binary = patch > mouse_color - 15
    x = ndimage.measurements.center_of_mass(binary)[1]
    y = ndimage.measurements.center_of_mass(binary)[0]

    # normalize the pixel coordinates betwee 0 and 1
    im_height, im_width = np.shape(binary)

    x_val = x/im_width
    y_val = y/im_height

    return(x_val, y_val, binary)

video_to_images(args.video, args.image_path, args.fps)

# Read in first image to extract bounding box
img = cv2.imread(args.image_path + '/' + sorted(os.listdir(args.image_path))[1])
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

corners = get_bounding_box(img)
patch = extract_rect(img, corners)
rand_value = np.random.randint(len(os.listdir(args.image_path)))
rand_img = cv2.imread(args.image_path + '/' + sorted(os.listdir(args.image_path))[rand_value])

rand_img = cv2.cvtColor(rand_img, cv2.COLOR_BGR2GRAY)
rand_patch = extract_rect(rand_img, corners)
mouse_color = get_mouse_color(rand_patch)
rand_x, rand_y, rand_binary = find_mouse(rand_patch, mouse_color)
plt.imshow(rand_binary)
plt.title("Evaluate whether the mouse and bounding box look appropriate\nIf yellow zones exist outside the mouse, tracking may degrade")
plt.show()

# Initialize tracking arrays
x, y, binary = find_mouse(patch, mouse_color)
x = [x]
y = [y]
zone = [get_zone(x[-1], y[-1])]
zone_entries = np.zeros(9)


if os.path.exists(args.output):
    shutil.rmtree(args.output)
os.mkdir(args.output)


for file in tqdm(sorted(os.listdir(args.image_path))[2:]):
    if file != '.DS_Store':
        # Read in the image
        img = cv2.imread(args.image_path + '/' + file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Crop the background from the images. Tight crop is necessary
        patch = extract_rect(img, corners)

        x_pos, y_pos, binary = find_mouse(patch, mouse_color)
        x.append(x_pos), y.append(y_pos)

        zone.append(get_zone(x[-1], y[-1]))

        if zone[-1] != zone[-2] and zone[-1] != 0 and zone[-2] != 0:
            zone_entries[zone[-1] - 1] += 1

        im_height, im_width = np.shape(binary)
        plt.figure(figsize=(4,4), dpi=100)
        if zone[-1] != zone[-2] and zone[-1] != 0:
            plt.imshow(patch + binary, cmap='gray')
            plt.title("🐭 TRANSITION!!!" + str(zone[-1]))
        elif zone[-1] == 0:
            plt.imshow(patch + binary, cmap='spring')
            plt.title("🐭 I can't find a mouse 😢")
        else:
            plt.imshow(patch + binary, cmap='gray')
            plt.title("🐭 is in zone " + str(zone[-1]))
        plt.scatter(x[-1] * im_width, y[-1] * im_height, c='r')
        plt.axis('off')
        plt.savefig(args.output + '/' + file)
        plt.close()

input_video_name = args.video.split('/')[-1][:-4] + '.mp4'
np.savetxt(os.path.join(args.output, input_video_name[:-4] + "_positions.csv"), np.array([x,y,[int(val) for val in zone]]).T, delimiter=",", fmt='%.2f', header="x position, y position, zone")

dist = 0
for x_val, y_val in zip(x, y):
    if x_val == x_val:
        dist += np.sqrt(x_val ** 2 + y_val ** 2)

summary = open(os.path.join(args.output, "{0}.txt".format(input_video_name[:-4])),"w")
summary.write("Test {0}\n".format(args.video[:-4]))

## NOTE!! To change the scale of the enclosure, modify the value below with the
## length of the cage!!
cage_length = 36
summary.write("\nDistance traveled measured in inches: {0:.0f}\n".format(dist * cage_length))

summary.write("\nNumber of seconds in:\n")
for i in range(1,10):
    summary.write("Zone {0}: {1}\n".format(i, sum(np.array(zone) == i)))

summary.write("\nNumber of transitions into:\n")
for i in range(9):
    summary.write("Zone {0}: {1}\n".format(i+1, int(zone_entries[i])))
summary.close()



video_name = os.path.join(args.output, 'tracked_' + args.video.split('/')[-2] + '_' + args.video.split('/')[-1])

if os.path.exists(video_name):
    os.remove(video_name)

print(args.output)
for file in tqdm(sorted(os.listdir(args.output))):
    print(file)
    if '.png' in file:
        img = cv2.imread(args.output + '/' + file)
        im_width, im_height, im_channels = np.shape(img)
        img = cv2.resize(img, (int( 2 * round( im_width / 2. )), int( 2 * round( im_height / 2. ))))
        cv2.imwrite(args.output + '/' + file, img)
os.system(f"cat {args.output}/*.png | ffmpeg -f image2pipe -framerate 30 -i - -c:v libx264 -vf format=yuv420p -r 30 {video_name}")
