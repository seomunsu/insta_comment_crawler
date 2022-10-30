from dataclasses import dataclass


@dataclass
class InstagramComment:
    profile: str
    post: str
    comment: str
