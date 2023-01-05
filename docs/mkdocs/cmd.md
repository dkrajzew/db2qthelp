Running on the Command Line
===========================

__db2qthelp__ is implemented in [Python](https://www.python.org/). It is started on the command line.


Description
-----------

__db2qthelp__ requires some prerequisites. In the following, the steps for a QtHelp from a DocBook book are described.


### Preparing your DocBook document

You should have a user documentation written as a DocBook book. Images should be stored in a single subfolder, at best one that is located in the same folder as the DocBook document itself. E.g. if you have a project, you may have a folder "docs" in which the document itself ("docs/userdocs.xml") is located and the images / figures it references are located in "docs/images/*".


### Converting DocBook to HTML

In the first step, you have to convert this document to a single-HTML document. Being in the docs folder, I use xsltproc for this using a call similar to this one:

```console
xsltproc.exe --output userdocs.html single_html.xsl userdocs.xml
```

Here, "single_html.xsl" is a slightly modified DocBook style sheet. You may find it in this package under "data/single_html.xsl". Please not that you have to update the references to your docbook stylesheets location.

What we get is a HTML-representation of the DocBook user docs named "userdocs.html".


### Prepare the QtHelp template

We now need a template for our QtHelp project. Generate it using __db2qthelp__ by calling:

```console
python db2qthelp --generate
```

You will get a file named "template.qhp". It should be located in the same folder as your docbook document. You may though name it differently to set it's name on generation use:

```console
python db2qthelp --generate --template new_template_name.qhp
```

Open it in an editr. It should look like this:

```XML
<?xml version="1.0" encoding="latin1"?>
<QtHelpProject version="1.0">
    <namespace>%namespace%.%appname%_v%appver%</namespace>
    <virtualFolder>doc</virtualFolder>
    <filterSection>
        <filterAttribute>%appname%</filterAttribute>
        <filterAttribute>%appver%</filterAttribute>
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

You now have to patch the namespace and the filters. Replaces

* %namespace% by your namespace (e.g. to org.foo.bar)
* %appname% to your application name (e.g. MyFancyApp)
* %appver% to the version of your application (e.g. 5.22)


### Generate the QtHelp 

Well, that's almost everything. Run __db2qthelp__ again to build the documentation:

```console
python db2qthelp -i userdocs.html -t new_template_name.qhp -s images
```

The options tell __db2qthelp__ to read the HTML document "userdocs.html" generated from our original DocBook book, to use our project template "new_template_name.qhp" and that images and figures are located in "images".




Options
-------

The script has the following options:

* __--input/-i _&lt;DOCBOOK_HTML&gt;___: Defines the DocBook HTML document to parse
* __--source/-s _&lt;ADDITIONAL_FILES_FOLDER&gt;___: Sets the image source folder
* __--destination/-d _&lt;DESTINATION_FOLDER&gt;___: Sets the output folder
* __--template/-t _&lt;TEMPLATE_FILE&gt;___: Defines the QtHelp project template to use; default: 'template.qhp'
* __--generate/-g__: If set, the template is written to the file as defined by --template; The application quits afterwards
* __--help__: Prints the help screen


Examples
--------

```console
python db2qthelp --generate
```

Generates the project template file "template.qhp".


```console
python db2qthelp -i userdocs.html -t template.qhp -s images --path c:\Qt\bin
```

Reads the HTML document "userdocs.html" and the project template "template.qhp" and converts the HTML document to QtHelp assuming images etc. being located in "images". The Qt binaries are assumed to be found in "c:\Qt\bin\".


