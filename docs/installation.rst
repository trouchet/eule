============
Installation
============

Stable release
--------------

To install eule, run this command in your terminal:

.. code-block:: console

    $ pip install eule

Optional Dependencies
---------------------

For advanced features, you can install eule with extra dependencies:

**For Continuous Intervals (Time/Numbers)**:

.. code-block:: console

    $ pip install "eule[interval]"

**For Geometry (2D/3D Shapes)**:

.. code-block:: console

    $ pip install "eule[geometry]"

**For Everything**:

.. code-block:: console

    $ pip install "eule[interval,geometry]"

From sources
------------

The sources for eule can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/trouchet/eule

Or download and untar the `tarball`_:

.. code-block:: console

    $ curl -L https://github.com/trouchet/eule/tarball/master -o eule.tar.gz
    $ tar -xzf eule.tar.gz

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ make install


.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Github repo: https://github.com/trouchet/eule
.. _tarball: https://github.com/trouchet/eule/tarball/master
