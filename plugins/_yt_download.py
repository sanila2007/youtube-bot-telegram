from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from youtubesearchpython import VideosSearch
from pytube import YouTube
import os


START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🔍Search YouTube", switch_inline_query_current_chat="")
        ]
    ]
)


@Client.on_inline_query()
async def inlinequery(client, inline_query):
    global search_yt
    search_yt = inline_query.query
    answer = []
    video = VideosSearch(search_yt, limit=10).result()
    yt_title = video["result"][0]["title"]
    yt_views = video["result"][0]["viewCount"]["short"]
    yt_duration = video["result"][0]["duration"]
    yt_publish = video["result"][0]["publishedTime"]
    yt_channel = video["result"][4]["channel"]["name"]
    global yt_link
    yt_link = video["result"][0]["link"]
    if inline_query.query == "":
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Search any YouTube video...",
                    input_message_content=InputTextMessageContent("Search Youtube Videos..."),
                    description="Type to search!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Search Videos...", switch_inline_query_current_chat="")
                            ]
                        ]
                    )
                )
            ]
        )
    elif inline_query.chat_type == inline_query.chat_type.BOT:
        print(len(list(video)))
        for i in range(len(list(video))):
            answer.append(
                InlineQueryResultArticle(
                    title=video["result"][i]["title"],
                    thumb_url=video["result"][i]["thumbnails"][0]["url"],
                    description=video["result"][i]["viewCount"]["short"],
                    input_message_content=InputTextMessageContent(
                        f"📝**Title:-** {yt_title}\n👁️‍🗨️**Views:-** {yt_views}\n⌛**Duration:-** {yt_duration}\n📅**Published:-** {yt_publish}\n📢**Published by:-** {yt_channel}\n📽️**Watch Video:-** <a href={yt_link}>Click here</a>"),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🎥Watch on YouTube", url=yt_link),
                                InlineKeyboardButton("🔍Search again", switch_inline_query_current_chat="")
                            ],
                            [
                                InlineKeyboardButton("📁Download", callback_data="link_down")
                            ]
                        ]
                    ),
                )

            ),
    elif inline_query.chat_type != inline_query.chat_type.BOT:
        for i in range(7):
            answer.append(
                InlineQueryResultArticle(
                    title=video["result"][0]["title"],
                    thumb_url=video["result"][1]["thumbnails"][0]["url"],
                    description=video["result"][0]["viewCount"]["short"],
                    input_message_content=InputTextMessageContent(
                        f"📝**Title:-** {yt_title}\n👁️‍🗨️**Views:-** {yt_views}\n⌛**Duration:-** {yt_duration}\n📅**Published:-** {yt_publish}\n📢**Published by:-** {yt_channel}\n📽️**Watch Video:-** <a href={yt_link}>Click here</a>"),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🎥Watch on YouTube", url=yt_link),
                                InlineKeyboardButton("🔍Search again", switch_inline_query_current_chat="")
                            ]
                        ]
                    ),
                )

            )
    await inline_query.answer(
        results=answer,
        cache_time=1
    )


QUALITY_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("📽️High Quality", callback_data="highest_res"),
            InlineKeyboardButton("📽️720p", callback_data="720p")
        ],
        [
            InlineKeyboardButton("📽️Low Quality", callback_data="lowest_res"),
            InlineKeyboardButton("📽️480p", callback_data="480p")
        ],
        [
            InlineKeyboardButton("🎵Audio", callback_data="audio"),
            InlineKeyboardButton("📽️360p", callback_data="360p")
        ]
    ]
)

yt_regex = r'(.*)youtube.com/(.*)[&|?]v=(?P<video>[^&]*)(.*)'


