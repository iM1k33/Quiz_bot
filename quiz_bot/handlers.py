from aiogram import F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from .dbfunctions import  update_quiz_index, get_quiz_index, get_user_score, update_user_score, save_quiz_result
from .questions import quiz_data

# Хэндлер команды /start
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Результаты"))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

# Хэндлер на команды /quiz
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await new_quiz(message)

# Хэндлер нового квиза
async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза в 0
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    #Сбрасываем значение результатов
    await update_user_score(user_id, 0)
    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)

# Функция запроса вопроса квиза
async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    current_question = quiz_data[current_question_index]
    # Генерируем клавиатуру с передачей индексов
    kb = generate_options_keyboard(current_question['options'])
    await message.answer(
        f"❔ Вопрос {current_question_index + 1}/{len(quiz_data)}:\n"
        f"{current_question['question']}",
        reply_markup=kb)

# Функция генерации кнопок
def generate_options_keyboard(answer_options):
    builder = InlineKeyboardBuilder()

    for index, option in enumerate(answer_options):
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"answer_{index}"))  # Передаем индекс вместо текста
    builder.adjust(1)
    return builder.as_markup()

async def answer_handler(callback: types.CallbackQuery):
    # Извлекаем индекс выбранного варианта
    selected_index = int(callback.data.replace("answer_", ""))
    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)
    current_question = quiz_data[current_question_index]
    # Получаем текст выбранного варианта
    selected_option_text = current_question['options'][selected_index]
    # Получаем правильный ответ
    correct_option_index = current_question['correct_option']
    correct_option_text = current_question['options'][correct_option_index]
    # Удаляем клавиатуру
    await callback.bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=None)
    
    # Проверяем правильность ответа
    if selected_index == correct_option_index:
        # Обработка правильного ответа
        await callback.message.answer(
            f"✅ Вы ответили правильно!\n"
            f"Ваш выбор: {selected_option_text}")
        # Увеличиваем счетчик
        current_score = await get_user_score(user_id)
        await update_user_score(user_id, current_score + 1)
    else:
        # Обработка неправильного ответа
        await callback.message.answer(
            f"❌ Вы выбрали: {selected_option_text}\n"
            f"Правильный ответ: {correct_option_text}")
    
    # Переход к следующему вопросу
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)
    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        # Завершение квиза
        total_score = await get_user_score(user_id)
        await save_quiz_result(user_id, total_score)
        #await update_user_score(user_id, 0)
        await callback.message.answer(
            f"🎉 Квиз завершен! Ваш результат: {total_score}/{len(quiz_data)}\n"
            f"Чтобы посмотреть статистику, используйте /stats")