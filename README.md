_v1.2.1_
#By RescueCat1100 on GitHub | meimei1100 on Discord

# General Discord Bot with Yu-Gi-Oh! OCG built-in function

## How to run

- Install Json Generator for generating data in correct json form
- Install required packages `pip install -r requirements.txt`
- Place json files in same directory as `bot.py`.
- The template of those files are included in this repo. You can make your own data and modify the reading process at `/cogs/slash/card_related.py`
- Edit `config.json` accordingly

## How to use

- Invite bot to server
- Run slash command `cardinfo` to search by name or `cardcode` to search by set code

## Known issues

- User need to either include special characters or skip them with a space. It should not be a problem unless card with multiple continuous special characters like `Maxx "C"`
- Delay time
- Not matching real-time data could lead to potential misinformation. But caching own data will asure the bot work even when 3rd party down.