@Client.on_message(filters.regex(yt_regex))
async def yt_download(bot, message):
    global chat_id
    chat_id = message.chat.id
    global link
    link = message.text
    dur = VideosSearch(link, limit=1).result()
    _duration = dur["result"][0]["duration"]
    reply_markup = QUALITY_BUTTONS
    await bot.send_message(message.chat.id, f"Select your preferred format\n\nDuration: {str(_duration)}",
                           reply_markup=reply_markup)


@Client.on_callback_query()
async def callback_query(Client, CallbackQuery):
    ## Download videos at the highest resolution
    if CallbackQuery.data == "highest_res":
        youtube_high = YouTube(link)
        high_vid = youtube_high.streams.get_highest_resolution().download(output_path="downloads")
        m = await CallbackQuery.edit_message_text(
            "Downloading."
        )
        m.delete()
        try:
            await Client.send_video(chat_id, high_vid, caption=youtube_high.title)
            print("success")
        except Exception as error:
            await Client.send_message(chat_id, f"Error occurred:\n<i>{error}</i>")
        os.remove(high_vid)
        await m.delete()
    ## Download videos at the lowest resolution
    elif CallbackQuery.data == "lowest_res":
        youtube_less = YouTube(link)
        less_vid = youtube_less.streams.get_lowest_resolution().download(output_path="downloads")
        m = await CallbackQuery.edit_message_text(
            "Downloading..."
        )
        try:
            await Client.send_video(chat_id, less_vid, caption=youtube_less.title)
        except Exception as error:
            await Client.send_message(chat_id, f"Error occurred!!\n<i>{error}</i>")
        os.remove(less_vid)
        await m.delete()
    ## Download audio
    elif CallbackQuery.data == "audio":
        youtube_audio = YouTube(link)
        aud = youtube_audio.streams.get_audio_only().download(output_path="downloads")
        m = await CallbackQuery.edit_message_text(
            "Downloading..."
        )
        try:
            await Client.send_audio(chat_id, aud, caption=youtube_audio.title, performer=youtube_audio.author, duration=youtube_audio.length)
        except Exception as error:
            await Client.send_message(chat_id, f"Something happened!\n<i>{error}</i>")
        os.remove(aud)
        await m.delete()
    ## 720p
    elif CallbackQuery.data == "720p":
        youtube_720 = YouTube(link)
        vid_720 = youtube_720.streams.get_by_resolution("720p").download("downloads")
        m = await CallbackQuery.edit_message_text(
            "Downloading..."
        )
        try:
            await Client.send_video(chat_id, vid_720, caption=youtube_720.title)
        except Exception as error:
            await Client.send_message(chat_id, f"Error occurred!!\n<i>{error}</i>")
        os.remove(vid_720)
        await m.delete()
    ## 360p
    elif CallbackQuery.data == "360p":
        youtube_360 = YouTube(link)
        vid_360 = youtube_360.streams.get_by_resolution("360p").download("downloads")
        m = await CallbackQuery.edit_message_text(
            "Downloading..."
        )
        try:
            await Client.send_video(chat_id, vid_360, caption=youtube_360.title)
        except Exception as error:
            await Client.send_message(chat_id, f"Error occurred!!\n<i>{error}</i>")
        os.remove(vid_360)
        await m.delete()
    ## 480p
    elif CallbackQuery.data == "480p":
        youtube_480 = YouTube(link)
        vid_480 = youtube_480.streams.get_lowest_resolution().download(output_path="downloads")
        m = await CallbackQuery.edit_message_text(
            "Downloading..."
        )
        try:
            await Client.send_video(chat_id, vid_480, caption=youtube_480.title)
        except Exception as error:
            await Client.send_message(chat_id, f"Error occurred!!\n<i>{error}</i>")
        os.remove(vid_480)
        await m.delete()
    ## Download video from a search result
    elif CallbackQuery.data == "link_down":
        youtube_down = YouTube(yt_link)
        await CallbackQuery.edit_message_text(
            f"File name:- {youtube_down.title}\n\n*Copy this link and send it directly(click this link to copy):- `{yt_link}`"
        )

