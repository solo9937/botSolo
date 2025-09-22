• أول فريق مصري متخصص في تطوير بايثون Python   
• القناة #Code الرسميـة الرائدة في تـعليم البرمجة عربيًا 
• جميع السورس سولو و النشر محفوظة:  ©️ SOLO™ 2015  
• مطور ومُنشئ المحتوى:  
• @TopSOLO
• @DevVeG







from youtubesearchpython import SearchVideos
import re, os
from yt_dlp import YoutubeDL


lists = {}
user_lists = {}


@Client.on_message(filters.command(["اضف لقائمتي"], ""))
async def add_to_user_list(client, message):
    group_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.split(None, 1)
    user_lists.setdefault(user_id, [])
    if len(user_lists[user_id]) >= 10:
        return await message.reply("**لا يمكنك إضافة أكثر من 10 مقاطع إلى قائمتك**")
    parts = message.text.split(None, 2)
    if len(parts) == 3:
        query = parts[2]
        search = SearchVideos(query, offset=1, mode="dict", max_results=1)
        code = search.result()
        if not code["search_result"]:
            return await message.reply("لم يتم العثور على نتائج.")
        video_info = code["search_result"][0]
        video_link = video_info["link"]
        videoid = video_info["id"]
        channel_name = video_info["channel"]
        thum = video_info["title"]
        title = re.sub(r"\W+", " ", thum).title()
        video_duration = video_info.get("duration", "0")
        views = video_info.get("views", "غير متوفر")
        useram = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
        audio_file = os.path.join(DOWNLOAD_FOLDER, f"{title}.mp4")
        if not os.path.exists(audio_file):
            opts = {
                "format": "bestaudio/best",
                "outtmpl": audio_file,
                "quiet": True,
              
            }
            with YoutubeDL(opts) as ytdl:
                ytdl_data = ytdl.extract_info(video_link, download=True)
                audio_file = ytdl.prepare_filename(ytdl_data)
        data = {
            "bot_username": client.me.username,
            "audio_file": audio_file,
            "vid": None,
            "code": code,
            "user_mention": message.from_user.mention,
            "useram": useram,
            "videoid": videoid,
            "video_duration": video_duration,
            "channel_name": channel_name,
            "thum": thum,
            "views": views
        }
        title = thum
        user_lists[user_id].append(data)
        return await message.reply(f"**تم إضافة {title[:25]} إلى قائمتك**")
    if group_id not in lists:
        return await message.reply("لا يوجد تشغيل حالي لإضافته")
    
    user_lists[user_id].append(lists[group_id].copy())
    return await message.reply("**تم إضافة آخر تشغيل إلى قائمتك الخاصة**")

@Client.on_message(filters.command(["قائمتي"], ""))
async def user_list(client, message):
    user_id = message.from_user.id if message.from_user else "None"    
    if user_id not in user_lists or not user_lists[user_id]:
        return await message.reply("**قائمتك فارغة**")
    buttons = []
    for i, item in enumerate(user_lists[user_id]):
        title = item.get("thum", "بدون عنوان")
        title = title[:20] if len(title) > 20 else title
        buttons.append([InlineKeyboardButton(text=f"{title}", callback_data=f"play_{i}_{user_id}")])
    markup = InlineKeyboardMarkup(buttons)
    await message.reply("**اختر مقطعًا لتشغيله:**", reply_markup=markup)

@Client.on_callback_query(filters.regex(r"^play_(\d+)_(\d+)$"))
async def delete_buttons(client, callback_query):
    user_id = callback_query.from_user.id
    index = int(callback_query.data.split("_")[1])
    if user_id not in user_lists or index >= len(user_lists[user_id]):
        return await callback_query.answer("هذا المقطع غير موجود.", show_alert=True)
    item = user_lists[user_id][index]
    title = item.get("thum", "بدون عنوان")
    title = title[:20] if len(title) > 20 else title
    buttons = [
        [
            InlineKeyboardButton("تشغيل", callback_data=f"do_play_{index}_{user_id}"),
            InlineKeyboardButton("حذف", callback_data=f"do_delete_{index}_{user_id}")
        ],
        [
            InlineKeyboardButton("رجوع للقائمة", callback_data=f"back_to_list_{user_id}")
        ]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_text(f"**{title}**", reply_markup=markup)
    await callback_query.answer()

@Client.on_callback_query(filters.regex(r"^do_play_(\d+)_(\d+)$"))
async def do_play(client, callback_query):
    user_id = callback_query.from_user.id
    group_id = callback_query.message.chat.id
    index = int(callback_query.data.split("_")[2])
    if user_id not in user_lists or index >= len(user_lists[user_id]):
        return await callback_query.answer("هذا المقطع غير موجود.", show_alert=True)
    item = user_lists[user_id][index]
    c = await join_call(
        item["bot_username"],
        client,
        callback_query.message,
        item["audio_file"],
        group_id,
        item["vid"],
        item["code"],
        item["user_mention"],
        item["useram"],
        item["videoid"],
        item["video_duration"],
        item["channel_name"],
        item["thum"],
        item["views"]
    )
    if c:
        await callback_query.message.edit_text(f"تم تشغيل المقطع: {item.get('channel_name', 'بدون عنوان')}")
    else:
        await callback_query.message.edit_text(f"تم تشغيل المقطع: {item.get('channel_name', 'بدون عنوان')}")

@Client.on_callback_query(filters.regex(r"^do_delete_(\d+)_(\d+)$"))
async def ddelete(client, callback_query):
    user_id = callback_query.from_user.id
    index = int(callback_query.data.split("_")[2])

    if user_id not in user_lists or index >= len(user_lists[user_id]):
        return await callback_query.answer("هذا المقطع غير موجود.", show_alert=True)

    deleted_title = user_lists[user_id][index].get("channel_name", "بدون عنوان")
    user_lists[user_id].pop(index)
    await callback_query.message.edit_text(f"تم حذف المقطع")

@Client.on_callback_query(filters.regex(r"^back_to_list_(\d+)$"))
async def back_to_list(client, callback_query):
    await sh_user_list(client, callback_query)
    await callback_query.answer()

async def sh_user_list(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in user_lists or not user_lists[user_id]:
        await callback_query.message.edit_text("**قائمتك فارغة**")
        return
    buttons = []
    for i, item in enumerate(user_lists[user_id]):
        title = item.get("thum", "بدون عنوان")
        title = title[:20] if len(title) > 20 else title
        buttons.append([InlineKeyboardButton(text=f"{title}", callback_data=f"play_{i}_{user_id}")])
    markup = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_text("**اختر مقطعًا لتشغيله:**", reply_markup=markup)