from pytube import Playlist
from pyrogram import Client, filters
from pyrogram.errors.exceptions import MessageIdInvalid
import os
from moviepy.editor import *

PLAYLIST_REGEX = r'(.*)youtube.com/(.*)[&|?]list=(?P<playlist>[^&]*)(.*)'


@Client.on_message(filters.command("playlist_aud"))
async def playlist_aud(bot, message):
    link = message.text[12:]
    global PLAYLIST_AUD, chat_id
    p_aud = Playlist(link)
    chat_id = message.chat.id
    lenth_of_playlist = str(p_aud.length)
    extend = int(lenth_of_playlist)
    f = 0
    m = await bot.send_message(message.chat.id,
                               f"Downloading {p_aud.title} **(Audio)**\n\n0 completed of {lenth_of_playlist}")
    for audio in p_aud.videos:
        PLAYLIST_AUD = audio.streams.get_audio_only().download(output_path="downloads")
        try:
            await bot.send_audio(chat_id=chat_id, audio=PLAYLIST_AUD, caption=audio.title + ".mp3",
                                 file_name=audio.title + ".mp3",
                                 duration=audio.length, performer=audio.author)
            os.remove(PLAYLIST_AUD)
        except Exception as error_aud:
            await bot.send_message(chat_id, f"Something happened!\n{error_aud}")
        f += 1
        try:
            if int(f) == int(lenth_of_playlist):
                await m.delete()
                await bot.send_message(message.chat.id,
                                       f"Downloaded successfully! **(Audio)**\n\n{str(f)} completed of {lenth_of_playlist}")
            else:
                await m.edit_text(
                    f"Downloading {p_aud.title}...\n\n{str(f)} completed of {lenth_of_playlist}")
        except MessageIdInvalid:
            pass
    await m.delete()


@Client.on_message(filters.regex(PLAYLIST_REGEX))
async def playlist_down(bot, message):
    link = message.text
    global PLAYLIST_VID, i, chat_id
    p = Playlist(link)
    chat_id = message.chat.id
    length_of_playlist = str(p.length)
    extend = int(length_of_playlist)
    i = 0
    m = await bot.send_message(message.chat.id, f"Downloading {p.title}\n\n0 completed of {length_of_playlist}")
    for video in p.videos:
        PLAYLIST_VID = video.streams.get_lowest_resolution().download(output_path="downloads")
        try:
            await bot.send_video(chat_id=chat_id, video=PLAYLIST_VID, caption=p.title)
            os.remove(PLAYLIST_VID)
        except Exception as ee:
            await bot.send_message(chat_id, f"Something happened!\n{ee}")
        i += 1
        try:
            if int(i) == int(length_of_playlist):
                await m.delete()
                await bot.send_message(message.chat.id,
                                       f"Downloaded successfully!\n\n{str(i)} completed of {length_of_playlist}")
            else:
                await m.edit_text(f"Downloading {p.title}...\n\n{str(i)} completed of {length_of_playlist}")
        except MessageIdInvalid:
            pass
    await m.delete()
