from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🎟 Купить билет', callback_data='pay_ticket'),
     InlineKeyboardButton(text='ℹ️ О мероприятии', callback_data='info')],
    [InlineKeyboardButton(text='💳 Как оплатить', callback_data='how_pay'),
     InlineKeyboardButton(text='📝 Обратная связь', callback_data='help')]
])

ticket_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Танцпол — 690₽", callback_data="ticket_standard")],
        [InlineKeyboardButton(text="Танцпол+ — 849₽", callback_data="ticket_plus")],
        [InlineKeyboardButton(text="Super VIP билет — 1390₽", callback_data="ticket_vip")],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    ]
)

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    ]
)
cancalls = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='cancel')]
    ]
)


