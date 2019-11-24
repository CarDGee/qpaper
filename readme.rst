qpaper
======

Pure Python wallpaper-setter for X11.

This was originally written as an extension for the Qtile_ window manager
(hence the name qpaper), though it works as a standalone program. It requires
the same dependencies as Qtile, i.e. cairocffi_ and xcffib_.


Usage
-----

The :code:`qpaper.Painter` acts as the wallpaper setting interface.
Instantiate it with the name of the target display, and then either all screens
can be painter by using the :code:`Painter.paint_all` method, or an individual
screen using the :code:`Painter.paint_screen` method. These two methods can both
take optional these keyword args:

 - image (:code:`str`) : path to image to set as wallpaper
 - colour (:code:`str`) : hex code to simply set a colour instead of an image
 - option (:code:`str`) : one of 'fill' or 'stretch'

:code:`Painter.paint_screen` should also be passed an :code:`int` to index the
target screen.

Example
```````

To set wallpapers for all screens upon Qtile startup, add something like this
to the Qtile config:

.. code-block:: python

   import os
   import qpaper
   from libqtile import hook

   @hook.subscribe.startup
   def startup():
       qpaper.Painter(os.environ.get("DISPLAY")).paint_all(
           image='/home/user/wallpaper.png', option='fill',
       )


.. _Qtile: https://github.com/qtile/qtile
.. _cairocffi: https://cairocffi.readthedocs.io/en/stable/
.. _xcffib: https://github.com/tych0/xcffib
