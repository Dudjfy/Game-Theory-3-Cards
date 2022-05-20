import requests as req
from bs4 import BeautifulSoup


class NewsSearcher:
    sources = {
        "expressen": "https://www.expressen.se/",
        "svt": "https://www.svt.se/",
        "aftonbladet": "https://www.aftonbladet.se/",
        "dn": "https://www.dn.se/",
    }
    alternative_sources = {
        "expressen": "https://www.expressen.se/",
        "svt": "https://www.svt.se/?nyhetsmeny=1",
        "aftonbladet": "https://www.aftonbladet.se/",
        "dn": "https://www.dn.se/",
    }
    topics = {
        "expressen": dict(),
        "svt": dict(),
        "aftonbladet": dict(),
        "dn": dict(),
    }
    common_topics = {
        "expressen": dict(),
        "svt": dict(),
        "aftonbladet": dict(),
        "dn": dict(),
    }
    general_topics = {
        "expressen": dict(),
        "svt": dict(),
        "aftonbladet": dict(),
        "dn": dict(),
    }
    common_topics_articles = {
        "expressen": dict(),
        "svt": dict(),
        "aftonbladet": dict(),
        "dn": dict(),
    }
    general_topics_articles = {
        "expressen": dict(),
        "svt": dict(),
        "aftonbladet": dict(),
        "dn": dict(),
    }
    display_names = {
        "expressen": "Expressen",
        "svt": "SVT",
        "aftonbladet": "Aftonbladet",
        "dn": "DN",
    }
    general_topics_examples = ["kultur",
                               "nöje",
                               "nyheter",
                               "sport",
                               "ekonomi",
                               "sverige",
                               "inrikes",
                               "utrikes",
                               "världen",
                               "vetenskap",
                               "ledare"]
    user_defined_sources = dict()
    user_defined_topics = dict()
    user_defined_topics_filtered = dict()
    user_defined_topics_filtered_one_topic = dict()
    user_defined_topics_articles = dict()

    def find_topics(self, sources, output_collection):
        for news_outlet, website in sources.items():
            url = req.get(website)
            soup = BeautifulSoup(url.text, "html.parser")

            for a_tag in soup.find_all("a"):
                if a_tag.has_attr("href") and isinstance(a_tag.string, str):
                    output_collection[news_outlet][a_tag.string.lower().strip()] = a_tag["href"]

    def find_common_topics(self):
        for topic, link in self.topics["expressen"].items():
            if topic not in self.topics["svt"]:
                continue
            if topic not in self.topics["aftonbladet"]:
                continue
            if topic not in self.topics["dn"]:
                continue

            for news_outlet, topic_collection in self.common_topics.items():
                self.common_topics[news_outlet][topic] = self.topics[news_outlet][topic]

    def transform_relative_links_to_absolute_topics(self, collection):
        for news_outlet, topic_collection in collection.items():
            for topic, link in topic_collection.items():
                if "https://" not in link:
                    collection[news_outlet][topic] = f"{self.sources[news_outlet][:-1]}{link}"

    def transform_relative_links_to_absolute_articles(self, collection):
        for news_outlet, topic_collection in collection.items():
            for topic, articles in topic_collection.items():
                for article, link in articles.items():
                    if "https://" not in link:
                        collection[news_outlet][topic][article] = f"{self.sources[news_outlet][:-1]}{link}"

    def create_common_topics(self):
        if len(self.topics["expressen"]) == 0:
            self.find_topics(self.alternative_sources, self.topics)
        self.find_common_topics()
        self.transform_relative_links_to_absolute_topics(self.common_topics)

        self.find_articles(self.common_topics, self.common_topics_articles)
        self.transform_relative_links_to_absolute_articles(self.common_topics_articles)

    def create_general_topics(self):
        if len(self.topics["expressen"]) == 0:
            self.find_topics(self.alternative_sources, self.topics)
        self.find_general_topics(self.topics, self.general_topics)
        self.transform_relative_links_to_absolute_topics(self.general_topics)

        self.find_articles(self.general_topics, self.general_topics_articles)
        self.transform_relative_links_to_absolute_articles(self.general_topics_articles)

    def find_general_topics(self, input_collection, output_collection):
        for news_outlet, topic_collection in input_collection.items():
            for topic, link in topic_collection.items():
                if topic in self.general_topics_examples:
                    output_collection[news_outlet][topic] = input_collection[news_outlet][topic]

    def display_topics(self, collection, article_collection, article_depth=3):
        for news_outlet, topic_collection in collection.items():
            print(f"{self.display_names[news_outlet]}:")
            for topic, link in topic_collection.items():
                print(f"\t{topic.capitalize()} - {link}")

                depth = 0
                for article, article_link in article_collection[news_outlet][topic].items():
                    print(f"\t\t{article} - {article_link}")

                    depth += 1
                    if depth >= article_depth:
                        return

            print()

    def find_articles(self, collection, articles_collection, article_depth=100):
        depth = 0
        for news_outlet, topic_collection in collection.items():
            for topic, link in topic_collection.items():
                url = req.get(link)
                soup = BeautifulSoup(url.text, "html.parser")

                articles_collection[news_outlet][topic] = dict()
                for article_tag in soup.find_all("article"):
                    if article_tag.a.has_attr("href") and article_tag.a.has_attr("title"):
                        articles_collection[news_outlet][topic][article_tag.a["title"]] = article_tag.a["href"]

                        depth += 1
                        if depth >= article_depth:
                            return

                a_tags = soup.find_all("a")
                for a_tag in a_tags:
                    headers = a_tag.find_all(["h1", "h2", "h3"])
                    if len(headers) > 0 \
                            and a_tag.has_attr("href") \
                            and isinstance(headers[0].string, str) \
                            and (a_tag["href"] not in self.sources.values()) \
                            and a_tag["href"] != "/":
                        articles_collection[news_outlet][topic][headers[0].string.strip()] = a_tag["href"]

                        depth += 1
                        if depth >= article_depth:
                            return

    def choosing_news_outlet(self):
        while True:
            self.print_news_outlets()

            num = input(f">>> ")
            print()

            if not num.isnumeric():
                print(f"Wrong news outlet! Please type a number from 1-{len(self.sources)}")
                print()
                continue

            num = int(num) - 1
            if not (0 <= num < len(self.sources)):
                print(f"Wrong news outlet! Please type a number from 1-{len(self.sources)}")
                print()
                continue

            return list(self.sources)[num]

    def choosing_general_topic(self, user_defined_topics):
        while True:
            self.print_user_defined_colection(user_defined_topics, "topics", len(user_defined_topics))

            num = input(f">>> ")
            print()

            if not num.isnumeric():
                print(f"Wrong topic! Please type a number from 1-{len(user_defined_topics)}")
                print()
                continue

            num = int(num) - 1
            if not (0 <= num < len(user_defined_topics)):
                print(f"Wrong topic! Please type a number from 1-{len(user_defined_topics)}")
                print()
                continue

            return list(user_defined_topics)[num]

    def user_choosing_by_input(self):
        news_outlet = self.choosing_news_outlet()
        self.create_user_defined_topics(news_outlet)

        topic = self.choosing_general_topic(self.user_defined_topics_filtered[news_outlet])
        self.create_user_defined_articles(news_outlet, topic)

        self.print_user_defined_colection(self.user_defined_topics_articles[news_outlet][topic], "articles")

    def print_news_outlets(self):
        print("Choose one of the following news outlets:")
        for i, names in enumerate(self.display_names.items()):
            internal_name, display_name = names
            print(f"\t{i + 1}. {display_name} - {self.sources[internal_name]}")
        print()

    def print_user_defined_colection(self, user_defined_collection, msg, article_depth=3):
        print(f"Choose one of the following {msg}:")
        depth = 0
        for i, topic_collection in enumerate(user_defined_collection.items()):
            topic, link = topic_collection
            print(f"\t{i + 1}. {topic.capitalize()} - {link}")

            depth += 1
            if depth >= article_depth:
                return
        print()

    def create_user_defined_topics(self, news_outlet):
        self.user_defined_sources = {news_outlet: self.alternative_sources[news_outlet]}
        self.user_defined_topics = {news_outlet: dict()}
        self.find_topics(self.user_defined_sources, self.user_defined_topics)
        self.user_defined_topics_filtered = {news_outlet: dict()}
        self.find_general_topics(self.user_defined_topics, self.user_defined_topics_filtered)
        self.transform_relative_links_to_absolute_topics(self.user_defined_topics_filtered)

    def create_user_defined_articles(self, news_outlet, topic, article_depth=100):
        self.user_defined_topics_filtered_one_topic = {news_outlet:
                                                 {topic: self.user_defined_topics_filtered[news_outlet][topic]}}
        self.user_defined_topics_articles = {news_outlet: {topic: dict()}}
        self.find_articles(self.user_defined_topics_filtered_one_topic, self.user_defined_topics_articles,
                           article_depth)
        self.transform_relative_links_to_absolute_articles(self.user_defined_topics_articles)