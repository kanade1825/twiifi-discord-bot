
discord = None
client = None

#VC入退出ログ
async def voice_log(CHANNEL_ID, member, before, after):
    from datetime import datetime

    if member.guild.id == 720532235987451983 and (before.channel != after.channel):
            now = datetime.now()
            alert_channel = client.get_channel(CHANNEL_ID)
            if before.channel is None:
                msg = f'{now:%m/%d-%H:%M} に {member.name} が {after.channel.name} に参加しました。'
                await alert_channel.send(msg)
            elif after.channel is None:
                msg = f'{now:%m/%d-%H:%M} に {member.name} が {before.channel.name} から退出しました。'
                await alert_channel.send(msg)

#メッセージ削除ログ
async def message_delete_log(CHANNEL_ID,message):
    from datetime import datetime

    now = datetime.now()

    embed = discord.Embed(title="メッセージ削除", color=discord.Color.red())
    embed.add_field(name="メッセージ", value=message.content, inline=False)
    embed.add_field(name="時刻", value=now.strftime('%Y /%m / %d　 %H : %M : %S'), inline=False)
    embed.add_field(name="チャンネル", value=message.channel.mention, inline=False)
    embed.set_footer(icon_url=message.author.avatar.url, text=message.author.display_name)
    channel = message.guild.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)

#メッセージ編集ログ
async def message_edit_log(CHANNEL_ID,before, after):
    channel = client.get_channel(CHANNEL_ID)

    await channel.send(before.content)
    await channel.send(after.content)
