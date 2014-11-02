# -*- coding: ascii -*-
from __future__ import print_function
import subprocess
from pygments import highlight
from pygments.lexers import JavascriptLexer
from pygments.formatters import HtmlFormatter
 
from IPython import display
from IPython.core.magic import (
    register_cell_magic,
    Magics,
    magics_class,
    cell_magic,
)
from IPython.core.magic_arguments import (
    argument,
    magic_arguments,
    parse_argstring,
)
 
@magics_class
class CoffeescriptMagics(Magics):
    '''
    Compiles and executes CoffeeScript code
    
    Example:
    
        %%coffeescript
        class Foo
            constructor: ->
                @bar = "baz"
    '''
    
    def __init__(self, shell):
        self.lexer = JavascriptLexer()
        super(CoffeescriptMagics, self).__init__(shell)
    
    @cell_magic
    @magic_arguments()
    @argument("-b", "--bare", default=False, action="store_true",
              help="Return the compiled code without wrapping in an IIFE.")
    @argument("-v", "--verbose", default=False, action="store_true",
              help="Show generated javascript")
    def coffeescript(self, line, cell):
        opts = parse_argstring(self.coffeescript, line)
        ps = subprocess.Popen(('coffee','-sc'), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        ps.stdin.write(cell)
        ps.stdin.close()
        return_code = ps.wait()
        output = ps.stdout.read()
        if return_code!=0:
            print(ps.stderr.read())
            return
        if opts.verbose:
            pretty = highlight(output, self.lexer, HtmlFormatter(full=True))
            display.display_html("%s" % (pretty), raw=True)

        return display.display_javascript(output, raw=True)
 
def load_magics():
    ip = get_ipython()
    ip.register_magics(CoffeescriptMagics)
