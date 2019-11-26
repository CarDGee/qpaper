"""
qpaper script with arg parser.
"""


import argparse
import os

from .painter import Painter


def main():
    parser = argparse.ArgumentParser(
        description='Python wallpaper setter for X',
    )

    parser.add_argument(
        'image', nargs=1,
        help='Path to image to set as wallpaper.',
        type=str,
        default=[],
    )

    parser.add_argument(
        '-o', '--option', nargs=1,
        help="Format, one of: 'fill' (default), 'stretch'",
        default=['fill'],
        type=str,
    )

    args = parser.parse_args()

    if args.image:
        painter = Painter(display=os.environ.get("DISPLAY"))
        painter.paint_all(
            image=args.image[0],
            option=args.option[0],
        )
