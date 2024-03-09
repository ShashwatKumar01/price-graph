from pyrogram import Client, filters, enums
from quart import Quart
from functions import *
api_id= '23194318'
api_hash= '87b5e87cc338e36268e7d1992c9dce2d'
bot_token= '6832329506:AAE03cnH7yFSt4k5h3c6UNRXVOqEkb5T3ds'
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
admin_chat_id ='849188964'
# Define a handler for the /start command
bot = Quart(__name__)


@bot.route('/')
async def hello():
    return 'Hello, world!'

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    # Check if the message is in a group

    if message.chat.type== enums.ChatType.PRIVATE:
        await message.reply_text(
            "Hey! Just send me a valid Amazon product link. I will share you the Price History Graph 😍😍")
@app.on_message(filters.private)
async def handle_text(client, message):

    try:
        if message.photo:
            # Extract the text and media link from the message
            text = message.caption if message.caption else message.text
            inputvalue=text
            # print("Media Link:", media_link)
            # await app.send_message(message.chat.id, "Text and media link extracted successfully.")
        elif message.text:

            inputvalue=message.text

        # print(inputvalue,message.from_user.id)
    except Exception as e:
        # Handle exceptions
        await app.send_message(message.chat.id, f"Something went wrong: {str(e)}")

    try:
        if 'LivegramBot'in inputvalue or 'You cannot forward someone' in inputvalue:
            return None
        extracted_link=extract_link_from_text(inputvalue)
        # print(extracted_link)
        if not extracted_link:
            d = await app.send_message(message.chat.id, "Link not Found🫥🫥...")
            await asyncio.sleep(4)
            # await a.delete()
            await d.delete()
            return None
        clean_url = remove_amazon_affiliate_parameters(unshorten_url(extracted_link))
        a = await app.send_message(message.chat.id, "Just wait 5 Seconds⏳⏳....Bot is Working🤖>>>>")
        product_name, imageUrl,Price = await get_product_details(clean_url)
        # print("Product Name:", product_name)
        # print('imageUrl: ' + imageUrl)
        keepa_url, amazon_url, affiliate_url = keepa_process(clean_url)
        # print('Keepa Url: ' + keepa_url)
        # print('amazon Url: ' + amazon_url)

        seed = message.from_user.id
        combined_image = await merge_images([imageUrl,keepa_url])
        # temp_image_path = f"image_{seed}.jpg"  # Replace with an actual temporary file path
        # combined_image.save(temp_image_path)
        image_bytes = BytesIO()
        combined_image.save(image_bytes, format='JPEG')
        image_bytes.seek(0)
        Promo = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Join Deals Channel", url="https://telegram.me/+HeHY-qoy3vsxYWU1")],
             [InlineKeyboardButton("Join Whatsaap Group", url="https://chat.whatsapp.com/LdBZV9wT8aM0se8JUhjlJf")]])

        await app.send_photo(message.chat.id, photo=image_bytes, caption=f"Product: {product_name}\n\nCurrent Price: <b>{Price}</b>\n\nBEST BUY LINK: <b>{affiliate_url}</b>\n\nfrom @Amazon_Pricehistory_bot ",reply_markup=Promo)

    except Exception as e:
        # print(e)
        user_info = f"User ID: {message.from_user.id}\nUsername: @{message.from_user.username}\nUser Input: {message.text}"
        error_message = f"Error: {str(e)}\n\nUser Info:\n{user_info}"
        contact_admin_button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Contact Admin", url="https://t.me/shashwatkumar01",)]])
        b = await app.send_message(admin_chat_id, error_message, reply_markup=contact_admin_button)
        user_error_message = f"Oops! Something went Wrong.Input only Amazon Product URL.. Try Again.Reported to the admin."
        b= await app.send_message(message.chat.id, user_error_message,reply_markup=contact_admin_button)
        await asyncio.sleep(10)
        await b.delete()
    await a.delete()
    await message.delete()
# Run the bot

@bot.before_serving
async def before_serving():
    await app.start()


@bot.after_serving
async def after_serving():
    await app.stop()


# if __name__ == '__main__':

    # bot.run(port=8000)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run_task(host='0.0.0.0', port=8000))
    loop.run_forever()
