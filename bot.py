import discord
from discord.ext import tasks, commands
import src.contentChecker as checker


class TabBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)

    async def on_ready(self):
        print("[BOT] Aplicativo pronto!")
        self.MyTask.start()

    @tasks.loop(seconds=15)
    async def MyTask(self):

        def splitTitle(title: str, length: int):
            oldTitle = title.split(' ')
            newTitleList = [oldTitle[0]]
            newTitle = ''
            while len(newTitle) <= length:
                newTitle = ' '.join(newTitleList)
                oldTitle.pop(0)
                newTitleList.append(oldTitle[0])
            return newTitle + '...'

        async def trySendMessage(content):
            url = "https://www.tabnews.com.br"

            if len(content['title']) > 70:
                content['title'] = splitTitle(content['title'], 45)
            if len(content['body']) > 190:
                content['body'] = content['body'][:190] + '...'

            embed = discord.Embed(
                title=content['title'],
                url=f"{url}/{content['owner_username']}/{content['slug']}",
                description=content['body'],
                color=0xF5F5F5
            ).set_author(
                name=content['owner_username'],
                url=f"{url}/{content['owner_username']}"
            ).set_image(
                url=f"{url}/api/v1/contents/{content['owner_username']}/{content['slug']}/thumbnail"
            )

            if content['source_url']:
                source_text = content['source_url']
                if len(source_text) > 50:
                    source_text = source_text[:50] + '...'
                embed.add_field(
                    name="🔗 Fonte:",
                    value=f"[{source_text}]({content['source_url']})",
                    inline=False
                )

            guilds = checker.MyFile("./JSON/TextChannels.json").read()

            for g in guilds:
                channel = bot.get_channel(g['channel_id'])
                guild = bot.get_guild(g['guild_id'])
                try:
                    await channel.send(embed=embed)
                    print(f"[BOT] Enviado em {guild.name}")
                except:
                    pass

        newContents = checker.checkContents()
        for content in newContents:
            await trySendMessage(content)


bot = TabBot()


@bot.tree.command(name="enable")
@discord.app_commands.guild_only()
@discord.app_commands.checks.has_permissions(manage_guild=True)
async def enable(inter: discord.Interaction, channel: discord.TextChannel):
    """
    Ative e defina em qual canal serão enviadas as atualizações.

    Parameters
    ----------
    channel: Canal em que serão enviadas as notificações.
    """
    await inter.response.send_message("As notificações serão enviadas no canal indicado.\n**Lembre-se de me dar as permissões de ler e enviar mensagens no canal.**", ephemeral=True)

    file = checker.MyFile("./JSON/TextChannels.json")
    data = file.read()
    for d in data:
        if d["guild_id"] == inter.guild_id:
            d["channel_id"] = channel.id
            file.write(data)
            return

    data.append({
        "guild_id": inter.guild_id,
        "channel_id": channel.id
    })
    file.write(data)


@bot.tree.command(name="disable")
@discord.app_commands.guild_only()
@discord.app_commands.checks.has_permissions(manage_guild=True)
async def disable(inter: discord.Interaction):
    """Desativar o recebimento de notificações de novas publicações."""
    await inter.response.send_message("Tudo bem, não irei enviar notificações sobre novas publicações.", ephemeral=True)

    file = checker.MyFile("./JSON/TextChannels.json")
    data = file.read()
    for d in data:
        if d["guild_id"] == inter.guild_id:
            data.remove(d)
            file.write(data)
            break
    return


@bot.command(name="sync")
@commands.is_owner()
async def sync(ctx: commands.Context):
    resp = await ctx.reply("Sincronizando comandos...")
    await bot.tree.sync()
    await resp.edit(content="Comandos sincronizados!")


bot.run("TOKEN")
