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

# commands / features

## gift code redemption (`giftcode`)

1. `users list`: list all the users
2. `users add`: add a user to the redemption list
3. `users remove`: remove a user from the redemption list
4. `users rename`: rename a user in the redemption list 

## calculation (`calculate`)

1. `time`: calculate the amount of time reduced after construction buffs

## database (`database`)

1. `chief_gear`: get information about a rarity of chief gear or the amount of resources needed to upgrade to that rarity
2. `chief_charm`: get information about a rarity of chief charm or the amount of resources needed to upgrade to that rarity
3. `fire_crystals`: get amount of fire crystals needed to upgrade buildings

# task list / future features

- [x] ~~migrate configuration from a json file to a python class~~ ([`ff0927c`](https://github.com/zenpaiang/wos-bot/commit/ff0927c55edbd2d070a0239b588a48f77ea415a1))
- [x] ~~remove alliance tag dependency~~ ([`6b64144`](https://github.com/zenpaiang/wos-bot/commit/6b64144ec9da8044fe360f5851112fcece4e0216))
- [x] ~~add fire crystal amounts from wos-database~~ ([`8d3f4a4`](https://github.com/zenpaiang/wos-bot/commit/8d3f4a47ca7c7657a135ce929901e93ba37b290f))
- [x] ~~add fire crystal thumbnails from wos-database~~ ([`eefea93`](https://github.com/zenpaiang/wos-bot/commit/eefea93b86c3dc0ed693ad19b4862663ee66ea8c))
- [x] ~~add paginator for user list~~ ([`f3680b4`](https://github.com/zenpaiang/wos-bot/commit/f3680b4c49929a0c178f771a2829891e071bdd91))
- [x] ~~add resource amount calculator~~ ([`31f20b6`](https://github.com/zenpaiang/wos-bot/commit/31f20b61fb62d671d1403c3134128ccaa815b152) + [`56e1de0`](https://github.com/zenpaiang/wos-bot/commit/56e1de0f016865d03dd96019f26ccaa16cc48a6b))

## scrapped ideas / unlikely to do

- [ ] add event-related commands
- [ ] add an auto-update feature
- [ ] add fc6 to fc10 data to wos-database and wos-bot