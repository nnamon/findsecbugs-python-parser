#!/usr/bin/env python

import xml.etree.ElementTree as ET

class ReportParser:

    def __init__(self, root):
        self.root = root
        self.initialise(root)

    def initialise(self, root):
        self.init_attribs(root.attrib)
        self.init_project(root)
        self.init_buginstances(root)
        self.init_errors(root)
        self.init_findbugssummary(root)
        self.init_classfeatures(root)
        self.init_history(root)

    def init_attribs(self, attribs):
        self.version = attribs.get('version', 'N/A')
        self.sequence = attribs.get('sequence', 'N/A')
        self.timestamp = attribs.get('timestamp', 'N/A')
        self.analysisTimestamp = attribs.get('analysisTimestamp', 'N/A')
        self.release = attribs.get('release', 'N/A')

    def init_project(self, root):
        pass

    def init_buginstances(self, root):
        pass

    def init_errors(self, root):
        pass

    def init_findbugssummary(self, root):
        pass

    def init_classfeatures(self, root):
        pass

    def init_history(self, root):
        pass

    @staticmethod
    def parse_string(xml_data):
        return ReportParser(ET.fromstring(xml_data))

    @staticmethod
    def parse_file(xml_file):
        return ReportParser(ET.parse(xml_file).getroot())


class BugCollection:
    pass

class Project:
    pass

class BugInstance:
    pass

class Errors:
    pass

class FindBugsSummary:
    pass

class ClassFeatures:
    pass

class History:
    pass
