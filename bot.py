import torch
import warnings
import telegram
import telegram.ext

from secret import *
from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import get_image_colorizer

torch.hub.set_dir('models')
warnings.filterwarnings('ignore')
torch.backends.cudnn.benchmark = True
device.set(device=DeviceId.CPU) # GPU0
colorizer = get_image_colorizer(artistic=False)

def handle_photo(update, context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    file_id = update.message.photo[-1]['file_id']
    context.bot.getFile(file_id).download('in.jpg')
    context.bot.send_message(chat_id, 'please, wait (~15s)')
    
    if user['id'] != TG_BOT_OWNER_ID:
        msg = f"@{user['username']} {user['id']}"
        context.bot.send_message(TG_BOT_OWNER_ID, msg)

    colorizer.get_transformed_image(
        'in.jpg', render_factor=35, 
        watermarked=False).save('out.jpg')
    
    with open('out.jpg', 'rb') as fd:
        context.bot.send_photo(chat_id, fd)

f = telegram.ext.Filters.photo
h = telegram.ext.MessageHandler
u = telegram.ext.Updater(TG_BOT_TOKEN)
u.dispatcher.add_handler(h(f,handle_photo))
u.start_polling(); u.idle()