# インストールした discord.py を読み込む
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

async def getMem(ctx):
    print(ctx.gulid.members)
    await ctx.channel.send('取得しました')

async def roulette():
    getMem()

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
    elif message.content == '/roulette':
        await message.channel.send(str(message.channel.members))
        print(message.channel.members)



# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)