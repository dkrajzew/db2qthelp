from __future__ import print_function
# ===================================================================
# db2qthelp - a DocBook book to QtHelp project converter.
# Version 0.4.
#
# Main module
#
# (c) Daniel Krajzewicz 2022-2023
# - daniel@krajzewicz.de
# - http://www.krajzewicz.de
# - https://github.com/dkrajzew/db2qthelp
# - http://www.krajzewicz.de/blog/db2qthelp.php
#
# Available under the BSD license.
# ===================================================================


# --- imports -------------------------------------------------------
import os
import sys
import shutil
import glob
import re
from optparse import OptionParser


# --- variables and constants ---------------------------------------
style = """
<style>
body {
 margin: 0;
 padding: 0 0 0 0;
 background-color: rgba(255, 255, 255, 1);
 font-size: 12pt;
}
ul { margin: -.8em 0em 1em 0em; }
li { margin: 0em 0em 0em 0em; }
p { margin: .2em 0em .4em 0em; }
h4 { font-size: 14pt; }
h3 { font-size: 16pt; }
h2 { font-size: 18pt; }
h1 { font-size: 20pt; }
pre { background-color: rgba(224, 224, 224, 1); }
.guimenu, .guimenuitem, .guibutton { font-weight: bold; }
table, th, td { border: 1px solid black; border-collapse: collapse; }
th, td { padding: 4px; }
th { background-color: rgba(204, 212, 255, 1); }
div.informalequation { text-align: center; font-style: italic; }
.note p { background-color: #e0f0ff; margin: 8px 8px 8px 8px; }
.tip p { background-color: #c0ffc0; margin: 8px 8px 8px 8px; }
.warning p { background-color: #ffff80; margin: 8px 8px 8px 8px; }
</style>
"""

template = """<?xml version="1.0" encoding="latin1"?>
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
"""

qhcp = """<?xml version="1.0" encoding="UTF-8"?>
<QHelpCollectionProject version="1.0">
    <docFiles>
        <generate>
            <file>
                <input>%appname%.qhp</input>
                <output>%appname%.qch</output>
            </file>
        </generate>
        <register>
            <file>%appname%.qch</file>
        </register>
    </docFiles>
</QHelpCollectionProject>
"""


# --- methods -------------------------------------------------------
def getID(html):
    """Returns the ID of the current section.

    The value of the first a-element's name attribute is assumed to be the ID.

    Args:
        html (str): The HTML snippet to get the next ID from

    Returns:
        (str): The next ID found in the snippet
    """
    id = html[html.find("<a name=\"")+9:]
    id = id[:id.find("\"")]
    return id


def getName(html):
    """Returns the name of the current section.

    Args:
        html (str): The HTML snippet to get the next name from

    Returns:
        (str): The next name found in the snippet
    """
    name = html[html.find("</a>")+4:]
    name = name[:name.find("</h")]
    name = name.replace("\"", "'")
    name = name.strip()
    return name


def writeSectionsRecursive(c, srcFolder, destFolder, sourceURL, fdo_content, level):
    """Writes the given section and it's sub-sections recursively.

    The id and the name of the section are retrieved, first.

    Then, the toc HTML file is extended and the reference to this section is
    appended to the returned toc. Keywords are extended by the section's name.

    The section is then split along the
    '&lt;div class="sect&lt;INDENT&gt;"&gt;' elements which are processed
    recursively.

    The (recursively) collected keywords and toc are returned.

    Args:
        c (str): The (string) content of the DocBook book section or appendix
        srcFolder (List[str]): The source folder(s) (where images are located)
        destFolder (str): The destination folder (where the documentation is built)
        sourceURL (str): The URL of the built QtHelp pages
        fdo_content (file): The content output file
        level (int): intendation level

    Returns:
        Tuple[str, str]: The table of content and the collected keywords

    """
    global style
    id = getID(c)
    if id=="user":
        id = "index" # @todo: check!
    name = getName(c)
    indent = " "*(level*3)
    fdo_content.write(indent + "<li><a href=\"%s.html\">%s</a></li>\n" % (id, name))
    toc = indent + "<section title=\"%s\" ref=\"%s.html\">\n" % (name, id)
    keywords = "   <keyword name=\"%s\" ref=\"./%s.html\"/>\n" %  (name, id)
    """
    #if level>3:
    #    fdo = open("qtdoc/%s.html" % id, "w")
    #    fdo.write(c)
    #    fdo.close()
    #    toc += indent + "</section>\n"
    #    return toc
    """
    subs = c.split("<div class=\"sect%s\">" % level)
    if subs[0].rfind("</div>")>=len(subs[0])-6:
        subs[0] = subs[0][:subs[0].rfind("</div>")]
    for s in srcFolder:
        subs[0] = subs[0].replace("src=\"%s/" % s, "src=\"qthelp://%s/doc/" % sourceURL)
    subs[0] = re.sub(r'<a href="#([^"]*)">([^<]*)</a>', r'<a href="\1.html">\2</a>', subs[0])
    subs[0] = re.sub(r'<a class="ulink" href="#([^"]*)">([^<]*)</a>', r'<a class="ulink" href="\1.html">\2</a>', subs[0])
    subs[0] = "<html><head>" + style + "</head><body>" + subs[0] + "</body></html>"
    fdo = open(destFolder + "/%s.html" % id, "w")
    fdo.write(subs[0])
    fdo.close()
    if len(subs)>1:
        fdo_content.write(indent + "<ul>\n")
        for i,sub in enumerate(subs):
            if i==0:
                continue
            sub = sub[:sub.rfind("</div>")]
            for s in srcFolder:
                sub = sub.replace("src=\"%s/" % s, "src=\"qthelp://%s/doc/" % sourceURL)
            tocA, keysA = writeSectionsRecursive(sub, srcFolder, destFolder, sourceURL, fdo_content, level+1)
            toc += tocA
            keywords += keysA
        fdo_content.write(indent + "</ul>\n")
    toc += indent + "</section>\n"
    return toc, keywords


