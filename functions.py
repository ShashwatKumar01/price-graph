import urllib
import asyncio
from PIL import Image ,ImageDraw,ImageFont
from io import BytesIO
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
import time
import requests as request
from urllib.parse import urlparse, parse_qs, urlunparse
import requests
import tgcrypto
import re
import aiohttp


def extract_link_from_text(text):
    # Regular expression pattern to match a URL
    url_pattern = r'https?://\S+'

    # Find all URLs in the text
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None

def unshorten_url(short_url):

    response = requests.head(short_url, allow_redirects=True,timeout=2)

    return response.url


def remove_amazon_affiliate_parameters(url):
    parsed_url = urlparse(url)
    # print(parsed_url)
    query_params = parse_qs(parsed_url.query)
    # print('query_params: '+str(query_params))
    if 'ru' in query_params:
        query_params={key: value for key, value in query_params.items() if key == 'ru'}
        parsed_url = urlparse(query_params['ru'][0])
        query_params = parse_qs(parsed_url.query)


    # List of Amazon affiliate parameters to remove
    amazon_affiliate_params = ['tag', 'ref', 'linkCode', 'camp', 'creative','linkId','ref_','language','content-id','_encoding']

    # Remove the Amazon affiliate parameters from the query parameters
    cleaned_query_params = {key: value for key, value in query_params.items() if key not in amazon_affiliate_params}
    # Rebuild the URL with the cleaned query parameters
    cleaned_url = urlunparse(parsed_url._replace(query='&'.join([f'{key}={value[0]}' for key, value in cleaned_query_params.items()])))

    return cleaned_url

def create_amazon_affiliate_url(normal_url, affiliate_tag):
    if "amazon" not in normal_url:
        return "Not a valid Amazon Product link."

    if not affiliate_tag:
        return "Please provide a valid affiliate tag."

    # Check if the URL already has query parameters
    separator = '&' if '?' in normal_url else '?'

    # Append the affiliate tag to the URL
    affiliate_url = f"{normal_url}{separator}tag={affiliate_tag}"

    return affiliate_url

def keepa_process(url):
# Extract the country code using regular expressions
    country_code_match = re.search(r"amazon\.(\w+)/", url)
    country_code = country_code_match.group(1) if country_code_match else None
    # Extract the product code using regular expressions
    product_code_match = re.search(r"/product/([A-Za-z0-9]{10})", url)

    product_code_match2 = re.search(r'/dp/([A-Za-z0-9]{10})', url)
    product_code = product_code_match.group(1) if product_code_match else product_code_match2.group(1)

    print("Product Code:", product_code)
    print("Country Code:", country_code)

    keepa_url=f'https://graph.keepa.com/pricehistory.png?asin={product_code}&domain={country_code}'

    amazon_url=f'https://www.amazon.{country_code}/dp/{product_code}'
    affiliate_url=create_amazon_affiliate_url(amazon_url,affiliate_tag='highfivesto0c-21' if country_code=='in'else 'highfivesto0c-20')

    return keepa_url,amazon_url,affiliate_url
