#!/usr/bin/env python3
# coding: utf8
import os, sys, pathlib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
#sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))
#print(sys.path)
from src.token import Token
import unittest
from unittest.mock import MagicMock, patch, mock_open
import copy
import toml
class TestToken(unittest.TestCase):
    def test_path(self):
        self.assertEqual(Token().Path, 'token.toml')
    @patch('toml.load')
    def test_get_none_file(self, mock_lib):
        Token().get('domain', 'username')
        mock_lib.assert_called_once()
    @patch('toml.load')
    def test_get_none_scopes(self, mock_lib):
        Token().get('domain', 'username')
        mock_lib.assert_called_once()
    @patch('toml.load')
    def test_get_with_scopes(self, mock_lib):
        Token().get('domain', 'username', ['read', 'write'])
        mock_lib.assert_called_once()

if __name__ == "__main__":
    unittest.main()
