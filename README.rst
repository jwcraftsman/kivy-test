kivytest
========

This project contains some simple Python programs that test various
aspects of the Kivy GUI framework.

Setup
-----

In order to run these Kivy test programs, Kivy needs to be installed
and configured.  Under Ubuntu 18.04, the following system packages
should be installed. ::

    sudo apt-get install -y \
        python3-pip \
        build-essential \
        git \
        python3 \
        python3-dev \
        ffmpeg \
        libsdl2-dev \
        libsdl2-image-dev \
        libsdl2-mixer-dev \
        libsdl2-ttf-dev \
        libportmidi-dev \
        libswscale-dev \
        libavformat-dev \
        libavcodec-dev \
        zlib1g-dev

    sudo apt-get install -y \
        libgstreamer1.0 \
        gstreamer1.0-plugins-base \
        gstreamer1.0-plugins-good \
        gstreamer1.0-plugins-bad \
        gstreamer1.0-libav

    sudo apt-get install \
        virtualenvwrapper \
        evtest

Next, a virtual environment should be set up for working on Kivy projects. ::

    mkdir -p ~/venv
    export WORKON_HOME=~/venv
    mkvirtualenv --no-site-packages --python=/usr/bin/python3 kivy

To avoid having to set the `WORKON_HOME` environment variable in every
terminal session, it is advisable to add the export command to *~/.profile*.

After creating the virtual environment, it will be active.  You can
deactivate the virtual environment at any time. ::

    deactivate

When using Kivy, the virtual environment needs to be active. ::

    workon kivy

Next, the `pip3` program should be used to install some prerequisite
packages locally. ::

    pip3 install pygments docutils Pillow pyEnchant Cython==0.28.2

Next, checkout a version of Kivy known to work with Ubuntu 18.04::

    git clone http://github.com/kivy/kivy
    cd kivy
    git checkout 1.10.1

If using a touchscreen under Linux, pull in the following pull request
(#5659).  ::

    git pull origin postproc_calibration_auto

Now build and install Kivy::

    cd ..
    pip3 install -e kivy

Kivy can be tested by running an example. ::

    cd kivy/examples/demo/touchtracer
    python3 main.py

The mouse should work fine, but the touchscreen may not work.  Note
that running the Kivy example above will create a
*~/.kivy/config.ini* file that can be tweaked as required.

In order to use a touchscreen, you must first give your use account
access to the required input devices.  ::

    sudo adduser username input

You must log out and log back in for the change to take effect.  Now
you must determine which device corresponds to the touchscreen. ::

    evtest

Once you have determined the touchscreen device name, edit the
*~/.kivy/config.ini* file by replacing::

    %(name)s = probesysfs

with::

    touch = probesysfs,provider=mtdev,match=ELAN Touchscreen,use_mouse=1

where ``ELAN Touchscreen`` is the name of the touchscreen device.  Now
append the following lines to the end of the config file::

    [postproc:calibration]
    touch = auto=1366x786

where ``1366x786`` is your screen resolution.  This line requires the
pull request #5659 mentioned above and is required to get the input
scaling for the touchscreen to work properly for non-fullscreen windows.

Hopefully the example will now work properly with the touchscreen. ::

    # In the kivy/examples/demo/touchtracer directory
    python3 main.py

Install Kivy Documentation
--------------------------

If you want to build a local copy of the Kivy HTML documentation follow
these steps from *kivy/doc/README.md*::

  workon kivy
  cd kivy/doc
  pip3 install sphinx
  pip3 install -r doc-requirements.txt
  make html
  firefox build/html/index.html

The *pdf* documentation can be built like this::

  sudo apt-get install texlive-full
  make pdf
  evince build/latex/Kivy.pdf
  
Programs
--------

The Python programs in this project were written to learn about Kivy
and test various functionality.  This project is an archive for my own
reference, but others may find it useful as well.

Useful Links
------------

- `Kivy Documentation <https://kivy.org/doc/stable/gettingstarted/intro.html>`_
- `Kivy Linux Installation Documentation <https://kivy.org/doc/stable/installation/installation-linux.html>`_
- `Kivy Development Version Installation Documentation <https://kivy.org/doc/stable/installation/installation.html#development-version>`_
