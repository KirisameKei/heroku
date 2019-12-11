import discord

async def expand(message,client1):
    embed = await fetch_embed(message,client1)
    await message.channel.send(embed=embed)


async def fetch_embed(message,client1):
    try:
        guild = client1.get_guild(int(message.content[32:50]))
        channel = guild.get_channel(int(message.content[51:69]))
        message = await channel.fetch_message(int(message.content[70:88]))
        return compose_embed(message)
    except AttributeError:
        return discord.Embed(title="404NotFriend")


def compose_embed(message):
    embed = discord.Embed(
        description=message.content,
        timestamp=message.created_at,
    )
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url,
    )
    embed.set_footer(
        text=message.channel.name,
        icon_url=message.guild.icon_url,
    )
    if message.attachments and message.attachments[0].proxy_url:
        embed.set_image(
            url=message.attachments[0].proxy_url
        )
    return embed