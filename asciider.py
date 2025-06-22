from matplotlib.image import imread
from math import ceil
import numpy as np
import argparse

import os
if os.name == 'nt': # Only if we are running on Windows
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)


args = None

def rgb_to_ascii_grayscale(x):
    return args.charset[(-1 if args.invert_brightness else 1) * int(np.interp(((x[0]/3) + (x[1]/3) + (x[2]/3)), [0, 1 if x[0].dtype == np.float32 else 255], [0, len(args.charset)-1]))]

def rgb_to_ascii(x):
    chan1 = int(x[0] * (255 if x[0].dtype == np.float32 else 1))
    chan2 = int(x[1] * (255 if x[0].dtype == np.float32 else 1))
    chan3 = int(x[2] * (255 if x[0].dtype == np.float32 else 1))
    channels = {
        args.channels_order[0]: chan1,
        args.channels_order[1]: chan2,
        args.channels_order[2]: chan3,
    }
    if args.invert:
        color_code = f"\x1b[38;2;{255-channels['r']};{255-channels['g']};{255-channels['b']}m"
    else:
        color_code = f"\x1b[38;2;{channels['r']};{channels['g']};{channels['b']}m"
    return (color_code +
            args.charset[(-1 if args.invert_brightness else 1) * int(np.interp(((x[0]/3) + (x[1]/3) + (x[2]/3)), [0, 1 if x[0].dtype == np.float32 else 255], [0, len(args.charset)-1]))] +
            "\x1b[0m")

def image_to_ascii(filepath, scale_to_terminal=True, grayscale=True, scale_to=None):
    try:
        img = imread(filepath)
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        exit(1)

    if args.debug:
        print(f"Image shape: {img.shape}")
        print(img)

    if scale_to_terminal and scale_to is None:
        img = scale_image(img)
    elif scale_to is not None:
        img = scale_image_to(img, scale_to)

    if grayscale:
        return np.apply_along_axis(rgb_to_ascii_grayscale, -1, img)
    else:
        return np.apply_along_axis(rgb_to_ascii, -1, img)


def scale_image_to(image, scale_to):
    x_scale = (image.shape[1] // scale_to[0]) + 1
    y_scale = (image.shape[0] // scale_to[1]) + 1
    image = image[::y_scale, ::x_scale]
    return image


def scale_image(image):
    try:
        terminal_size = os.get_terminal_size()
        x_scale = ceil(image.shape[1] / terminal_size[0])
        y_scale = ceil(image.shape[0] / terminal_size[1])

        image = image[::y_scale, ::x_scale]
    except OSError:
        return image
    return image

def print_image(image):
    text = ""
    if not args.debug:
        os.system('cls' if os.name == 'nt' else 'clear')

    for row in image:
        out = ""
        for cell in row:
            out += cell
        print(out, end="\n")
        text += out + "\n"
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
    arg_parser.add_argument("filepath", help="Path to image.")

    args = arg_parser.parse_args()

    ascii_image = image_to_ascii(args.filepath, not args.no_scale, not args.color, args.scale)
    text = print_image(ascii_image)

    if args.out is not None:
        with open(args.out, "wb") as f:
            f.write(text.encode("utf-8"))

