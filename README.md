# Simple python CLI image to ascii converter
This simple python program can be used to convert most commonly used image formats into an ascii art (grayscale and color). It comes with handy options, like defining your own charset, scaling down image, inverting colors and brighntess or printing ascii art with ANSI escape codes for colorful display.

## Example usage
Example usage on following image of an apple (`apple.webp`):  
![image](https://github.com/user-attachments/assets/3c7cb0f6-1aee-43ce-a843-97c5eb96c4ba)  
  
Result of running `python asciider.py apple.webp --scale 64 32`  
![image](https://github.com/user-attachments/assets/c303d309-aa35-4663-9cca-a4837f42a29a)  
  
Result of running `python asciider.py apple.webp --scale 64 32 --color`  You have unread notifications
![image](https://github.com/user-attachments/assets/88d56c08-9bb7-4dbc-9e07-9e0cb5116a82)  
  
Result of running `python asciider.py apple.webp --scale 64 32 --invert-brightness`  
![image](https://github.com/user-attachments/assets/c2a60a5b-df57-4193-9992-83d2af00571f)  
  
Result of running `python asciider.py apple.webp --scale 64 32 --color --channels-order bgr` (changing order in which color channels are interpreted)  
![image](https://github.com/user-attachments/assets/3199a133-792f-482b-86a0-7c6b18894f8d)

### Video rendering
Using `--video` program will treat file as a video file and will render its contents in ASCII art form to the terminal. Frame rate of the rendering can be configured using `--fps` flag followed by an integer.  
Below is result of running `python asciider.py rickroll-roll.gif --color --video --channels-order bgr --scale 64 32 --fps 20`  
![out](https://github.com/user-attachments/assets/86cc23ea-a09f-4133-9dae-fd0419f51fa6)  
  

## How to install
To run this program you will need a python enviroment with matplotlib and numpy, to create a virtual enviroment simply run following command:
``` bash
python -m venv .venv
```
Then to enter the venv type:  
(on Linux):
``` bash
source .venv/bin/activate
```
(on Windows):
``` bash
.venv/Scripts/activate
```

Then run following command to install dependencies
``` bash
pip install -r requirements.txt
```

That's it. After pip finishes downloading libraries you can run the program from command line.  
    
If you have already setup a venv before, you can activate it by running:  
(on Linux):
``` bash
source .venv/bin/activate
```
  
(on Windows):
``` bash
.venv/Scripts/activate
```
  
### One-liners
Linux one-liner:
``` bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```
Windows one-liner:
``` bash
python -m venv .venv && .venv/Scripts/activate && pip install -r requirements.txt
```
  
## How to run
To run the program make sure you have required libraries and run following in the command line:
``` bash
python asciider.py <path_to_image>
```
  
Program can be run with diffrent flags all of which can be seen by typing:
``` bash
python asciider.py -h
```
