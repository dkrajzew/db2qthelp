# Download and Installation

__db2qthelp__ is a [Python](https://www.python.org/) script. To run it, you must have [Python](https://www.python.org/) installed. If you have not installed [Python](https://www.python.org/), yet, please read instructions on installing [Python](https://www.python.org/) first (see below).

Assuming that you are interested in [DocBook](https://docbook.org/), you are probably aware of [xsltproc](https://gitlab.gnome.org/GNOME/libxslt) as a processing tool. In case your [DocBook](https://docbook.org/) document is not yet converted, you will need [xsltproc](https://gitlab.gnome.org/GNOME/libxslt). Please see below for a brief information about installing [xsltproc](https://gitlab.gnome.org/GNOME/libxslt).


## Installing db2qthelp

The current version is [db2qthelp-0.4.0](https://github.com/dkrajzew/db2qthelp/releases/tag/0.4.0).

You have different options for installing __db2qthelp__.

### Installing from PyPi

You may __install db2qthelp__ using

```console
python -m pip install db2qthelp
```

This will install __db2qthelp__ as a script that may be directly called on the command line. The PyPi version only includes the (executable) source code and files needed to run it. You may consider building a virtual environment, first.

You may then run __db2qthelp__ using 

```console
db2qthelp
```

### Cloning the repository

You may __clone the repository__ which is available at [db2qthelp&apos;s github page](https://github.com/dkrajzew/db2qthelp).

```console
git clone https://github.com/dkrajzew/db2qthelp.git
cd db2qthelp
```

You may then run __db2qthelp__ using 

```console
python db2qthelp/db2qthelp.py
```

Please note that the current repository version may contain an in-between version with new, undescribed, or even buggy behavior. You should rather use a recent release version.

### Download the latest release

Besides, you may __download the current release__ here:

* [db2qthelp-0.4.0.zip](https://github.com/dkrajzew/db2qthelp/archive/refs/tags/0.4.0.zip)
* [db2qthelp-0.4.0.tar.gz](https://github.com/dkrajzew/db2qthelp/archive/refs/tags/0.4.0.tar.gz)

You will get the complete copy of the repository which you have to decompress. A folder named ```db2qthelp-0.4.0``` will be generated.

You may run __db2qthelp__ using 

```console
python db2qthelp/db2qthelp.py
```


## Installing Python

[Python](https://www.python.org/) is an interpreted programming language. For running __db2qthelp__ and other scripts written in Python you have to install [Python](https://www.python.org/) itself, first.

For installing [Python](https://www.python.org/), use an installer for your system from <https://www.python.org>.

You should as well install **pip**, a package manager for [Python](https://www.python.org/). After installing [Python](https://www.python.org/), you should be able to install **pip** using:

```console
python get-pip.py
```

You may upgrade pip using:

```console
pip install --upgrade pip
```

## Installing xsltproc

[xsltproc](https://gitlab.gnome.org/GNOME/libxslt) is an XSLT processor included in libxslt. There is [gitlab libxslt repository](https://gitlab.gnome.org/GNOME/libxslt) and a [libxslt release downloads](https://download.gnome.org/sources/libxslt/) page.

On Ubuntu Linux you should be able to install [xsltproc](https://gitlab.gnome.org/GNOME/libxslt) using

```console
sudo apt-get install xsltproc
```

On Windows, I got my [xsltproc](https://gitlab.gnome.org/GNOME/libxslt) and need libraries from [Igor Zlatkovic's website](https://www.zlatkovic.com/libxml.en.html). Please note that you need libxslt, iconc, libxml2, and zlib. I collected them in a single folder&#8230;

## Some further notes

You should add both, [xsltproc](https://gitlab.gnome.org/GNOME/libxslt) folder as well as the folder your [Qt](https://www.qt.io/) binaries reside in to the path. On Windows (of course, depending on the location on your system):

```console
set PATH=%PATH%;D:\libs\Qt\5.15.2\msvc2019\bin;D:\z_dev\docbook\libxslt-1.1.26.win32\bin
```

And you should set the XML_CATALOG_FILES to point to the ```catalog.xml``` file of your [DocBook](https://docbook.org/) xsl catalogue.

```console
set XML_CATALOG_FILES=D:\z_dev\docbook\docbook-xsl-1.79.2\catalog.xml
```

