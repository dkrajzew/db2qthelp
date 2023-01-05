<xsl:stylesheet 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:fo="http://www.w3.org/1999/XSL/Format"
  version="1.0">
<xsl:import
  href="../../foreign/docbook/docbook-xsl-1.78.1/html/docbook.xsl"/>
  
<xsl:param name="local.l10n.xml" select="document('')"/> 

<l:i18n xmlns:l="http://docbook.sourceforge.net/xmlns/l10n/1.0">
  <l:l10n language="en"> 
    <l:context name="title-numbered"> 
      <l:template name="chapter" text="%n.&#160;%t "/> 
    </l:context>    
  </l:l10n>
</l:i18n>
<xsl:param name="chapter.autolabel" select="1"/> 
<xsl:param name="section.autolabel" select="1"/> 
<xsl:param name="section.label.includes.component.label" select="1"/> 
<xsl:param name="component.label.includes.part.label" select="1"/> 
<xsl:param name="label.from.part" select="1"/> 
<xsl:param name="use.extensions" select="0"/> 
<xsl:param name="blurb.on.titlepage.enabled" select="0"/> 
<xsl:param name="toc.section.depth" select="1"/>
<xsl:param name="ulink.show" select="0"/>
<xsl:param name="ulink.target" select="new"/>
<xsl:param name="ulink.footnotes" select="1"/>
<xsl:attribute-set name="xref.properties">
  <xsl:attribute name="color">
    <xsl:choose>
      <xsl:when test="self::ulink">blue</xsl:when>
      <xsl:otherwise>inherit</xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
  <xsl:attribute name="text-decoration">
    <xsl:choose>
      <xsl:when test="self::ulink">underline</xsl:when>
      <xsl:otherwise>inherit</xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
</xsl:attribute-set>

  
<xsl:param name="generate.toc">
appendix  title
article/appendix  nop
article   nop
book      toc,title
chapter   nop
part      nop
preface   nop
qandadiv  nop
qandaset  nop
reference toc,title
sect1     nop
sect2     nop
sect3     nop
sect4     nop
sect5     nop
section   nop
set       toc,title
</xsl:param>
</xsl:stylesheet>
