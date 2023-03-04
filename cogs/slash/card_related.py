import datetime
import re
import aiohttp
import disnake
import requests
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from helpers import checks
from pathlib import Path

async def search_engine(input_string, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:       
                data = await r.json()
                if "cards" in str(url):
                    for card in data:
                        for card_name in card:
                            card_details = card[card_name]
                            jp_name = card_details["Japanese name"]
                            id = card_details["Card ID"]
                            details = card_details["Details"]
                        
                            if re.sub('[^a-zA-Z0-9 \n\.]', ' ', input_string).lower() \
                            == re.sub('[^a-zA-Z0-9 \n\.]', ' ', card_name).lower():
                            
                                embed = disnake.Embed(
                                title=card_name,
                                description=jp_name,
                                timestamp=datetime.datetime.now(),
                                color=0x9C84EF
                                )

                                for detail in details:                        
                                    for set_code in detail:
                                        
                                        price = "Out stock!"
                                        if detail[set_code]['price'] != 0:
                                            price = "{} JPY".format(detail[set_code]['price'])
                                        
                                        rarity = detail[set_code]['rarity']
                                        if rarity == "ｼｰｸﾚｯﾄ":
                                            rarity = "SCR"
                                        elif rarity == "【TRC1】ﾚｱﾘﾃｨ･ｺﾚｸｼｮﾝ":
                                            rarity = "CR"
                                        elif rarity == "ｱﾙﾃｨﾒｯﾄ":
                                            rarity = "Ultimate R"
                                        
                                        condition = detail[set_code]['condition']
                                        
                                        embed.add_field(name="Info", 
                                        value="{}\nPrice: {}\nRarity: {}\nCondition: {}" \
                                        .format(set_code, price, rarity, condition),
                                        inline=True)
                                        
                                id = int(id)
                                path = "pics/{}.jpg".format(id)

                                if Path(path).is_file():
                                    pass
                                else:
                                    img_url = "https://images.ygoprodeck.com/images/cards/{}.jpg".format(id)
                                    img_data = requests.get(img_url).content
                                    with open(path, 'wb') as handler:
                                        handler.write(img_data)

                                embed.set_image(file=disnake.File(path))
                                embed.set_footer(text="Card ID: {}".format(id),)
                                return embed


                    for card in data:
                        for card_name in card:
                            card_details = card[card_name]
                            jp_name = card_details["Japanese name"]
                            id = card_details["Card ID"]
                            details = card_details["Details"]
                            
                            if re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(input_string)).lower() \
                            in re.sub('[^a-zA-Z0-9 \n\.]', ' ', card_name).lower():
                                
                                embed = disnake.Embed(
                                title=card_name,
                                description=jp_name,
                                timestamp=datetime.datetime.now(),
                                color=0x9C84EF
                                )

                                for detail in details:                        
                                    for set_code in detail:
                                        
                                        price = "Out stock!"
                                        if detail[set_code]['price'] != 0:
                                            price = "{} JPY".format(detail[set_code]['price'])
                                        
                                        rarity = detail[set_code]['rarity']
                                        if rarity == "ｼｰｸﾚｯﾄ":
                                            rarity = "SCR"
                                        elif rarity == "【TRC1】ﾚｱﾘﾃｨ･ｺﾚｸｼｮﾝ":
                                            rarity = "CR"
                                        elif rarity == "ｱﾙﾃｨﾒｯﾄ":
                                            rarity = "Ultimate R"
                                        
                                        condition = detail[set_code]['condition']
                                        
                                        embed.add_field(name="Info", 
                                        value="{}\nPrice: {}\nRarity: {}\nCondition: {}" \
                                        .format(set_code, price, rarity, condition),
                                        inline=True)
                                        
                                id = int(id)
                                path = "pics/{}.jpg".format(id)

                                if Path(path).is_file():
                                    pass
                                else:
                                    img_url = "https://images.ygoprodeck.com/images/cards/{}.jpg".format(id)
                                    img_data = requests.get(img_url).content
                                    with open(path, 'wb') as handler:
                                        handler.write(img_data)

                                embed.set_image(file=disnake.File(path))
                                embed.set_footer(text="Card ID: {}".format(id),)
                                return embed
                elif "code" in str(url):
                    #embed = disnake.Embed()
                    for set_code in data:
                        if re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(input_string)).lower() \
                            in re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(set_code)).lower():
                            embed = disnake.Embed(
                            title=set_code,
                            #description=jp_name,
                            timestamp=datetime.datetime.now(),
                            color=0x9C84EF
                            )
                            for code in data[set_code]:
                                card_name = code["English name"]
                                jp_name = code["Japanese name"]
                                id = code["Card ID"]
                                
                                
                                price = "Out stock!"
                                if code['Details']['Price'] != 0:
                                    price = "{} JPY".format(code['Details']['Price'])
                                rarity = code['Details']['Rarity']
                                if rarity == "ｼｰｸﾚｯﾄ":
                                    rarity = "SCR"
                                elif rarity == "【TRC1】ﾚｱﾘﾃｨ･ｺﾚｸｼｮﾝ":
                                    rarity = "CR"
                                elif rarity == "ｱﾙﾃｨﾒｯﾄ":
                                    rarity = "Ultimate R"
                                
                                condition = code['Details']['Condition']
                                embed.add_field(name="Info", 
                                value="Price: {}\nRarity: {}\nCondition: {}" \
                                .format(price, rarity, condition),
                                inline=True)
                                
                            id = int(id)
                            path = "pics/{}.jpg".format(id)

                            if Path(path).is_file():
                                pass
                            else:
                                img_url = "https://images.ygoprodeck.com/images/cards/{}.jpg".format(id)
                                img_data = requests.get(img_url).content
                                with open(path, 'wb') as handler:
                                    handler.write(img_data)

                            embed.set_image(file=disnake.File(path))
                            embed.set_footer(text="Card ID: {}".format(id),)
                            return embed
                            #print(code)
                            #print(set_code[code]["English name"])
            else:
                embed = disnake.Embed(
                    title="Error!",
                    description="There is something wrong with the server, please try again later. \
                    Or contact me at MeiMei#3717 on Discord if the error still continue",
                    color=0xE02B2B
                )
                return embed
