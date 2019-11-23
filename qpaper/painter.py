#!/usr/bin/env python
"""
qpaper - Qtile extension to set X wallpaper.

How to use:

    painter = Painter(display=os.environ.get("DISPLAY"))
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

def _hex_to_decimal(colour):
    """
    Get a (R, G, B) tuple from a #RRGGBB hex colour code.
    """
    if colour[0] == '#':
        colour = colour[1:]
    return [float.fromhex(i + j) for i, j in zip(colour[0::2], colour[1::2])]


class Painter:
    """
    Interface for painting the X wallpaper.
    """
    def __init__(self, display=None, conn=None):
        if conn:
            self.conn = conn
        elif display:
            self.conn = xcffib.connect(display=display)
        else:
            SystemError('Painter requires either a display or a connection')

        self.screens = self.conn.get_setup().roots
        self.conn.core.SetCloseDownMode(xcffib.xproto.CloseDown.RetainPermanent)
        self._image = None
        self._option = None
        self._colour = None

    def paint_all(self, image=None, colour=None, option=None):
        """
        Paint wallpaper on all screens.
        """
        if image:
            self._image = _load_image(image)
        elif colour:
            self._colour = _hex_to_decimal(colour)

        if option:
            self._option = option

        for screen in self.screens:
            self._paint(screen)

    def paint_screen(self, index, image=None, colour=None, option=None):
        """
        Paint wallpaper on single screen.
        """
        if image:
            self._image = _load_image(image)
        elif colour:
            self._colour = _hex_to_decimal(colour)

        self._paint(self.screens[index])

    def _paint(self, screen):
        """
        Render the specified image or colour onto a screen.
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
            if self._image:
                self._context_configure_source(context, screen)
            elif colour:
                context.set_source_rgba(*colour)
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
        self.conn.disconnect()

    def _context_configure_source(self, context, screen):
        """
        Prepare image for painting.
        """
        image = self._image

        if self._option == 'fill':
            image_w = image.get_width()
            image_h = image.get_height()
            screen_w = screen.width_in_pixels
            screen_h = screen.height_in_pixels
            width_ratio = screen_w / image_w
            if width_ratio * image_h >= screen_h:
                context.scale(sx=width_ratio)
                context.translate(0, (image_h - screen_h) / 2)
            else:
                height_ratio = screen_h / image_h
                context.translate(
                    - (image_w * height_ratio - screen_w) // 2,
                    0
                )
                context.scale(sx=height_ratio)

        elif self._option == 'stretch':
            context.scale(
                sx=screen.width_in_pixels / image.get_width(),
                sy=screen.height_in_pixels / image.get_height(),
            )

        context.set_source_surface(image)
