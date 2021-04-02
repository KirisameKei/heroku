async def on_raw_reaction_add(client1, payload):
    """
    リアクションが付けられた時用の関数"""

    channel = client1.get_channel(payload.channel_id)
    user = client1.get_user(payload.user_id)
    guild = client1.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if channel.id == 827355843183640617:
        if not payload.message_id == 827359213721485383:
            return
        if user == client1.user:
            return
        msg = await channel.fetch_message(payload.message_id)
        await msg.remove_reaction(f"{payload.emoji}", user)
        emoji_list = [
            "\U0001f1e6",
            "\U0001f1e7"
        ]
        role_id_list = [
            594643451354677248,
            612389273101926467
        ]
        if payload.emoji.name in emoji_list:
            emoji_index = emoji_list.index(payload.emoji.name)
            role = guild.get_role(role_id_list[emoji_index])
            if role in member.roles:
                await member.remove_roles(role)
                await channel.send(f"{member.mention}から{role.name}を剥奪しました", delete_after=3)
            else:
                await member.add_roles(role)
                await channel.send(f"{member.mention}に{role.name}を付与しました", delete_after=3)

        else:
            await channel.send(f"{member.mention}その絵文字は使用できません", delete_after=3)