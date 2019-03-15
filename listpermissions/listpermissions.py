from redbot.core import commands
from prettytable import PrettyTable
from fuzzywuzzy import process
import discord
from typing import Union, Optional

class ListPermissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["lp"])
    async def listpermissions(self, ctx):
        """Generates the permissions of a certain object and puts them in a nice table for you."""
        pass

    @listpermissions.group(name="guild")
    async def lp_guild(self, ctx):
        """Generates the permissions for a role or member guild wide.  These will change between channels."""
        pass

    @lp_guild.command(name="role")
    async def guild_role(self, ctx, *, rolename):
        """Generates the permissions of a role.
        
        Permissions Values:
            True: means that the role has that permission
            False: means that the role does not have that permission"""
        roles = [role.name for role in ctx.guild.roles]
        results = process.extract(rolename, roles, limit=1)
        if results[0][1] <= 70:
            return await ctx.send("Match was too low to be sure the role was found.")
        role = [role for role in ctx.guild.roles if role.name == results[0][0]][0]
        t = PrettyTable(["Permission", "Value"])
        for perm, value in role.permissions:
            t.add_row([perm, value])
        # Send two messages in case the rolename is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Permissions for role: {results[0][0]}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @lp_guild.command(name="member")
    async def guild_member(self, ctx, member: discord.Member=None):
        """Generates the guild wide permissions for a member.  This only takes into account their guild permissions, not any for specific channels."""
        if not member:
            member = ctx.author
        permissions = member.guild_permissions
        t = PrettyTable(["Permission", "Value"])
        for perm, value in permissions:
            t.add_row([perm, value])
        # Send two messages in case the member name is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Permissions for user {member.display_name} in guild {ctx.guild.name}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @listpermissions.group(name="channel")
    async def lp_channel(self, ctx):
        """Generates the permissions of a channel for either a member or a role."""
        pass

    @lp_channel.command(name="member")
    async def channel_member(self, ctx, member: discord.Member=None, channel: Union[discord.VoiceChannel, discord.TextChannel, discord.CategoryChannel]=None):
        """Generates the permissions for a member in a channel.
        
        Permissions Values:
            True: means that the person has that permission
            False: means that the person does not have that permission"""
        if not channel:
            channel = ctx.channel
        if not member:
            member = ctx.author
        
        permissions = channel.permissions_for(member)
        t = PrettyTable(["Permission", "Value"])
        for perm, value in permissions:
            t.add_row([perm, value])
        # Send two messages in case the member/channel name is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Permissions for user {member.display_name} in channel {channel.name}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @lp_channel.command(name="role")
    async def channel_role(self, ctx, channel: Optional[Union[discord.VoiceChannel, discord.TextChannel, discord.CategoryChannel]]=None, *, rolename):
        """Generates the basic permissions for a role in a channel.  Note that these are only the basic permissions, True or False will only show when the permissions is different from the default permissions of a role.
        
        Permissions Values:
            None: means that it depends on the role permissions
            True: means that a person can explicitly do that, despite role permissions
            False: means that a person can explicitly not do that, despite role permissions
        """
        if not channel:
            channel = ctx.channel
        roles = [role.name for role in ctx.guild.roles]
        results = process.extract(rolename, roles, limit=1)
        if results[0][1] <= 70:
            return await ctx.send("Match was too low to be sure the role was found.")
        role = [role for role in ctx.guild.roles if role.name == results[0][0]][0]
        permissions = channel.overwrites_for(role)
        t = PrettyTable(["Permission", "Value"])
        for perm, value in permissions:
            t.add_row([perm, value])
        # Send two messages in case the rolename or channel name is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Permissions for role {results[0][0]} in channel {channel.name}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @commands.group(aliases=["ap"])
    async def availablepermissions(self, ctx):
        """Generates the permissions of a certain object and puts them in a nice table for you.  Only shows the available permissions."""
        pass

    @availablepermissions.group(name="guild")
    async def ap_guild(self, ctx):
        """Generates the permissions for a role or member guild wide.  These will change between channels."""
        pass

    @ap_guild.command(name="role")
    async def ap_guild_role(self, ctx, *, rolename):
        """Generates the permissions of a role.
        
        Permissions Values:
            True: means that the role has that permission
            False: means that the role does not have that permission"""
        roles = [role.name for role in ctx.guild.roles]
        results = process.extract(rolename, roles, limit=1)
        if results[0][1] <= 70:
            return await ctx.send("Match was too low to be sure the role was found.")
        role = [role for role in ctx.guild.roles if role.name == results[0][0]][0]
        t = PrettyTable(["Permission", "Value"])
        for perm, value in role.permissions:
            if not value:
                continue
            t.add_row([perm, value])
        # Send two messages in case the rolename is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Available permissions for role: {results[0][0]}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @ap_guild.command(name="member")
    async def ap_guild_member(self, ctx, member: discord.Member=None):
        """Generates the guild wide permissions for a member.  This only takes into account their guild permissions, not any for specific channels."""
        if not member:
            member = ctx.author
        permissions = member.guild_permissions
        t = PrettyTable(["Permission", "Value"])
        for perm, value in permissions:
            if not value:
                continue
            t.add_row([perm, value])
        # Send two messages in case the member name is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Available permissions for user {member.display_name} in guild {ctx.guild.name}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @availablepermissions.group(name="channel")
    async def ap_channel(self, ctx):
        """Generates the permissions of a channel for either a member or a role."""
        pass

    @ap_channel.command(name="member")
    async def ap_channel_member(self, ctx, member: discord.Member=None, channel: Union[discord.VoiceChannel, discord.TextChannel, discord.CategoryChannel]=None):
        """Generates the permissions for a member in a channel.
        
        Permissions Values:
            True: means that the person has that permission
            False: means that the person does not have that permission"""
        if not channel:
            channel = ctx.channel
        if not member:
            member = ctx.author
        
        permissions = channel.permissions_for(member)
        t = PrettyTable(["Permission", "Value"])
        for perm, value in permissions:
            if not value:
                continue
            t.add_row([perm, value])
        # Send two messages in case the member/channel name is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Available permissions for user {member.display_name} in channel {channel.name}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @ap_channel.command(name="role")
    async def ap_channel_role(self, ctx, channel: Optional[Union[discord.VoiceChannel, discord.TextChannel, discord.CategoryChannel]]=None, *, rolename):
        """Generates the basic permissions for a role in a channel.  Note that these are only the basic permissions, True or False will only show when the permissions is different from the default permissions of a role.
        
        Permissions Values:
            None: means that it depends on the role permissions
            True: means that a person can explicitly do that, despite role permissions
            False: means that a person can explicitly not do that, despite role permissions
        """
        if not channel:
            channel = ctx.channel
        roles = [role.name for role in ctx.guild.roles]
        results = process.extract(rolename, roles, limit=1)
        if results[0][1] <= 70:
            return await ctx.send("Match was too low to be sure the role was found.")
        role = [role for role in ctx.guild.roles if role.name == results[0][0]][0]
        permissions = channel.overwrites_for(role)
        t = PrettyTable(["Permission", "Value"])
        for perm, value in permissions:
            if not value:
                continue
            t.add_row([perm, value])
        # Send two messages in case the rolename or channelname is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Available permissions for role {results[0][0]} in channel {channel.name}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @commands.group(aliases=["dp"])
    async def deniedpermissions(self, ctx):
        """Generates the permissions of a certain object and puts them in a nice table for you.  Only shows the denied permissions."""
        pass

    @deniedpermissions.group(name="guild")
    async def dp_guild(self, ctx):
        """Generates the permissions for a role or member guild wide.  These will change between channels."""
        pass

    @dp_guild.command(name="role")
    async def dp_guild_role(self, ctx, *, rolename):
        """Generates the permissions of a role.
        
        Permissions Values:
            True: means that the role has that permission
            False: means that the role does not have that permission"""
        roles = [role.name for role in ctx.guild.roles]
        results = process.extract(rolename, roles, limit=1)
        if results[0][1] <= 70:
            return await ctx.send("Match was too low to be sure the role was found.")
        role = [role for role in ctx.guild.roles if role.name == results[0][0]][0]
        t = PrettyTable(["Permission", "Value"])
        for perm, value in role.permissions:
            if value:
                continue
            t.add_row([perm, value])
        # Send two messages in case the rolename is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Denied permissions for role: {results[0][0]}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @dp_guild.command(name="member")
    async def dp_guild_member(self, ctx, member: discord.Member=None):
        """Generates the guild wide permissions for a member.  This only takes into account their guild permissions, not any for specific channels."""
        if not member:
            member = ctx.author
        permissions = member.guild_permissions
        t = PrettyTable(["Permission", "Value"])
        for perm, value in permissions:
            if value:
                continue
            t.add_row([perm, value])
        # Send two messages in case the member name is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Denied permissions for user {member.display_name} in guild {ctx.guild.name}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @deniedpermissions.group(name="channel")
    async def dp_channel(self, ctx):
        """Generates the permissions of a channel for either a member or a role."""
        pass

    @dp_channel.command(name="member")
    async def dp_channel_member(self, ctx, member: discord.Member=None, channel: Union[discord.VoiceChannel, discord.TextChannel, discord.CategoryChannel]=None):
        """Generates the permissions for a member in a channel.
        
        Permissions Values:
            True: means that the person has that permission
            False: means that the person does not have that permission"""
        if not channel:
            channel = ctx.channel
        if not member:
            member = ctx.author
        
        permissions = channel.permissions_for(member)
        t = PrettyTable(["Permission", "Value"])
        for perm, value in permissions:
            if value:
                continue
            t.add_row([perm, value])
        # Send two messages in case the member/channel name is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Denied permissions for user {member.display_name} in channel {channel.name}]```")
        await ctx.send("```py\n" + str(t) + "```")

    @dp_channel.command(name="role")
    async def dp_channel_role(self, ctx, channel: Optional[Union[discord.VoiceChannel, discord.TextChannel, discord.CategoryChannel]]=None, *, rolename):
        """Generates the basic permissions for a role in a channel.  Note that these are only the basic permissions, True or False will only show when the permissions is different from the default permissions of a role.
        
        Permissions Values:
            None: means that it depends on the role permissions
            True: means that a person can explicitly do that, despite role permissions
            False: means that a person can explicitly not do that, despite role permissions
        """
        if not channel:
            channel = ctx.channel
        roles = [role.name for role in ctx.guild.roles]
        results = process.extract(rolename, roles, limit=1)
        if results[0][1] <= 70:
            return await ctx.send("Match was too low to be sure the role was found.")
        role = [role for role in ctx.guild.roles if role.name == results[0][0]][0]
        permissions = channel.overwrites_for(role)
        t = PrettyTable(["Permission", "Value"])
        for perm, value in permissions:
            if value:
                continue
            t.add_row([perm, value])
        # Send two messages in case the rolename or channel name is really long, in order to make sure we don't exceed the 2000 character limit
        await ctx.send(f"```ini\n[Denied permissions for role {results[0][0]} in channel {channel.name}]```")
        await ctx.send("```py\n" + str(t) + "```")