# wos-bot

a whiteout survival giftcode redeemer + utility bot

# installation + usage

1. clone this repository `git clone https://github.com/zenpaiang/wos-bot.git`
2. go into the directory `cd wos-bot`
3. install requirements `pip install -r requirements.txt`
4. [configure](#configuration) the bot
5. run the bot `python bot.py`

# configuration

this repo contains an example of the [configuration file](config.py) `config.py`, which has 3 values to configure.

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

# task list / future features

- [x] ~~migrate configuration from a json file to a python class~~ ([`ff0927c`](https://github.com/zenpaiang/wos-bot/commit/ff0927c55edbd2d070a0239b588a48f77ea415a1))
- [x] ~~remove alliance tag dependency~~ ([`6b64144`](https://github.com/zenpaiang/wos-bot/commit/6b64144ec9da8044fe360f5851112fcece4e0216))
- [x] ~~add fire crystal amounts from wos-database~~ ([`8d3f4a4`](https://github.com/zenpaiang/wos-bot/commit/8d3f4a47ca7c7657a135ce929901e93ba37b290f))
- [ ] add calculator for resources needed

## scrapped ideas

- [ ] add event-related commands
- [ ] add an auto-update feature