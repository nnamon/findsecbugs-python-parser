#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from collections import OrderedDict


class ReportParser:

    def __init__(self, root):
        self.root = root
        self.initialise(root)

    def initialise(self, root):
        bugcollection_proto = self.init_attribs(root.attrib)

        project = self.init_project(root)
        bugcollection_proto.set_project(project)

        buginstances = self.init_buginstances(root)
        bugcollection_proto.set_buginstances(buginstances)

        errors = self.init_errors(root)
        bugcollection_proto.set_errors(errors)

        bugssummary = self.init_findbugssummary(root)
        bugcollection_proto.set_findbugssummary(bugssummary)

        classfeatures = self.init_classfeatures(root)
        bugcollection_proto.set_classfeatures(classfeatures)

        history = self.init_history(root)
        bugcollection_proto.set_history(history)

        self.bugcollection = bugcollection_proto

    def init_attribs(self, attribs):
        version = attribs.get('version', 'N/A')
        sequence = int(attribs.get('sequence', -1))
        timestamp = int(attribs.get('timestamp', -1))
        analysisTimestamp = int(attribs.get('analysisTimestamp', -1))
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
        attribs = bi_root.attrib
        self.type = attribs.get('type', 'N/A')
        self.priority = attribs.get('priority', 'N/A')
        self.rank = attribs.get('rank', 'N/A')
        self.abbrev = attribs.get('abbrev', 'N/A')
        self.category = attribs.get('category', 'N/A')

        self.strings = OrderedDict()
        string_elements = bi_root.findall('String')
        for i in string_elements:
            role = i.attrib.get('role')
            value = i.attrib.get('value')
            self.strings[role] = value

        bug_class_element = bi_root.find('Class')
        self.bug_class = BugClass(bug_class_element)

        bug_method_element = bi_root.find('Method')
        self.bug_method = BugMethod(bug_method_element)

        self.sourcelines = SourceLines(bi_root)


class BugClass:

    def __init__(self, bc_root):
        pass


class BugMethod:

    def __init__(self, bm_root):
        pass


class SourceLines:

    def __init__(self, root):
        sourceline_elements = root.findall('SourceLine')
        self.lines = []
        for i in sourceline_elements:
            self.lines.append(SourceLine(i))


class SourceLine:

    def __init__(self, sl_root):
        attribs = sl_root.attrib
        self.classname = attribs.get('classname', 'N/A')
        self.start = int(attribs.get('start', -1))
        self.end = int(attribs.get('end', -1))
        self.startBytecode = int(attribs.get('startBytecode', -1))
        self.endBytecode = int(attribs.get('endBytecode', -1))
        self.sourcefile = attribs.get('sourcefile', 'N/A')
        self.sourcepath = attribs.get('sourcepath', 'N/A')


class Errors:

    def __init__(self, errors_root):
        attribs = errors_root.attrib
        self.num_errors = int(attribs.get('errors', 0))
        self.num_missingclasses = int(attribs.get('missingClasses', 0))
        self.errors = []
        for i in errors_root.findall('Error'):
            pass  # TODO: Populate the error list.
        self.missingclasses = []
        for i in errors_root.findall('MissingClass'):
            self.missingclasses.append(i.text)


class FindBugsSummary:

    def __init__(self, bs_root):
        attribs = bs_root.attrib
        self.timestamp = attribs.get('timestamp', 'N/A')
        self.total_classes = attribs.get('total_classes', 'N/A')
        self.referenced_classes = attribs.get('referenced_classes', 'N/A')
        self.total_bugs = attribs.get('total_bugs', 'N/A')
        self.total_size = attribs.get('total_size', 'N/A')
        self.num_packages = attribs.get('num_packages', 'N/A')
        self.java_version = attribs.get('java_version', 'N/A')
        self.vm_version = attribs.get('vm_version', 'N/A')
        self.cpu_seconds = attribs.get('cpu_seconds', 'N/A')
        self.clock_seconds = attribs.get('clock_seconds', 'N/A')
        self.peak_mbytes = attribs.get('peak_mbytes', 'N/A')
        self.alloc_mbytes = attribs.get('alloc_mbytes', 'N/A')
        self.gc_seconds = attribs.get('gc_seconds', 'N/A')
        self.priority_2 = attribs.get('priority_2', 'N/A')
        self.priority_1 = attribs.get('priority_1', 'N/A')

        self.packagestats = []
        packagestat_elements = bs_root.findall('PackageStats')
        for i in packagestat_elements:
            self.packagestats.append(PackageStats(i))

        fbp_element = bs_root.find('FindBugsProfile')
        self.findbugsprofile = FindBugsProfile(fbp_element)


class PackageStats:

    def __init__(self, ps_root):
        attribs = ps_root.attrib
        self.package = attribs.get('package', 'N/A')
        self.total_bugs = attribs.get('total_bugs', 'N/A')
        self.total_types = attribs.get('total_types', 'N/A')
        self.total_size = attribs.get('total_size', 'N/A')

        self.classstats = []
        classstats_elements = ps_root.findall('ClassStats')
        for i in classstats_elements:
            self.classstats.append(ClassStats(i))


class ClassStats:

    def __init__(self, cs_root):
        attribs = cs_root.attrib
        self.class_name = attribs.get('class', 'N/A')
        self.source_file = attribs.get('sourceFile', 'N/A')
        self.interface = attribs.get('interface', 'N/A')
        self.size = int(attribs.get('size', -1))
        self.bugs = int(attribs.get('bugs', -1))


class FindBugsProfile:

    def __init__(self, profile_root):
        self.classprofiles = []
        classprofile_elements = profile_root.findall('ClassProfile')
        for i in classprofile_elements:
            self.classprofiles.append(ClassProfile(i))


class ClassProfile:

    def __init__(self, cp_root):
        attribs = cp_root.attrib
        self.name = attribs.get('name', 'N/A')
        self.totalMilliseconds = int(attribs.get('totalMilliseconds', -1))
        self.invocations = int(attribs.get('invocations', -1))
        self.avgMicrosecondsPerInvocation = int(attribs.get('avgMicrosecondsPerInvocation', -1))
        self.maxMicrosecondsPerInvocation = int(attribs.get('maxMicrosecondsPerInvocation', -1))
        self.standardDeviationMicrosecondsPerInvocation = int(attribs.get(
            'standardDeviationMicrosecondsPerInvocation', -1))


class ClassFeatures:

    def __init__(self, cf_root):
        # TODO: Not implemented yet since the samples leave the property empty.
        pass


class History:

    def __init__(self, history_root):
        # TODO: Not implemented yet since the samples leave the property empty.
        pass
