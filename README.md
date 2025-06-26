# Telegram Quiz Bot 🤖❓  
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://aiogram.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
Телеграм-бот для проведения викторин с возможностью ведения статистики пользователей. Бот задает вопросы из базы данных, обрабатывает ответы и сохраняет результаты.
## 🌟 Особенности
- Интерактивная викторина с вопросами и вариантами ответов  
- Система подсчета очков и ведения статистики  
- Удобная клавиатура для взаимодействия  
- Хранение данных в SQLite базе данных  
- Легко расширяемая база вопросов  
## 🚀 Быстрый старт
### Предварительные требования
- Python 3.11+  
- Аккаунт Telegram и токен бота от [@BotFather](https://t.me/BotFather)  
### Установка
```bash
git clone https://github.com/iM1k33/Quiz_bot.git
cd Quiz_bot
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
# Установка зависимостей
pip install -r requirements.txt
```
### Настройка бота
1. Скопируйте файл-пример конфигурации:
```bash
cp quiz_bot/api_example.py quiz_bot/api.py
```
2. Откройте `quiz_bot/api.py` и замените строку:
```python
API_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # ← Вставьте сюда ваш токен
```
### Запуск
```bash
python run.py
```
## 🎮 Использование
- `/start` - Начать взаимодействие с ботом  
- "Начать игру" - Запустить новую викторину  
- "Результаты" - Просмотреть свою статистику  
- `/quiz` - Альтернативная команда для запуска викторины  
- `/stats` - Альтернативная команда для просмотра статистики  
**Во время викторины**:  
- Бот задает вопросы по одному  
- Пользователь выбирает вариант ответа  
- После каждого ответа показывается правильный вариант  
- В конце сессии выводится общий результат  
## 📚 Организация базы вопросов
Вопросы хранятся в файле `quiz_bot/questions.py`:
```python
quiz_data = [
    {
        "question": "Какой язык программирования создал Гвидо ван Россум?",
        "options": ["Java", "Python", "C++", "JavaScript"],
        "correct_option": 1,  # Индекс правильного ответа
        "explanation": "Python был создан Гвидо ван Россумом в 1991 году."
    },
    {
        "question": "Какой тип данных в Python неизменяем?",
        "options": ["list", "dict", "tuple", "set"],
        "correct_option": 2,
        "explanation": "Кортежи (tuple) являются неизменяемыми."
    },
    # Добавьте свои вопросы...
]
```
### Особенности базы вопросов:
1. Легко редактируемый формат  
2. Поддержка объяснений к ответам  
3. Автоматическая проверка корректности ответов  
## 🗂️ Структура проекта
```
Quiz_bot/
├── .gitignore
├── README.md               # Этот файл
├── requirements.txt        # Зависимости
├── run.py                  # Точка входа
└── quiz_bot/               # Основной пакет
    ├── __init__.py         # Инициализация пакета
    ├── main.py             # Главный модуль бота
    ├── handlers.py         # Обработчики сообщений
    ├── dbfunctions.py      # Функции работы с БД
    ├── api.py              # Токен бота (создается пользователем)
    ├── api_example.py      # Пример файла конфигурации
    └── questions.py        # База вопросов викторины
```
## ⚙️ Технологии
- [aiogram](https://aiogram.dev/) - Асинхронный фреймворк для Telegram Bot API  
- [SQLite](https://sqlite.org/) - Встроенная база данных  
- [aiosqlite](https://aiosqlite.omnilib.dev/) - Асинхронный доступ к SQLite  
## 📈 Возможные улучшения
- Добавление категорий вопросов  
- Система уровней сложности  
- Рейтинговая таблица лидеров  
- Поддержка изображений в вопросах  
- Мультиязычная поддержка  
- Интеграция с внешними API  
## 🤝 Как внести вклад
1. Форкните репозиторий  
2. Создайте ветку: `git checkout -b feature/your-feature`  
3. Сделайте коммит: `git commit -m 'Add some feature'`  
4. Запушьте ветку: `git push origin feature/your-feature`  
5. Откройте Pull Request  
## 📜 Лицензия
Проект распространяется под лицензией MIT. Подробнее в файле [LICENSE](LICENSE).