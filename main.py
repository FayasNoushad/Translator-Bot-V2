import os
from vars import *
from googletrans import Translator
from googletrans.constants import LANGUAGES
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


Bot = Client(
    "Translator Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)


START_TEXT = """Hello {},

I am a google translator telegram bot. I can translate text to any language."""

HELP_TEXT = """**More Help**

- Just send a text/message to translate.
- And select a language for translating"""

ABOUT_TEXT = """**About Me**

- **Bot :** `Translator Bot V2`
- **Creator :** [GitHub](https://github.com/FayasNoushad) | [Telegram](https://telegram.me/FayasNoushad)
- **Source :** [Click here](https://github.com/FayasNoushad/Translator-Bot-V2)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Feedback', url='https://telegram.me/FayasNoushad')
        ],
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
CLOSE_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton('Close', callback_data='close')]]
)
TRANSLATE_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton('⚙ Feedback ⚙', url='https://telegram.me/FayasNoushad')]]
)


def language_buttons():
    pages = []
    button_limit = 2
    line_limit = 8
    for language in LANGUAGES:
        button = InlineKeyboardButton(text=LANGUAGES[language].capitalize(), callback_data=language)
        if len(pages) == 0 or len(pages[-1]) >= line_limit and len(pages[-1][-1]) >= button_limit:
            pages.append([[button]])
        elif len(pages[-1]) == 0 or len(pages[-1][-1]) >= button_limit:
            pages[-1].append([button])
        else:
            pages[-1][-1].append(button)
    page_no = 0
    no_buttons = []
    if len(pages) == 1:
        return pages
    for page in pages:
        page_no += 1
        page_buttons = []
        if page == pages[0]:
            page_buttons.append(
                InlineKeyboardButton(
                    text="-->",
                    callback_data="page+"+str(page_no+1)
                )
            )
        elif page == pages[-1]:
            page_buttons.append(
                InlineKeyboardButton(
                    text="<--",
                    callback_data="page+"+str(page_no-1)
                )
            )
        else:
            page_buttons.append(
                InlineKeyboardButton(
                    text="<--",
                    callback_data="page+"+str(page_no-1)
                )
            )
            page_buttons.append(
                InlineKeyboardButton(
                    text="-->",
                    callback_data="page+"+str(page_no+1)
                )
            )
        pages[page_no-1].append(page_buttons)
        no_buttons.append(
            InlineKeyboardButton(
                text=str(page_no),
                callback_data="page+"+str(page_no)
            )
        )
        pages[page_no-1].append(no_buttons)
    return pages


CUSTOM_LANGUAGE_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("മലയാളം", callback_data="Malayalam"),
            InlineKeyboardButton("தமிழ்", callback_data="Tamil"),
            InlineKeyboardButton("हिन्दी", callback_data="Hindi")
        ],
        [
            InlineKeyboardButton("ಕನ್ನಡ", callback_data="Kannada"),
            InlineKeyboardButton("తెలుగు", callback_data="Telugu"),
            InlineKeyboardButton("मराठी", callback_data="Marathi")
        ],
        [
            InlineKeyboardButton("ગુજરાતી", callback_data="Gujarati"),
            InlineKeyboardButton("ଓଡ଼ିଆ", callback_data="Odia"),
            InlineKeyboardButton("বাংলা", callback_data="bn")
        ],
        [
            InlineKeyboardButton("ਪੰਜਾਬੀ", callback_data="Punjabi"),
            InlineKeyboardButton("فارسی", callback_data="Persian"),
            InlineKeyboardButton("English", callback_data="English")
        ],
        [
            InlineKeyboardButton("español", callback_data="Spanish"),
            InlineKeyboardButton("français", callback_data="French"),
            InlineKeyboardButton("русский", callback_data="Russian")
        ],
        [
            InlineKeyboardButton("עִברִית", callback_data="hebrew"),
            InlineKeyboardButton("العربية", callback_data="arabic")
        ]
    ]
)

LANGUAGE_BUTTONS = InlineKeyboardMarkup(
    language_buttons()[0]
)

@Bot.on_callback_query()
async def cb_data(bot, message):
    if message.data == "home":
        await message.message.edit_text(
            text=START_TEXT.format(message.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif message.data == "help":
        await message.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif message.data == "about":
        await message.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    elif message.data == "close":
        await message.message.delete()
    elif message.data.startswith("page+"):
        await message.answer("Processing")
        page_no = int(message.data.split("+")[1]) - 1
        await message.message.edit_reply_markup(
            InlineKeyboardMarkup(
                language_buttons()[page_no]
            )
        )
    else:
        await message.message.edit_text("`Translating...`")
        text = message.message.reply_to_message.text
        language = message.data
        translator = Translator()
        try:
            translate = translator.translate(text, dest=language)
            lang_text = f"{LANGUAGES[language].capitalize()} ({language})"
            translate_text = f"**Translated to {lang_text}**"
            translate_text += f"\n\n{translate.text}"
            if len(translate_text) < 4096:
                await message.message.edit_text(
                    text=translate_text,
                    disable_web_page_preview=True,
                    reply_markup=TRANSLATE_BUTTON
                )
            else:
                with BytesIO(str.encode(str(translate_text))) as translate_file:
                    translate_file.name = language + ".txt"
                    await message.reply_document(
                        document=translate_file,
                        reply_markup=TRANSLATE_BUTTON
                    )
                await message.delete()
        except Exception as error:
            print(error)
            await message.edit_text("Something wrong.")


@Bot.on_message(filters.command(["start"]))
async def start(bot, message):
    text = START_TEXT.format(message.from_user.mention)
    reply_markup = START_BUTTONS
    await message.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.command(["help"]))
async def help(bot, message):
    text = HELP_TEXT
    reply_markup = HELP_BUTTONS
    await message.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.command(["about"]))
async def about(bot, message):
    text = ABOUT_TEXT
    reply_markup = ABOUT_BUTTONS
    await message.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


# Language list
@Bot.on_message(filters.command(["list", "languages", "langs", "languages_list"]))
async def languages_list(bot, message):
    languages = LANGUAGES
    languages_text = "**Languages**\n"
    for language in languages:
        languages_text += f"\n`{languages[language].capitalize()}` -> `{language}`"
    await message.reply_text(
        text=languages_text,
        disable_web_page_preview=True,
        reply_markup=TRANSLATE_BUTTON,
        quote=True
    )


@Bot.on_message(filters.private & filters.text)
async def translate(bot, message):
    # to avoid command only messages
    if message.text.startswith("/") and len(message.text) == 1:
        return
    buttons = CUSTOM_LANGUAGE_BUTTONS if CUSTOM else LANGUAGE_BUTTONS
    await message.reply_text(
        text="Select a language below for translating",
        disable_web_page_preview=True,
        reply_markup=buttons,
        quote=True
    )


Bot.run()
