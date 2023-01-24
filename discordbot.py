# インストールした discord.py を読み込む

import json
import os
import random

# capcha
import discord
from discord.channel import VoiceChannel
from discord.ext import commands, tasks

import botlog as log
import coinhistricaldata
from Tools.translate import Translate
from Tools.utils import getGuildPrefix
from voice_generator import creat_WAV

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(getGuildPrefix, intents = intents)

# HELP
bot.remove_command("help") # To create a personal help command

# Translate
bot.translate = Translate()

# Load cogs
if __name__ == '__main__':
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")





# 自分のBotのアクセストークンに置き換えてください
TOKEN = ''
CHANNEL_ID = 720532235987451986
CHANNEL_ID2 = 1065245120666017832
ID = 1066019582239854642
channel_sent = None
# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.messages = True
#client = discord.Client(intents=discord.Intents.all())
log.client = bot
log.discord = discord



async def start():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("ログインしました。")


# メンバー取得処理。ロールIDは要リクエスト
async def getMem(command):
    member = command.channel.members

    member_list = []
    for i in member:
        role = i.roles
        require_role = discord.utils.find(lambda role: role.id == 1065901716240863292, command.guild.roles)
        if require_role in role:
            member_list.append(i.id)
    print(member_list)
    await command.channel.send('取得しました')
    return member_list



# ランダム抽選処理
async def roulette(message1):
    all_member = await getMem(message1)
    choice_member = random.choice(all_member)
    return choice_member

#価格を一定間隔で喋らせるシステム
@tasks.loop(seconds=10)
async def send_message_every_10sec():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    price  = await coinhistricaldata.real_time_price()
    VoiCE = 881175320194076672
    VoiCE1 = bot.get_channel(VoiCE)
    voice_client = VoiCE1.guild.voice_client
    message = "現在の価格は" + price + "ドルです"
    await channel.send(message)
    creat_WAV(message)
    if voice_client.is_playing():
        voice_client.stop()
    VoiCE1.guild.voice_client.play(discord.FFmpegPCMAudio("output.wav"))


# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    await start()
    print(f'We have logged in as {bot.user}')
    print(discord.__version__)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"?help"))
    VoiCE = 881175320194076672
    VoiCE1 = bot.get_channel(VoiCE)
    await VoiceChannel.connect(VoiCE1)
    send_message_every_10sec.start()


# ------------------------ RUN ------------------------ #
with open("config.json", "r") as config:
    data = json.load(config)
    token = data["token"]


# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    # ランダム抽選コマンド
    elif message.content == '/roulette':
        log = await roulette(message)
        await message.channel.send(" <@{}> さん当選おめでとうございます！".format(log))
    elif message.content == '!connect':
        await VoiceChannel.connect(message.author.voice.channel)
        await message.channel.send('読み上げBotが参加しました')


    elif message.content == '!disconnect':
        server = message.guild.voice_client
        await server.disconnect()

        await message.channel.send('読み上げBotが退出しました')


    else:
        if message.guild.voice_client:
            print(message.content)
            creat_WAV(message.content)
            message.guild.voice_client.play(discord.FFmpegPCMAudio("output.wav"))



# メッセージVCログイン云々
@bot.event
async def on_voice_state_update(member, before, after):
    await log.voice_log(CHANNEL_ID, member, before, after)


# メッセージ削除ログ
@bot.event
async def on_message_delete(message):
    await log.message_delete_log(CHANNEL_ID, message)


# メッセージ編集ログ
@bot.event
async def on_message_edit(before, after):
    await log.message_edit_log(CHANNEL_ID, before, after)


# Botの起動とDiscordサーバーへの接続
if __name__ == '__main__':
    bot.run(token)
