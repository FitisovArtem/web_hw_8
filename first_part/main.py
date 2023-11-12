from typing import Any
import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


if __name__ == '__main__':
    print("""
Для пошуку по Автору: name:Steve Martin або name:Steve,Albert
Для пошуку по Тегам: tag:life або tags:life,live""")
    while True:
        data = input("Введіть запит для пошуку або exit для виходу: ")
        if data == 'exit':
            break
        split_data = data.split(":")
        if len(split_data) >= 2:
            if split_data[0] == "tag":
                [print(find_by_tag(i)) for i in split_data[1].split(",")]
            elif split_data[0] == "name":
                [print(find_by_author(i)) for i in split_data[1].split(",")]
        else:
            print("Перевірте правильність вводу!")
