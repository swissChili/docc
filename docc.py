#!/usr/bin/python3

import re
import sys
import os
from markdown import markdown
from bs4 import BeautifulSoup
import jinja2
import toml

def read(f):
    with open(f, "r") as f_:
        return f_.read()

def parse_template(f):
    with open(f, "r") as f_:
        return jinja2.Template(f_.read())

def write(to, string):
    with open(to, "w") as to_:
        to_.write(string)
        to_.close()
    if read(to) == string: 
        return True 
    else: 
        return False

def sluggify(string):
    string = str(string).lower()
    return "-".join(string.split(" "))

def prettify(string):
    string = string.split("-")
    string = [ word[0].upper() + word[1:] for word in string ]
    return ' '.join(string)

def compile_markdown(files, template="template.html", title="Docc", output="dist"):
    if not os.path.exists(output):
        os.makedirs(output)
    for html, md in files.items():
        comp = BeautifulSoup(markdown(read(md)), features="html.parser")

        headers = comp.find_all("h1")

        links = []
        pages = []

        for h in headers:
            href = "bookmark-" + sluggify(h.string)
            h["id"] = href
            links.append({
                "href": "#" + href,
                "name": h.string
            })

        for page, source in files.items():
            if not page == html:
                pages.append({
                    "href": page,
                    "name": prettify("-".join(page.split(".")[:-1]))
                })

        write(os.path.join(output, html),parse_template(template).render(docc = comp, 
                                                                         title=title, 
                                                                         links=links,
                                                                         pages=pages))
    print("Successfully compiled {} files".format(len(files)))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        walk_dir = sys.argv[1]
    else:
        walk_dir = "."

    config = {
        "title": "Docc",
        "out": "dist",
        "ignore": [],
        "template": "/etc/docc/template.html"
    }

    if os.path.exists("docc.toml"):
        for key, val in toml.loads(read("docc.toml")).items():
            config[key] = val
        print("Using config found at docc.toml")

    paths = []
    for path, dirs, files in os.walk(walk_dir):
        for f in files:
            if ( f.endswith(".md") or f.endswith(".markdown") ) and not f in config["ignore"]:
                paths.append(os.path.join(path, f))
    # This is why I like python
    # I'm gonna hate myself when I have to fix this garbage fire
    files = { (html if not html.startswith("./") else html[2:]) : (md if not md.startswith("./") else md[2:]) for html, md in { '.'.join(path.split('.')[:-1]) + ".html" : path for path in paths }.items() }
    compile_markdown(files, template=config["template"], title="Docc Example", output=config["out"])
