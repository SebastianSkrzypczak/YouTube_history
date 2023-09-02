from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime


@dataclass
class Video:

    videoId: str
    publishedAt: datetime
    channelId: str
    categoryId: int
    duration: str
    viewCount: int
    likeCount: int


@dataclass
class Channel:
    channelId: str
    title: str
    publishedAt: datetime
    viewCount: int
    subscriberCount: int
    videoCount: int


class Repository(ABC):

    @abstractmethod
    def add(self):
        return ...
