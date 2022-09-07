import json
from script import HELP_MESSAGE
from pyrogram import Client, filters
from pyrogram.types import Message
from modules.gdrive import gdriveDownload
from modules.tg import tgDownload
from modules.ddl import ddlDownload, URLRx
from modules.cache import CacheSize, clearCache
import os
from dotenv import load_dotenv
import re
load_dotenv()

service_id_rx = re.compile("#(\d{1,2})")
authorized_list = json.loads(os.getenv('authorized_list'))

app = Client("my_account", api_id=os.getenv('api_id'),
             api_hash=os.getenv('api_hash'), bot_token=os.getenv('bot_token')

if not os.path.exists('Downloads'):
      os.makedirs('Downloads')

print("Bot started by @oVo-HxBots", flush=True)
@app.on_message(filters.text)
def echo(client, message: Message):
    if '/help' in message.text:
        message.reply(SCRIPT.HELP_MESSAGE, disable_web_page_preview=True, quote=True)
        return
    try:
        if '/up' in message.text:
            serviceID = service_id_rx.search(message.text)
            if serviceID:
                serviceID = int(serviceID.group(1))-1
                if serviceID > 13:
                    message.reply_text("Invalid Host ID")
                    return
            else:
                serviceID = int(os.getenv('default_host_id')) - 1
            if 'drive.google' in message.text:
                progressMessage =  message.reply("Please wait while I download your G-Drive file...")
                gdriveDownload(message, serviceID, progressMessage)
            elif message.reply_to_message:
                progressMessage =  message.reply("Please wait while I download your Telegram file...")
                tgDownload(message, serviceID, progressMessage)
            elif URLRx.search(message.text):
                progressMessage =  message.reply("Please wait while I download your link...")
                ddlDownload(message, serviceID, progressMessage)
        elif '/stats' in message.text:
            CacheSize(message)
        elif '/clear' in message.text:
            clearCache(message)
    except Exception as e:
        print(e, flush=True)
        message.reply(e)
        return
app.run()