def _makeClean(destFolder):
    """ Deletes previously collected and built files.

    Deletes all .html, .png, and .gif files within the destination folder.

    Args:
        destFolder (str): The destination folder (where the documentation is built)
    """
    # delete previous files
    files = glob.glob(destFolder + "/*.html")
    files.extend(glob.glob(destFolder + "/*.png"))
    files.extend(glob.glob(destFolder + "/*.gif"))
    for f in files:
        os.remove(f)


def _copyFiles(srcFolder, destFolder):
    """Collects images to include in the documenatation.

    Copies them from the source to the destination folder.

    Args:
        srcFolder (str): The source folder(s) (where images are located)
        destFolder (str): The destination folder (where the documentation is built)
    """
    # copy new files
    for s in srcFolder:
        files = glob.glob(os.path.join(s, "*.png"))
        files.extend(glob.glob(os.path.join(s, "*.gif")))
        for f in files:
            p, n = os.path.split(f)
            shutil.copy(f, destFolder + "/" + n)


def main(arguments=None):
    """The main method using parameter from the command line.

    The application deletes previously collected and build .html, .png, and
    .gif-files within the folder defined by --destination. Then, it copies
    .png and .gif-files from the folders defined using --files into the
    destination folder.

    It then reads the HTML-file generated from DocBook defined using --input
    and processes it. Processing means here that the file is split at sections
    and appendices. Each subpart is written into the destination folder defined
    using --destination and included in the table of contents (toc). The paths
    to references images as defined using --files are replaced by the
    destination path defined using --destination. In addition, the headers are
    included in the list of keywords.

    Then, the qhp-templated defined using --template is loaded and the
    placeholders (see above) are replaced by the given / collected data.

    db2qthelp generates a qhcp file afterwards as
    "&lt;DESTINATION_FOLDER>/&lt;APPLICATION_NAME&gt;.qhcp".

    Finally, the script calls two QtHelp processing applications which must be
    located in the folder defined using --path:

    &lt;QT_PATH&gt;/qhelpgenerator &lt;APPLICATION_NAME&gt;.qhp -o &lt;APPLICATION_NAME&gt;.qch
    &lt;QT_PATH&gt;/qcollectiongenerator &lt;APPLICATION_NAME&gt;.qhcp -o &lt;APPLICATION_NAME&gt;.qhc

    Args:
        arguments (List[str]): The command line arguments, parsed as options using OptionParser.

    Options
    -------

    The following options must be set:

    --input / -i &lt;DOCBOOK_HTML&gt;:
        Defines the DocBook HTML document to parse

    --appname / -a &lt;APPLICATION_NAME&gt;:
        Sets the name of the application

    --source / -s &lt;ADDITIONAL_FILES_FOLDER&gt;:
        Sets the documentation source url


    The following options are optional:

    --files / -f &lt;ADDITIONAL_FILES_FOLDER&gt;[,&lt;ADDITIONAL_FILES_FOLDER&gt;]*:
        Sets the folder(s) to collect files from

    --destination / -d &lt;DESTINATION_FOLDER&gt;:
        Sets the output folder

    --template / -t &lt;TEMPLATE_FILE&gt;:
        Defines the QtHelp project template to use; default: 'template.qhp'

    --generate / -g:
        If set, the template is written to the file as defined by --template;
        The application quits afterwards

    --path / -p &lt;QT_PATH&gt;:
        Sets the path to the Qt binaries to use

    --help:
        Prints the help screen
    """
    #sys.tracebacklimit = 0
    # parse options
    optParser = OptionParser(usage="usage:\n  db2qthelp.py [options]", version="db2qthelp.py 0.4")
    optParser.add_option("-i", "--input", type="string", dest="input", default=None, help="Defines the DocBook HTML document to parse")
    optParser.add_option("-a", "--appname", type="string", dest="appname", default=None, help="Sets the name of the application")
    optParser.add_option("-s", "--source", type="string", dest="source", default=None, help="Sets the documentation source url")
    optParser.add_option("-f", "--files", type="string", dest="files", default="user_images", help="Sets the folder to collect files from")
    optParser.add_option("-d", "--destination", type="string", dest="destination", default="qtdoc", help="Sets the output folder")
    optParser.add_option("-t", "--template", type="string", dest="template", default="template.qhp", help="Defines the QtHelp project template to use")
    optParser.add_option("-g", "--generate", dest="generate", action="store_true", default=False, help="If set, a template is generated")
    optParser.add_option("-p", "--path", type="string", dest="path", default="", help="Sets the path to the Qt binaries to use")
    options, remaining_args = optParser.parse_args(args=arguments)
    # - generate the template and quit, if wished
    if options.generate:
        with open(options.template, "w") as fdo:
            global template
            fdo.write(template)
        print ("Written qhp template to '%s'" % options.template)
        sys.exit(0)
    # - build documentation
    # check options
    ret = 0
    if options.input is None:
        print("Error: no input file given (use -i <HTML_DOCBOOK>)...", file=sys.stderr)
        ret = 2
    if options.appname is None:
        print("Error: no application name given (use -a <APP_NAME>)...", file=sys.stderr)
        ret = 2
    if options.source is None:
        print("Error: no source url given(use -s <SOURCE_URL>)...", file=sys.stderr)
        ret = 2
    if ret!=0:
        print("Usage: db2qthelp.py -i <HTML_DOCBOOK> [options]+", file=sys.stderr)
        sys.exit(2)
    # get settings
    appName = options.appname
    srcFolder = [v.replace("\\", "/") for v in options.files.split(",")]
    srcFolder.sort(key=lambda t: len(t), reverse=True)
    sourceURL = options.source
    destFolder = options.destination
    if not os.path.exists(destFolder):
        os.mkdir(destFolder)
    tocFileName = destFolder + "/toc.html"
    qtPath = options.path
    # delete previous files
    _makeClean(destFolder)
    # copy images
    _copyFiles(srcFolder, destFolder)
    # read doc
    with open(options.input) as fdi:
        doc = fdi.read()
    # process document
    toc = ""
    keywords = ""
    fdo_content = open(tocFileName, "w")
    fdo_content.write("<html><head>" + style + "</head><body>\n")
    chapters = doc.split("<div class=\"chapter\">")
    appendices = chapters[-1].split('<div class="appendix">')
    chapters = chapters[:-1]
    chapters.extend(appendices)
    for c in chapters:
        tocA, keysA = writeSectionsRecursive(c, srcFolder, destFolder, sourceURL, fdo_content, 1)
        toc += tocA
        keywords += keysA
    fdo_content.write("</body></html>\n")
    fdo_content.close()
    # read template, write extended by collected data
    with open(options.template) as fdi:
        template = fdi.read()
    path = destFolder + "/" + appName
    with open(path + ".qhp", "w") as fdo:
        fdo.write(template.replace("%toc%", toc).replace("%keywords%", keywords).replace("%source%", sourceURL).replace("%appname%", appName))
    # generate qhcp
    with open(path + ".qhcp", "w") as fdo:
        global qhcp
        fdo.write(qhcp.replace("%appname%", appName))
    # generate QtHelp
    os.system("%s/qhelpgenerator %s.qhp -o %s.qch" % (qtPath, path, path))
    os.system("%s/qcollectiongenerator %s.qhcp -o %s.qhc" % (qtPath, path, path))


# -- main check
if __name__ == '__main__':
    main(sys.argv)
