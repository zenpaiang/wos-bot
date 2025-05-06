# wos-bot (captcha + v2 update!)

a whiteout survival giftcode redeemer + utility bot using [ddddocr](https://github.com/sml2h3/ddddocr) for captcha detection

this bot is not related to [relo's bot](https://github.com/Reloisback/Whiteout-Survival-Discord-Bot) in any way.

if you like the project, please give it a :star:! 😊

# hardware requirements

this bot uses an onnx based OCR model which is not only fast, but is **~50MB** in size, meaning the bot runs at under **100MB** of RAM, and doesn't need any special hardware such as a CUDA supported GPU. this also means that the storage space needed is **<1GB**, allowing it to be run on a cheap VPS, a free one, or even on small SBCs.

# issues

please report any issues by creating an issue on github or messaging me on discord `@zenpaiang`

# usage

> [!NOTE]
> if you are migrating from v1, head to [migration](#migration-from-v1)

1. clone the repo: `git clone https://github.com/zenpaiang/wos-bot.git`
2. [configure](#configuration) the bot's `config.json`
3. rename `players.example.json` to `players.json`
4. install dependencies `pip install -r requirements.txt` or `pip3 install -r requirements.txt`
5. run the bot using `python bot.py` or `python3 bot.py`

> [!TIP]
> if you're on python 3.13 and above, run `pip install -r requirements.txt --ignore-requires-python` for step 4 instead. this is a temporary workaround.

# configuration

configuration is done by renaming `config.example.json` to `config.json`, which has 7 values to configure

```json
{
    "token": "[PUT YOUR BOT TOKEN HERE]",
    "admins": [],
    "players_file": "players.json",
    "bot_owner": 0,
    "auto_rename_users_during_redemption": true,
    "sync_discord_usernames": false,
    "redeem_locked_to_admins": false,
    "members_lock_to_admins": true
}
```

`token`: your bot token. for instructions on how to obtain one, click [here](https://interactions-py.github.io/interactions.py/Guides/02%20Creating%20Your%20Bot/) 

`admins`: this value is configured inside the bot  

`players_file`: this value stores the path to the players database. do not change if you don't know what you're doing.  

`bot_owner`: put your discord user ID here. for instructions on how to get it, click [here](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID)  

`auto_rename_users_during_redemption`: this value is configured inside the bot with `/admin settings`. it controls whether to automatically rename users in your database during redemption.  

`sync_discord_usernames`: this value is configured inside the bot with `/admin settings`. it controls whether the bot will sync wos usernames to linked discord users. (**note: this feature is currently under development and does not work.**)  

`redeem_locked_to_admins`: this value is configured inside the bot with `/admin settings`. it controls whether `/redeem` is usable by non-admins  

`members_lock_to_admins`: this value is configured inside the bot with `/admin settings`. it controls whether `/giftcode users` is usable by non-admins

# migration from v1

> [!CAUTION]
> doing this WILL override your old `players.json` file so if for whatever reason you still want the old version, please make a backup before doing this.

after cloning this repository:
1. copy your old `players.json` file into the directory
2. run the migration tool `python migration_tool.py`

# commands / features

view the commands and features list [here](commands_and_features.md)

# to-do list

- [x] ~~captcha detection + v2 update~~ ([`c5c5b47`](https://github.com/zenpaiang/wos-bot/commit/c5c5b4798e929320dce7550541c79e1fa3909414))
- [x] ~~functioning user list~~ ([`342f626`](https://github.com/zenpaiang/wos-bot/commit/342f6262b51cde98890de80d7e530ec6092ec2c1))
- [ ] better user list with search feature
- [ ] wos-database caching
- [ ] wos to discord player name sync
- [ ] auto update system
- [ ] bulk addition of ids