# wos-bot (captcha + v2 update!)

a whiteout survival giftcode redeemer + utility bot using [ddddocr](https://github.com/sml2h3/ddddocr) for captcha detection

# hardware requirements

this bot uses an onnx based OCR model which is not only fast, but is **~50MB** in size, meaning the bot runs at under **100MB** of RAM, and doesn't need any special hardware such as a CUDA supported GPU. this also means that the storage space needed is **<1GB**, allowing it to be run on a cheap VPS, a free one, or even on small SBCs.

# usage

> [!NOTE]
> if you are migrating from v1, head to [migration](#migration-from-v1)

1. clone the repo: `git clone https://github.com/zenpaiang/wos-bot.git`
2. [configure](#configuration) the bot's `config.json`
3. rename `players.example.json` to `players.json`
4. install dependencies `pip install -r requirements.txt`

# configuration

configuration is done by renaming `config.example.json` to `config.json`, which has 7 values to configure

```json
{
    "token": "", // your bot token
    "admins": [], // automatically configured by the bot, can change manually if wanted
    "players_file": "players.json", // players database
    "bot_owner": 0, // replace with your discord user ID
    "auto_rename_users_during_redemption": true, // whether to rename users during redemption
    "sync_discord_usernames": true, // whether to sync discord usernames with wos usernames
    "redeem_locked_to_admins": false, // whether the /redeem command is locked to admins
    "members_lock_to_admins": true // whether member modification is locked to admins
}
```

the last 4 values will be configurable from inside wos-bot in a future update.

> [!WARNING]
> wos to discord username syncing is currently under development and does not work.

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
- [ ] wos-database cachine
- [ ] wos to discord player name sync
- [ ] auto update system
- [ ] bulk addition of ids