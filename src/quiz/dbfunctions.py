import aiosqlite
from aiogram import types
from questions import quiz_data
DB_NAME = 'db/quiz_bot.db'

async def create_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Таблица для текущего вопроса
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        # Таблица для текущего счета
        await db.execute('''CREATE TABLE IF NOT EXISTS user_scores (user_id INTEGER PRIMARY KEY, score INTEGER)''')
        # Таблица для сохранения результатов
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, score INTEGER, total_questions INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        # Сохраняем изменения
        await db.commit()

async def update_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()

async def get_quiz_index(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def get_user_score(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем результат для заданного пользователя
        async with db.execute('SELECT score FROM user_scores WHERE user_id = ?', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def update_user_score(user_id, score):
    async with aiosqlite.connect(DB_NAME) as db:
        #Обновляем результат для заданного пользователя
        await db.execute(
            'INSERT OR REPLACE INTO user_scores (user_id, score) VALUES (?, ?)', (user_id, score))
        await db.commit()

async def save_quiz_result(user_id, score):
    async with aiosqlite.connect(DB_NAME) as db:
        #Сохраняем результат прохождения квиза для заданного пользователя
        await db.execute(
            'INSERT INTO quiz_results (user_id, score, total_questions) VALUES (?, ?, ?)', (user_id, score, len(quiz_data)))
        await db.commit()

async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    # Получаем последний результат
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            'SELECT score, total_questions, timestamp FROM quiz_results '
            'WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1',
            (user_id,)) as cursor:
            result = await cursor.fetchone()
    if result:
        score, total_questions, timestamp = result
        await message.answer(
            f"📊 Ваша статистика:\n"
            f"Последний результат: {score}/{total_questions}\n"
            f"Дата прохождения: {timestamp}")
    else:
        await message.answer("Вы еще не проходили квиз. Начните с команды /quiz")