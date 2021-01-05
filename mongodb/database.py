import sys

sys.path.append("..")
import config


def add_record(articles):
    updated = False
    for article in articles:
        result = config.db.articles.find_one({"href": article["href"]})
        if not result:
            config.db.articles.insert_one(article)
            updated = True
    return updated