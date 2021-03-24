# Coded by D4n1l3k300
# t.me/D4n13l3k00s
from .. import loader, utils
import telethon
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import *
import requests, io, base64
@loader.tds
class FDQuoteMod(loader.Module):
    strs = {
        "name": "FDQuote",
        "processing":"<b>[FDQ]</b> Processing...",
        "processing_api":"<b>[FDQ]</b> </code>API Processing...</code>",
        "photo":"[Фото]",
        "video":"[Видео]",
        "audio":"[Аудио]",
        "voice":"[Голосовое сообщение]",
        "videonote":"[Видеосообщение]",
        "poll":"[Опрос]",
        "quiz":"[Викторина]",
        "sticker":"[Стикер]",
        "animsticker":"[Анимированый стикер]",
        "file":"[Файл {}]",
        "api_error":"<b>[FDQ]</b> API Error: <code>{}</code>",
        "error":"<b>[FDQ]</b> Err...",
        "deleted_acc":"Удалённый аккаунт",
        "need_reply":"<b>[FDQ]</b> Reply to message..."
    }
    def __init__(self):
        self.name = self.strs['name']
        self.api_url = "https://api.d4n13l3k00.ml/quotes/generate"
    
    @loader.owner
    async def fdqcmd(self, m: Message):
        # self.strs['']
        ".fdq <реплай на юзера и текст> или <@username и текст> или <реплай и @username> или <реплай> - Создать квотес"
        reply = await m.get_reply_message()
        args = m.text.split(maxsplit=2)
        args.pop(0)
        catch_reply = repl = pic = False
        if reply:
            if args:
                if args[0].startswith('@'):
                    user_id = args[0][1:]
                    text = reply.text
                else:
                    user_id = reply.from_id or reply.fwd_from.channel_id
                    text = ' '.join(args)
            else:
                user_id = reply.from_id or reply.fwd_from.channel_id
                text = reply.text
                catch_reply = True
        elif len(args) == 2 and args[0].startswith('@'):
            user_id = args[0][1:]
            text = args[1]
        else: return await utils.answer(m, self.strs['need_reply'])
        try: user = await m.client.get_entity(user_id)
        except ValueError: return await utils.answer(m, self.strs['error'])
        await utils.answer(m, self.strs['processing'])
        name = telethon.utils.get_display_name(user) if type(user) == Channel else (self.strs['deleted_acc'] if user and user.deleted else telethon.utils.get_display_name(user))
        id   = user.id
        avatar = await m.client.download_profile_photo(user, bytes)
        if reply: repl = await reply.get_reply_message()
        if reply and reply.file and 'image' in reply.file.mime_type: pic = base64.b64encode(await reply.download_media(bytes)).decode()
        if repl and catch_reply:
            r = await m.client.get_entity(repl.from_id or repl.fwd_from.channel_id)
            if repl.raw_text : replText = repl.raw_text if repl.raw_text else ""
            elif repl.photo  : replText = self.strs['photo']
            elif repl.video  : replText = self.strs['videonote'] if repl.video.attributes[0].round_message else self.strs['video']
            elif repl.audio  : replText = self.strs['audio']
            elif repl.voice  : replText = self.strs['voice']
            elif repl.sticker: replText = self.strs['sticker']
            elif repl.file   : replText = self.strs['animsticker'] if repl.file.mime_type == "application/x-tgsticker" else self.strs['file'].format(repl.file.name)
            elif repl.poll   : replText = self.strs['quiz'] if repl.media.poll.quiz else self.strs['poll']
            repl = {"name":telethon.utils.get_display_name(r) if type(r) == Channel else (self.strs['deleted_acc'] if r and r.deleted else telethon.utils.get_display_name(r)), "text":replText}
        else: repl = None
        await utils.answer(m, self.strs['processing_api'])
        r = requests.post(self.api_url, json={"avatar": base64.b64encode(avatar).decode() if avatar else None, "name":name, "text":text, "id":id, "pic":pic, "reply":repl})
        if r.status_code == 200:
            quote  = io.BytesIO(r.content)
            quote.name = "q.webp"
            if reply: await reply.reply(file=quote)
            else: await m.respond(file=quote)
            await m.delete()
        else: await utils.answer(m, self.strs['api_error'].format(r.json()['err']))