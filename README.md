# wos-bot

a whiteout survival giftcode redeemer + utility bot

# installation + usage

1. clone this repository `git clone https://github.com/zenpaiang/wos-bot.git`
2. go into the directory `cd wos-bot`
3. install requirements `pip install -r requirements.txt`
4. rename `config.example.py` to `config.py`
5. rename `players.example.json` to `players.json`
6. [configure](#configuration) the bot
7. run the bot `python bot.py`

# configuration

this repo contains an example of the [configuration file](config.example.py) `config.example.py`, which has 3 values to configure.

1. `BOT_TOKEN`: your discord bot token
2. `PLAYERS_FILE`: the path of the players list
3. `ACTIVITY`: the activity to be displayed on the bot (set to `None` to turn off)

the api reference for activities in the library i use can be found [here](https://interactions-py.github.io/interactions.py/API%20Reference/API%20Reference/models/Discord/activity/).

# updating the bot

when updating the bot, all you need to do is  
  
1. cd into the repo folder `cd wos-bot`
2. fetch the latest update `git pull`

migration to new formats of the config/database will be done automatically, as with the current `players.json` version 2.

# commands / features

## gift code redemption (`giftcode`)

1. `redeem`: redeem a giftcode to everyone in the database
2. `users list`: list all the users
3. `users add`: add a user to the database
4. `users remove`: remove a user from the database
5. `users rename`: rename a user in the database
6. `autorename`: automatically rename all users in the database to their latest usernames

## calculation (`calculate`)

1. `time`: calculate the amount of time reduced after construction buffs
2. `gathering`: calculate how to distribute your gathering queues to equalize your resources

## database (`database`)

1. `chief_gear`: get information about a rarity of chief gear or the amount of resources needed to upgrade to that rarity
2. `chief_charm`: get information about a rarity of chief charm or the amount of resources needed to upgrade to that rarity
3. `fire_crystals`: get amount of fire crystals needed to upgrade buildings

## user (`user`)

1. `info`: get profile picture and furnace level for a user

# task list / future features

- [x] ~~migrate configuration from a json file to a python class~~ ([`ff0927c`](https://github.com/zenpaiang/wos-bot/commit/ff0927c55edbd2d070a0239b588a48f77ea415a1))
- [x] ~~remove alliance tag dependency~~ ([`6b64144`](https://github.com/zenpaiang/wos-bot/commit/6b64144ec9da8044fe360f5851112fcece4e0216))
- [x] ~~add fire crystal amounts from wos-database~~ ([`8d3f4a4`](https://github.com/zenpaiang/wos-bot/commit/8d3f4a47ca7c7657a135ce929901e93ba37b290f))
- [x] ~~add fire crystal thumbnails from wos-database~~ ([`eefea93`](https://github.com/zenpaiang/wos-bot/commit/eefea93b86c3dc0ed693ad19b4862663ee66ea8c))
- [x] ~~add paginator for user list~~ ([`f3680b4`](https://github.com/zenpaiang/wos-bot/commit/f3680b4c49929a0c178f771a2829891e071bdd91))
- [x] ~~add resource amount calculator~~ ([`31f20b6`](https://github.com/zenpaiang/wos-bot/commit/31f20b61fb62d671d1403c3134128ccaa815b152) + [`56e1de0`](https://github.com/zenpaiang/wos-bot/commit/56e1de0f016865d03dd96019f26ccaa16cc48a6b) + [`73798a6`](https://github.com/zenpaiang/wos-bot/commit/73798a6258f3cbe197c5eadccf63f16e8d1179ab))
- [x] ~~add status message support in config~~ ([`46f8a31`](https://github.com/zenpaiang/wos-bot/commit/46f8a3110f40f83edae5986b8d095c8134cba0ae))
- [x] ~~add support for fetching a user's furnace level + profile picture~~ ([`0514ef4`](https://github.com/zenpaiang/wos-bot/commit/0514ef429fb4678e0d4f8a924ec693e99b3ef150))
- [x] ~~add rank support when adding players~~ ([`074705c`](https://github.com/zenpaiang/wos-bot/commit/074705c90be0b0f8587bcb622d0b6264ce3adc67))
- [x] ~~add auto rename system during giftcode redemption~~ ([`12f00c7`](https://github.com/zenpaiang/wos-bot/commit/12f00c76864a1d620527f58e914c12ffb81250d2))
- [x] ~~add fc6 to fc10 data to wos-database and wos-bot~~ ([`8d10546`](https://github.com/zenpaiang/wos-bot/commit/8d1054697f5c2c7f98abb56371e3081bf04734e8))

## scrapped ideas / unlikely to do

- [ ] add event-related commands
- [ ] add an auto-update feature
- [ ] add support for linking discord users to a whiteout survival user