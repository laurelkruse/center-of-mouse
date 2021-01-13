How to run center_of_mouse.py

1. Navigate to the mouse tracking folder in terminal by using the command
`cd ` and drag and drop the folder into the terminal window. 
Alternatively, because you know where the folder is, you can type this into terminal and press enter:
`cd /Users/laurelkruse/Documents/mouse_tracking`

2. Run the program. The program name is `center_of_mouse.py`. You want to run this program with `python3`
So, type `python3 center_of_mouse.py` into the terminal

3. Next, you need to provide the program with arguments to run it on your specific video. The available arguments are:
  -h, --help            show this help message and exit
  --video VIDEO         input video for tracking
  --image_path IMAGE_PATH
                        directory for image export
  --output OUTPUT       directory for tracked frame export
  --fps FPS             frame rate for image extraction

--video is the only required argument. However, I'd recommend setting the fps   to small value as tracking a mouse at the video frame rate (probably 30 frames per second) is excessive.

In this case, you'll add the video and fps arguments like this:
`python3 center_of_mouse.py --video {drag and drop your video file into terminal} --fps 1`

4. Your final command should look like this:
`python3 center_of_mouse.py --video untracked_videos/NEUR\ 369\ F19\ 60\ OF\ 2019-12-06\ 10-17-22\ \(1\).avi --fps 1`

5. The output file should be stored in the directory with the original video. There are two outputs, one is a csv file with the tracked mouse position and quadrant at each tracked frame. The other is a summary of statistics including total distance.

Note!!! In order to properly calculate distance, make sure to set the appropriate dimensions in cage_length variable on line 211 in the `center_of_mouse.py` file. If it would be helpful, we can also make this an argument that you pass to the program (e.g. `python3 center_of_mouse.py --video mouse.mp4 --fps 1 --cage_length 36`