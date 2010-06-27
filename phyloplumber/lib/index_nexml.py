#!/usr/bin/python
from dendropy.utility.ElementTree import _escape_attrib


def new_index(project_name, description='')
    if description:
        d_str = '<meta id="a1" datatype="xsd:string" xsi:type="nex:LiteralMeta" property="phyp:projectName" content="%(n)s"/>' % {'n' : _escape_attrib(description)}
    else:
        d_str = ''
    n_str = '<meta id="a1" datatype="xsd:string" xsi:type="nex:LiteralMeta" property="phyp:projectName" content="%(n)s"/>' % {'n' : project_name}
    return '\n'.join([_NEXML_HEADER, n_str, d_str, _NEXML_FOOTER])

_NEXML_HEADER = '''<?xml version="1.0"?>
<nex:nexml 
    version="0.9" 
    xsi:schemaLocation="http://www.nexml.org/2009 ../xsd/nexml.xsd"
    xmlns:nex="http://www.nexml.org/2009" 
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
    xmlns:xml="http://www.w3.org/XML/1998/namespace" 
    xmlns:xsd="http://www.w3.org/2001/XMLSchema#" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:cdao="http://www.evolutionaryontology.org/cdao.owl#"
    xmlns:phyp="http://github.com/mtholder/phyloplumber/xsd/2010"
    xmlns="http://www.nexml.org/2009">
'''

_NEXML_FOOTER = '''</nex:nexml>'''
