from __future__ import annotations
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Callable,
    Generator,
    Sequence,
    Optional,
    TypeVar,
    Type,
)

from .core.graph import Graph
from .config import config
from neonize.client import NewClient
from neonize.proto.Neonize_pb2 import Message
from .utils import ChainMessage, log
from .types import MessageType as IMessageType
from .config import config_toml


class Filter(ABC):
    invert = False

    def __or__(self, __value: Filterable) -> FilterOP:
        return FilterOP(left=self, op=OP.OR, right=__value, invert=self.invert)

    def __and__(self, __value: Filterable) -> FilterOP:
        return FilterOP(left=self, op=OP.AND, right=__value, invert=self.invert)

    def __invert__(self):
        self.invert = not self.invert
        return self

    @abstractmethod
    def filter(self, client: NewClient, message: Message) -> bool: ...

    def _filter(self, client: NewClient, message: Message):
        result = self.filter(client, message)
        if self.invert:
            return not result
        return result

    def __repr__(self):
        return self.__class__.__name__


@dataclass
class FilterOP(Filter):
    left: Filter
    op: OP
    right: Filter
    invert: bool

    def filter(self, client: NewClient, message: Message) -> bool:
        left = self.left._filter(client, message)
        if self.invert:
            left = not left
        if self.op == OP.OR and left:
            return True
        return getattr(left, self.op.value)(self.right._filter(client, message))

    def __repr__(self):
        if self.op == OP.AND:
            rep = f"{self.left} ^ {self.right}"
        else:
            rep = f"{self.left} | {self.right}"
        if self.invert:
            rep = f"~({rep})"
        return rep


Filterable = TypeVar("Filterable", Filter, FilterOP)


class OP(Enum):
    OR = "__or__"
    AND = "__and__"


@dataclass
class CommandFunc:
    name: str
    filter: Filter | FilterOP
    description: str
    func: Callable[[NewClient, Message]]
    category: Sequence[str]
    allow_broadcast: bool
    on_error: Optional[str | Callable[[NewClient, Message, Exception], None]] = None


class GlobalCommand(dict[str, CommandFunc], Graph):
    start_point: int = 1

    def get_all_names(self) -> Generator[str, None, None]:
        for command in self.values():
            yield command.name

    @classmethod
    def generate_name(cls, start_point: int):
        point = start_point
        uid = ""
        while point > 0:
            r = point % 26
            uid += chr(97 + r)
            point = point // 26
        return uid[::-1]

    def add(self, command: CommandFunc):
        self.update({self.generate_name(self.start_point): command})
        self.start_point += 1

    def execute(self, client: NewClient, message: Message):
        for v in self.values():
            if (
                v.allow_broadcast
                or not message.Info.MessageSource.Chat.User == "broadcast"
            ):
                if v.filter.filter(client, message):
                    try:
                        v.func(client, message)
                    except Exception as e:
                        if isinstance(v.on_error, str):
                            client.reply_message(message.Message, message)
                        elif v.on_error and callable(v.on_error):
                            v.on_error(client, message, e)
                        else:
                            raise e
                    return True

    def register(
        self,
        filter: Filterable,
        name: str = "",
        description: str = "",
        category: Sequence[str] = ["all"],
        allow_broadcast: bool = False,
        on_error: Optional[
            str | Callable[[NewClient, Message, Exception], None]
        ] = None,
    ):
        def command(f: Callable[[NewClient, Message], Any]):
            log.debug(f"{name} command loaded")
            self.add(
                CommandFunc(
                    name=name or f.__name__,
                    filter=filter,
                    description=description,
                    func=f,
                    category=category,
                    allow_broadcast=allow_broadcast,
                    on_error=on_error,
                )
            )
            return f

        return command


command = GlobalCommand()


class Command(Filter):
    def __init__(
        self, command: str, prefix: Optional[str] = None, space_detection: bool = False
    ) -> None:
        """
        Initializes a Command instance.

        :param command: The command that this instance will represent.
        :type command: str
        :param prefix: An optional prefix for the command, defaults to None. If no prefix is provided, the prefix from the global config will be used.
        :type prefix: Optional[str], optional
        :param space_detection: A flag indicating whether to append a space to the command, defaults to False.
        :type space_detection: bool, optional
        """
        self.command = command + (" " if space_detection else "")
        self.prefix = config.prefix if prefix is None else prefix
        super().__init__()

    def filter(self, client: NewClient, message: Message) -> bool:
        """
        Checks whether the provided message starts with the command this instance represents.

        :param client: The client that received the message.
        :type client: NewClient
        :param message: The message to check.
        :type message: Message
        :return: True if the message starts with the command, False otherwise.
        :rtype: bool
        """
        text = ChainMessage.extract_text(message.Message)
        matched = re.match(self.prefix, text)
        if matched:
            _, end = matched.span(0)
            return text[end:].startswith(self.command)
        return False

    def __repr__(self):
        return (
            f"{(config.prefix if self.prefix is None else self.prefix) + self.command}"
        )


class MessageType(Filter):
    def __init__(self, *types: Type[IMessageType]) -> None:
        """Initialize MessageType filter with specified message types.

        :param types: Types of messages to be filtered.
        :type types: Type[IMessageType]
        """
        self.types = types

    def filter(self, client: NewClient, message: Message) -> bool:
        """Filter messages based on their types.

        :param client: The client object.
        :type client: NewClient
        :param message: The message object.
        :type message: Message
        :return: True if the message type matches any of the specified types, False otherwise.
        :rtype: bool
        """
        for _, v in message.Message.ListFields():
            if v.__class__ in self.types:
                return True
        return False

    def __repr__(self) -> str:
        """Representation of MessageType filter.

        :return: String representation of the filter.
        :rtype: str
        """
        types = " | ".join(map(lambda x: x.__name__, self.types))
        if self.types.__len__() > 1:
            return f"({types})"
        return types


class Owner(Filter):
    def filter(self, client: NewClient, message: Message) -> bool:
        """Filter messages based on whether the sender is the owner.

        :param client: The client object.
        :type client: NewClient
        :param message: The message object.
        :type message: Message
        :return: True if the sender is the owner, False otherwise.
        :rtype: bool
        """
        return message.Info.MessageSource.Sender.User in config_toml["thundra"]["owner"]
