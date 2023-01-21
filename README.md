[![License: BSD](https://img.shields.io/badge/License-BSD-green.svg)](https://github.com/dkrajzew/db2qthelp/blob/master/LICENSE) 
[![PyPI version](https://badge.fury.io/py/db2qthelp.svg)](https://pypi.python.org/pypi/db2qthelp)
[![Downloads](https://pepy.tech/badge/db2qthelp)](https://pepy.tech/project/db2qthelp)


db2qthelp &mdash; a DocBook book to QtHelp project converter

db2qthelp &mdash; a DocBook book to QtHelp project converter

Introduction
============

__db2qthelp__ converts a [DocBook](https://docbook.org/) [book](https://tdg.docbook.org/tdg/4.5/book.html) to a [QtHelp](https://doc.qt.io/qt-5/qthelp-framework.html) project.

__db2qthelp__ is in an early stage of &ldquo;development&rdquo;. It works well for me but it may work with my setup only.

Any feedback is appreciated.


Background
==========

I usually write my user documentation using [DocBook](https://docbook.org/). For my recent applications built on top of [Qt](https://www.qt.io/), I needed something
that generates in-app help pages. __db2qthelp__ does this.


Download and Installation
=========================

The __current version__ is [db2qthelp-0.2](https://github.com/dkrajzew/db2qthelp/releases/tag/0.2).

You may __install db2qthelp__ using

```console
python -m pip install db2qthelp
```

You may __download a copy or fork the code__ at [db2qthelp&apos;s github page](https://github.com/dkrajzew/db2qthelp).

Besides, you may __download the current release__ here:

* [db2qthelp-0.2.zip](https://github.com/dkrajzew/db2qthelp/archive/refs/tags/0.2.zip)
* [db2qthelp-0.2.tar.gz](https://github.com/dkrajzew/db2qthelp/archive/refs/tags/0.2.tar.gz)


License
=======

__db2qthelp__ is licensed under the [BSD license](LICENSE).


Running on the Command Line
===========================

__db2qthelp__ is implemented in [Python](https://www.python.org/). It is started on the command line.


Description
-----------

__db2qthelp__ requires some prerequisites. In the following, the steps for a QtHelp from a DocBook book are described.


### Preparing your DocBook document

You should have a user documentation written as a DocBook book. Images should be stored in a subfolder, at best one that is located in the same folder as the DocBook document itself. E.g. if you have a project, you may have a folder &ldquo;docs&rdquo; in which the document itself (&ldquo;docs/userdocs.xml&rdquo;) is located and the images / figures it references are located in &ldquo;docs/images/*&rdquo;.


### Converting DocBook to HTML

In the first step, you have to convert this document to a single-HTML document. Being in the docs folder, I use xsltproc for this using a call similar to this one:

```console
xsltproc.exe --output userdocs.html single_html.xsl userdocs.xml
```

Here, &ldquo;single_html.xsl&rdquo; is a slightly modified DocBook style sheet. You may find it in this package under &ldquo;data/single_html.xsl&rdquo;. Please not that you have to update the references to your docbook stylesheets location.

What we get is a HTML-representation of the DocBook user docs named &ldquo;userdocs.html&rdquo;.


### Prepare the QtHelp template

We now need a template for our QtHelp project. Generate it using __db2qthelp__ by calling:

```console
python db2qthelp --generate
```

You will get a file named &ldquo;template.qhp&rdquo;. It should be located in the same folder as your DocBook document. You may though name it differently to set it&apos;s name on generation use:

```console
python db2qthelp --generate --template new_template_name.qhp
```

Open it in an editor. It should look like this:

```XML
<?xml version="1.0" encoding="latin1"?>
<QtHelpProject version="1.0">
    <namespace>%source%</namespace>
    <virtualFolder>doc</virtualFolder>
    <filterSection>
        <filterAttribute>%appname%</filterAttribute>
        <toc>
%toc%
        </toc>
        <keywords>
%keywords%
        </keywords>
        <files>
            <file>*.html</file>
            <file>*.png</file>
            <file>*.gif</file>
        </files>
    </filterSection>
</QtHelpProject>
```

You may note that there are some placeholders. Both will be later on filled by __db2qthelp__

* %source% is the complete URL to your documentation, it usually looks like &ldquo;org.foo.bar.MyFancyApp_v0.1&rdquo;
* %appname% is your application name (e.g. &ldquo;MyFancyApp&rdquo;)
* %toc% will be replaced by the documentation&apos;s structure (table of contents)
* %keywords% will be replaced by the collected keywords

You may add additional filter attributes.


### Generate the QtHelp

Well, that&apos;s almost everything. Run __db2qthelp__ again to build the documentation:

```console
python db2qthelp -i userdocs.html -t new_template_name.qhp -s org.foo.bar.MyFancyApp_v0.1 -a MyFancyApp -p c:\Qt\bin
```

The options tell __db2qthelp__ to read the HTML document &ldquo;userdocs.html&rdquo; generated from our original DocBook book, to use our project template &ldquo;new_template_name.qhp&rdquo; and that images and figures are located in &ldquo;images&rdquo;.

As we did not define the destination folder, __db2qthelp__ uses the default &ldquo;qtdocs&rdquo;.

The built documentation can be found in the destination folder. You need two files to include it in your application:

* &lt;APPLICATION_NAME&gt;.qch
* &lt;APPLICATION_NAME&gt;.qhc

Options
-------

The script has the following options:

* __--input/-i _&lt;DOCBOOK_HTML&gt;___: Defines the DocBook HTML document to parse
* __--appname/-a _&lt;APPLICATION_NAME&gt;___: Sets the name of the application
* __--source/-s _&lt;ADDITIONAL_FILES_FOLDER&gt;___: Sets the documentation source url
* __--files/-f _&lt;ADDITIONAL_FILES_FOLDER&gt;[,&lt;ADDITIONAL_FILES_FOLDER&gt;]*___: Sets the folder(s) to collect files from
* __--destination/-d _&lt;DESTINATION_FOLDER&gt;___: Sets the output folder
* __--template/-t _&lt;TEMPLATE_FILE&gt;___: Defines the QtHelp project template to use; default: &lsquo;template.qhp&rsquo;
* __--generate/-g__: If set, the template is written to the file as defined by --template; The application quits afterwards
* __--path/-p _&lt;QT_PATH&gt;___: Sets the path to the Qt binaries to use
* __--help__: Prints the help screen


Explanation
-----------

__db2qthelp__ copies *.png and *.gif-files from the folders defined using --files, first.

It then reads the HTML-file generated from DocBook defined using --input and processes it. Processing means here that the file is split at sections and appendices. Each subpart is written into the destination folder defined using --destination and included in the table of contents (toc). The paths to references images as defined using --files are replaced by the destination path defined using --destination. In addition, the headers are included in the list of keywords.

Then, the qhp-templated defined using --template is loaded and the placeholders (see above) are replaced by the given / collected data.

__db2qthelp__ generates a qhcp file afterwards as &ldquo;&lt;DESTINATION_FOLDER&gt;/&lt;APPLICATION_NAME&gt;.qhcp&rdquo;.

Finally, the script calls two QtHelp processing applications which must be located in the folder defined using --path:

```console
<QT_PATH>/qhelpgenerator <APPLICATION_NAME>.qhp -o <APPLICATION_NAME>.qch
<QT_PATH>/qcollectiongenerator <APPLICATION_NAME>.qhcp -o <APPLICATION_NAME>.qhc
```


Examples
--------

```console
python db2qthelp --generate
```

Generates the project template file &ldquo;template.qhp&rdquo;.


```console
python db2qthelp -i userdocs.html -t template.qhp -s org.foo.bar.MyFancyApp_v0.1  --path c:\Qt\bin
```

Reads the HTML document &ldquo;userdocs.html&rdquo; and the project template &ldquo;template.qhp&rdquo; and converts the HTML document to QtHelp assuming images etc. being located in &ldquo;images&rdquo;. The Qt binaries are assumed to be found in &ldquo;c:\Qt\bin\&rdquo;.


Further Documentation
---------------------

* A (maybe even more) complete documentation is located at: https://krajzewicz.de/docs/db2qthelp/index.html
* The github repository is located at: https://github.com/dkrajzew/db2qthelp
* The issue tracker is located at: https://github.com/dkrajzew/db2qthelp/issues
* The PyPI page is located at: https://pypi.org/project/db2qthelp/
* The code documentation (pydoc) is located at: http://www.krajzewicz.de/docs/db2qthelp.html


Examples / Users
================

* [PaletteWB](https://www.palettewb.com/) &mdash; a sophisticated palette editor for MS Windows.


Change Log
==========

db2qthelp-0.2 (07.01.2023)
--------------------------

* Initial checkin
* Adding configuration options
* Adding a documentation
* Adding first tests


Summary
=======

Well, have fun. If you have any comments / ideas / issues, please submit them to [db2qthelp's issue tracker](https://github.com/dkrajzew/db2qthelp/issues) on github.


