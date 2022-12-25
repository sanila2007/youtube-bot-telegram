from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🔍Search YouTube", switch_inline_query_current_chat="")
        ]
    ]
)


@Client.on_message(filters.command("help") & filters.private)
async def help(bot, message):
    await message.reply(
        "This bot can search for YouTube videos & download YouTube videos, playlists and more. Use below methods to do these\n\n"
        "◉ Search for videos - <i>Use inline mode</i>\n"
        "◉ Download videos - <i>Send any link of a Youtube video and select a quality</i>\n"
        "◉ Download videos from playlist - <i>Send any link of a YouTube playlist</i>\n\nThis is quite simple. ||Enjoy it!!||\nAny issues? ",
        reply_markup=BUTTONS
    )
