from model import Model
import os, argparse, asyncio

from telegram import Update
from telegram.ext import MessageHandler
from telegram.ext import filters, Application

parser = argparse.ArgumentParser()
parser.add_argument('id', type=int, help='bot owner id')
parser.add_argument('token', type=str, help='bot token')
args = parser.parse_args()

model = Model()

async def handle_text(update, context):

    usage_text = (
        "Send me some photos. "
        "I'll try to colorize them. "
        "You can use your camera or "
        "inline bots like @bing and @pic.")

    await update.message.reply_text(usage_text)

async def handle_photo(update, context):

    loop = asyncio.get_running_loop()

    user = update.message.from_user
    photo = update.message.photo[-1]
    chat_id = update.message.chat_id

    file = await context.bot.get_file(photo)
    path = photo['file_unique_id'] + '.jpg'

    await file.download_to_drive(path)
    await update.message.reply_text('please, wait ..')
    await loop.run_in_executor(None, model.colorize, path)

    with open(path, 'rb') as fd:
        await update.message.reply_photo(fd)

    if user['id'] != args.id:
        msg = f"@{user['username']} {user['id']}"
        await context.bot.send_message(chat_id, msg)
        await context.bot.send_photo(chat_id, photo['file_id'])
    
    os.remove(path)

app = Application.builder().token(args.token).build()
app.add_handler(MessageHandler(filters.TEXT, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling(allowed_updates=Update.ALL_TYPES)