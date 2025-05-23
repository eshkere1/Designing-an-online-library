import os
import json
from dotenv import load_dotenv
from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


def on_reload():
    path = os.environ.get("META_DATA_PATH", "meta_data.json")
    with open(path, "r", encoding="utf-8") as my_file:
        books = json.load(my_file)
    books_count = 10
    download_books_pages = list(chunked(books, books_count))
    os.makedirs("pages", exist_ok=True)
    for number, books_page in enumerate(download_books_pages):
        env = Environment(
            loader=FileSystemLoader("."),
            autoescape=select_autoescape(["html", "xml"])
        )
        template = env.get_template("template.html")
        rendered_page = template.render(
            books=books_page,
            number_page = number + 1,
            total_pages = len(download_books_pages)
        )
        with open(f"pages/index{number+1}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    load_dotenv()
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".", default_filename="./pages/index1.html")


if __name__ == "__main__":
    main()