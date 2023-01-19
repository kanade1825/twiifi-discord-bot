# インストールした discord.py を読み込む
import random

import discord

# 自分のBotのアクセストークンに置き換えてください
TOKEN = ''
CHANNEL_ID = 720532235987451986
# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=discord.Intents.all())

async def start():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("ログインしました。")


#メンバー取得処理
async def getMem(command):
    member = command.channel.members
    memberlist = []
    for i in member:
        memberlist.append(i.id)
    print(memberlist)
    await command.channel.send('取得しました')
    return memberlist

#ランダム抽選処理
async def roulette(message1):
    allmenber = await getMem(message1)
    choicemenber =  random.choice(allmenber)
    return choicemenber


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    await start()

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    #ランダム抽選コマンド
    elif message.content == '/roulette':
        log = await roulette(message)
        await message.channel.send(" <@{}> さん当選おめでとうございます！".format(log))



# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)