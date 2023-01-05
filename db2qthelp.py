from __future__ import print_function
# ===================================================================
# db2qthelp - a DocBook book to QtHelp project converter.
# Version 0.2.
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
"""


# --- methods -------------------------------------------------------
def getID(html):
    """Returns the ID of the current section

    The value of the first a-element's name attribute is assumed to be the ID.
    
    Args:
        html (string): The HTML snippet to get the next ID from

    Returns:
        string: The next ID found in the snippet
    """
    id = html[html.find("<a name=\"")+9:]
    id = id[:id.find("\"")]
    return id


def getName(html):
    """Returns the name of the current section
    
    Args:
        html (string): The HTML snippet to get the next name from

    Returns:
        string: The next name found in the snippet
    """
    name = html[html.find("</a>")+4:]
    name = name[:name.find("</h")]
    name = name.replace("\"", "'")
    name = name.strip()
    return name


def writeSectionsRecursive(c, fdo_content, level):
    """
    
    Args:
        c (string): The character (string) content
        fdo_content (output file handle): The content output file
        level (int): intendation level

    Returns:
        toc, keywords: The table of content and the collected keywords

    """
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
    fdo = open("qtdoc/%s.html" % id, "w")
    if subs[0].rfind("</div>")>=len(subs[0])-6:
        subs[0] = subs[0][:subs[0].rfind("</div>")]
    subs[0] = subs[0].replace("src=\"user_images/icons/", "src=\"qthelp://de.dks.shaderwb_v0.2.0/doc/")
    subs[0] = subs[0].replace("src=\"user_images/", "src=\"qthelp://de.dks.shaderwb_v0.2.0/doc/")
    subs[0] = re.sub(r'<a href="#([^"]*)">([^<]*)</a>', r'<a href="\1.html">\2</a>', subs[0]) 
    subs[0] = re.sub(r'<a class="ulink" href="#([^"]*)">([^<]*)</a>', r'<a class="ulink" href="\1.html">\2</a>', subs[0]) 
    subs[0] = "<html><head>" + style + "</head><body>" + subs[0] + "</body></html>"
    fdo.write(subs[0])
    fdo.close()
    if len(subs)>1:
        fdo_content.write(indent + "<ul>\n")
        for i,sub in enumerate(subs):
            if i==0:
                continue
            sub = sub[:sub.rfind("</div>")]
            sub = sub.replace("src=\"user_images/icons/", "src=\"qthelp://de.dks.shaderwb_v0.2.0/doc/")
            sub = sub.replace("src=\"user_images/", "src=\"qthelp://de.dks.shaderwb_v0.2.0/doc/")
            sub = "<html><head>" + style + "</head><body>" + sub + "</body></html>"
            tocA, keysA = writeSectionsRecursive(sub, fdo_content, level+1)
            toc += tocA
            keywords += keysA
        fdo_content.write(indent + "</ul>\n")
    toc += indent + "</section>\n"
    return toc, keywords


def _makeClean(destFolder):
    """ Deletes previously collected and built files
    
    Args:
        destFolder (string): The destination folder (where the documentation is built)
    """
    # delete previous files
    files = glob.glob(destFolder + "/*.html")
    files.extend(glob.glob(destFolder + "/*.png"))
    files.extend(glob.glob(destFolder + "/*.gif"))
    for f in files:
        os.remove(f)
    
    
def _copyFiles(srcFolder, destFolder):    
    """Collects images to include in the documenatation
    
    Copies them from the source to the destination folder
    
    Args:
        srcFolder (string): The source folder (where images are located)
        destFolder (string): The destination folder (where the documentation is built)
    """
    # copy new files
    files = glob.glob("./user_images/*.png")
    files.extend(glob.glob("./user_images/icons/*.png"))
    for f in files:
        p, n = os.path.split(f)
        shutil.copy(f, destFolder + "/" + n)


def readDocBook(filename):
    """Reads the named file
    
    Args:
        filename (string): The path to the docbook HTML file to read
    """
    fd = open(filename)
    doc = fd.read()
    fd.close()
    return doc


def main(arguments):
    sys.tracebacklimit = 0
    # parse options
    optParser = OptionParser(usage="usage:\n  db2qthelp.py [options]", version="db2qthelp.py 0.2")
    optParser.add_option("-i", "--input", dest="input", default=None, help="Defines the DocBook HTML document to parse")
    optParser.add_option("-s", "--source", dest="source", default="user_images", help="Sets the image source folder")
    optParser.add_option("-d", "--destination", dest="destination", default="qtdoc", help="Sets the output folder")
    optParser.add_option("-t", "--template", dest="template", default="template.qhp", help="Defines the QtHelp project template to use")
    optParser.add_option("-g", "--generate", dest="generate", action="store_true", default=False, help="If set, a template is generated")
    optParser.add_option("-p", "--path", dest="path", default="", help="Sets the path to the Qt binaries to use")
    options, remaining_args = optParser.parse_args(args=arguments)
    # - generate the template and quit, if wished
    if options.generate:
        with open(options.template, "w") as fdo:
            fdo.write(template)
        print ("Written qhp template to '%s'" % options.template)
        sys.exit(0)
    # - build documentation
    # check options
    if options.input is None:
        print("Error: no input file given (use -i <HTML_DOCBOOK>)...", file=sys.stderr)
        print("Usage: db2qthelp.py -i <HTML_DOCBOOK> [options]+", file=sys.stderr)
        sys.exit(2)
    # get settings
    srcFolder = options.source
    destFolder = options.destination
    tocFileName = destFolder + "/toc.html"
    qtPath = options.path
    # delete previous files
    _makeClean(destFolder)
    # copy images
    _copyFiles(srcFolder, destFolder)
    # read the docbook file (content)
    doc = readDocBook(options.input)
    # 
    toc = ""
    keywords = ""
    fdo_content = open(tocFileName, "w")
    fdo_content.write("<html><head>" + style + "</head><body>\n")
    chapters = doc.split("<div class=\"chapter\">")
    t = chapters[-1].split('<div class="appendix">')
    chapters = chapters[:-1]
    chapters.extend(t)
    for c in chapters:
        tocA, keysA = writeSectionsRecursive(c, fdo_content, 1)
        toc += tocA
        keywords += keysA
    fdo_content.write("</body></html>\n")
    fdo_content.close()
    # read template
    fd = open("qhelpproject_template.qhp")
    prj = fd.read()
    fd.close()
    # write project
    prj = prj.replace("%namespace%", options.namespace).replace("%appname%", options.appname).replace("%appver%", options.version).replace("%toc%", toc).replace("%keywords%", keywords)
    path = destFolder + "/" + options.appname
    fdo = open(path + ".qhp", "w")
    fdo.write(prj)
    fdo.close()
    # generate QtHelp
    os.system("%s/qhelpgenerator %s.qhp -o %s.qch" % (qtPath, path, path))
    os.system("%s/qcollectiongenerator %s.qhcp -o %s.qhc" % (qtPath, path, path))

    
# -- main check
if __name__ == '__main__':
    main(sys.argv)
    