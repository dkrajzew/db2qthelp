Release Steps
=============

* check the [ChangeLog](https://github.com/dkrajzew/db2qthelp/blob/master/CHANGES.md)
* patch the release number and the copyright information in
  * the [README.md](https://github.com/dkrajzew/db2qthelp/blob/master/README.md) file
  * the blog pages
  * the [setup.py](https://github.com/dkrajzew/db2qthelp/blob/master/setup.py) file
  * the scripts and tests
* run the tests (run build_docs.bat)
* build the pydoc documentation, copy it to the web pages
* commit changes
* build the github release (tag: &lt;VERSION&gt;, name: db2qthelp-&lt;VERSION&gt;)
* build the PyPI release (run build_release.bat)
