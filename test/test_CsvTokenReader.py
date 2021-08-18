#!/usr/bin/env python3
# coding: utf8
import os, sys, pathlib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.token import CsvTokenReader
import unittest
from unittest.mock import MagicMock, patch, mock_open
import copy
import toml
class TestCsvTokenReader(unittest.TestCase):
    def test_path(self):
        self.assertEqual(os.path.basename(CsvTokenReader().Path), 'token.tsv')
#    @patch('csv.reader')
    @patch('src.token.CsvTokenReader._CsvTokenReader__get_rows')
    def test_get_hit_one_of_one(self, mock_lib):
        domain = 'test.com'
        username = 'test-user'
        scopes = ['read']
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        mock_lib.return_value = [[domain, username, scopes, token]]
        actual = CsvTokenReader().get(domain, username)
        mock_lib.assert_called_once()
        self.assertEqual(actual, token)
#    @patch('csv.reader')
    @patch('src.token.CsvTokenReader._CsvTokenReader__get_rows')
    def test_get_hit_one_of_two(self, mock_lib):
        domain = 'test.com'
        username = 'test-user'
        scopes = ['read']
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        mock_lib.return_value = [
            [domain, username, scopes, token],
            [domain+'2', username+'2', scopes, token+'2'],
        ]
        actual = CsvTokenReader().get(domain, username)
        mock_lib.assert_called_once()
        self.assertEqual(actual, token)
    @patch('csv.reader')
#    @patch('src.token.CsvTokenReader._CsvTokenReader__get_rows')
    def test_get_hit_two_of_two(self, mock_lib):
        domain = 'test.com'
        username = 'test-user'
        scopes = ['read']
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        mock_lib.return_value = [
            [domain, username, scopes, token],
            [domain, username, ['write'], 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'],
        ]
        actual = CsvTokenReader().get(domain, username)
        mock_lib.assert_called_once()
        self.assertEqual(actual, token)
#    @patch('csv.reader')
    @patch('src.token.CsvTokenReader._CsvTokenReader__get_rows')
    def test_get_not_hit_one(self, mock_lib):
        domain = 'test.com'
        username = 'test-user'
        scopes = ['read']
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        mock_lib.return_value = [
            [domain, username, ','.join(scopes), token],
        ]
        actual = CsvTokenReader().get(domain + '2', username)
        mock_lib.assert_called_once()
        self.assertEqual(actual, None)
        actual = CsvTokenReader().get(domain, username + '2')
        self.assertEqual(actual, None)
        actual = CsvTokenReader().get(domain, username, ['write'])
        self.assertEqual(actual, None)
#    @patch('csv.reader')
    @patch('src.token.CsvTokenReader._CsvTokenReader__get_rows')
    def test_get_not_hit_two(self, mock_lib):
        domain = 'test.com'
        username = 'test-user'
        scopes = ['read']
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        mock_lib.return_value = [
            [domain, username, ','.join(scopes), token],
            [domain, username, 'write', 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'],
        ]
        for case in [
            (([domain+'2', username], None), None),
            (([domain, username+'2'], None), None),
            (([domain, username], ['follow']), None),
        ]:
            with self.subTest(args=case[0][0], kwargs=case[0][1], expected=case[1]):
                actual = CsvTokenReader().get(*case[0][0], scopes=case[0][1])
                self.assertEqual(actual, None)
        """
        actual = CsvTokenReader().get(domain + '2', username)
        mock_lib.assert_called_once()
        self.assertEqual(actual, None)
        actual = CsvTokenReader().get(domain, username + '2')
        self.assertEqual(actual, None)
        actual = CsvTokenReader().get(domain, username, ['follow'])
        self.assertEqual(actual, None)
        """

if __name__ == "__main__":
    unittest.main()
