from __future__ import print_function
import os
import subprocess
import IPython
from IPython.core import display
import urllib
import json
import random
import os

__all__ = ['display_assets', 'load_magics']


def coffeescript_recipe(input_filename, input_dir="", output_dir=""):
    input_path_full = os.path.join(input_dir, input_filename)
    file_stem = input_filename.split('.coffee')[0]
    output_file_name = os.path.join(output_dir, file_stem + '.js')

    if not os.path.exists(output_file_name) or\
        os.path.getmtime(input_path_full)>os.path.getmtime(output_file_name):
        # Compile coffeescript to javascript + source map
        subprocess.check_output(['coffee', '-c', '-m','-o', output_dir,
                                 input_path_full],
                                 stderr=subprocess.STDOUT)
    
    output_mapping_file_name = os.path.join(output_dir, file_stem + '.js.map')
    
    # Coffeescript can only output source maps as files and they are bound by their file names
    # So for inlined javascript it is necessary to wrangle the two output files
    js_code = file(output_file_name).read()
    # Remove sourceMappingUrl directive which contains a useless file name
    
    js_code = "\n".join([line for line in js_code.split("\n")
                     if not line.startswith('//# sourceMappingURL=')])

    
    # Load coffeescript source code for inclusion into source map
    coffee_code = file(os.path.join(input_dir, input_filename)).read()
    
    # load source map as a dict structure to amend some particulars
    mapping = json.loads(file(output_mapping_file_name).read())
    
    # In Chrome Dev Tools newly inlined source maps don't replace old source maps for the same file name
    unique_token = os.urandom(4).encode('hex') # Create a relatively unique token
    
    # Change source map to work nicely when inlined
    mapping['sourceRoot'] = ''
    mapping['sourcesContent'] = [coffee_code]
    mapping['sources'] = [input_filename + unique_token]

    mapping['file'] = input_filename + unique_token
    
    source_map = json.dumps(mapping)
    js_code += "\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,"+source_map.encode("base64").replace('\n', '')+'\n'
    display.display_javascript(js_code, raw=True)


def javascript_recipe(input_filename, input_dir="", output_dir=""):
    # Output dir is ignored because files are copied as-is
    input_path_full = os.path.join(input_dir, input_filename)
    js_code = file(input_path_full).read()
    display.display_javascript(js_code, raw=True)

recipes = {'coffeescript': coffeescript_recipe,
           'javascript': javascript_recipe}

def display_assets(assets, input_dir='', output_dir=''):
    for recipe_name, input_filename in assets:
        recipes[recipe_name](input_filename, input_dir, output_dir)

def load_magics():
    import coffeescript_magic
    coffeescript_magic.load_magics()
