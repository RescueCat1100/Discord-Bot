import datetime
import re
import aiohttp
import disnake
import requests
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from helpers import checks
from pathlib import Path
import json


###############################################################################
###############################################################################
# -----------------------------------------------------------------------------#
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
        with open("cards.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        found = False
        
        for cards in data:
            for card in cards:
                if re.sub('[^a-zA-Z0-9 \n\.]', ' ', input_name).lower() \
                        == re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(card)).lower():
                    card_details = cards[card]
                    card_en_name = str(card)
                    card_jp_name = str(card_details['Japanese name'])
                    card_id = str(card_details['Card ID'])
                    found = True
                    break
                elif re.sub('[^a-zA-Z0-9 \n\.]', ' ', input_name).lower() \
                        in re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(card)).lower():
                    card_details = cards[card]
                    card_en_name = str(card)
                    card_jp_name = str(card_details['Japanese name'])
                    card_id = str(card_details['Card ID'])
                    found = True
            else:
                continue
            break
        if (found):
            embed = disnake.Embed(title=card_en_name,
                                  description=card_jp_name,
                                  timestamp=datetime.datetime.now(),
                                  color=0x9C84EF
                                  )
            
            for detail in card_details['Details']:
                for set_code in detail:
                    card_set_code = str(set_code)
                    rarity = detail[set_code]['rarity']
                    price = detail[set_code]['price']
                    condition = detail[set_code]['condition']
                    embed.add_field(name="Info",
                                    value="{}\nPrice: {}\nRarity: {}\nCondition: {}"
                                    .format(card_set_code, price, rarity, condition),
                                    inline=True)
            card_id = int(card_id)
            path = "pics/{}.jpg".format(card_id)

            if Path(path).is_file():
                pass
            else:
                card_img_url = "https://images.ygoprodeck.com/images/cards/{}.jpg".format(card_id)
                img_data = requests.get(card_img_url).content
                with open(path, 'wb') as handler:
                    handler.write(img_data)

            embed.set_image(file=disnake.File(path))
            embed.set_footer(text="Card ID: {}".format(card_id),)
        else:
            embed = disnake.Embed(
                title="Error!",
                description="Cannot find the card for now. \n Most likely our databases do not have the card.",
                color=0xE02B2B
            )

        await interaction.send(embed=embed)


#############################################################
#############################################################
    @commands.slash_command(
        name="cardcode",
        description="Input set code to find details about card. Contact MeiMei#3717 if things went wrong"
    )
    @checks.not_blacklisted()
    async def card_code_search(self, interaction: ApplicationCommandInteraction, input_code: str):
        
        await interaction.response.defer()
        with open("log.txt", "a") as log:
            log.write(input_code + "\n")
        with open("set_code.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        found = False

        for item in data:
            for set_code in item:
                if re.sub('[^a-zA-Z0-9 \n\.]', ' ', input_code).lower() \
                        in re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(set_code)).lower():
                    card_set_code = str(set_code)
                    card_en_name = item[set_code]['English name']
                    card_jp_name = item[set_code]['Japanese name']
                    card_id = item[set_code]['Card ID']
                    found = True
                    break
            else:
                continue
            break
        if(found):
            embed = disnake.Embed(
                                    title=card_set_code,
                                    description=card_en_name,
                                    timestamp=datetime.datetime.now(),
                                    color=0x9C84EF
                                 )
            with open("formatted_set_code.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                if re.sub('[^a-zA-Z0-9 \n\.]', ' ', input_code).lower() \
                        in re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(item)).lower():
                    for detail in data[item]:
                        rarity = (detail['Rarity'])
                        price = (detail['Price'])
                        condition = (detail['Condition'])
                    embed.add_field(name="Info",
                        value="Price: {}\nRarity: {}\nCondition: {}"
                        .format(price, rarity, condition),
                        inline=True)

            id = int(card_id)
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
        
        else:
            embed = disnake.Embed(
                title="Error!",
                description="Cannot find the card for now. \n Most likely our databases do not have the card.",
                color=0xE02B2B
            )
        
        await interaction.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.


def setup(bot):
    bot.add_cog(card_realted(bot))
