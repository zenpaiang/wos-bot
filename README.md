# wos-bot-captcha

a whiteout survival giftcode redeemer + utility bot using [ddddocr](https://github.com/sml2h3/ddddocr) for captcha detection based on the upcoming (now abandoned) [v2 branch of wos-bot](https://github.com/zenpaiang/wos-bot/tree/v2)

average accuracy in captcha detection: 70%

# usage

1. clone the repo: `git clone --branch captcha https://github.com/zenpaiang/wos-bot.git`
2. configure the bot's `config.json`
3. install dependencies `pip install -r requirements.txt`

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
> some of the last 4 features are not working yet.

# commands / features

## gift code redemption (`giftcode`)

1. `redeem`: redeem a giftcode to everyone in the database
2. `users list`: list all the users (**NOT FUNCTIONAL**)
3. `users add`: add a user to the database
4. `users remove`: remove a user from the database
5. `users rename`: rename a user in the database

## calculation (`calculate`)

1. `time`: calculate the amount of time reduced after construction buffs
2. `gathering`: calculate how to distribute your gathering queues to equalize your resources

# upcoming / complete feature list

:x: = not developed :warning: = developed but untested :white_check_mark: = working + tested

## giftcode redemption

| feature | status | upcoming feature | status |
| --- | --- | --- | --- |
| adding users | :white_check_mark: | auto renaming of users during redemption | :white_check_mark: |
| removing users | :white_check_mark: | linking wos users to discord users | :white_check_mark: |
| listing users | :x: | username sync between wos and discord users | :x: |
| redemption of giftcodes | :white_check_mark: | permission system | :warning: |
| changing rank of users | :white_check_mark: | captcha detection | :white_check_mark: |

## database

| feature | status | upcoming feature | status |
| --- | --- | --- | --- |
| fire crystal database | :x: | automatic fetching / caching | :x: |
| chief gear database | :x: |
| chief charm database | :x: |