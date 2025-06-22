from matplotlib.image import imread
from math import ceil
import numpy as np
import argparse
import sys
import cv2 as cv
from time import sleep

import os
if os.name == 'nt': # Only if we are running on Windows
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)

class AsciiConverter:
    args = {
    "no_scale": False,
    "scale": None,
    "color": False,
    "debug": False,
    "channels_order": "rbg",
    "invert": False,
    "invert_brightness": False,
    "out": None,
    "charset": " `. - ':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@",
    "video": False,
    "fps": 30
    }
    image = np.array([])

    def __init__(self, args=None):
        if args is not None:
            self.args = vars(args)

    def rgb_to_ascii_grayscale(self, x):
        return self.args["charset"][(-1 if self.args["invert_brightness"] else 1) * int(np.interp(((x[0]/3) + (x[1]/3) + (x[2]/3)), [0, 1 if x[0].dtype == np.float32 else 255], [0, len(self.args["charset"])-1]))]

    def rgb_to_ascii(self, x):
        chan1 = int(x[0] * (255 if x[0].dtype == np.float32 else 1))
        chan2 = int(x[1] * (255 if x[0].dtype == np.float32 else 1))
        chan3 = int(x[2] * (255 if x[0].dtype == np.float32 else 1))
        channels = {
            self.args["channels_order"][0]: chan1,
            self.args["channels_order"][1]: chan2,
            self.args["channels_order"][2]: chan3,
        }
        if self.args["invert"]:
            color_code = f"\x1b[38;2;{255-channels['r']};{255-channels['g']};{255-channels['b']}m"
        else:
            color_code = f"\x1b[38;2;{channels['r']};{channels['g']};{channels['b']}m"
        return (color_code +
                self.args["charset"][(-1 if self.args["invert_brightness"] else 1) * int(np.interp(((x[0]/3) + (x[1]/3) + (x[2]/3)), [0, 1 if x[0].dtype == np.float32 else 255], [0, len(self.args["charset"])-1]))] +
                "\x1b[0m")

    def image_to_ascii(self, image=None):
        if image is not None:
            self.image = image

        if self.args["debug"]:
            print(f"Image shape: {self.image.shape}")
            print(self.image)

        if not self.args["no_scale"] and self.args["scale"] is None:
            self.scale_image()
        elif self.args["scale"] is not None:
            self.scale_image_to()

        if self.args["color"]:
            self.image = np.apply_along_axis(self.rgb_to_ascii, -1, self.image)
        else:
            self.image = np.apply_along_axis(self.rgb_to_ascii_grayscale, -1, self.image)

        text = ""
        for row in self.image:
            out = "".join(row[i] for i in range(len(row)))
            text += out + "\n"
        return text


    def scale_image_to(self):
        x_scale = (self.image.shape[1] // self.args["scale"][0]) + 1
        y_scale = (self.image.shape[0] // self.args["scale"][1]) + 1
        self.image = self.image[::y_scale, ::x_scale]

    def scale_image(self):
        try:
            terminal_size = os.get_terminal_size()
            x_scale = ceil(self.image.shape[1] / terminal_size[0])
            y_scale = ceil(self.image.shape[0] / terminal_size[1])

            self.image = self.image[::y_scale, ::x_scale]
        except OSError:
             return

    def load_image(self, filepath):
        try:
            self.image = imread(filepath)
        except FileNotFoundError:
            print(f"File {self.args["filepath"]} not found.")
            exit(1)

    def render_video(self, filepath):
        sys.stdout.write("\033[2J")
        sys.stdout.write("\033[?25l")
        cap = cv.VideoCapture(filepath)
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                ascii_frame = self.image_to_ascii(frame)
                render_frame(ascii_frame)
                sleep(1/self.args["fps"])
        except KeyboardInterrupt:
            pass
        finally:
            cap.release()
            sys.stdout.write("\033[?25h")


def render_frame(frame):
    sys.stdout.write('\033[H')
    sys.stdout.write(frame)
    sys.stdout.flush()

def print_image(text):
    sys.stdout.write("\033[2J")
    sys.stdout.write('\033[H')
    sys.stdout.write(text)
    sys.stdout.flush()
    return text


if __name__ == "__main__":
    charset = " `. - ':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"


    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--no-scale", action="store_true", help="Do not scale image. By default image is scaled to terminal window.")
    arg_parser.add_argument("--scale", type=int, nargs=2, default=None, help="Scale image to given width and height. Must provide 2 integers seperated by space (Note: will only downscale imgae not upscale)")
    arg_parser.add_argument("--color", action="store_true", help="Whether or not to color image. By default image is in grayscale.")
    arg_parser.add_argument("--debug", action="store_true", help="Debug mode.")
    arg_parser.add_argument("--channels-order", default="rgb", help="Change order of color channels. Must be a transformation of 'rgb' string, e.q. 'bgr'")
    arg_parser.add_argument("--invert", action="store_true", help="Invert image colors. Doesn't affect grayscale images.")
    arg_parser.add_argument("--invert-brightness", action="store_true", help="Invert image brightness.")
    arg_parser.add_argument("--out", default=None, help="Specify output file. By default, image is only written to stdout.")
    arg_parser.add_argument("--charset", default=charset, help="Provide charset for image. Leftmost characters are used as 'dark pixels' and righmost as 'white pixels'. By default, program uses charset is ASCII characters sorted by their brightness.")
    arg_parser.add_argument("--video", action="store_true", help="Treat input file as video file, rendering its contents in ASCII art (experimental)")
    arg_parser.add_argument("--fps", type=int, default=30, help="Set FPS of video rendering. Default: 30")
    arg_parser.add_argument("filepath", help="Path to image.")

    args = arg_parser.parse_args()

    converter = AsciiConverter(args)
    if args.video:
        converter.render_video(args.filepath)
    else:
        converter.load_image(args.filepath)
        ascii_image = converter.image_to_ascii()
        print_image(ascii_image)
        if args.out is not None:
            with open(args.out, "wb") as f:
                f.write(ascii_image.encode("utf-8"))

