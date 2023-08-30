import httpx
import asyncio
from parsel import Selector

"""
    Homework#7
    1.0. Создать еще один скрапер но уже асинхронный 
"""


class AsyncParseData:
    START_URL = "https://www.euronews.com"
    URL_XPATH = "/travel/travel-series/adventures"

    links_xpath = '//a[@class="media__img__link"]/@href'
    img_url_xpath = '//a[@class="media__img__link"]/img'

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def fetch_data(self, url):
        try:
            response = await self.client.get(url)
            return response.text
        except httpx.HTTPError as e:
            print(f"Error: {e}")

    async def __aenter__(self):
        print('Open')
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        print('closed')
        await self.client.aclose()

    async def get_links(self):
        response = await self.fetch_data(self.START_URL + self.URL_XPATH)
        tree = Selector(text=response)
        links = tree.xpath(self.links_xpath).extract()
        for link in links:
            print(self.START_URL + link)

    async def get_titles(self):
        response = await self.fetch_data(self.START_URL + self.URL_XPATH)
        tree = Selector(text=response)
        titles = tree.xpath(self.img_url_xpath)
        for title in titles:
            print(title.css("img::attr(alt)").get())

    async def get_img_links(self):
        response = await self.fetch_data(self.START_URL + self.URL_XPATH)
        tree = Selector(text=response)
        imgs = tree.xpath(self.img_url_xpath)
        for img in imgs:
            print(img.css("img::attr(src)").get())

    async def main(self):
        task_link = asyncio.create_task(self.get_links())
        task_title = asyncio.create_task(self.get_titles())
        task_img = asyncio.create_task(self.get_img_links())

        await asyncio.gather(task_link, task_title, task_img)


if __name__ == '__main__':
    async def main():
        async with AsyncParseData() as parser:
            await parser.main()
    asyncio.run(main())
