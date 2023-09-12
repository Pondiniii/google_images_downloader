from lossless_recursive_avif_encoder import process_images_in_folder, get_folder_size, calculate_size_reduction
from driver import driver_init, driver_search, driver_extract_links, wait_for_script_tag
from async_downloader import main_downloader_init
from search_query_gen import search_query_gen
import asyncio
import os

print("init chrome driver...")
driver = driver_init()

with open("words.txt", "r") as file:
    for line in file:
        keyword = line.strip()

        folder_path = os.path.join("tmp", keyword)

        if not os.path.exists(folder_path):
            print(f"There is no folder named {keyword} - Starting scraping")

            query = search_query_gen(keyword)

            driver_search(driver, query)

            wait_for_script_tag(driver)

            urls = driver_extract_links(driver)

            asyncio.run(main_downloader_init(urls, keyword))

            before_compression_folder_size = get_folder_size(folder_path)

            process_images_in_folder('tmp/')

            after_compression_folder_size = get_folder_size(folder_path)
            print(f"Original size: {before_compression_folder_size / (1024 * 1024):.2f} MB")
            print(f"Size after compression: {after_compression_folder_size / (1024 * 1024):.2f} MB")

            reduction, percentage = calculate_size_reduction(before_compression_folder_size,
                                                             after_compression_folder_size)
            print(f"Size reduced by {reduction / (1024 * 1024):.2f} MB or {percentage:.2f}%")
