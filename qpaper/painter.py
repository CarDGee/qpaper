#!/usr/bin/env python
"""
qpaper - Qtile extension to set X wallpaper.

How to use:

    painter = Painter(os.environ.get("DISPLAY"))    # initialise painter
    painter.paint_all(image_path)                   # paint all screens
    painter.paint_screen(0, image_path)             # paint first screen
    painter.paint_screen(1, image_path)             # paint second screen

"""


import cairocffi
import cairocffi.pixbuf
import cairocffi.xcb
import xcffib
import xcffib.xproto


def _load_image(image_path):
    """
    Load image from file.
    """
    with open(image_path, 'rb') as f:
        image, _ = cairocffi.pixbuf.decode_to_image_surface(f.read())
    return image


class Painter:
    """
    Interface for painting the X wallpaper.
    """
    def __init__(self, display):
        self.conn = xcffib.connect(display=display)
        self.screens = self.conn.get_setup().roots
        self.conn.core.SetCloseDownMode(xcffib.xproto.CloseDown.RetainPermanent)

    def paint_all(self, image_path):
        """
        Paint wallpaper on all screens.
        """
        image = _load_image(image_path)
        for screen in self.screens:
            self._paint(screen, image)

    def paint_screen(self, index, image_path):
        """
        Paint wallpaper on single screen.
        """
        image = _load_image(image_path)
        self._paint(self.screens[index], image)

    def _paint(self, screen, image):
        """
        This function does the heavy lifting.
        """
        pixmap = self.conn.generate_id()
        self.conn.core.CreatePixmap(
            screen.root_depth,
            pixmap, screen.root,
            screen.width_in_pixels, screen.height_in_pixels,
        )

        for depth in screen.allowed_depths:
            for visual in depth.visuals:
                if visual.visual_id == screen.root_visual:
                    root_visual = visual
                    break

        surface = cairocffi.xcb.XCBSurface(
            self.conn, pixmap, root_visual,
            screen.width_in_pixels, screen.height_in_pixels,
        )

        context = cairocffi.Context(surface)
        with context:
            context.set_source_surface(image)
            context.paint()

        self.conn.core.ChangeProperty(
            xcffib.xproto.PropMode.Replace,
            screen.root,
            self.conn.core.InternAtom(False, 13, '_XROOTPMAP_ID').reply().atom,
            xcffib.xproto.Atom.PIXMAP,
            32, 1, [pixmap]
        )
        self.conn.core.ChangeProperty(
            xcffib.xproto.PropMode.Replace,
            screen.root,
            self.conn.core.InternAtom(False, 16, 'ESETROOT_PMAP_ID').reply().atom,
            xcffib.xproto.Atom.PIXMAP,
            32, 1, [pixmap]
        )

        self.conn.core.ChangeWindowAttributes(
            screen.root, xcffib.xproto.CW.BackPixmap, [pixmap]
        )
        self.conn.core.ClearArea(
            0, screen.root, 0, 0, screen.width_in_pixels, screen.height_in_pixels
        )
        self.conn.flush()
