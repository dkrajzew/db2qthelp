from __future__ import print_function
"""db2qthelp.py

A DocBook to QtHelp converter.
Version 0.2

(c) Daniel Krajzewicz 2022-2023
daniel@krajzewicz.de
http://www.krajzewicz.de
https://github.com/dkrajzew/db2qtdoc
http://www.krajzewicz.de/blog/db2qtdoc.php

Available under the BSD License.
"""


import os
import shutil
import glob
import re


# Configuration
appName = "shaderwb"
appVersion = "0.2.0"

# Style - exclude into a file
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
    id = c[c.find("<a name=\"")+9:]
    id = id[:id.find("\"")]
    return id

def getName(c):
    name = c[c.find("</a>")+4:]
    name = name[:name.find("</h")]
    name = name.replace("\"", "'")
    name = name.strip()
    return name

def writeSectionsRecursive(c, fdo_content, level):
    id = getID(c)
    if id=="user":
        id = "index"
    name = getName(c)
    indent = " "*(level*3) 
    fdo_content.write(indent + "<li><a href=\"%s.html\">%s</a></li>\n" % (id, name))
    toc = indent + "<section title=\"%s\" ref=\"%s.html\">\n" % (name, id)
    keywords = "   <keyword name=\"%s\" ref=\"./%s.html\"/>\n" %  (name, id)
    #print ("%s %s %s" % (id, name, level))
    """
    if level>3:
        fdo = open("qtdoc/%s.html" % id, "w")
        fdo.write(c)
        fdo.close()
        toc += indent + "</section>\n"
        return toc
    """
    #print ("a1 %s" % (c.find("<div class=\"sect%s\">" % level)))
    subs = c.split("<div class=\"sect%s\">" % level)
    """
    if id=="user-palettes":
        print (subs)
    """
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
    #print ("a2 %s " % len(subs))
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
    

def main(argv):
    # delete previous files
    files = glob.glob("qtdoc/*.html")
    files.extend(glob.glob("qtdoc/*.png"))
    files.extend(glob.glob("qtdoc/*.gif"))
    for f in files:
        os.remove(f)
    # copy new files
    files = glob.glob("./user_images/*.png")
    files.extend(glob.glob("./user_images/icons/*.png"))
    for f in files:
        p, n = os.path.split(f)
        shutil.copy(f, "qtdoc/" + n)

    # open output documents
    fd = open("shaderwb_userdocs.html")
    doc = fd.read()
    fd.close()

    toc = ""
    keywords = ""
    fdo_content = open("qtdoc/toc.html", "w")
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
    
    fd = open("qtdoc/qhelpproject_template.qhp")
    prj = fd.read()
    fd.close()

    # write project
    prj = prj.replace("%appname%", appName).replace("%appver%", appVersion).replace("%toc%", toc).replace("%keywords%", keywords)
    fdo = open("qtdoc/shaderwb.qhp", "w")
    fdo.write(prj)
    fdo.close()

    # generate QtDocs
    # !!! patch paths
    os.system("C:\\Qt\\5.14.2\\msvc2017\\bin\\qhelpgenerator qtdoc/shaderwb.qhp -o qtdoc/shaderwb.qch")
    os.system("C:\\Qt\\5.14.2\\msvc2017\\bin\\qcollectiongenerator qtdoc/shaderwb.qhcp -o qtdoc/shaderwb.qhc")

    
    

# -- main check
if __name__ == '__main__':
    main(sys.argv)
    