import conf

import argparse
import json
import random
import re

from faker import Faker


def main():
    parser = create_parser()
    args = parser.parse_args()
    my_gen_book = generate_book(args)
    book_list = []
    for i in range(args.count):
        book_list.append(next(my_gen_book))
        # print(next(my_gen_book))

    to_json(book_list, "cancer.json")


def to_json(obj, filename, dent=4):
    with open(filename, 'w', encoding="utf-8") as json_file:
        json.dump(obj, json_file, indent=dent, ensure_ascii=False)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("count", help="Number of books to generate", type=int)
    parser.add_argument("-a", "--authors", help="Authors per book", type=int, default=-1)
    parser.add_argument("-s", "--sale", help="Sale percentage(0-100)", type=int, default=-1)
    return parser


def fetch_title():
    """
    Fetching the title for a book
    :return: random title from the list in file set by BOOK_TITLES
    """
    with open(conf.BOOK_TITLES, encoding="utf-8") as titles:
        title_list = titles.readlines()
    title_list = [line.strip("\n") for line in title_list]
    size = len(title_list)
    title = title_list[random.randrange(size)]
    return title


def check_name_file(name_list):
    for line in name_list:
        a = re.fullmatch("[A-ZА-Я][a-zа-я]+? [A-ZА-Я][a-zа-я]+", line)
        if a is None:
            raise Exception(ValueError)


def fetch_authors(num):
    with open(conf.AUTHORS, encoding="utf-8") as names:
        name_list = names.readlines()
    name_list = [line.strip() for line in name_list]

    size = len(name_list)
    author_names = []
    for i in range(num):
        author_names.append(name_list[random.randrange(size)])
    return author_names


def generate_book(args):
    pk = 0
    fake = Faker()
    Faker.seed(0)
    while True:
        amt_authors = args.authors if args.authors != -1 else random.randint(1, 3)
        sale = args.sale if args.sale != -1 else random.randint(0, 100)
        pk += 1
        fields = {
            "title": fetch_title(),
            "year": random.randint(1800, 2020),
            "pages": random.randint(100, 500),
            "isbn13": fake.isbn13(),
            "rating": random.randint(0, 5),
            "price": round(random.random()*500, 2),
            "discount": sale,
            "author": fetch_authors(amt_authors)
        }
        new_book = {
            "model": conf.MODEL,
            "pk": pk,
            "fields": fields,
        }

        yield new_book


if __name__ == '__main__':
    main()
