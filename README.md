# Center of Mouse 🐭 - The home for all your mouse tracking needs 🐁
## Installation

### 1. Download Code:
Download code from github. Click the green code button in the upper right. For easiest results, select `Download ZIP`. Unzip the folder (doubleclick) and place it somewhere accessible.

### 2. Install Homebrew
Copy and paste `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` into your terminal and press enter. It may take a little time to install.

Once you see that Homebrew has been installed you will see a message that says next steps. 
Once you see this message copy and past this command into terminal `(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)" ') >> /Users/w. zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"`

After this has been installed type `brew help` and click enter. This ensures that the homebrew is accurately installed

### 3. Install ffmpeg
Enter `brew install ffmpeg` and press enter.

### 4. Install Python 🐍
Enter `brew install python@3.9`

### 5. Install required packages
1. Navigate to the mouse tracking folder in terminal by using the command
`cd ` and drag and drop the folder into the terminal window. Alternatively, because you know where the folder is, you can type this into terminal and press enter
2. Once you are in your directory, enter `pip3 install -r requirements.txt` and press return. You should see a flurry of activity before the action completes.

## How to run `center_of_mouse.py`

1. The program name is `center_of_mouse.py`. You want to run this program with `python3`, so you'll type `python3 center_of_mouse.py` into the terminal.

2. Next, you need to provide the program with arguments to run it on your specific video. The available arguments are:
  `-h`, `--help`            show this help message and exit
  `--video` VIDEO         input video for tracking
  `--image_path` IMAGE_PATH
                        directory for image export
  `--output` OUTPUT       directory for tracked frame export
  `--fps` FPS             frame rate for image extraction

`--video` is the only required argument. However, I'd recommend setting the fps   to small value as tracking a mouse at the video frame rate (probably 30 frames per second) is excessive.

In this case, you'll add the video and fps arguments like this:
`python3 center_of_mouse.py --video {drag and drop your video file into terminal} --fps 1`

3. Your final command should look like this:
`python3 center_of_mouse.py --video example_video/ee_5_short.mp4 --fps 1`

4. The output file should be stored in the output directory. There are three outputs. One is a csv file with the tracked mouse position and quadrant at each tracked frame. Another is a summary of statistics including total distance. And lastly, it will output a video of the tracked mouse.

Note!!! In order to properly calculate distance, make sure to set the appropriate dimensions in cage_length variable on line 211 in the `center_of_mouse.py` file. If it would be helpful, we can also make this an argument that you pass to the program (e.g. `python3 center_of_mouse.py --video mouse.mp4 --fps 1 --cage_length 36`

## If you exit out of terminal and want to run the program again`
Navigate to the mouse tracking folder in terminal by using the command
`cd ` and drag and drop the folder into the terminal window. 
Then repeat the steps found in the How to run center_of_mouse.py section
