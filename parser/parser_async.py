import asyncio
import aiohttp

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

    async def get_soup(self, session):
        async with session.get(self.url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, features='lxml')
            return soup

    async def parse(self, session):
        soup = await self.get_soup(session)
        if soup is not None:
            problems = iter(soup.find('table', class_='problems').find_all('tr'))
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

    async def get_links(self, session):
        url_pattern = 'https://codeforces.com/problemset/page/{}?order=BY_SOLVED_DESC&locale=ru'
        soup = await self.get_soup(session)
        if soup is None:
            return []
        selector = soup.select("#pageContent > div.pagination")[0].find_all('li')
        links_amount = int(selector[-2].a.text)
        links_list = [url_pattern.format(number)
                      for number in range(1, links_amount + 1)]
        return links_list

    async def parse_site_data(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for link in (await self.get_links(session)):
                page = Page(link)
                task = asyncio.create_task(page.parse(session))
                tasks.append(task)
            await asyncio.gather(*tasks)


async def run_parser():
    page = Page("https://codeforces.com/problemset")
    while True:
        await page.parse_site_data()
        await asyncio.sleep(3600)

