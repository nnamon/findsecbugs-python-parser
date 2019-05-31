#!/usr/bin/env python

import xml.etree.ElementTree as ET

class ReportParser:

    def __init__(self, root):
        self.root = root
        self.initialise(root)

    def initialise(self, root):
        bugreport_proto = self.init_attribs(root.attrib)

        project = self.init_project(root)
        bugreport_proto.set_project(project)

        buginstances = self.init_buginstances(root)
        bugreport_proto.set_buginstances(buginstances)

        errors = self.init_errors(root)
        bugreport_proto.set_errors(errors)

        bugssummary = self.init_findbugssummary(root)
        bugreport_proto.set_findbugssummary(bugssummary)

        classfeatures = self.init_classfeatures(root)
        bugreport_proto.set_classfeatures(classfeatures)

        history = self.init_history(root)
        bugreport_proto.set_history(history)

        self.bugreport = bugreport_proto

    def init_attribs(self, attribs):
        version = attribs.get('version', 'N/A')
        sequence = attribs.get('sequence', 'N/A')
        timestamp = attribs.get('timestamp', 'N/A')
        analysisTimestamp = attribs.get('analysisTimestamp', 'N/A')
        release = attribs.get('release', 'N/A')
        bc = BugCollection(version, sequence, timestamp, analysisTimestamp, release)
        return bc

    def init_project(self, root):
        project = root.find('Project')
        if project is None:
            return None

        project_proto = Project(project)
        return project_proto

    def init_buginstances(self, root):
        buginstances = root.findall('BugInstance')
        buginstances_proto = []
        for i in buginstances:
            buginstances_proto.append(BugInstance(i))
        return buginstances_proto

    def init_errors(self, root):
        errors = root.find('Errors')
        if errors is None:
            return None

        errors_proto = Errors(errors)
        return errors_proto

    def init_findbugssummary(self, root):
        bs = root.find('FindBugsSummary')
        if bs is None:
            return None

        bs_proto = FindBugsSummary(bs)
        return bs_proto

    def init_classfeatures(self, root):
        classfeatures = root.find('ClassFeatures')
        if classfeatures is None:
            return None

        classfeatures_proto = ClassFeatures(classfeatures)
        return classfeatures_proto

    def init_history(self, root):
        history = root.find('History')
        if history is None:
            return None

        history_proto = History(history)
        return history_proto

    @staticmethod
    def parse_string(xml_data):
        return ReportParser(ET.fromstring(xml_data))

    @staticmethod
    def parse_file(xml_file):
        return ReportParser(ET.parse(xml_file).getroot())


class BugCollection:

    def __init__(self, version, sequence, timestamp, analysisTimestamp, release):
        self.version = version
        self.sequence = sequence
        self.timestamp = timestamp
        self.analysisTimestamp = analysisTimestamp
        self.release = release

    def set_project(self, project):
        self.project = project

    def set_buginstances(self, buginstances):
        self.buginstances = buginstances

    def set_errors(self, errors):
        self.errors = errors

    def set_findbugssummary(self, findbugssummary):
        self.findbugssummary = findbugssummary

    def set_classfeatures(self, classfeatures):
        self.classfeatures = classfeatures

    def set_history(self, history):
        self.history = history

class Project:

    def __init__(self, project_root):
        self.project_name = project_root.attrib.get('projectName', 'N/A')
        jar_element = project_root.find('Jar')
        self.jar = jar_element.text
        plugin_element = project_root.find('Plugin')
        self.plugin = plugin_element.attrib

class BugInstance:

    def __init__(self, bi_root):
        pass

class Errors:

    def __init__(self, errors_root):
        pass

class FindBugsSummary:

    def __init__(self, bs_root):
        pass

class ClassFeatures:

    def __init__(self, cf_root):
        pass

class History:

    def __init__(self, history_root):
        pass
