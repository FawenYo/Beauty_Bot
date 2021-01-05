import sys
import requests
import threading
from bs4 import BeautifulSoup
import re
from datetime import datetime

sys.path.append(".")
import config
import mongodb.database

BLACK_LIST = ["公告", "投稿", "注意", "推薦", "猜題", "工具", "整理"]


class PTT_Beauty:
    def __init__(self) -> None:
        self.main()

    def update(self, current_page):
        articles = self.parse_article_info(current_page=current_page)
        mongodb.database.add_record(articles=articles)

    def main(self):
        threads = []
        next_page = True
        execution_data = config.db.status.find_one()
        last_execution_page = execution_data["last_execution_page"]
        while next_page:
            url = f"{config.PTT_URL}/bbs/Beauty/index{last_execution_page}.html"
            current_page = self.get_web_content(url=url)
            if current_page:
                print(f"add: {url}")
                last_execution_page += 1
                thread = threading.Thread(target=self.update, args=(current_page,))
                threads.append(thread)
            else:
                next_page = False

        print("start fetching data...")
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        execution_data["last_execution_page"] = last_execution_page - 1
        config.db.status.update_one({}, {"$set": execution_data})
        print("update done!")

    def parse_article_info(self, current_page):
        results = []
        articles = self.get_articles(current_page)
        for article in articles:
            page = self.get_web_content(url=f"{config.PTT_URL}{article['href']}")
            if page:
                img_urls = self.get_images(page)
                date = self.get_date(page)
                if len(img_urls) > 0 and date.year >= 2015:
                    article["images"] = img_urls
                    article["date"] = date
                    results.append(article)
        return articles

    def get_web_content(self, url) -> str:
        resp = requests.get(url=url, cookies={"over18": "1"})
        if resp.status_code == 200:
            return resp.text
        else:
            print("Invalid url: " + resp.url)
            return None

    def get_articles(self, dom):
        soup = BeautifulSoup(dom, "html.parser")

        articles = []
        divs = soup.find_all("div", "r-ent")
        for div in divs:
            push_count = 0
            push_str = div.find("div", "nrec").text
            if push_str:
                try:
                    push_count = int(push_str)
                except ValueError:
                    if push_str == "爆":
                        push_count = 99
                    elif push_str.startswith("X"):
                        push_count = -10

            if div.find("a"):
                href = div.find("a")["href"]
                title = div.find("a").text

                # 是否為無關文章
                not_related = False
                for each in BLACK_LIST:
                    if each in title:
                        not_related = True
                        break
                if not not_related or push_count >= 0:
                    articles.append(
                        {
                            "title": title,
                            "href": href,
                            "push_count": push_count,
                        }
                    )
        return articles

    def get_images(self, dom) -> list:
        soup = BeautifulSoup(dom, "html.parser")
        links = soup.find(id="main-content").find_all("a")
        img_urls = []
        for link in links:
            if re.match(r"^https?://(i.)?(m.)?imgur.com", link["href"]):
                img_urls.append(link["href"])
        return img_urls

    def get_date(self, dom, date=datetime.now()):
        soup = BeautifulSoup(dom, "html.parser")
        for each in soup.select(
            ".article-metaline+ .article-metaline .article-meta-value"
        ):
            date_str = each.text
            date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
            return date
