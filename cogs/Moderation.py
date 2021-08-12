from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def test1(self, ctx, argument):
       await self.client.say("Stuff")  



def setup(client):
    client.add_cog(Moderation(client))