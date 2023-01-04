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

# Methods

def getID(c):
    """Returns the ID of the current section
    
    :param c: The text content
    """
    id = c[c.find("<a name=\"")+9:]
    id = id[:id.find("\"")]
    return id


def getName(c):
    """Returns the name of the current section
    
    :param c: The text content
    """
    name = c[c.find("</a>")+4:]
    name = name[:name.find("</h")]
    name = name.replace("\"", "'")
    name = name.strip()
    return name


def writeSectionsRecursive(c, fdo_content, level):
    """
    
    :param c: The character (string) content
    :param fdo_content: The content output file
    :param level: intendation level
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
    """ Deletes previously collected files
    
    :param destFolder: The destination folder (where the documentation is built)
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
    
    :param srcFolder: The source folder (where images are located)
    :param destFolder: The destination folder (where the documentation is built)
    """
    # copy new files
    files = glob.glob("./user_images/*.png")
    files.extend(glob.glob("./user_images/icons/*.png"))
    for f in files:
        p, n = os.path.split(f)
        shutil.copy(f, destFolder + "/" + n)


def readDocBook(file):
    """Reads the named file
    
    :param file: The path to the docbook HTML file to read
    """
    fd = open(file)
    doc = fd.read()
    fd.close()
    return doc


def main(argv):
    sys.tracebacklimit = 0
    # parse options
    optParser = OptionParser(usage="usage:\n  db2qthelp.py [options]", version="db2qthelp.py 0.2")
    optParser.add_option("-n", "--namespace", dest="namespace", default="org", help="Sets the documentation namespace")
    optParser.add_option("-a", "--appname", dest="appname", default=None, help="Sets the name of the application to build the docs for")
    optParser.add_option("-V", "--version", dest="version", default=None, help="Sets the version of the application to build the docs for")
    optParser.add_option("-s", "--source", dest="source", default="user_images", help="Sets the image source folder")
    optParser.add_option("-d", "--destination", dest="destination", default="qtdoc", help="Sets the output folder")
    optParser.add_option("-i", "--input", dest="input", default=None, help="Defines the DocBook HTML document to parse")
    options, remaining_args = optParser.parse_args(args=args)
    # check options
    ret = 0
    if options.input is None:
        print("Error: no input file given (use -i <HTML_DOCBOOK>)...", file=sys.stderr)
        ret = 2
    if options.appname is None:
        print("Error: no application name given (use -a <NAME>)...", file=sys.stderr)
        ret = 2
    if options.version is None:
        print("Error: no application version given (use -V <APP_VERSION>)...", file=sys.stderr)
        ret = 2
    if ret!=0:
        print("Usage: db2qthelp.py -i <HTML_DOCBOOK> -a <APPNAME> -V <APP_VERSION> [options]+", file=sys.stderr)
        sys.exit(2)
    
    # get settings
    srcFolder = options.source
    destFolder = options.destination
    tocFileName = destFolder + "/toc.html"
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
    # generate QtDocs
    # !!! patch paths
    os.system("C:\\Qt\\5.14.2\\msvc2017\\bin\\qhelpgenerator %s.qhp -o %s.qch" % (path, path))
    os.system("C:\\Qt\\5.14.2\\msvc2017\\bin\\qcollectiongenerator %s.qhcp -o %s.qhc" % (path, path))

    
# -- main check
if __name__ == '__main__':
    main(sys.argv)
    