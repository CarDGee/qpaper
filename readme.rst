qpaper
======

Pure Python wallpaper-setter for X11.

This was originally written as an extension for the Qtile_ window manager
(hence the name qpaper), though it works as a standalone program. It requires
the same dependencies as Qtile, i.e. cairocffi_ and xcffib_.


Example Usage
-------------

To (re)set wallpapers for all screens upon Qtile startup and randr screen
change, add something like this to the Qtile config:

.. code-block:: python

   import os
   from qpaper import Painter
   from libqtile import hook
   DISPLAY = os.environ.get("DISPLAY")

   @hook.subscribe.startup
   def startup():
       Painter(DISPLAY).paint_all(wallpaper)

   @hook.subscribe.screen_change
   def screen_change(qtile, ev):
       Painter(DISPLAY).paint_all(wallpaper)


.. _Qtile: https://github.com/qtile/qtile
.. _cariocffi: https://cairocffi.readthedocs.io/en/stable/
.. _xcffib: https://github.com/tych0/xcffib
