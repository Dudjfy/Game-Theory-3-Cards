"""A module for a news searcher program, compatible with both console and tkinter based systems"""

import requests as req
from bs4 import BeautifulSoup


class NewsSearcher:
    """A News Searcher class. Main purpose is to search news, find topics and articles in those"""

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
        "expressen": {},
        "svt": {},
        "aftonbladet": {},
        "dn": {},
    }
    common_topics = {
        "expressen": {},
        "svt": {},
        "aftonbladet": {},
        "dn": {},
    }
    general_topics = {
        "expressen": {},
        "svt": {},
        "aftonbladet": {},
        "dn": {},
    }
    common_topics_articles = {
        "expressen": {},
        "svt": {},
        "aftonbladet": {},
        "dn": {},
    }
    general_topics_articles = {
        "expressen": {},
        "svt": {},
        "aftonbladet": {},
        "dn": {},
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
    user_defined_sources = {}
    user_defined_topics = {}
    user_defined_topics_filtered = {}
    user_defined_topics_filtered_one_topic = {}
    user_defined_topics_articles = {}

    @staticmethod
    def find_topics(sources, output_collection):
        """A static method which finds all topics for all news outlets based on input sources"""
        for news_outlet, website in sources.items():
            url = req.get(website)
            soup = BeautifulSoup(url.text, "html.parser")

            for a_tag in soup.find_all("a"):
                if a_tag.has_attr("href") and isinstance(a_tag.string, str):
                    output_collection[news_outlet][a_tag.string.lower().strip()] = a_tag["href"]

    def find_common_topics(self):
        """Finds topics in common for different news outlets"""
        for topic in self.topics["expressen"]:
            if topic not in self.topics["svt"]:
                continue
            if topic not in self.topics["aftonbladet"]:
                continue
            if topic not in self.topics["dn"]:
                continue

            for news_outlet, common_topic in self.common_topics.items():
                common_topic[topic] = self.topics[news_outlet][topic]

    def transform_relative_links_to_absolute_topics(self, collection):
        """Transforms relative links to absolute for topics"""
        for news_outlet, topic_collection in collection.items():
            for topic, link in topic_collection.items():
                if "https://" not in link:
                    collection[news_outlet][topic] = f"{self.sources[news_outlet][:-1]}{link}"

    def transform_relative_links_to_absolute_articles(self, collection):
        """Transforms relative links to absolute for articles"""
        for news_outlet, topic_collection in collection.items():
            for topic, articles in topic_collection.items():
                for article, link in articles.items():
                    if "https://" not in link:
                        collection[news_outlet][topic][article] = \
                            f"{self.sources[news_outlet][:-1]}{link}"

    def create_common_topics(self):
        """Creates common topics collections for all news outlets in multiple steps"""
        if len(self.topics["expressen"]) == 0:
            self.find_topics(self.alternative_sources, self.topics)
        self.find_common_topics()
        self.transform_relative_links_to_absolute_topics(self.common_topics)

        self.find_articles(self.common_topics, self.common_topics_articles)
        self.transform_relative_links_to_absolute_articles(self.common_topics_articles)

    def create_general_topics(self):
        """Creates general topics collections for all news outlets in multiple steps,
        based on predetermined wanted topics collection"""
        if len(self.topics["expressen"]) == 0:
            self.find_topics(self.alternative_sources, self.topics)
        self.find_general_topics(self.topics, self.general_topics)
        self.transform_relative_links_to_absolute_topics(self.general_topics)

        self.find_articles(self.general_topics, self.general_topics_articles)
        self.transform_relative_links_to_absolute_articles(self.general_topics_articles)

    def find_general_topics(self, input_collection, output_collection):
        """Finds general topics for all news outlets"""
        for news_outlet, topic_collection in input_collection.items():
            for topic in topic_collection:
                if topic in self.general_topics_examples:
                    output_collection[news_outlet][topic] = input_collection[news_outlet][topic]

    def display_topics(self, collection, article_collection, article_depth=3):
        """Displays topics based on input collection and article search depth"""
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
        """Finds articles in the given topics collections. Can be adjusted to work faster with
        shallower search depth"""
        depth = 0
        for news_outlet, topic_collection in collection.items():
            for topic, link in topic_collection.items():
                url = req.get(link)
                soup = BeautifulSoup(url.text, "html.parser")

                articles_collection[news_outlet][topic] = {}
                for article_tag in soup.find_all("article"):
                    if article_tag.a.has_attr("href") and article_tag.a.has_attr("title"):
                        articles_collection[news_outlet][topic][article_tag.a["title"]] = \
                            article_tag.a["href"]

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
                        articles_collection[news_outlet][topic][headers[0].string.strip()] = \
                            a_tag["href"]

                        depth += 1
                        if depth >= article_depth:
                            return

    def choosing_news_outlet(self):
        """Chooses news outlets based on user input"""
        while True:
            self.print_news_outlets()

            num = input(">>> ")
            print()

            if not num.isnumeric():
                print(f"Wrong news outlet! Please type a number from 1-{len(self.sources)}")
                print()
                continue

            num = int(num) - 1
            if not 0 <= num < len(self.sources):
                print(f"Wrong news outlet! Please type a number from 1-{len(self.sources)}")
                print()
                continue

            return list(self.sources)[num]

    def choosing_general_topic(self, user_defined_topics):
        """Chooses topics based on user input"""
        while True:
            self.print_user_defined_collection(user_defined_topics, "topics",
                                               len(user_defined_topics))

            num = input(">>> ")
            print()

            if not num.isnumeric():
                print(f"Wrong topic! Please type a number from 1-{len(user_defined_topics)}")
                print()
                continue

            num = int(num) - 1
            if not 0 <= num < len(user_defined_topics):
                print(f"Wrong topic! Please type a number from 1-{len(user_defined_topics)}")
                print()
                continue

            return list(user_defined_topics)[num]

    def user_choosing_by_input(self):
        """Puts together all user based choices and displays final result in console"""
        news_outlet = self.choosing_news_outlet()
        self.create_user_defined_topics(news_outlet)

        topic = self.choosing_general_topic(self.user_defined_topics_filtered[news_outlet])
        self.create_user_defined_articles(news_outlet, topic)

        self.print_user_defined_collection(self.user_defined_topics_articles[news_outlet][topic],
                                           "articles")

    def print_news_outlets(self):
        """Prints out the news outlets"""
        print("Choose one of the following news outlets:")
        for i, names in enumerate(self.display_names.items()):
            internal_name, display_name = names
            print(f"\t{i + 1}. {display_name} - {self.sources[internal_name]}")
        print()

    @staticmethod
    def print_user_defined_collection(user_defined_collection, msg, article_depth=3):
        """A static method which prints out a collection based on input, message and/or
        article depth"""
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
        """Creates topics based on users choice of news outlets"""
        self.user_defined_sources = {news_outlet: self.alternative_sources[news_outlet]}
        self.user_defined_topics = {news_outlet: {}}
        self.find_topics(self.user_defined_sources, self.user_defined_topics)
        self.user_defined_topics_filtered = {news_outlet: {}}
        self.find_general_topics(self.user_defined_topics, self.user_defined_topics_filtered)
        self.transform_relative_links_to_absolute_topics(self.user_defined_topics_filtered)

    def create_user_defined_articles(self, news_outlet, topic, article_depth=100):
        """Creates articles based on user defined news outlets and topics within it/them"""
        self.user_defined_topics_filtered_one_topic = {news_outlet:
                                    {topic: self.user_defined_topics_filtered[news_outlet][topic]}}
        self.user_defined_topics_articles = {news_outlet: {topic: {}}}
        self.find_articles(self.user_defined_topics_filtered_one_topic,
                           self.user_defined_topics_articles,
                           article_depth)
        self.transform_relative_links_to_absolute_articles(self.user_defined_topics_articles)
