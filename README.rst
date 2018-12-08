maelstrom
=========

A minimalist multimedia streaming server

Requirements
------------

* FFMPEG
* Python 3.6+


Setup
-----

.. code:: shell

    pip install -e .


Running
-------

.. code:: shell

    maelstrom -m <media-dir> --transcode-cache <cache-dir>


After the server is started, navigate to http://localhost:8000
and select the media file to play.
