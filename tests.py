#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Red Dove Consultants Limited
#
import argparse
import io
import os
import sys
import unittest

DEBUGGING = 'PY_DEBUG' in os.environ

if not sys.platform.startswith('java'):
    print('This program needs to be run under Jython.')
    sys.exit(1)

from java.nio.file import Paths
from java.util import HashMap
from org.parsers.preprocessor import PreprocessorParser, ParseException

class BaseTest(unittest.TestCase):
    def do_test(self, fn, symbols, csharp_mode, check_expected=True):
        p = os.path.join('testfiles', fn)
        if not symbols:
            mapping = None
        else:
            mapping = symbols
        parser = PreprocessorParser(Paths.get(p), mapping, csharp_mode)
        markers = parser.PP_Root()
        with io.open(p, encoding='utf-8') as f:
            lines = f.read().splitlines()
        result = []
        for i, line in enumerate(lines):
            if markers.get(i + 1):
                result.append(line)
        actual = '\n'.join(result)
        if not check_expected:
            return actual
        p = os.path.join('testfiles', 'expected', fn)
        with io.open(p, encoding='utf-8') as f:
            expected = f.read()
        self.assertEqual(actual, expected)
            
    def test_csgood(self):
        self.do_test('csmode_good.txt', None, True)
        
    def test_csbad(self):
        self.do_test('csmode_bad1.txt', None, False)
        with self.assertRaises(ParseException) as ec:
            self.do_test('csmode_bad1.txt', None, True)
        self.assertEqual(ec.exception.message, 'Symbols cannot have defined values in C# mode.')

    def test_predefined(self):
        d = {'CODELANG': 'python'}
        actual = self.do_test('predefined.txt', d, False, check_expected=False)
        self.assertEqual(actual, 'Should be Python.')
        d = {'CODELANG': 'java'}
        actual = self.do_test('predefined.txt', d, False, check_expected=False)
        self.assertEqual(actual, 'Should be Java.')
        d = {'CODELANG': 'csharp'}
        actual = self.do_test('predefined.txt', d, False, check_expected=False)
        self.assertEqual(actual, 'Should be neither Python nor Java.')

    def test_combined(self):
        d = {'CODELANG': 'python'}
        actual = self.do_test('combined.txt', d, False, check_expected=False)
        self.assertEqual(actual, '1. Should be Python.')
        d = {'CODELANG': 'java'}
        actual = self.do_test('combined.txt', d, False, check_expected=False)
        self.assertEqual(actual, '1. Should be neither Python nor Java.')
        d = {'CODELANG': 'csharp'}
        actual = self.do_test('combined.txt', d, False, check_expected=False)
        self.assertEqual(actual, '1. Should be neither Python nor Java.')


def main():
    adhf = argparse.ArgumentDefaultsHelpFormatter
    ap = argparse.ArgumentParser(formatter_class=adhf)
    aa = ap.add_argument
    # aa('--example', help='Example argument')
    options = ap.parse_args()
    unittest.main()

if __name__ == '__main__':
    try:
        rc = main()
    except KeyboardInterrupt:
        rc = 2
    except Exception as e:
        if DEBUGGING:
            s = ' %s:' % type(e).__name__
        else:
            s = ''
        sys.stderr.write('Failed:%s %s\n' % (s, e))
        if DEBUGGING: import traceback; traceback.print_exc()
        rc = 1
    sys.exit(rc)
