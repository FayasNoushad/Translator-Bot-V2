from pyrogram import Client, filters
from googletrans import Translator

FayasNoushad = Client(
    "Translator Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

TRANSLATOR = Translator()

@FayasNoushad.on_message(filters.private & filters.text)
async def translate(bot, update):
    if " | " in update.text:
        text, language = update.text.split(" | ", -1)
    else:
        return
    translate = TRANSLATOR.translate(text, dest=language)
    try:
        await update.reply_text(
            text=translate.text
        )
    except Exception as error:
        print(error)

FayasNoushad.run()
