#!/usr/bin/env python3
# coding: utf8
import os, sys
# 親ディレクトリをパスに追加する
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import access_token
from access_token import This, Token, Command, App, SubCmdParser, Cli
import unittest
from unittest.mock import MagicMock, patch, mock_open
import copy
import toml
class TestToken(unittest.TestCase):
    def test_path(self):
        self.assertEqual(Token().Path, 'token.toml')
    """
    def test_get_none_scopes(self):
        mock_lib = MagicMock()
#        print(Token().get('mstdn.jp', 'ytyaru'))
#        with patch('toml.load', return_value=mock_lib):
        with patch('builtins.filter', return_value=mock_lib):
            Token().get('', '')
            mock_lib.assert_called_once()
    def test_get_with_scopes(self):
        mock_lib = MagicMock()
        with patch('toml.load', return_value=mock_lib):
            Token().get('', '', scopes=['read', 'write'])
            mock_lib.assert_called_once()
    """

if __name__ == "__main__":
    unittest.main()
