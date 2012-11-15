#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (c) 2011 Omoto Kenji
# Released under the MIT license. See `LICENSE` for details.
from __future__ import division, unicode_literals, print_function
"""
Python CoffeeScript is a bridge to the JS CoffeeScript compiler.

Usage:

    >>> import coffeescript
    >>> coffeescript.compile('add = (a, b) -> a + b')
    '(function() {\n  var add;\n\n  add = function(a, b) {\n    return a + b;\n  };\
    n\n}).call(this);\n'
    >>> print(coffeescript.compile('add = (a, b) -> a + b'))
    (function() {
      var add;

      add = function(a, b) {
        return a + b;
      };

    }).call(this);
"""
VERSION = (1, 0, 5)
__version__ = ".".join(map(str, VERSION))
__license__ = "MIT License"
__all__ = (
    'compile', 'compile_file', 'compile_files', 'Compiler',
    'EngineError', 'CompilationError',
)

import io
import execjs

EngineError = execjs.RuntimeError
CompilationError = execjs.ProgramError


class Compiler:
    """Python CoffeeScript Compiler"""
    def __init__(self, compiler_script, runtime):
        self._compiler_script = compiler_script
        self._runtime = runtime

    def compile(self, script, bare=False):
        """Compile CoffeeScript string and return JavaScript string

        Args:
            script
                CoffeeScript string
            bare
                Compile the JavaScript without the top-level function safety wrapper

        Return:
            Compiled JavaScript string
        """
        if not hasattr(self, '_context'):
            self._context = self._runtime.compile(self._compiler_script)
        return self._context.call("CoffeeScript.compile", script, {'bare': bare})

    def compile_file(self, filename, encoding="utf-8", bare=False):
        """Compile CoffeeScript file and return JavaScript string

        Args:
            filename
                CoffeeScript file
            encoding
                Encoding of the CoffeeScript file
            bare
                Compile the JavaScript without the top-level function safety wrapper

        Return:
            Compiled JavaScript string
        """
        with io.open(filename, encoding=encoding) as fp:
            return self.compile(fp.read(), bare=bare)

    def compile_files(self, filenames, encoding="utf-8", bare=False):
        """Compile and Join CoffeeScript files and return JavaScript string

        Args:
            filenames
                List of CoffeeScript files
            encoding
                Encoding of the CoffeeScript files
            bare
                Compile the JavaScript without the top-level function safety wrapper

        Return:
            Compiled JavaScript string
        """
        buf = []
        for filename in filenames:
            with io.open(filename, encoding=encoding) as fp:
                buf.append(fp.read())
        return self.compile("\n\n".join(buf), bare=bare)

    @classmethod
    def _default_compiler_script(cls):
        from os.path import dirname, join
        filename = join(dirname(__file__), 'coffee-script.js')
        with io.open(filename, encoding='utf8') as fp:
            return fp.read()

    @classmethod
    def _default_runtime(cls):
        return execjs.get()

    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            compiler_script = cls._default_compiler_script()
            runtime = cls._default_runtime()
            cls._instance = cls(compiler_script, runtime)
        return cls._instance


def _default_compiler():
    return _default_compiler.cls.instance()

_default_compiler.cls = Compiler


def compile(script, bare=False):
    """Compile CoffeeScript string and return JavaScript string

    Args:
        script
            CoffeeScript string
        bare
            Compile the JavaScript without the top-level function safety wrapper

    Return:
        Compiled JavaScript string
    """
    return _default_compiler().compile(script, bare=bare)


def compile_file(filename, encoding="utf-8", bare=False):
    """Compile CoffeeScript file and return JavaScript string

    Args:
        filename
            CoffeeScript file
        encoding
            Encoding of the CoffeeScript file
        bare
            Compile the JavaScript without the top-level function safety wrapper

    Return:
        Compiled JavaScript string
    """
    return _default_compiler().compile_file(filename, encoding=encoding, bare=bare)


def compile_files(filenames, encoding="utf-8", bare=False):
    """Compile and Join CoffeeScript files and return JavaScript string

    Args:
        filenames
            List of CoffeeScript files
        encoding
            Encoding of the CoffeeScript files
        bare
            Compile the JavaScript without the top-level function safety wrapper

    Return:
        Compiled JavaScript string
    """
    return _default_compiler().compile_files(filenames, encoding=encoding, bare=bare)
