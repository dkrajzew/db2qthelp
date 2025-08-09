#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""db2qthelp - a DocBook book to QtHelp project converter"""
# ===========================================================================
__author__     = "Daniel Krajzewicz"
__copyright__  = "Copyright 2022-2025, Daniel Krajzewicz"
__credits__    = ["Daniel Krajzewicz"]
__license__    = "BSD"
__version__    = "0.2.0"
__maintainer__ = "Daniel Krajzewicz"
__email__      = "daniel@krajzewicz.de"
__status__     = "Development"
# ===========================================================================
# - https://github.com/dkrajzew/db2qthelp
# - http://www.krajzewicz.de/docs/db2qthelp/index.html
# - http://www.krajzewicz.de
# ===========================================================================


# --- imports ---------------------------------------------------------------
import os
import sys
import shutil
import glob
import re
import argparse
import configparser
import io
import tempfile
import subprocess
from typing import List


# --- variables and constants -----------------------------------------------
STYLE = """
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

TEMPLATE = """<?xml version="1.0" encoding="latin1"?>
<QtHelpProject version="1.0">
    <namespace>%appname%</namespace>
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

QCHP = """<?xml version="1.0" encoding="UTF-8"?>
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

# --- functions -------------------------------------------------------------
class Db2QtHelp:
    def __init__(self, qt_path : str, xslt_path : str, source : str, src_folder : List[str], dst_folder : str, app_name : str):
        """Contructor

        Args:
            qt_path (str): Path to the Qt binaries
            source (str): Path to the docbook/html source to process
            url (str): The url of the documentation
            src_folder (List[str]): The source folder(s) (where images are located)
            dst_folder (str): The destination folder (where the documentation is built)
            app_name (str): The name of the application
        """
        self._qt_path = qt_path
        self._xslt_path = xslt_path
        self._source = source
        self._src_folder = src_folder
        self._dst_folder = dst_folder
        self._app_name = app_name
        self._toc = ""
        self._keywords = ""


    def _get_id(self, html : str) -> str:
        """Return the docbook ID of the current section.

        The value of the first a-element's name attribute is assumed to be the docbook ID.

        Args:
            html (str): The HTML snippet to get the next docbook ID from

        Returns:
            (str): The next ID found in the snippet
        """
        db_id = html[html.find("<a name=\"")+9:]
        db_id = db_id[:db_id.find("\"")]
        return db_id


    def _get_name(self, html : str) -> str:
        """Return the name of the current section.

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


    def _get_title(self, html : str) -> str:
        """Return the name of the current section.

        Args:
            html (str): The HTML snippet to get the next name from

        Returns:
            (str): The next name found in the snippet
        """
        name = html[html.find("<title>")+7:]
        name = name[:name.find("</title>")]
        name = name.replace("\"", "'")
        name = name.strip()
        return name


    def _write_sections_recursive(self, c : str, fdo_content : io.TextIOWrapper, level : int) -> None:
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
            fdo_content (file): The content output file
            level (int): intendation level
        """
        db_id = self._get_id(c)
        name = self._get_name(c)
        indent = " "*(level*3)
        fdo_content.write(indent + f"<li><a href=\"{db_id}.html\">{name}</a></li>\n")
        self._toc += indent + f"<section title=\"{name}\" ref=\"{db_id}.html\">\n"
        self._keywords += f"   <keyword name=\"{name}\" ref=\"./{db_id}.html\"/>\n"
        subs = c.split(f"<div class=\"sect{level}\">")
        if subs[0].rfind("</div>")>=len(subs[0])-6:
            subs[0] = subs[0][:subs[0].rfind("</div>")]
        for s in self._src_folder:
            subs[0] = subs[0].replace(f"src=\"{s}/", f"src=\"qthelp://{self._app_name}/doc/")
        subs[0] = re.sub(r'<a href="#([^"]*)">([^<]*)</a>', r'<a href="\1.html">\2</a>', subs[0])
        subs[0] = re.sub(r'<a class="ulink" href="#([^"]*)">([^<]*)</a>', r'<a class="ulink" href="\1.html">\2</a>', subs[0])
        subs[0] = "<html><head>" + STYLE + "</head><body>" + subs[0] + "</body></html>"
        with open(self._dst_folder + f"/{db_id}.html", "w", encoding="utf-8") as fdo:
            fdo.write(subs[0])
        if len(subs)>1:
            fdo_content.write(indent + "<ul>\n")
            for i,sub in enumerate(subs):
                if i==0:
                    continue
                sub = sub[:sub.rfind("</div>")]
                for s in self._src_folder:
                    sub = sub.replace(f"src=\"{s}/", f"src=\"qthelp://{self._app_name}/doc/")
                self._write_sections_recursive(sub, fdo_content, level+1)
            fdo_content.write(indent + "</ul>\n")
        self._toc += indent + "</section>\n"


    def _process_single(self) -> None:
        """Processes a single (not chunked) HTML document generated by docbook"""
        # read doc
        with open(self._source) as fdi:
            doc = fdi.read()
        # process document
        with open(f"{self._dst_folder}/toc.html", "w", encoding="utf-8") as fdo_content:
            fdo_content.write("<html><head>" + STYLE + "</head><body>\n")
            chapters = doc.split("<div class=\"chapter\">")
            appendices = chapters[-1].split('<div class="appendix">')
            chapters = chapters[:-1]
            chapters.extend(appendices)
            for c in chapters:
                self._write_sections_recursive(c, fdo_content, 1)
            fdo_content.write("</body></html>\n")


    def _generate_html(self, folder : str) -> int:
        """Generates a chunked HTML document from the source docbook document

        Args:
            folder (str): A (temporary) folder to store the xsltproc output to
        """
        shutil.rmtree(folder, ignore_errors=True)
        #print(f"{os.path.join(self._xslt_path, 'xsltproc')} --stringparam base.dir {folder} chunk_html.xsl {self._source}")
        try:
            result = subprocess.run([os.path.join(self._xslt_path, 'xsltproc'),
                "--stringparam", "base.dir", folder,
                "chunk_html.xsl", self._source], check = True)
        except subprocess.CalledProcessError:
            raise RuntimeError("could not invoke xsltproc...")
        except FileNotFoundError:
            raise RuntimeError("could not invoke xsltproc...")
        if isinstance(result, subprocess.CompletedProcess):
            ret = result.returncode
        else:
            ret = 3
        return ret


    def _process_chunked(self, folder : str) -> None:
        """Processes a the set of HTML documents generated by chunking docbook

        Args:
            folder (str): A (temporary) folder to store the xsltproc output to
        """
        # collect entries
        entries = []
        max_depth = 0
        for file in glob.glob(os.path.join(folder, "*.html")):
            _, filename = os.path.split(file)
            if filename=="index.html":
                continue
            with open(file) as fd:
                html = fd.read()
            title = self._get_title(html)
            tchapter = title.split()[0].split(".")[:-1]
            chapter = [int(x) for x in tchapter]
            max_depth = max(len(chapter), max_depth)
            entries.append([filename, title, chapter])
        # sort entries
        # https://stackoverflow.com/questions/14861843/sorting-chapters-numbers-like-1-2-1-or-1-4-2-4
        def expand_chapter(ch, depth):
            ch = ch + [0,] * (depth - len(ch))
            return ch
        entries.sort(key = lambda x: expand_chapter(x[2], max_depth))
        #
        level = 1
        for ie,e in enumerate(entries):
            filename = e[0]
            title = e[1]
            nlevel = len(e[2])
            while ie!=0 and nlevel<=level:
                indent = " "*(level*3)
                self._toc += indent + "</section>\n"
                level -= 1
            level = nlevel
            indent = " "*(level*3)
            self._toc += indent + f"<section title=\"{title}\" ref=\"{filename}\">\n"
            self._keywords += f"   <keyword name=\"{title}\" ref=\"./{filename}\"/>\n"
        while level>0:
            indent = " "*(level*3)
            self._toc += indent + "</section>\n"
            level -= 1


    def process(self, qhp_template : str) -> None:
        """Performs the conversion"""
        # clear output folder
        #shutil.rmtree(self._dst_folder, ignore_errors=True)
        os.makedirs(self._dst_folder, exist_ok=True)
        # copy images etc.
        for s in self._src_folder:
            files = glob.glob(os.path.join(s, "*.png"))
            files.extend(glob.glob(os.path.join(s, "*.gif")))
            for f in files:
                _, n = os.path.split(f)
                shutil.copy(f, f"{self._dst_folder}/{n}")
        # process
        if os.path.isdir(self._source):
            print(f"Processing chunked HTML output from '{self._source}'")
            self._process_chunked(self._source)
        elif os.path.isfile(self._source):
            if self._source.endswith(".html"):
                print(f"Processing single HTML output from '{self._source}'")
                self._process_single()
            elif self._source.endswith(".xml"):
                print(f"Processing docboook '{self._source}'")
                tmp_dir = "tst1" # tempfile.TemporaryDirectory()
                print("... generating chunked HTML")
                ret = self._generate_html(tmp_dir)
                if ret!=0:
                    raise ValueError(f"xsltproc failed with ret={ret}")
                print("... processing chunked HTML")
                self._process_chunked(tmp_dir)
            else:
                raise ValueError(f"unsupported file extension of '{self._source}'")
        else:
            raise ValueError(f"unknown file '{self._source}'")
        # read template, write extended by collected data
        if qhp_template is None:
            qhp_template = TEMPLATE
        path = f"{self._dst_folder}/{self._app_name}"
        with open(path + ".qhp", "w", encoding="utf-8") as fdo:
            fdo.write(qhp_template.replace("%toc%", self._toc).replace("%keywords%", self._keywords).replace("%appname%", self._app_name))
        # generate qhcp
        with open(path + ".qhcp", "w", encoding="utf-8") as fdo:
            fdo.write(QCHP.replace("%appname%", self._app_name))
        # generate QtHelp
        os.system(f"{self._qt_path}/qhelpgenerator {path}.qhp -o {path}.qch")
        os.system(f"{self._qt_path}/qcollectiongenerator {path}.qhcp -o {path}.qhc")


def main(arguments : List[str] = None) -> int:
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
    # parse options
    # https://stackoverflow.com/questions/3609852/which-is-the-best-way-to-allow-configuration-options-be-overridden-at-the-comman
    defaults = {}
    conf_parser = argparse.ArgumentParser(prog='db2qthelp', add_help=False)
    conf_parser.add_argument("-c", "--config", metavar="FILE", help="Reads the named configuration file")
    args, remaining_argv = conf_parser.parse_known_args(arguments)
    if args.config is not None:
        if not os.path.exists(args.config):
            print (f"db2qthelp: error: configuration file '{str(args.config)}' does not exist", file=sys.stderr)
            raise SystemExit(2)
        config = configparser.ConfigParser()
        config.read([args.config])
        defaults.update(dict(config.items("db2qthelp")))
    parser = argparse.ArgumentParser(prog='db2qthelp', parents=[conf_parser],
        description="a DocBook book to QtHelp project converter",
        epilog='(c) Daniel Krajzewicz 2022-2025')
    parser.add_argument("-i", "--input", dest="input", default=None, help="Defines the DocBook HTML document to parse")
    parser.add_argument("-f", "--files", dest="files", default="user_images", help="Sets the folder to collect files from")
    parser.add_argument("-d", "--destination", dest="destination", default="qtdoc", help="Sets the output folder")
    parser.add_argument("-t", "--template", dest="template", default=None, help="Defines the QtHelp project template to use")
    parser.add_argument("-a", "--appname", dest="appname", default="na", help="Sets the name of the application")
    parser.add_argument("-g", "--generate", dest="generate", action="store_true", default=False, help="If set, a template is generated")
    parser.add_argument("-q", "--qt-path", dest="qt_path", default="", help="Sets the path to the Qt binaries")
    parser.add_argument("-x", "--xslt-path", dest="xslt_path", default="", help="Sets the path to xsltproc")
    parser.add_argument('--version', action='version', version='%(prog)s 0.2.0')
    parser.set_defaults(**defaults)
    args = parser.parse_args(remaining_argv)
    # - generate the template and quit, if wished
    if args.generate:
        template_name = args.template if args.template is not None else "template.qhp"
        with open(template_name, "w", encoding="utf-8") as fdo:
            fdo.write(TEMPLATE)
        print (f"Written qhp template to '{args.template}'")
        sys.exit(0)
    # check
    errors = []
    if args.input is None:
        errors.append("no input file given (use -i <HTML_DOCBOOK>)...")
    elif os.path.isfile(args.input) and (not args.input.endswith(".html") and not args.input.endswith(".xml")):
        errors.append("unrecognized input extension '{os.path.splitext(args.input)[1]}'")
    elif not os.path.exists(args.input):
        errors.append(f"did not find input '{args.input}'")
    if args.template is not None and not os.path.exists(args.template):
        errors.append(f"did not find template file '{args.template}'; you may generate one using the option -g")
    if len(errors)!=0:
        for e in errors:
            print(f"db2qthelp: error: {e}", file=sys.stderr)
        raise SystemExit(2)
    # get settings
    if args.template is not None:
        with open(args.template) as fdi:
            template = fdi.read()
    else:
        template = TEMPLATE
    src_folder = [v.replace("\\", "/") for v in args.files.split(",")]
    src_folder.sort(key=lambda t: len(t), reverse=True)
    # process
    ret = 0
    db2qthelp = Db2QtHelp(args.qt_path, args.xslt_path, args.input, src_folder, args.destination, args.appname)
    try:
        db2qthelp.process(template)
    except Exception as e:
        print(f"db2qthelp: error: {str(e)}", file=sys.stderr)
        ret = 2
    return ret


def script_run() -> int:
    """Execute from command line."""
    sys.exit(main(sys.argv[1:])) # pragma: no cover


# -- main check
if __name__ == '__main__':
    main(sys.argv[1:]) # pragma: no cover

