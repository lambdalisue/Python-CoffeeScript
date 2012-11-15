#!python3
#encoding:utf-8
from __future__ import unicode_literals
import doctest
import unittest

import os
import io
import tempfile
import itertools

import execjs
import coffeescript


cfcode = """
#このコメントはasciiで表現できない文字列です(This is a non-ascii comment)
helloworld = "こんにちは世界"
add = (x, y) ->
    x + y
"""
hello = "こんにちは"
world = "世界"
helloworld = "こんにちは世界"


class CoffeeScriptTest(unittest.TestCase):
    def setUp(self):
        self.runtimes = list(execjs.available_runtimes().values())
        
        self.compilers = []
        self.compilers.append(coffeescript) #default compiler
        
        from os.path import join, dirname
        with io.open(join(dirname(coffeescript.__file__), "coffee-script.js")) as fp:
            compiler_script = fp.read()
        
        for runtime in self.runtimes:
            self.compilers.append(coffeescript.Compiler(compiler_script, runtime))
        
    
    def test_compile(self):
        for compiler, runtime in itertools.product(self.compilers, self.runtimes):
            compile = compiler.compile
            
            jscode = compile(cfcode, bare=True)
            ctx = runtime.compile(jscode)
            self.assertEqual(ctx.call("add", 1, 2), 3)
            self.assertEqual(ctx.call("add", hello, world), helloworld)
            self.assertEqual(ctx.eval("helloworld"), helloworld)
            
            jscode = compile(cfcode, bare=False)
            ctx = runtime.compile(jscode)
            with self.assertRaises(execjs.ProgramError):
                self.assertEqual(ctx.call("add", 1, 2), 3)
            with self.assertRaises(execjs.ProgramError):
                self.assertEqual(ctx.call("add", hello, world), helloworld)
            with self.assertRaises(execjs.ProgramError):
                self.assertEqual(ctx.eval("helloworld"), helloworld)
    
    
    def test_compile_files(self):
        encodings = "shift-jis utf-8 euc-jp".split()
        
        for compiler, encoding, runtime in itertools.product(self.compilers, encodings, self.runtimes):
            compile_file = compiler.compile_file
            
            (fd, filename) = tempfile.mkstemp()
            os.close(fd)
            try:
                with io.open(filename, "w", encoding=encoding) as fp:
                    fp.write(cfcode)
                
                jscode = coffeescript.compile_file(filename, 
                    encoding=encoding, bare=True)
                ctx = runtime.compile(jscode)
                self.assertEqual(ctx.call("add", 1, 2), 3)
                self.assertEqual(ctx.call("add", hello, world), helloworld)
                self.assertEqual(ctx.eval("helloworld"), helloworld)
                
                jscode = coffeescript.compile_file(filename,
                    encoding=encoding, bare=False)
                ctx = runtime.compile(jscode)
                with self.assertRaises(execjs.ProgramError):
                    self.assertEqual(ctx.call("add", 1, 2), 3)
                with self.assertRaises(execjs.ProgramError):
                    self.assertEqual(ctx.call("add", hello, world), helloworld)
                with self.assertRaises(execjs.ProgramError):
                    self.assertEqual(ctx.eval("helloworld"), helloworld)
                
                for wrong_encoding in set(encodings) - set([encoding]):
                    with self.assertRaises(UnicodeDecodeError):
                        coffeescript.compile_file(filename,
                            encoding=wrong_encoding, bare=True)
                    with self.assertRaises(UnicodeDecodeError):
                        coffeescript.compile_file(filename,
                            encoding=wrong_encoding, bare=False)
            finally:
                os.remove(filename)

    def test_compile_files_together(self):
        from os.path import join
        cfcodes = (
            "add = (a, b) -> a + b",
            "sub = (a, b) -> a - b",
            "mul = (a, b) -> a * b",
            "div = (a, b) -> a / b",
        )

        # Create Temp CoffeeScript files
        root = tempfile.mkdtemp()
        filenames = []
        for i, cfcode in enumerate(cfcodes):
            filename = join(root, "{0}.coffee".format(i))
            with io.open(filename, "w") as fp:
                fp.write(cfcode)
            filenames.append(filename)

        try:
            for compiler, runtime in itertools.product(self.compilers, self.runtimes):
                jscode = coffeescript.compile_files(filenames, bare=True)
                ctx = runtime.compile(jscode)
                self.assertEqual(ctx.call("add", 1, 2), 3)
                self.assertEqual(ctx.call("sub", 2, 1), 1)
                self.assertEqual(ctx.call("mul", 2, 3), 6)
                self.assertEqual(ctx.call("div", 8, 2), 4)

                jscode = coffeescript.compile_files(filenames, bare=False)
                ctx = runtime.compile(jscode)
                with self.assertRaises(execjs.ProgramError):
                    self.assertEqual(ctx.call("add", 1, 2), 3)
                with self.assertRaises(execjs.ProgramError):
                    self.assertEqual(ctx.call("sub", 1, 2), 3)
                with self.assertRaises(execjs.ProgramError):
                    self.assertEqual(ctx.call("mul", 1, 2), 3)
                with self.assertRaises(execjs.ProgramError):
                    self.assertEqual(ctx.call("div", 1, 2), 3)
        finally:
            import shutil
            shutil.rmtree(root)

def load_tests(loader, tests, ignore):
##    tests.addTests(doctest.DocTestSuite(coffeescript))
    return tests

def main():
    unittest.main()


if __name__ == "__main__":
    main()
