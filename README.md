# 🤖 Telegram Reminder Bot

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Aiogram](https://img.shields.io/badge/aiogram-3.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

*Умный бот для напоминаний с уведомлениями в Telegram и на email*

[Особенности](#-особенности) • [Установка](#-установка) • [Использование](#-использование) • [Структура](#-структура-проекта)

</div>

## ✨ Особенности

- 🕐 **Гибкие напоминания** — создавай напоминания на любое время
- 📧 **Email-уведомления** — дублирование напоминаний на почту
- 💾 **Хранение данных** — все напоминания сохраняются в БД
- 🔔 **Повторные уведомления** — дополнительное напоминание через 20 минут
- 🎯 **Удобный интерфейс** — inline-кнопки и понятные команды
- ⚡ **Асинхронность** — быстрая и отзывчивая работа

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.9 или выше
- Telegram Bot Token (получи у [@BotFather](https://t.me/botfather))
- Почта Gmail (для email-уведомлений)

### Установка

```bash
# 1. Клонируй репозиторий
git clone https://github.com/hexrootdev/aiogram_bot_reminder.git
cd aiogram_bot_reminder

# 2. Создай виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# 3. Установи зависимости
pip install -r requirements.txt
```

### Настройка

1. Скопируй файл окружения:
```bash
cp .env.example .env
```

2. Открой `.env` и заполни своими данными:
```env
# Telegram Bot Token от @BotFather
BOT_TOKEN=ваш_токен_бота

# Настройки почты (Gmail)
MAILER=ваша_почта@gmail.com
EMAIL_APP_PASS=ваш_пароль_приложения

# Настройки базы данных
DB_PASSWORD=пароль_базы_данных
```

### Запуск

```bash
python main.py
```

Бот запустится и будет готов к работе! Перейди в Telegram и начни общение с ботом.

## 💡 Использование

### Основные команды

| Команда | Описание | Пример |
|---------|----------|---------|
| `/start` | Начать работу с ботом | `/start` |
| `/help` | Показать справку | `/help` |


## 🛠️ Технологии

<div align="center">

![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/-Aiogram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-D71F00?style=for-the-badge&logo=databricks&logoColor=white)
![APScheduler](https://img.shields.io/badge/-APScheduler-FF6F00?style=for-the-badge)

</div>

- **Python 3.9+** — основной язык
- **Aiogram 3.x** — асинхронный фреймворк для Telegram Bot API
- **APScheduler** — планировщик задач для напоминаний
- **SQLAlchemy** — ORM для работы с базой данных
- **PostgreSQL** — хранение данных
- **AIOSMTP** — отправка email-уведомлений

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

---

<div align="center">

### ⭐ Если проект понравился, поставь звезду на GitHub!

**Разработано с ❤️ для удобных напоминаний**

[📁 Код](https://github.com/hexrootdev/aiogram_bot_reminder) • 
[🐛 Сообщить об ошибке](https://github.com/hexrootdev/aiogram_bot_reminder/issues) • 
[💡 Предложить улучшение](https://github.com/hexrootdev/aiogram_bot_reminder/pulls)

</div>
```
