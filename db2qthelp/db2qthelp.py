#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""db2qthelp - a DocBook book to QtHelp project converter"""
# ===========================================================================
__author__     = "Daniel Krajzewicz"
__copyright__  = "Copyright 2022-2025, Daniel Krajzewicz"
__credits__    = ["Daniel Krajzewicz"]
__license__    = "GPLv3"
__version__    = "0.4.0"
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
import subprocess
from typing import List, Set, Tuple


# --- variables and constants -----------------------------------------------
CSS_DEFINITION = """body {
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
"""

QHP_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
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
    def __init__(self, qt_path : str, xsltproc_path : str, css_definition : str, qhp_template : str):
        """Contructor

        Args:
            qt_path (str): Path to the Qt binaries
            xsltproc_path (str): Path to the xsltproc binary
            css_definition (str): CSS definition to use
            qhp_template (str): Template for the .qhp file
        """
        self._qt_path = qt_path
        self._xsltproc_path = xsltproc_path
        self._css_definition = css_definition if css_definition is not None else CSS_DEFINITION
        self._css_definition = "\n<style>\n" + self._css_definition + "</style>\n"
        self._qhp_template = qhp_template if qhp_template is not None else QHP_TEMPLATE


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


    def patch_links(self, doc : str, app_name : str, files : Set[str]) -> str:
        """Extracts references to images; patches links to point to main document folder

        Args:
            doc (str): The HTML document to process
            app_name (str): The application name
            files (Set[str]): The container to store links into

        Returns:
            (str): The changed document
        """
        srcs = re.findall(r'src\s*=\s*"(.+?)"', doc)
        seen = set()
        for src in srcs:
            filename = os.path.split(src)[1]
            if filename in seen:
                continue
            seen.add(filename)
            nsrc = f"qthelp://{app_name}/doc/{filename}"
            doc = doc.replace(src, nsrc)
            files.add(src)
        return doc


    def _write_sections_recursive(self, html : str, dst_folder : str, pages : List[Tuple[str, str]], level : int) -> None:
        """Writes the given section and it's sub-sections recursively.

        The id and the name of the section are retrieved, first.

        Then, the toc HTML file is extended and the reference to this section is
        appended to the returned toc. Keywords are extended by the section's name.

        The section is then split along the
        '&lt;div class="sect&lt;INDENT&gt;"&gt;' elements which are processed
        recursively.

        The (recursively) collected keywords and toc are returned.

        Args:
            html (str): The (string) content of the DocBook book section or appendix
            dst_folder (str): The folder to write the section into
            pages (List[Tuple[str, str]]): The list of HTML sections to fill
            level (int): intendation level
        """
        db_id = self._get_id(html)
        name = self._get_name(html)
        pages.append([f"{db_id}.html", name])
        subs = html.split(f"<div class=\"sect{level}\">")
        if subs[0].rfind("</div>")>=len(subs[0])-6:
            subs[0] = subs[0][:subs[0].rfind("</div>")]
        # patch links (convert links to anchors, to the proper links to split pages)
        subs[0] = re.sub(r'<a href="#([^"]*)">([^<]*)</a>', r'<a href="\1.html">\2</a>', subs[0])
        subs[0] = re.sub(r'<a class="ulink" href="#([^"]*)">([^<]*)</a>', r'<a class="ulink" href="\1.html">\2</a>', subs[0])
        # write the document part as document
        subs[0] = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>' + self._css_definition + "</head><body>" + subs[0] + "</body></html>"
        with open(dst_folder + f"/{db_id}.html", "w", encoding="utf-8") as fdo:
            fdo.write(subs[0])
        if len(subs)>1:
            for i,sub in enumerate(subs):
                if i==0:
                    continue
                sub = sub[:sub.rfind("</div>")]
                self._write_sections_recursive(sub, dst_folder, pages, level+1)


    def _process_single(self, source : str, dst_folder : str, pages : List[Tuple[str, str]], files : Set[str], app_name : str) -> None:
        """Processes a single (not chunked) HTML document generated by docbook

        Args:
            source (str): The HTML document to process
            dst_folder (str): The folder to write the section into
            pages (List[Tuple[str, str]]): The list of HTML sections to fill
            files (Set[str]): The set of referenced files (images) to fill
            app_name (str): The application name
        """
        # read doc
        with open(source, encoding="utf-8") as fdi:
            doc = fdi.read()
        doc = self.patch_links(doc, app_name, files)
        # process document
        chapters = doc.split("<div class=\"chapter\">")
        appendices = chapters[-1].split('<div class="appendix">')
        chapters = chapters[:-1]
        chapters.extend(appendices)
        for c in chapters:
            self._write_sections_recursive(c, dst_folder, pages, 1)


    def _generate_html(self, source : str, folder : str) -> int:
        """Generates a chunked HTML document from the source docbook document

        Args:
            source (str): The XML DocBook document to process
            folder (str): A (temporary) folder to store the xsltproc output to
        """
        shutil.rmtree(folder, ignore_errors=True)
        chunk_xsl_path = os.path.join(os.path.split(__file__)[0], "data", "chunk_html.xsl")
        try:
            result = subprocess.run([os.path.join(self._xsltproc_path, 'xsltproc'),
                "--stringparam", "base.dir", folder,
                chunk_xsl_path, source], check = True)
        except subprocess.CalledProcessError:
            raise RuntimeError("could not invoke xsltproc...")
        except FileNotFoundError:
            raise RuntimeError("could not invoke xsltproc...")
        if isinstance(result, subprocess.CompletedProcess):
            ret = result.returncode
        else:
            ret = 3
        return ret


    def _process_chunked(self, folder : str, pages : List[Tuple[str, str]], files : Set[str], app_name : str, dst_folder) -> None:
        """Processes a the set of HTML documents generated by chunking docbook

        Args:
            folder (str): A (temporary) folder to store the xsltproc output to
            pages (List[Tuple[str, str]]): The list of HTML sections to fill
            files (Set[str]): The set of referenced files (images) to fill
            app_name (str): The application name
        """
        # collect entries
        for file in glob.glob(os.path.join(folder, "*.html")):
            _, filename = os.path.split(file)
            if filename=="index.html":
                continue
            with open(file, encoding="utf-8") as fd:
                html = fd.read()
            html = self.patch_links(html, app_name, files)
            if html.find('content="text/html; charset=">')>=0:
                html = html.replace('content="text/html; charset=">', 'content="text/html; charset=UTF-8">')
            title_end = html.find("</title>") + 8
            html = html[:title_end] + self._css_definition + html[title_end:]
            title = self._get_title(html)
            pages.append([filename, title])
            _, filename = os.path.split(file)
            with open(os.path.join(dst_folder, filename), "w", encoding="utf-8") as fd:
                fd.write(html)


    def _copy_files(self, files : Set[str], source : str, dst_folder : str) -> None:
        """Copies referenced files into the destination folder

        Args:
            files (Set[str]): The files to compy
            source (str): The origin folder
            dst_folder (str): The destination folder
        """
        base_path = source if os.path.isdir(source) else os.path.split(source)[0]
        for file in files:
            _, filename = os.path.split(file)
            shutil.copy(os.path.join(base_path, file), f"{dst_folder}/{filename}")


    def build_toc_sections(self, pages : List[Tuple[str, str, List[int]]]) -> str:
        """Generates a hierarchical list of pages to be embedded in the toc-section
        of the qhp-file.

        Args:
            pages (List[Tuple[str, str, List[int]]]): The sorted list of pages

        Returns:
            (str): The pages formatted as toc-sections
        """
        toc = ""
        level = 1
        for ie,e in enumerate(pages):
            filename = e[0]
            title = e[1]
            nlevel = len(e[2])
            while ie!=0 and nlevel<=level:
                indent = " "*(level*4+8)
                toc += indent + "</section>\n"
                level -= 1
            level = nlevel
            indent = " "*(level*4+8)
            toc += indent + f"<section title=\"{title}\" ref=\"{filename}\">\n"
        while level>0:
            indent = " "*(level*4+8)
            toc += indent + "</section>\n"
            level -= 1
        return toc


    def process(self, source : str, dst_folder : str, app_name : str) -> None:
        """Performs the conversion

        Args:
            source (str): The input file or folder
            dst_folder (str): The destination folder (where the documentation is built)
            app_name (str): The name of the application
        """
        # clear output folder
        shutil.rmtree(dst_folder, ignore_errors=True)
        os.makedirs(dst_folder, exist_ok=True)
        # process
        pages = []
        files = set()
        if os.path.isdir(source):
            print(f"Processing chunked HTML output from '{source}'")
            self._process_chunked(source, pages, files, app_name, dst_folder)
        elif os.path.isfile(source):
            if source.endswith(".html"):
                print(f"Processing single HTML output from '{source}'")
                self._process_single(source, dst_folder, pages, files, app_name)
            elif source.endswith(".xml"):
                print(f"Processing docboook '{source}'")
                tmp_dir = "_tmp_db2qthelp_dir"
                os.makedirs(tmp_dir, exist_ok=True)
                print("... generating chunked HTML")
                ret = self._generate_html(source, tmp_dir)
                if ret!=0:
                    raise ValueError(f"xsltproc failed with ret={ret}")
                print("... processing chunked HTML")
                self._process_chunked(tmp_dir, pages, files, app_name, dst_folder)
                shutil.rmtree(tmp_dir, ignore_errors=True)
            else:
                raise ValueError(f"unsupported file extension of '{source}'")
        else:
            raise ValueError(f"unknown file '{source}'")
        # copy images etc.
        self._copy_files(files, source, dst_folder)
        # sort pages
        # https://stackoverflow.com/questions/14861843/sorting-chapters-numbers-like-1-2-1-or-1-4-2-4
        def expand_chapter(ch, depth):
            ch = ch + [0,] * (depth - len(ch))
            return ch
        max_depth = 0
        for page in pages:
            if page[1][0]=='A':
                chapter = [ord(page[1].split()[1][0]) + 1000]
            else:
                chapter = [int(x) for x in page[1].split()[0].split(".")[:-1]]
            if len(chapter)==0:
                chapter = [0]
            page.append(chapter)
            max_depth = max(len(chapter), max_depth)
        pages.sort(key = lambda x: expand_chapter(x[2], max_depth))
        #
        toc = self.build_toc_sections(pages)
        keywords = "\n".join(" "*12 + f"<keyword name=\"{page[1]}\" ref=\"./{page[0]}\"/>" for page in pages)
        # read template, write extended by collected data
        path = f"{dst_folder}/{app_name}"
        with open(path + ".qhp", "w", encoding="utf-8") as fdo:
            fdo.write(self._qhp_template.replace("%toc%", toc).replace("%keywords%", keywords).replace("%appname%", app_name))
        # generate qhcp
        with open(path + ".qhcp", "w", encoding="utf-8") as fdo:
            fdo.write(QCHP.replace("%appname%", app_name))
        # generate QtHelp
        os.system(f"{os.path.join(self._qt_path, 'qhelpgenerator')} {path}.qhp -o {path}.qch")
        os.system(f"{os.path.join(self._qt_path, 'qhelpgenerator')} {path}.qhcp -o {path}.qhc")


