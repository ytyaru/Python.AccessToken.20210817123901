#!/usr/bin/env python3
# coding: utf8
import os, sys, pathlib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.token import TomlTokenReader
import unittest
from unittest.mock import MagicMock, patch, mock_open
import copy
import toml
class TestCsvTokenReader(unittest.TestCase):
    def test_path(self):
        self.assertEqual(os.path.basename(TomlTokenReader().Path), 'token.toml')
    @patch('toml.load')
    def test_get_hit_one_of_one(self, mock_lib):
        domain = 'test.com'
        username = 'test-user'
        scopes = ['read']
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        mock_lib.return_value = {'tokens':[{
            'domain': domain,
            'username': username,
            'scopes': scopes,
            'token': token
        }]}
        actual = TomlTokenReader().get(domain, username)
        mock_lib.assert_called_once()
        self.assertEqual(actual, token)
    @patch('toml.load')
    def test_get_hit_one_of_two(self, mock_lib):
        domain = 'test.com'
        username = 'test-user'
        scopes = ['read']
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        mock_lib.return_value = {'tokens':[{
            'domain': domain,
            'username': username,
            'scopes': scopes,
            'token': token
        },{
            'domain': domain + '2',
            'username': username + '2',
            'scopes': scopes,
            'token': token + '2'
        }]}
        actual = TomlTokenReader().get(domain, username)
        mock_lib.assert_called_once()
        self.assertEqual(actual, token)
    @patch('toml.load')
    def test_get_hit_two_of_two(self, mock_lib):
        domain = 'test.com'
        username = 'test-user'
        scopes = ['read']
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        mock_lib.return_value = {'tokens':[{
            'domain': domain,
            'username': username,
            'scopes': scopes,
            'token': token
        },{
            'domain': domain,
            'username': username,
            'scopes': ['write'],
            'token': 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
        }]}
        actual = TomlTokenReader().get(domain, username)
        mock_lib.assert_called_once()
        self.assertEqual(actual, token)
    @patch('toml.load')
    def test_get_not_hit_one(self, mock_lib):
        domain = 'test.com'
        username = 'test-user'
        scopes = ['read']
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        mock_lib.return_value = {'tokens':[{
            'domain': domain,
            'username': username,
            'scopes': scopes,
            'token': token
        }]}
        actual = TomlTokenReader().get(domain + '2', username)
        mock_lib.assert_called_once()
        self.assertEqual(actual, None)
        actual = TomlTokenReader().get(domain, username + '2')
        self.assertEqual(actual, None)
        actual = TomlTokenReader().get(domain, username, ['write'])
        self.assertEqual(actual, None)
    @patch('toml.load')
    def test_get_not_hit_two(self, mock_lib):
        domain = 'test.com'
        username = 'test-user'
        scopes = ['read']
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        mock_lib.return_value = {'tokens':[{
            'domain': domain,
            'username': username,
            'scopes': scopes,
            'token': token
        },{
            'domain': domain,
            'username': username,
            'scopes': ['write'],
            'token': 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
        }]}
        for case in [
            (([domain+'2', username], None), None),
            (([domain, username+'2'], None), None),
            (([domain, username], ['follow']), None),
        ]:
            with self.subTest(args=case[0][0], kwargs=case[0][1], expected=case[1]):
                actual = TomlTokenReader().get(*case[0][0], scopes=case[0][1])
                self.assertEqual(actual, None)
        """
        actual = TomlTokenReader().get(domain + '2', username)
        mock_lib.assert_called_once()
        self.assertEqual(actual, None)
        actual = TomlTokenReader().get(domain, username + '2')
        self.assertEqual(actual, None)
        actual = TomlTokenReader().get(domain, username, ['follow'])
        self.assertEqual(actual, None)
        """

if __name__ == "__main__":
    unittest.main()
