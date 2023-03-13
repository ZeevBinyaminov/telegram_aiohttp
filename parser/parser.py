import asyncio
import requests
from bs4 import BeautifulSoup
from database.database import db


class Task:
    def __init__(self, themes, solutions_number, title, difficulty):
        self.themes = themes
        self.solutions_number = solutions_number
        self.title = title
        self.difficulty = difficulty

    def submit(self):
        db.add_task(self)
        db.connection.commit()


class Page:
    def __init__(self, url):
        self.url = url

    @property
    def response(self):
        response = requests.get(self.url,
                                params={
                                    "order": "BY_SOLVED_DESC",
                                    "locale": "ru",
                                })
        return response

    @property
    def soup(self):
        if self.response.status_code == 200:
            return BeautifulSoup(self.response.content, features="lxml")
        return None

    def get_links(self):
        url_pattern = 'https://codeforces.com/problemset/page/{}'
        selector = self.soup.select("#pageContent > div.pagination")[0].find_all('li')
        links_amount = int(selector[-2].a.text)
        links_list = [url_pattern.format(number)
                      for number in range(1, links_amount + 1)]
        return links_list

    def parse(self):
        problems = iter(self.soup.find('table', class_='problems').find_all('tr'))
        next(problems)

        for problem in problems:
            problem_info = problem.find_all("td")
            themes = ', '.join([theme.text for theme in problem_info[1].find_all('a', class_='notice')])
            solutions_number = int('0' + problem_info[4].text.replace('x', '').strip())
            title = problem_info[1].div.text.strip() + ' ' + problem_info[0].a.text.strip()
            difficulty = int('0' + problem_info[3].text.strip())

            task = Task(themes, solutions_number,
                        title, difficulty)
            if not db.exists(task):
                task.submit()

    def parse_all(self):
        for url in self.get_links():
            page = Page(url)
            page.parse()


async def run_parser():
    page = Page("https://codeforces.com/problemset")
    while True:
        page.parse_all()
        await asyncio.sleep(240)
