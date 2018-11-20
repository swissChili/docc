#!/usr/bin/python3

import re
import sys
import os
from markdown import markdown
from bs4 import BeautifulSoup
import jinja2

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

def compile_markdown(files, template="template.html", title="Docc"):
    if not os.path.exists("dist"):
        os.makedirs("dist")
    for html, md in files.items():
        comp = BeautifulSoup(markdown(read(md)), features="html.parser")

        headers = comp.find_all("h1")

        links = []

        for h in headers:
            href = "bookmark-" + sluggify(h.string)
            h["id"] = href
            links.append({
                "href": "#" + href,
                "name": h.string
            })

        write(os.path.join("dist", html),parse_template(template).render(docc = comp, title=title, links=links))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        paths = []
        for path, dirs, files in os.walk(sys.argv[1]):
            for f in files:
                if f.endswith(".md") or f.endswith(".markdown"):
                    paths.append(os.path.join(path, f))
        # This is why I like python
        # I'm gonna hate myself when I have to fix this garbage fire
        files = { (html if not html.startswith("./") else html[2:]) : (md if not md.startswith("./") else md[2:]) for html, md in { '.'.join(path.split('.')[:-1]) + ".html" : path for path in paths }.items() }
        compile_markdown(files, title="Docc Example")
    else:
        print("No path specified. Please specify a path to use docc")
