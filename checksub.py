from aiogram import BaseMiddleware, Bot
from aiogram.types import CallbackQuery , Message
from aiogram.enums import ChatMemberStatus
from aiogram import types
from typing import Callable, Dict, Any, Awaitable
from tgbot.keyboards.inline_user import sub_to_channel_finl

class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, channel_id: int):
        self.bot = bot
        self.channel_id = channel_id
        super().__init__()

    async def check_subscription(self, user_id: int) -> bool:
        """Проверка подписки по ID канала"""
        chat_member = await self.bot.get_chat_member(self.channel_id, user_id)
        return chat_member.status in {ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}

    async def __call__(
        self, handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]], 
        event: CallbackQuery, data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if await self.check_subscription(user_id):
            return await handler(event, data)
        else:
            await event.message.answer(
                text="❌ Для использования бота необходимо вступить в наш канал.",
                reply_markup=sub_to_channel_finl(),
            )
            return



class TextSubscriptionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, channel_id: int):
        self.bot = bot
        self.channel_id = channel_id
        super().__init__()

    async def check_subscription(self, user_id: int) -> bool:
        """Проверка подписки по ID канала"""
        chat_member = await self.bot.get_chat_member(self.channel_id, user_id)
        return chat_member.status in {ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}

    async def __call__(
        self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
        event: Message, data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if await self.check_subscription(user_id):
            return await handler(event, data)
        else:
            await event.answer(
                text="❌ Для использования бота необходимо вступить в наш канал.",
                reply_markup=sub_to_channel_finl(),
            )
            return

