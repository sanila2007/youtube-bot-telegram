# Copyright ©️ 2022 Sanila Ranatunga. All Rights Reserved
# You are free to use this code in any of your project, but you MUST include the following in your README.md (Copy & paste)
# ##Credits - [YouTube-Bot](https://github.com/sanila2007/YouTube_bot_telegram)

# Read GNU General Public License v3.0: https://github.com/sanila2007/YouTube_bot_telegram/blob/mai/LICENSE
# Don't forget to follow github.com/sanila2007 because I am doing these things for free and open source
# Star, fork, enjoy!


from pytube import Playlist
from pyrogram import Client, filters
from pyrogram.errors.exceptions import MessageIdInvalid
import os

PLAYLIST_REGEX = r'(.*)youtube.com/(.*)[&|?]list=(?P<playlist>[^&]*)(.*)'


@Client.on_message(filters.regex(PLAYLIST_REGEX))
async def playlist_down(bot, message):
    link = message.text
    global PLAYLIST_VID, i, chat_id
    p = Playlist(link)
    chat_id = message.chat.id
    length_of_playlist = str(p.length)
    extend = int(length_of_playlist) + 1
    i = 0
    m = await bot.send_message(message.chat.id, f"Downloading {p.title}\n\n0 completed of {length_of_playlist}")
    for x in range(extend):
        for video in p.videos:
            PLAYLIST_VID = video.streams.get_lowest_resolution().download()
            try:
                await bot.send_video(chat_id=chat_id, video=PLAYLIST_VID, caption=p.title)
                os.remove(PLAYLIST_VID)
            except Exception as ee:
                await bot.send_message(chat_id, f"Something happened!\n{ee}")
            i += 1
            try:
                if int(i) == int(length_of_playlist):
                    await m.delete()
                    await bot.send_message(message.chat.id, f"Downloaded successfully!\n\n{str(i)} completed of {length_of_playlist}")
                else:
                    await m.edit_text(f"Downloading {p.title}...\n\n{str(i)} completed of {length_of_playlist}")
            except MessageIdInvalid:
                pass
        await m.delete()


