from pyrogram import Client, filters, enums

from functions import *
api_id= '23194318'
api_hash= '87b5e87cc338e36268e7d1992c9dce2d'
bot_token= '6832329506:AAE03cnH7yFSt4k5h3c6UNRXVOqEkb5T3ds'
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
admin_chat_id ='849188964'
# Define a handler for the /start command

@app.on_message(filters.command("start") & (filters.private | filters.group))
async def start(client, message):
    # Check if the message is in a group
    if message.chat.type== enums.ChatType.PRIVATE:
        await message.reply_text(
            "Hey! Just send me a valid Amazon product link. I will share you the Price History Graph 😍😍")
    else:
        chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
        is_admin = chat_member.status in ["administrator", "OWNER"]
        if is_admin:
            message.reply_text(
                "Hey! Just send me a valid Amazon product link. I will share you the Price History Graph 😍😍")
        else:
            message.reply_text("Sorry, only group admins can use this command.")
    # await message.reply_text("Hey! Just Send me a valid amazon product link.I will share you the Price History Graph😍😍")

# Defin

@app.on_message(filters.private | filters.group)
async def handle_text(client, message):
    a=await app.send_message(message.chat.id,"Just wait 5 Seconds⏳⏳....Bot is Working🤖>>>>")
    try:
        if message.photo:
            # Extract the text and media link from the message
            text = message.caption if message.caption else message.text
            inputvalue=text
            # print("Media Link:", media_link)
            # await app.send_message(message.chat.id, "Text and media link extracted successfully.")
        elif message.text:
            inputvalue=message.text

        # print(inputvalue)
    except Exception as e:
        # Handle exceptions
        await app.send_message(message.chat.id, f"Something went wrong: {str(e)}")

    # await a.delete()
    try:
        extracted_link=extract_link_from_text(inputvalue)
        # print(extracted_link)
        if not extracted_link:
            d = await app.send_message(message.chat.id, "Link not Found🫥🫥...")
            await asyncio.sleep(4)
            await a.delete()
            await d.delete()
            return None
        clean_url = remove_amazon_affiliate_parameters(unshorten_url(extracted_link))

        product_name, imageUrl,Price = await get_product_details(clean_url)
        # print("Product Name:", product_name)
        # print('imageUrl: ' + imageUrl)
        keepa_url, amazon_url, affiliate_url = keepa_process(clean_url)
        # print('Keepa Url: ' + keepa_url)
        # print('amazon Url: ' + amazon_url)


        # image = Image.open(BytesIO(response.content))
        combined_image = merge_images([imageUrl,keepa_url])
        temp_image_path = "image.jpg"  # Replace with an actual temporary file path
        combined_image.save(temp_image_path)
        Promo = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Join Deals Channel", url="https://telegram.me/+HeHY-qoy3vsxYWU1")],
             [InlineKeyboardButton("Join Whatsaap Group", url="https://chat.whatsapp.com/LdBZV9wT8aM0se8JUhjlJf")]])

        await app.send_photo(message.chat.id, temp_image_path, caption=f"Product: {product_name}\n\nCurrent Price: <b>{Price}</b>\n\nBEST BUY LINK: <b>{affiliate_url}</b>\n\nfrom @Amazon_Pricehistory_bot ",reply_markup=Promo)

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
app.run()


# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# }
# response = request.get(keepa_url,headers=headers)
#
# image = Image.open(BytesIO(response.content))
# image.show()