###############################################################################
###############################################################################
#-----------------------------------------------------------------------------#
######### Here we name the cog and create a new class for the cog.#############
class card_realted(commands.Cog, name="card-slash"):
    def __init__(self, bot):
        self.bot = bot
    
    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="cardinfo",
        description="Database update every 30 days. Contact MeiMei#3717 if something huge dropped.",
    )
    @checks.not_blacklisted()
    async def card_name_search(self, interaction: ApplicationCommandInteraction, input_name: str):
        await interaction.response.defer()
        with open("log.txt", "a") as log:
            log.write(input_name + "\n")
        embed = disnake.Embed(
            title="Error!",
            description="Cannot find the card for now. \n Most likely our databases do not have the card.",
            color=0xE02B2B
        )
        embed = await search_engine(input_string=input_name, url="http://localhost:8000/cards.json")
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="cardcode",
        description="Input set code to find details about card. Contact MeiMei#3717 if things went wrong"
    )
    @checks.not_blacklisted()
    async def card_code_search(self, interaction: ApplicationCommandInteraction, input_code: str):
        await interaction.response.defer()
        with open("log.txt", "a") as log:
            log.write(input_code + "\n")
        
        embed = disnake.Embed(
            title="Error!",
            description="Cannot find the card for now. \n Most likely our databases do not have the card.",
            color=0xE02B2B
        )
        embed = await search_engine(input_string=input_code, url="http://localhost:8000/formatted_set_code.json")
        await interaction.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(card_realted(bot))   
