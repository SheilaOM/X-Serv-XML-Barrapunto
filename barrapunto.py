#!/usr/bin/python3
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import os.path


class myContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.titulo = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = self.theContent
                fich.write("\t\t\t<li><a href='" + self.link + "'>" +
                           self.titulo + "</a></li>\n")
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog
if len(sys.argv) < 2:
    print("Usage: python xml-parser-barrapunto.py <document>")
    print("")
    print(" <document>: file name of the document to parse")
    sys.exit(1)

# Load parser and driver
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
global fich
if os.path.exists("barrapunto.html"):
    fich = open("barrapunto.html", "w")
else:
    fich = open("barrapunto.html", "a")

fich.write("<html>\n\t<head>\n\t\t<meta http-equiv='Content-Type'" +
           "content='text/html; charset=utf-8'/>" +
           "\n\t</head>\n\t<body>\n\t\t<ul>\n")

xmlFile = open(sys.argv[1], "r")
theParser.parse(xmlFile)

fich.write("\t\t</ul>\n\t</body>\n</html>")

print("Parse complete")
