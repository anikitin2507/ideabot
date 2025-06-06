# Инструкция по деплою Decision Bot

## 📋 Предварительные требования

1. **GitHub аккаунт** - для хостинга кода
2. **Railway аккаунт** - для деплоя (railway.app)
3. **Telegram Bot Token** - создать через @BotFather
4. **OpenAI API Key** - получить на platform.openai.com

## 🔧 Шаг 1: Публикация на GitHub

### 1.1 Создание репозитория на GitHub
1. Перейдите на [github.com](https://github.com)
2. Нажмите **"New repository"**
3. Введите название: `decision-bot`
4. Описание: `🤖 Telegram bot for decision making with GPT-4.1-mini`
5. Оставьте репозиторий **Public**
6. **НЕ** инициализируйте с README (у нас уже есть файлы)
7. Нажмите **"Create repository"**

### 1.2 Подключение локального репозитория
Выполните команды в терминале:

```bash
# Добавьте удаленный репозиторий (замените USERNAME на ваш GitHub username)
git remote add origin https://github.com/USERNAME/decision-bot.git

# Переименуйте ветку в main
git branch -M main

# Загрузите код
git push -u origin main
```

## 🚀 Шаг 2: Деплой на Railway

### 2.1 Создание проекта Railway
1. Перейдите на [railway.app](https://railway.app)
2. Нажмите **"Start a New Project"**
3. Выберите **"Deploy from GitHub repo"**
4. Найдите и выберите репозиторий `decision-bot`
5. Railway автоматически определит Dockerfile и начнет деплой

### 2.2 Настройка переменных окружения
В панели Railway перейдите в **Variables** и добавьте:

```
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_MODEL=gpt-4.1-mini
MAX_OPTIONS=5
RESPONSE_TIMEOUT=30
LOG_LEVEL=INFO
```

### 2.3 Получение Telegram Bot Token
1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в переменную `BOT_TOKEN`

### 2.4 Получение OpenAI API Key
1. Перейдите на [platform.openai.com](https://platform.openai.com/api-keys)
2. Войдите в аккаунт или зарегистрируйтесь
3. Нажмите **"Create new secret key"**
4. Скопируйте ключ в переменную `OPENAI_API_KEY`

## ✅ Шаг 3: Проверка деплоя

### 3.1 Проверка работы бота
1. После деплоя найдите ваш бот в Telegram
2. Отправьте `/start`
3. Попробуйте запрос: "Пицца или суши?"

### 3.2 Проверка health check
Перейдите по ссылке: `https://YOUR-RAILWAY-DOMAIN/health`
Должен вернуться JSON: `{"status": "healthy", "service": "decision-bot"}`

### 3.3 Мониторинг логов
В Railway панели откройте вкладку **"Deployments"** → **"Logs"** для просмотра логов

## 🔄 Автоматический деплой

После настройки каждый `git push` в ветку `main` будет автоматически деплоиться на Railway.

## 🛠️ Локальная разработка

Для локального тестирования:

```bash
# Создайте файл .env
cp .env.example .env

# Заполните переменные в .env
# BOT_TOKEN=your_bot_token
# OPENAI_API_KEY=your_openai_key

# Установите зависимости
pip install -e ".[dev]"

# Запустите бота
python main.py
```

## 📊 Мониторинг и логи

- **Railway Dashboard**: Просмотр метрик и логов
- **Health Check**: `/health` endpoint для мониторинга
- **Structured Logs**: JSON формат для анализа

## 🔧 Обновления

Для обновления бота:
1. Внесите изменения в код
2. Зафиксируйте изменения: `git commit -am "Update: description"`
3. Отправьте на GitHub: `git push`
4. Railway автоматически деплоит обновления

## 🆘 Troubleshooting

### Проблема: Бот не отвечает
- Проверьте логи в Railway
- Убедитесь, что `BOT_TOKEN` правильный
- Проверьте статус деплоя

### Проблема: OpenAI ошибки
- Проверьте `OPENAI_API_KEY`
- Убедитесь, что у аккаунта OpenAI есть кредиты
- Проверьте лимиты API

### Проблема: Деплой не работает
- Проверьте, что все переменные окружения установлены
- Убедитесь, что Docker файл корректный
- Проверьте логи сборки в Railway

---

🎉 **Поздравляем! Ваш Decision Bot готов к работе!** 