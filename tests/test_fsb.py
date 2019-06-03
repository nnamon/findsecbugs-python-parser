#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from distutils import dir_util

from findsecbugs_parser.fsb import (BugClass, BugCollection, BugInstance,
                                    BugMethod, ClassFeatures, Errors,
                                    FindBugsProfile, FindBugsSummary, History,
                                    PackageStats, Project, ReportParser)
from pytest import fixture


@fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


@fixture
def samplexml(datadir):
    sample_report_fd = datadir.join('sample_report.xml')
    return sample_report_fd.read()

# @fixture
# def samplehtml(datadir):
#    sample_report_fd = datadir.join('sample_report.html')
#    return sample_report_fd.read()


@fixture
def parsedreport(samplexml):
    return ReportParser.parse_string(samplexml)


@fixture
def parsedreport_path(datadir):
    sample_report_fd = datadir.join('sample_report.xml')
    return str(sample_report_fd)


def test_reportparser_fromstring(parsedreport):
    assert parsedreport is not None


def test_reportparser_fromfile(parsedreport_path):
    frompath = ReportParser.parse_file(parsedreport_path)
    assert frompath is not None


def test_reportparser_instantiation(parsedreport):
    obj = parsedreport
    assert obj is not None


def test_reportparser_parsed_bugcollection(parsedreport):
    assert parsedreport.bugcollection is not None
    assert type(parsedreport.bugcollection) is BugCollection
    bc = parsedreport.bugcollection
    assert bc.version == '3.1.5'
    assert bc.sequence == 0
    assert bc.timestamp == 1559244040000
    assert bc.analysisTimestamp == 1559244097257
    assert bc.release == ''


def test_reportparser_parsed_project(parsedreport):
    assert parsedreport.bugcollection.project is not None
    assert type(parsedreport.bugcollection.project) is Project
    project = parsedreport.bugcollection.project
    assert project.project_name == ''
    assert project.jar == '/Users/amon/sproink/guacamole/guacamole-1.0.0.war'
    assert type(project.plugin) is dict
    assert len(project.plugin.keys()) == 2
    assert project.plugin['id'] == 'com.h3xstream.findsecbugs'
    assert project.plugin['enabled'] == 'true'


def test_reportparser_parsed_errors(parsedreport):
    assert parsedreport.bugcollection.errors is not None
    assert type(parsedreport.bugcollection.errors) is Errors
    errors = parsedreport.bugcollection.errors
    assert errors.num_errors == 0


def test_reportparser_parsed_findbugssummary(parsedreport):
    assert parsedreport.bugcollection.findbugssummary is not None
    assert type(parsedreport.bugcollection.findbugssummary) is FindBugsSummary
    bs = parsedreport.bugcollection.findbugssummary
    assert len(bs.packagestats) > 0
    assert False not in [type(i) == PackageStats for i in bs.packagestats]
    assert type(bs.findbugsprofile) == FindBugsProfile


def test_reportparser_parsed_classfeatures(parsedreport):
    assert parsedreport.bugcollection.classfeatures is not None
    assert type(parsedreport.bugcollection.classfeatures) is ClassFeatures
    # errors = parsedreport.bugcollection.classfeatures


def test_reportparser_parsed_history(parsedreport):
    assert parsedreport.bugcollection.history is not None
    assert type(parsedreport.bugcollection.history) is History
    # errors = parsedreport.bugcollection.history


def test_reportparser_parsed_buginstances(parsedreport):
    assert parsedreport.bugcollection.buginstances is not None
    assert type(parsedreport.bugcollection.buginstances) is list
    bi = parsedreport.bugcollection.buginstances
    assert len(bi) > 0
    assert False not in (type(bi_item) is BugInstance for bi_item in bi)
    bi_item = bi[0]
    assert bi_item.type is not None
    assert bi_item.priority is not None
    assert bi_item.rank is not None
    assert bi_item.abbrev is not None
    assert bi_item.category is not None
    assert bi_item.strings is not None
    assert bi_item.bug_class is not None
    assert bi_item.bug_method is not None
    assert bi_item.sourcelines is not None


def test_reportparsed_parsed_bugclass(parsedreport):
    bi_item = parsedreport.bugcollection.buginstances[0]
    bc = bi_item.bug_class
    assert type(bc) is BugClass
    assert bc.classname is not None
    assert bc.sourcelines is not None


def test_reportparsed_parsed_bugmethod(parsedreport):
    bi_item = parsedreport.bugcollection.buginstances[0]
    bm = bi_item.bug_method
    assert type(bm) is BugMethod
    assert bm.classname is not None
    assert bm.name is not None
    assert bm.signature is not None
    assert bm.isStatic is not None
    assert bm.sourcelines is not None
