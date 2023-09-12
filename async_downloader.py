import aiohttp
import asyncio
import os
import time
import string
import random
from PIL import Image
from io import BytesIO
from tqdm import tqdm


def generate_unique_filename(extension='.png'):
    timestamp = int(time.time() * 1000)
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    filename = f"{timestamp}_{random_string}{extension}"
    return filename


async def download_image(url, session, directory_path, pbar):
    # Very Important. If you are using slow internet connection you may consider increasing timeout.
    timeout = aiohttp.ClientTimeout(total=30)

    try:
        async with session.get(url, timeout=timeout) as response:

            # Sprawdzenie statusu odpowiedzi
            if response.status != 200:
                print(f"Error while downloading {url}: {response.status}")
                return

            # 30 MB max for image
            if int(response.headers.get('Content-Length', 0)) > 30 * 1024 * 1024 * 1024:
                print(f"File {url} is too large according to header, skipping.")
                return

            content = bytearray()
            chunk_size = 1024 * 1024
            total_size = 0
            async for chunk in response.content.iter_chunked(chunk_size):
                total_size += len(chunk)
                if total_size > 10 * 1024 * 1024:
                    print(f"File {url} is too large during download, aborting.")
                    return
                content.extend(chunk)

            # Sprawdzenie czy odpowiedź nie jest pusta
            if not content:
                print(f"Empty response for URL: {url}")
                return

            try:
                image = Image.open(BytesIO(content))
                if image.format not in ['PNG', 'WEBP']:
                    print(f"Unsupported image format {image.format} for URL: {url}")
                    return
                extension = '.png' if image.format == 'PNG' else '.webp'
                image.close()
            except Exception as e:
                print(f"Error processing image for URL {url}: {e}")
                return

            # Zmieniamy ścieżkę zapisu pliku, aby była względem directory_path
            filename = os.path.join(directory_path, generate_unique_filename(extension))
            try:
                with open(filename, 'wb') as file:
                    file.write(content)
                # print(f"Pobrano {url} do {filename}")
                pbar.update(1)
            except Exception as e:
                print(f"Error saving image for URL {url} to {filename}: {e}")


    except aiohttp.client_exceptions.ClientConnectorError:
        print(f"Cannot connect to host for URL: {url}")
    except asyncio.TimeoutError:
        print(f"The time limit for the URL has been exceeded:{url}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading the URL{url}: {e}")


async def main_downloader_init(urls: list, keyword: str):
    directory_path = os.path.join('tmp', keyword)

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    conn = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=conn) as session:
        with tqdm(total=len(urls), desc="Downloading images") as pbar:
            tasks = [download_image(url, session, directory_path, pbar) for url in urls]
            await asyncio.gather(*tasks)
