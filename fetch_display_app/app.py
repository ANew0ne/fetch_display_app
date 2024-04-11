import asyncio
import json
from http import HTTPStatus

import httpx


URL = 'https://jsonplaceholder.typicode.com/posts/1'


class FetchDisplayData:
    """A class to fetch and display data asynchronously from a given URL."""

    def __init__(self, url):
        self.client = httpx.AsyncClient()
        self.data = None
        self.url = url

    async def fetch_data(self):
        """Fetch data asynchronously from the URL."""
        try:
            response = await self.client.get(self.url)
            if response.status_code == HTTPStatus.OK:
                self.data = response.json()
            else:
                print('Error during data fetching: '
                      f'{response.status_code}')
        except httpx.RequestError as e:
            print(f'Error during query execution: {e}')

    async def display_data(self):
        """Display fetched data."""
        try:
            if self.data:
                print(json.dumps(self.data, indent=4))
            else:
                print('No data available.')
        except Exception as e:
            print(f'Error occurred during data display: {e}')

    async def fetch_loop(self):
        """Loop to fetch data at intervals."""
        while True:
            fetch_task = asyncio.create_task(self.fetch_data())
            await asyncio.sleep(5)
            fetch_task.cancel()

    async def display_loop(self):
        """Loop to display fetched data."""
        while True:
            asyncio.create_task(self.display_data())
            await asyncio.sleep(1)

    async def gather_tasks(self):
        """Gather and run fetch and display loops."""
        fetch_task = asyncio.create_task(self.fetch_loop())
        display_task = asyncio.create_task(self.display_loop())
        await asyncio.gather(fetch_task, display_task)


async def main():
    fetch_display_data = FetchDisplayData(URL)
    task = asyncio.create_task(fetch_display_data.gather_tasks())
    while True:
        command = await asyncio.get_event_loop().run_in_executor(
            None, input, 'To end the programm enter E:\n\n'
        )
        if command.lower() == 'e':
            task.cancel()
            break


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
