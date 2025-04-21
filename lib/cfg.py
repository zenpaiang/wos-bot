from dataclasses import dataclass

@dataclass
class Config:
    token: str
    admins: list[str]
    players_file: str
    bot_owner: int
    auto_rename_users_during_redemption: bool
    sync_discord_usernames: bool
    redeem_locked_to_admins: bool
    members_lock_to_admins: bool

    @classmethod
    def from_dict(cls, config: dict) -> "Config":
        return cls(**config)

    def to_dict(self) -> dict:
        return self.__dict__