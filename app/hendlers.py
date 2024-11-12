from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import F
import io
from aiogram import Router, types
import app.keyBoards as kb

from . import database
from .pdf_parser import extract_text_from_pdf, get_line_from_text
import random
import qrcode

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    user = message.from_user
    database.add_user(user.id, user.username, user.first_name)
    await message.answer_photo(
        photo="https://i.ibb.co/ThZqqFz/bn.jpg",
        caption='Привет, дружище! Готов к самому крутому вечеру?\n'
                'Здесь ты можешь быстро и легко приобрести билет на наше мероприятие, '
                'узнать все детали и быть в курсе событий. \nДавай, выбирай, что тебе нужно, '
                'и до встречи на тусовке!',
        reply_markup=kb.main
    )


@router.callback_query(F.data == 'cancel')
async def cancel_all(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="https://i.ibb.co/ThZqqFz/bn.jpg",
        caption='Привет, дружище! Готов к самому крутому вечеру?\n'
                'Здесь ты можешь быстро и легко приобрести билет на наше мероприятие,'
                'узнать все детали и быть в курсе событий. \nДавай, выбирай, что тебе нужно,'
                'и до встречи на тусовке!',
        reply_markup=kb.main
    )


@router.callback_query(F.data == 'pay_ticket')
async def pay_ticket(callback: CallbackQuery):
    database.add_or_update_ticket(callback.from_user.id, callback.data, 'Выбирает', 'Не оплачен')
    await callback.answer(" ")
    await callback.message.delete()
    await callback.message.answer(
        'Выберите тип билета 🎟:\n'
        '- Танцпол: 690₽\n'
        '- Танцпол+: 849₽\n'
        '- Super VIP: 1390₽\nНажмите на нужный вариант для оформления заказа.',
        reply_markup=kb.ticket_keyboard
    )


@router.callback_query(F.data == "ticket_standard")
async def ticket_standard_callback(callback: CallbackQuery):
    database.add_or_update_ticket(callback.from_user.id, callback.data, 'Выбран', 'Не оплачен')

    await callback.answer(" ")
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="https://i.ibb.co/x2X0W1d/dancefloor.jpg",
        caption="📝 ***Вы выбрали Танцпол билет***\n"
                "💵 Стоимость: 690₽\n"
                "👉 Для оплаты через перевод на карту, выполните следующие шаги:\n"
                "1. Переведите 690₽ на карту: ВАШ НОМЕР КАРТЫ ***(Сбербанк, ваш банк тоже должен быть Сбербанк)***.\n"
                "2. После перевода сохраните чек в формате PDF.\n"
                "3. Отправьте этот чек боту для подтверждения оплаты.\n"
                "⚠️ После получения подтверждения, ваш билет будет активирован, "
                "и вы получите электронный билет на мероприятие.\n"
                "Если возникнут вопросы, обращайтесь к организаторам через наш чат поддержки ВАШ ТГ АЙДИ.",
        parse_mode="Markdown",
        reply_markup=kb.confirm_keyboard
    )


@router.message(F.document)
async def handle_pdf_upload(message: Message):
    telegram_id = message.from_user.id
    file_name = f'pdf/{telegram_id}.pdf'
    user_id = message.from_user.id
    file_id = message.document.file_id
    document = await message.bot.get_file(file_id)
    await message.bot.download_file(document.file_path, file_name)

    pdf_text = extract_text_from_pdf(file_name)

    line_sum = 17  # Сумма перевода
    line_name = 7  # ФИО отправителя
    result_line_sum = get_line_from_text(pdf_text, line_sum)
    result_line_name = get_line_from_text(pdf_text, line_name)

    if result_line_sum.strip() == "690,00 ₽" and result_line_name.strip() == "Имя в чеке сбербанк":
        database.update_payment_status(user_id, "Оплачено")

        # Создаем QR-код
        qr = qrcode.make(

            f'{random.randint(1, 1011) * random.randint(10, 10) * random.randint(10, 101)}'
            f'\nТип билета: Танцпол\nСтатус: Оплачено')

        # Сохраняем изображение QR-кода в памяти
        qr_bytes = io.BytesIO()
        qr.save(qr_bytes, format='PNG')
        qr_bytes.seek(0)  # Возвращаемся к началу потока данных

        # Создаем BufferedInputFile для отправки фото из памяти
        input_file = types.BufferedInputFile(qr_bytes.getvalue(), filename="qr_code.png")
        await message.answer_photo(photo=input_file)

    elif result_line_sum.strip() == "849,00 ₽" and result_line_name.strip() == "Имя получателя сбербанк":
        database.update_payment_status(user_id, "Оплачено")

        # Создаем QR-код
        qr = qrcode.make(
            f'Уникальный код:{random.randint(1, 1011) * random.randint(10, 10) * random.randint(10, 101)}'
            f'\nТип билета: Танцпол+\nСтатус: Оплачено')

        # Сохраняем изображение QR-кода в памяти
        qr_bytes = io.BytesIO()
        qr.save(qr_bytes, format='PNG')
        qr_bytes.seek(0)  # Возвращаемся к началу потока данных

        input_file = types.BufferedInputFile(qr_bytes.getvalue(), filename="qr_code.png")
        await message.answer_photo(photo=input_file)

    elif result_line_sum.strip() == "1390,00 ₽" and result_line_name.strip() == "Имя получателя сбербанк":

        database.update_payment_status(user_id, "Оплачено")

        qr = qrcode.make(
            f'{random.randint(1, 1011) * random.randint(10, 10) * random.randint(10, 101)}'
            f'\nТип билета: VIP\nСтатус: Оплачено')

        qr_bytes = io.BytesIO()
        qr.save(qr_bytes, format='PNG')
        qr_bytes.seek(0)

        input_file = types.BufferedInputFile(qr_bytes.getvalue(), filename="qr_code.png")
        await message.answer_photo(photo=input_file)

    else:
        await message.answer("Оплата не подтверждена. Проверьте сумму и ФИО.")


