# Football Telegram Bot

Telegram-бот для отслеживания футбольных матчей с AI-прогнозами и ревью на основе DeepSeek.

## О проекте

Бот собирает данные о футбольных матчах из внешнего API (RapidAPI), кеширует их в SQLite и предоставляет пользователю:
- список матчей по датам и лигам
- детали матча: составы, счёт, статистику
- AI-прогнозы на исход матча (DeepSeek)
- AI-обзоры прошедших матчей

## Возможности

-  **Матчи по датам** — выбери лигу (EPL, La Liga, Bundesliga) и дату
-  **Детали матча** — составы, схема, рейтинг игроков
-  **AI-прогнозы** — DeepSeek анализирует статистику и даёт прогноз
-  **AI-обзоры** — краткий разбор прошедших матчей
-  **Кеширование** — SQLite, автообновление для завершённых матчей
-  **REST API** — FastAPI с эндпоинтами для матчей и составов
-  **Логирование** — с ротацией файлов и фильтрами

## Технологии

- **Python 3.11+**
- **pyTelegramBotAPI** — Telegram-бот
- **FastAPI** — REST API
- **SQLite** — кеш данных
- **DeepSeek API** — AI-прогнозы
- **RapidAPI** (Football API) — источник данных
- **Railway** — деплой
- **pytest** — тесты


# ⚽ Football Telegram Bot

Telegram-бот для отслеживания футбольных матчей с AI-прогнозами на основе DeepSeek.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 О проекте

Бот собирает данные о футбольных матчах из внешнего API (RapidAPI), кеширует их в SQLite и предоставляет пользователю:
- список матчей по датам и лигам
- детали матча: составы, счёт, статистику
- AI-прогнозы на исход матча (DeepSeek)
- AI-обзоры прошедших матчей

Дополнительно реализован **REST API** на FastAPI для доступа к данным.

## ✨ Возможности

- 📅 **Матчи по датам** — выбери лигу (EPL, La Liga, Bundesliga) и дату
- 📊 **Детали матча** — составы, схема, рейтинг игроков
- 🧠 **AI-прогнозы** — DeepSeek анализирует статистику и даёт прогноз
- 📝 **AI-обзоры** — краткий разбор прошедших матчей
- 💾 **Кеширование** — SQLite, автообновление для завершённых матчей
- 🌐 **REST API** — FastAPI с эндпоинтами для матчей и составов
- 📝 **Логирование** — с ротацией файлов и фильтрами

## 🛠 Технологии

- **Python 3.11+**
- **pyTelegramBotAPI** — Telegram-бот
- **FastAPI** — REST API
- **SQLite** — кеш данных
- **DeepSeek API** — AI-прогнозы
- **RapidAPI** (Football API) — источник данных
- **Railway** — деплой
- **pytest** — тесты

## Структура проекта

my_telegram_bot/
├── api/                # FastAPI приложение
│   └── main.py
├── tests/              # Тесты (pytest)
│   ├── conftest.py
│   ├── test_api.py
│   └── test_database.py
├── screenshots/        # Скриншоты для README
├── bot.py              # Точка входа (прод, webhook)
├── bot_local.py        # Точка входа (локально, polling)
├── handlers.py         # Обработчики команд и callback
├── keyboards.py        # Клавиатуры
├── database.py         # Работа с SQLite
├── api_client.py       # Клиент Football API
├── ai_client.py        # Клиент DeepSeek
├── logger.py           # Настройка логирования
├── utils.py            # Утилиты
├── config.py           # Конфигурация (читает .env)
├── requirements.txt
├── pytest.ini
└── README.md

### 4. Переменные окружения

Создай файл `.env` в корне проекта:

```env
TOKEN=your_telegram_bot_token
API_KEY=your_rapidapi_key
DEEPSEEK_API_KEY=your_deepseek_key
```

**Где взять:**
- `TOKEN` — [@BotFather](https://t.me/BotFather) → `/newbot`
- `API_KEY` — [RapidAPI Football](https://rapidapi.com/)
- `DEEPSEEK_API_KEY` — [platform.deepseek.com](https://platform.deepseek.com/)

## API эндпоинты

| Метод | Путь | Описание |
| GET | `/health` | Проверка статуса |
| GET | `/matches_by_date?league_id=&date=` | Матчи по дате и лиге |
| GET | `/matches_by_id/{match_id}` | Детали матча по ID |
| GET | `/lineups/{match_id}` | Состав команд |

## Автор

**Казаков Михаил**
**pv88sbgs4j-max**
- GitHub: [@pv88sbgs4j-max](https://github.com/pv88sbgs4j-max)