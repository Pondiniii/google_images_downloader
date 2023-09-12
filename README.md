
---

# Google Images Downloader

A robust scraper designed to download images from Google with ease and efficiency.

## File Descriptions:

- **async_downloader.py**: This script enables asynchronous downloading of images. It incorporates time limits, security features, image verification, and monitors the number of megabytes downloaded.

- **driver.py**: Contains key functions for the `undetected_chromedriver` and `selenium`. It initializes the driver, contains regex for finding image URLs, and checks if it's necessary to click the "reject all" button on Google's page.

- **enc_test.py**: Here, I tested the performance of the `avif_test` plugin for Pillow against ImageMagick. From my findings, the plugin proved superior.

- **lossless_recursive_avif_encoder.py**: Contrary to its name, this script is not completely lossless. However, it aids in drastically reducing image file size post-download using the AVIF codec.

- **RUN**: Utilizes functions from all the files mentioned above to assemble the scraper.

- **search_query_gen.py**: Generates the Google Images URL based on your search query. This function can be modified to produce more tailored image search results.

- **words.txt**: A dictionary containing the phrases you wish to use for downloading images.

## Why was this created?

Many scrapers available were subpar. This minimalist scraper can easily be tailored to your needs. It was primarily developed to fetch several million images for dataset creation.

## How it works:

Images will be saved in a "tmp" directory, categorized by their query name.

## Compatibility:

I haven't tested this on Windows, but it runs smoothly on Ubuntu 22.04.

## Pro Tips:
- Consider using the `--user-profile-path` option with undetected chromium to decrease the likelihood of detection.

## Useful Resources:
- [Google Advanced Image Search](https://www.google.com/advanced_image_search)

---