@router.callback_query(F.data == "ticket_plus")
async def ticket_plus_callback(callback: CallbackQuery):
    database.add_or_update_ticket(callback.from_user.id, callback.data, 'Выбран', 'Не оплачен')
    await callback.answer(" ")
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="https://i.ibb.co/tmPmvNS/dancefloor.jpg",
        caption="📝 ***Вы выбрали Танцпол+ билет***\n"
                "💵 Стоимость: 849₽\n"
                "👉 Для оплаты через перевод на карту, выполните следующие шаги:\n"
                "1. Переведите 849₽ на карту: ВАШ НОМЕР КАРТЫ ***(Сбербанк, ваш банк тоже должен быть Сбербанк)***.\n"
                "2. После перевода сохраните чек в формате PDF.\n"
                "3. Отправьте этот чек боту для подтверждения оплаты.\n"
                "⚠️ После получения подтверждения, ваш билет будет активирован, "
                "и вы получите электронный билет на мероприятие.\n"
                "Если возникнут вопросы, обращайтесь к организаторам через наш чат поддержки ВАШ ТГ АЙДИ.",
        parse_mode="Markdown",
        reply_markup=kb.confirm_keyboard
    )


@router.callback_query(F.data == "ticket_vip")
async def ticket_vip_callback(callback: CallbackQuery):
    database.add_or_update_ticket(callback.from_user.id, callback.data, 'Выбран', 'Не оплачен')
    await callback.answer(" ")
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="https://i.ibb.co/xDZqDYP/superr-vip.jpg",
        caption="📝 ***Вы выбрали SUPER VIP билет***\n"
                "💵 Стоимость: 1390₽\n"
                "👉 Для оплаты через перевод на карту, выполните следующие шаги:\n"
                "1. Переведите 1390₽ на карту: ВАШ НОМЕР КАРТЫ ***(Сбербанк, ваш банк тоже должен быть Сбербанк)***.\n"
                "2. После перевода сохраните чек в формате PDF.\n"
                "3. Отправьте этот чек боту для подтверждения оплаты.\n"
                "⚠️ После получения подтверждения, ваш билет будет активирован, "
                "и вы получите электронный билет на мероприятие.\n"
                "Если возникнут вопросы, обращайтесь к организаторам через наш чат поддержки ВАШ ТГ АЙДИ.",
        parse_mode="Markdown",
        reply_markup=kb.confirm_keyboard
    )


@router.callback_query(F.data == 'info')
async def catalog(callback: CallbackQuery):
    await callback.answer(" ")
    await callback.message.delete()
    await callback.message.answer(
        text='📅 Когда: 9 ноября \n'
             '📍 Где: Aurora Concert Hall\n'
             '***Почему продажа билетов идет через телеграмм бота?***\n '
             "\n"
             'Мы захотели сделать максимально удобным наше взаимодействие'
             ' с вами и создать телеграмм бота, который вы можете использовать'
             ' не только для покупки билетов, но и для получения обратной связи'
             ' от нас, уведомления о новых мероприятиях и нововведениях.',
        parse_mode="Markdown",
        reply_markup=kb.cancalls
    )


@router.callback_query(F.data == 'how_pay')
async def how_pay(callback: CallbackQuery):
    await callback.answer(" ")
    await callback.message.delete()
    await callback.message.answer(
        text="1. Переведите XXXX₽ на карту: ВАШ НОМЕР КАРТЫ ***(Сбербанк, ваш банк тоже должен быть Сбербанк)***.\n"
             "2. После перевода сохраните чек.\n"
             "3. Отправьте этот чек боту для подтверждения оплаты.\n"
             "***⚠️ После получения подтверждения, ваш билет будет активирован,"
             " и вы получите электронный билет на мероприятие.***\n"
             "Если возникнут вопросы, обращайтесь к организаторам через наш чат поддержки.",
        parse_mode='Markdown',
        reply_markup=kb.cancalls
    )


@router.callback_query(F.data == 'help')
async def help_user(callback: CallbackQuery):
    await callback.answer(" ")
    await callback.message.delete()
    await callback.message.answer(
        text='Если у вас возникли проблемы с ботом.\n'
             'Напишите нашему администратору ВАШ ТГ АЙДИ.',
        reply_markup=kb.cancalls
    )