def main(arguments : List[str] = None) -> int:
    """The main method using parameter from the command line.

    Args:
        arguments (List[str]): A list of command line arguments.

    Returns:
        (int): The exit code (0 for success).
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
    parser.add_argument("-d", "--destination", dest="destination", default="qtdoc", help="Sets the output folder")
    parser.add_argument("-a", "--appname", dest="appname", default="na", help="Sets the name of the application")
    parser.add_argument("--css-definition", dest="css_definition", default=None, help="Defines the CSS definition file to use")
    parser.add_argument("--generate-css-definition", dest="generate_css_definition", action="store_true", default=False, help="If set, a CSS definition file is generated")
    parser.add_argument("--qhp-template", dest="qhp_template", default=None, help="Defines the QtHelp project (.qhp) template to use")
    parser.add_argument("--generate-qhp-template", dest="generate_qhp_template", action="store_true", default=False, help="If set, a QtHelp project (.qhp) template is generated")
    parser.add_argument("-Q", "--qt-path", dest="qt_path", default="", help="Sets the path to the Qt binaries")
    parser.add_argument("-X", "--xslt-path", dest="xslt_path", default="", help="Sets the path to xsltproc")
    parser.add_argument('--version', action='version', version='%(prog)s 0.4.0')
    parser.set_defaults(**defaults)
    args = parser.parse_args(remaining_argv)
    # - generate the css template and quit, if wished
    if args.generate_css_definition:
        template_name = args.css_definition if args.css_definition is not None else "template.css"
        with open(template_name, "w", encoding="utf-8") as fdo:
            fdo.write(CSS_DEFINITION)
        print (f"Written css definition to '{template_name}'")
        sys.exit(0)
    # - generate the qhp template and quit, if wished
    if args.generate_qhp_template:
        template_name = args.qhp_template if args.qhp_template is not None else "template.qhp"
        with open(template_name, "w", encoding="utf-8") as fdo:
            fdo.write(QHP_TEMPLATE)
        print (f"Written qhp template to '{template_name}'")
        sys.exit(0)
    # check
    errors = []
    if args.input is None:
        errors.append("no input file given (use -i <HTML_DOCBOOK>)...")
    elif not os.path.isdir(args.input) and (not args.input.endswith(".html") and not args.input.endswith(".xml")):
        errors.append(f"unrecognized input extension '{os.path.splitext(args.input)[1]}'")
    elif not os.path.exists(args.input):
        errors.append(f"did not find input '{args.input}'")
    if args.qhp_template is not None and not os.path.exists(args.qhp_template):
        errors.append(f"did not find QtHelp project (.qhp) template file '{args.qhp_template}'; you may generate one using the option --generate-qhp-template")
    if args.css_definition is not None and not os.path.exists(args.css_definition):
        errors.append(f"did not find CSS definition file '{args.css_definition}'; you may generate one using the option --generate-css-definition")
    if len(errors)!=0:
        for e in errors:
            print(f"db2qthelp: error: {e}", file=sys.stderr)
        raise SystemExit(2)
    # get settings
    qhp_template = None
    if args.qhp_template is not None:
        with open(args.qhp_template, encoding="utf-8") as fdi:
            qhp_template = fdi.read()
    css_definition = None
    if args.css_definition is not None:
        with open(args.css_definition, encoding="utf-8") as fdi:
            css_definition = fdi.read()
    # process
    ret = 0
    db2qthelp = Db2QtHelp(args.qt_path, args.xslt_path, css_definition, qhp_template)
    try:
        db2qthelp.process(args.input, args.destination, args.appname)
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