# def get_product_details(url):
#     amazon_img_url = ''
#     amazon_product_name = ''
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#     }
#     retries = 1
#     for i in range(40):
#         if 'amazon' not in url:
#             break
#         print(i)
#         response =  requests.get(url, headers=headers)
#         print(response)
#         # print(response.text)
#
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             product_title =  soup.find('span', {'id': 'productTitle'})
#             product_image= soup.find('img', {'id': 'landingImage'})
#             price_element = soup.find('span', {'class': 'a-offscreen'})
#             unavailable_element = soup.find(lambda tag: tag.name == 'span' and
#                                            tag.get('class') == ['a-size-medium a-color-success'] and
#                                            tag.text.strip() == 'Currently unavailable.')
#
#             if product_image:
#                 img_url=product_image.get('src')
#                 if not amazon_img_url:
#                     amazon_img_url=img_url
#                     # response = requests.get(amazon_img_url)
#                     # img = Image.open(BytesIO(response.content))
#                     #
#                     # img.show()
#             if product_title:
#                 amazon_product_name=product_title.text.strip()
#                 if unavailable_element:
#                     price_element ='Out Of Stock'
#                 elif price_element:
#                     price_element=price_element.text.strip()
#                 else:
#                     price_element='Unable to get Price'
#                 # price_element=price_element.text.strip()
#                 return amazon_product_name, amazon_img_url,price_element
#                 break
#                 if i==29:
#                     return 'Product Name unable to Scrap',''
#
#             else:
#                 None
#
#              # get_product_name(url)
#         elif response.status_code == 503:
#             print("503 Error: Server busy, retrying...")
#             break
#             return amazon_product_name, amazon_img_url, price_element
#               # Wait for a while before retrying
#
#         elif response.status_code == 404:
#             print("Error 404:", response.status_code)
#             break
#         else:
#             None
#
#     return None
async def get_product_details(url):
    amazon_img_url = ''
    amazon_product_name = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    async with aiohttp.ClientSession() as session:
        retries = 1
        for i in range(40):
            print(i)
            if 'amazon' not in url:
                break

            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    product_title = soup.find('span', {'id': 'productTitle'})
                    product_image = soup.find('img', {'id': 'landingImage'})
                    price_element = soup.find('span', {'class': 'a-offscreen'})
                    unavailable_element = soup.find(lambda tag: tag.name == 'span' and
                                                     tag.get('class') == ['a-size-medium a-color-success'] and
                                                     tag.text.strip() == 'Currently unavailable.')

                    if product_image:
                        img_url = product_image.get('src')
                        if not amazon_img_url:
                            amazon_img_url = img_url

                    if product_title:
                        amazon_product_name = product_title.text.strip()

                        if unavailable_element:
                            price_element = 'Out Of Stock'
                        elif price_element:
                            price_element = price_element.text.strip()
                        else:
                            price_element = 'Unable to get Price'

                        return amazon_product_name, amazon_img_url, price_element

                elif response.status == 503:
                    print("503 Error: Server busy, retrying...")
                    break

                elif response.status == 404:
                    print("Error 404:", response.status)
                    break

            await asyncio.sleep(1)  # Wait before retrying

    return None

import requests
from PIL import Image
from io import BytesIO


def resize_image(image, target_size):
    # Resize the image while preserving aspect ratio
    width_percent = target_size[0] / float(image.width)
    height_percent = target_size[1] / float(image.height)
    resize_percent = min(width_percent, height_percent)
    new_width = int(image.width * resize_percent)
    new_height = int(image.height * resize_percent)
    return image.resize((new_width, new_height), Image)


async def merge_images(image_urls):
    images = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    for url in image_urls:
        img=None
        if 'https:/' in url :
            response = requests.get(url,headers=headers)
            if response.status_code==200:
                img = Image.open(BytesIO(response.content))
                if 'https://graph' in url:
                    width, height = img.size
                    new_width = width - 80  # Adjust the amount to be cropped from the right as needed
                    img = img.crop((0, 0, new_width, height))
        if img:
            images.append(img)
    print('image count:', len(images))
    if len(images)==2:
        # Determine the size of the combined image
        total_width = sum(img.width for img in images)
        max_height = max(img.height for img in images)

        # Create a new blank image with the combined size
        combined_image = Image.new('RGB', (total_width, max_height))

        # Paste each image into the combined image
        x_offset = 0
        for img in images:
            combined_image.paste(img, (x_offset, 0))
            x_offset += img.width

        draw = ImageDraw.Draw(combined_image)
        font = ImageFont.load_default()  # You can use a custom font if needed

        text_position = (combined_image.width - 210, combined_image.height - 60)
        draw.text(text_position, 'Web:  dealsanddiscounts.in\nTelegram:   deals_and_discounts_channel', fill="white", font=font)
        return combined_image
    # Display or save the combined image
    # combined_image.show()
    else:
        return images[0].convert('RGB')


