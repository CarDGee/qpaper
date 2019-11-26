import setuptools

with open("readme.rst", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="qpaper",
    version="0.1",
    author="mcol",
    author_email="mcol@posteo.net",
    description="Python wallpaper setter for X",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/m-col/qpaper",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['qpaper = qpaper.script:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
    ],
)
