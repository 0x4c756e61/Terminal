import discord
from discord.ext import commands

class syst(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(description="Lists a category's channels, lists content of . if none is specified\nNotes:\n'/' represent the discord server\nA category is required to use the --ids flag", usage="$ls [CATEGORY]")
    async def ls(self, ctx, chan="",*,options=""):
        if "--help" in options or "--help" in chan:
            helps = """```
Usage:
    ls [category] [options]

Options:
    --ids   Display channel id next to it's name

Note: a category must be specified to any option
            ```
            """
            await ctx.send(helps)
            return
        channel = chan.lower()
        result = "```\n"
        found = False
        if channel == "/":
            for c in ctx.guild.categories:
                result += c.name + "\n"
                for ch in c.channels:
                    if "--ids" in options:
                        result += f" ╰─ {ch.name}--{ch.id}\n"
                    else:
                        result += f" ╰─ {ch.name}\n"
        elif channel.strip():
            for c in ctx.guild.categories:
                if not (channel in c.name.lower()):
                    continue
                found = True
                result += c.name + "\n"
                for ch in c.channels:
                    if "--ids" in options:
                        result += f" ╰─ {ch.name}--{ch.id}\n"
                    else:
                        result += f" ╰─ {ch.name}\n"
        else:
            result += ctx.message.channel.category.name + "\n"
            for c in ctx.message.channel.category.channels:
                if "--ids" in options:
                    result += f" ╰─ {c.name}--{c.id}\n"
                else:
                    result += f" ╰─ {c.name}\n"
        
        if not found and result == "```\n":
            await ctx.send(f"Terminal: ls : {channel} :No such category")
        elif len(result) > 2000:
            await ctx.send("Terminal: ls: output is too long")
        else:
            await ctx.send(result + "```")

    @commands.command(description="Bans a user", usage="$userdel [USER]")
    @commands.has_permissions(ban_members=True)
    async def userdel(self, ctx, user: discord.Member = ""):
        if not user:
            await ctx.send("```\nuserdel: please specify a user\n```")
            return
        try:
            await user.ban()
        except:
            await ctx.send(f"```\nuserdel: Unable to ban {user}\n```")

    @commands.command(description="Show help about the commands and their usages", usage="$man [COMMAND]")
    async def man(self, ctx, cmd_arg=""):
        if not cmd_arg:
            await ctx.send("```\nWhat manual page do you want ?\nFor example, try $man man\n```")
            return

        found = False
        for cmd in self.client.commands:
            if cmd_arg == cmd.name:
                found = True
                await ctx.send(f"```\nTerminal/{cmd.name.upper()}\n\n{cmd.description}\n\nExample: {cmd.usage}\n```")
                return
        if not found: await ctx.send(f"```\nNo manual page for {cmd_arg}\n```")

    @commands.command(description="Creates a channel or multiple ones", usage="$mkchan [--text||--voice||--categ] <CHANNEL1> [CHANNEL2]")
    @commands.has_permissions(manage_channels=True)
    async def mkchan(self, ctx, *,args=""):
        if not args.strip():
            await ctx.send("```\nmkchan: please specify at least one channel name\n```")
            return

        bypass_next = False
        args_list = args.split(" ")
        for i in range(len(args_list)):
            arg = args_list[i]
            if bypass_next:
                bypass_next = False
                continue

            if arg == "--text":
                bypass_next = True
                await ctx.message.guild.create_text_channel(args_list[i+1])
            elif arg == "--voice":
                bypass_next = True
                await ctx.message.guild.create_voice_channel(args_list[i+1])
            elif arg == "--categ":
                bypass_next = True
                await ctx.message.guild.create_category(args_list[i+1])
            else:
                await ctx.message.guild.create_text_channel(arg)
    
    @commands.command(description="Removes a channel or multiple ones", usage="$rmchan <CHANNEL1> [CHANNEL2]")
    @commands.has_permissions(manage_channels=True)
    async def rmchan(self, ctx, *,args=""):
        if not args.strip():
            await ctx.send("```\nrmchan: please specify at least one channel\n```")
            return

        chans = args.split(" ")
        for chan in chans:
            for c in ctx.guild.channels:
                if chan == c.name:
                    await c.delete()

    @commands.command(description="Adds/removes one role to/from a user ", usage="$usermod <@USER> <-a||-r> <ROLE NAME>")
    @commands.has_permissions(manage_roles=True)
    async def usermod(self,ctx,user:discord.Member="", *,args = ""):
        if not user:
            await ctx.send("```\nusermod: please specify a user\n```")
            return
        if not args.strip():
            await ctx.send("```\nrmchan: please specify a method and a role\n```")
            return

        cmd_args = args.split()
        bypass_next = False
        for i in range(len(cmd_args)):
            arg = cmd_args[i]
            if bypass_next:
                bypass_next = False
                continue
            if arg == "-a":
                bypass_next = True
                for role in ctx.guild.roles:
                    if role.name == cmd_args[i+1]:
                        await user.add_roles(role)
                        return
            elif arg == "-r":
                bypass_next = True
                for role in ctx.guild.roles:
                    if role.name == cmd_args[i+1]:
                        await user.remove_roles(role)
                        return
    @commands.command(description="Moved a channel into a category, if no category is provided the selected channel moves out of it's parrent one", usage="$mv <CHANNEL> [CATEGORY]")
    @commands.has_permissions(manage_channels=True)
    async def mv(self,ctx, channel: discord.TextChannel="", *, categ = ""):
        if not channel:
            await ctx.send("```\mv: please specify a channel\n```")
            return
        if not categ:
            await channel.edit(category=None)
            return
        
        found = False
        for category in ctx.message.guild.categories:
            if categ.lower() in category.name.lower():
                found = True
                await channel.edit(category=category)
                return
        
        if not found: await ctx.send(f"```\nmv: Couldn't find category {categ}\n```")
    
    @commands.command(description="Change a channel position relatively to it's category\nNOTE: you cannot move a channel out of it's category", usage="$chpos <CHANNEL> <UP||DOWN||NUMBER>")
    @commands.has_permissions(manage_channels=True)
    async def chpos(self,ctx,channel: discord.TextChannel="",pos=""):
        if not channel:
            await ctx.send("```\nchpos: please specify a channel\n```")
            return
        if not pos:
            await ctx.send("```\nchpos: please specify a position\n```")
            return

        if pos == "up":
            await channel.edit(position=channel.position-1)
        elif pos == "down":
            await channel.edit(position=channel.position+1)
        elif pos == "get":
            await ctx.send(f"```\nchpos: position of \"{channel.name}\": {channel.position}\n```")
        else:
            await channel.edit(position=int(pos))
    @commands.command(description="Quits discord", usage="$exit")
    async def exit(self, ctx):
        await ctx.send("exit")
        await self.client.close()
    
    @userdel.error
    async def userdel_err(self,error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await client.send_message(ctx.message.channel, "```\nuserdel: Permission denied.\n```")
    
    @mkchan.error
    async def mkchan_err(self,error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await client.send_message(ctx.message.channel, "```\mkchan: Permission denied.\n```")
        
    @usermod.error
    async def usermod_err(self,error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await client.send_message(ctx.message.channel, "```\nusermod: Permission denied.\n```")

    @mv.error
    async def mv_err(self,error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await client.send_message(ctx.message.channel, "```\mv: Permission denied.\n```")

def setup(client):
    client.add_cog(syst(client))
