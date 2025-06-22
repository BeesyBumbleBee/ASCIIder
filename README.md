# Simple python CLI image to ascii converter
This simple python program can be used to convert most commonly used image formats into an ascii art (grayscale and color). It comes with handy options, like defining your own charset, scaling down image or printing ascii art with ANSI escape codes for colorful display.

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

Then run following command to install dependacies
``` bash
pip install -r requirements.txt
```

Linux one-liner:
``` bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Windows one-liner:
``` bash
python -m venv .venv && .venv/Scripts/activate && pip install -r requirements.txt
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

## How to run
To run the program make sure you have required libraries and run following in the command line:
``` bash
python asciider.py <path_to_image>
```

Program can be run with diffrent flags all of which can be seen by typing:
``` bash
python asciider.py -h
```

Most used 
