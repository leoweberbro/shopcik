# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
import asyncio

from tgbot.database import Settingsx, Positionx, Categoryx
from tgbot.keyboards.inline_user import user_support_finl, sub_to_channel_finl
from tgbot.keyboards.inline_user_page import prod_item_position_swipe_fp
from tgbot.keyboards.reply_main import menu_frep
from tgbot.utils.const_functions import ded
from tgbot.utils.misc.bot_filters import IsBuy, IsRefill, IsWork
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.const_functions import remove_reply_keyboard
from tgbot.utils.text_functions import position_open_user
from tgbot.data.config import CHANNEL_ID, CHANNEL_LINK

# Игнор-колбэки покупок
prohibit_buy = [
    'buy_category_swipe',
    'buy_category_open',
    'buy_position_swipe',
    'buy_position_open',
    'buy_item_open',
    'buy_item_confirm',
]

# Игнор-колбэки пополнений
prohibit_refill = [
    'user_refill',
    'user_refill_method',
    'Pay:Cryptobot',
    'Pay:Yoomoney',
    'Pay:',
]

router = Router(name=__name__)


################################################################################
########################### СТАТУС ТЕХНИЧЕСКИХ РАБОТ ###########################
# Фильтр на технические работы - сообщение
@router.message(IsWork())
async def filter_work_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_settings = Settingsx.get()

    if get_settings.misc_support != "None":
        return await message.answer(
            "<b>⛔ Бот находится на технических работах</b>",
            reply_markup=user_support_finl(get_settings.misc_support),
        )

    await message.answer("<b>⛔ Бот находится на технических работах</b>")


# Фильтр на технические работы - колбэк
@router.callback_query(IsWork())
async def filter_work_callback(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await call.answer("⛔ Бот находится на технических работах.", True)


################################################################################
################################# СТАТУС ПОКУПОК ###############################
# Фильтр на доступность покупок - сообщение
@router.message(IsBuy(), F.text == "🎁 Купить")
@router.message(IsBuy(), StateFilter('here_item_count'))
async def filter_buy_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer("<b>⛔ Покупки временно отключены</b>")


# Фильтр на доступность покупок - колбэк
@router.callback_query(IsBuy(), F.text.startswith(prohibit_buy))
async def filter_buy_callback(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await call.answer("⛔ Покупки временно отключены.", True)


################################################################################
############################### СТАТУС ПОПОЛНЕНИЙ ##############################
# Фильтр на доступность пополнения - сообщение
@router.message(IsRefill(), StateFilter('here_pay_amount'))
async def filter_refill_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer("<b>⛔ Пополнение временно отключено</b>")


# Фильтр на доступность пополнения - колбэк
@router.callback_query(IsRefill(), F.text.startswith(prohibit_refill))
async def filter_refill_callback(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await call.answer("⛔ Пополнение временно отключено.", True)


################################################################################
#################################### ПРОЧЕЕ ####################################
# Открытие главного меню
@router.message(F.text.in_(('🔙 Главное меню', '/start')))
async def main_start(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    # Проверка на вступление в канал по ID
    user_id = message.from_user.id
      # Замените на ID вашего канала

    member = await bot.get_chat_member(CHANNEL_ID, user_id)
    if member.status not in ['member', 'administrator', 'creator']:
        await message.answer(
            text="❌",
            reply_markup={"remove_keyboard": True},
        )
        await message.delete()

        await message.answer(
            text="❌ Для использования бота необходимо вступить в наш канал.",
            reply_markup=sub_to_channel_finl(),
        )
        return

    await message.answer(
        ded("""
            🔸 Бот готов к использованию.
            🔸 Если не появились вспомогательные кнопки
            🔸 Введите /start
        """),
        reply_markup=menu_frep(message.from_user.id),
    )


# Открытие диплинков
@router.message(F.text.startswith('/start '))
async def main_start_deeplink(message: Message, bot: Bot, state: FSM, arSession: ARS):
    deepling_args = message.text[7:]

    if deepling_args.startswith("p_"):
        position_id = deepling_args[2:]

        get_position = Positionx.get(position_id=position_id)

        if get_position is not None:
            await position_open_user(bot, message.from_user.id, position_id, 0)
    elif deepling_args.startswith("c_"):
        category_id = deepling_args[2:]

        get_category = Categoryx.get(category_id=category_id)

        if get_category is not None:
            await message.answer(
                f"<b>🎁 Текущая категория: <code>{get_category.category_name}</code></b>",
                reply_markup=prod_item_position_swipe_fp(0, category_id),
            )
