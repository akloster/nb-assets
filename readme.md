NB-Assets
===

NB-Assets simplifies development and distribution of javascript code for use in the IPython Noteboook. It is a simple asset manager, ideal for IPython extensions, notebook-aware libraries or published notebooks which need to include and execute javascript code without depending on HTTP requests.

As a bonus, it also includes a CoffeeScript cell magic.

Usage
---


```python
assets =  [("coffeescript", "test.coffee"),
           ("javascript", "hello_javascript.js")]
nb_assets.display_assets(assets, input_dir="assets", output_dir="static")
```

To compile CoffeeScript code you need a CoffeeScript compiler executable available as 'coffee' in the system environment.

See notebooks/Tutorial.ipynb for more information.
