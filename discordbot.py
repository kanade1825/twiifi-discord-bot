# インストールした discord.py を読み込む
import discord
from pycparser.c_ast import ID

import botlog as log
import random
from discord.channel import VoiceChannel

# 自分のBotのアクセストークンに置き換えてください
TOKEN = ''
CHANNEL_ID = 720532235987451986
CHANNEL_ID2 = 1065245120666017832
ID = 1066019582239854642
# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.messages = True
client = discord.Client(intents=discord.Intents.all())
log.client = client
log.discord = discord


async def start():
    channel = client.get_channel(CHANNEL_ID)
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


ID_ROLE_WELCOME = 1066022111925252146  # 付けたい役職のID
UnicodeEmoji = '👍'


# リアクション判定
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == ID:
        checked_emoji = payload.emoji.name
        print(checked_emoji)
        # channel_id から Channel オブジェクトを取得
        channel = client.get_channel(payload.channel_id)
        # 該当のチャンネル以外はスルー
        if channel.id != CHANNEL_ID2:
            return
        # guild_id から Guild オブジェクトを取得
        guild = client.get_guild(payload.guild_id)
        # user_id から Member オブジェクトを取得
        member = guild.get_member(payload.user_id)
        # 用意した役職IDから Role オブジェクトを取得
        role = guild.get_role(ID_ROLE_WELCOME)
        # リアクションを付けたメンバーに役職を付与
        if checked_emoji == UnicodeEmoji:
            await member.add_roles(role)
            # 分かりやすいように歓迎のメッセージを送る
            await channel.send('いらっしゃいませ！')


@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == ID:
        print(payload.emoji.name)
        checked_emoji = payload.emoji.name

    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    channel = client.get_channel(payload.channel_id)

    if checked_emoji == UnicodeEmoji:
        role = guild.get_role(ID_ROLE_WELCOME)
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)
        await channel.send('ばいばい')



# メッセージVCログイン云々
@client.event
async def on_voice_state_update(member, before, after):
    await log.voice_log(CHANNEL_ID, member, before, after)


# メッセージ削除ログ
@client.event
async def on_message_delete(message):
    await log.message_delete_log(CHANNEL_ID, message)


# メッセージ編集ログ
@client.event
async def on_message_edit(before, after):
    await log.message_edit_log(CHANNEL_ID, before, after)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
