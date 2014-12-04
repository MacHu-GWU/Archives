from .js import load_js

def load_statelist():
    return load_js(r"lib\refdata\statelist.json", enable_verbose=False)

def load_lastnamelist():
    return load_js(r"lib\refdata\lastnamelist.json", enable_verbose=False)