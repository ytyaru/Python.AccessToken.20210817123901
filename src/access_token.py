#!/usr/bin/env python3
# coding: utf8
import os, sys, toml, datetime
from string import Template
from collections import namedtuple
class This:
    def __init__(self):
        self.__Names = namedtuple('Names' , 'parent name ext')
        self.__make_this()
    def __make_this(self):
        name, ext = os.path.splitext(os.path.basename(__file__))
        parent = os.path.abspath(os.path.dirname(__file__))
        self.__this = self.__Names(parent, name, ext)
    @property
    def Names(self): return self.__this
This = This()
class Token:
    @property
    def Path(self): return 'token.toml'
    def get(self, domain, username, scopes=None):
        tokens = toml.load(self.Path)['tokens']
        if scopes is None:
            f = filter(lambda t: t['domain'] == domain and t['username'] == username, tokens)
        else:
            f = filter(lambda t: t['domain'] == domain and t['username'] == username and all(s in t['scopes'] for s in scopes), tokens)
        l = list(f)
        if 0 < len(l): return l[0]['token']
class Command:
    @property
    def Version(self): return '0.0.1'
    @property
    def Description(self): return 'アクセストークンを返す。'
    @property
    def Usage(self): return f'{This.Names.name}{This.Names.ext} DOMAIN USER [SCOPES]...'
    @property
    def Help(self):
        path = os.path.join(This.Names.parent, 'help.txt')
        with open(path, mode='r', encoding='utf-8') as f:
            t = Template(f.read().rstrip('\n'))
            return t.substitute(description=self.Description, 
                                usage=self.Usage, 
                                this=f'{This.Names.name}{This.Names.ext}', 
                                version=self.Version)
    @property
    def Since(self):
        return datetime.datetime(2021, 8, 12, 0, 0, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    @property
    def Author(self):
        a = {}
        a['name'] = 'ytyaru'
        a['url'] = f'https://github.com/{a["name"]}'
        return a
    @property
    def Copyright(self): return f'© {self.Since.year} {self.Author["name"]}'
    @property
    def License(self):
        l = {}
        l['name'] = 'MIT'
        l['spdx'] = l['name']
        l['url'] = 'https://opensource.org/licenses/MIT'
        return l
    @property
    def Url(self): return 'https://github.com/ytyaru/Python.Mastodon.Api.Toot.20210812120350'
class App(Command):
    def token(self, *args, **kwargs): return Token().get(*args, **kwargs)
class SubCmdParser:
    def __init__(self):
        self.__SubCmd = namedtuple('SubCmd' , 'candidate text')
        self.__candidates  = []
    def __cmd(self, text):
        print(text)
        sys.exit(0)
    def __sub_cmd(self, arg, candidate, text):
        if arg in candidate: self.__cmd(text)
    def add(self, candidate, text):
        self.__candidates.append(self.__SubCmd(candidate, text))
    def parse(self):
        for c in self.__candidates:
            self.__sub_cmd(sys.argv[1], c.candidate, c.text)
class Cli:
    def __cmd(self, text):
        print(text)
        sys.exit(0)
    def __get_args(self): return sys.argv[1:]
    def __parse(self):
        if 2 == len(sys.argv):
            parser = SubCmdParser()
            parser.add(['-h', 'h', 'help'], App().Help)
            parser.add(['-v', 'v', 'version'], App().Version)
            parser.add(['d', 'description'], App().Description)
            parser.add(['u', 'url'], App().Url)
            parser.add(['a', 'author'], App().Author['name'])
            parser.add(['s', 'since'], App().Since.isoformat())
            parser.add(['c', 'copyright'], App().Copyright)
            parser.add(['l', 'license'], App().License['name'])
            parser.parse()
            self.__cmd(App().Help)
        elif 2 < len(sys.argv):
#            self.__cmd(App().token(self.__get_args()))
            self.__cmd(App().token(sys.argv[1], sys.argv[2], scopes=sys.argv[3:] if 3 < len(sys.argv) else None))
        else: self.__cmd(App().Help)
    def run(self): self.__parse()

if __name__ == "__main__":
    Cli().run()
#    t = toml.load(FILE_PATH)
#    print(t)
    
