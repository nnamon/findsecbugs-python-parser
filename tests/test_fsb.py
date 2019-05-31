#!/usr/bin/env python

from __future__ import unicode_literals
from findsecbugs_parser.fsb import ReportParser
from distutils import dir_util
from pytest import fixture
import os


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

@fixture
def samplehtml(datadir):
    sample_report_fd = datadir.join('sample_report.html')
    return sample_report_fd.read()

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

def test_reportparser(parsedreport):
    obj = parsedreport
    assert obj is not None
