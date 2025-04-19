from livereload import Server, shell
from more_itertools import chunked
import os

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

with open("meta_data.json", "r", encoding="utf-8") as my_file:
    books = json.load(my_file)


def on_reload():
    books_count = 10
    download_books_pages = list(chunked(books, books_count))
    os.makedirs("pages", exist_ok=True)
    for number, books_page in enumerate(download_books_pages):
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('template.html')
        rendered_page = template.render(
            books=books_page
        )
        with open(f'pages/index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')

