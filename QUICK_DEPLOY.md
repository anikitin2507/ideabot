# 🚀 Быстрый деплой в Railway

## ✅ Готово к деплою!
Код размещен: **https://github.com/anikitin2507/ideabot**

## 🔥 Пошаговый деплой (5 минут)

### 1. Создайте Telegram бота
1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте `/newbot` и следуйте инструкциям
3. **Сохраните токен** - понадобится для Railway

### 2. Получите OpenAI API Key
1. Перейдите на [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Войдите или зарегистрируйтесь
3. Создайте новый API ключ
4. **Сохраните ключ** - понадобится для Railway

### 3. Деплой на Railway
1. Перейдите на [railway.app](https://railway.app)
2. Войдите через GitHub
3. **"Start a New Project"** → **"Deploy from GitHub repo"**
4. Выберите репозиторий: **`anikitin2507/ideabot`**
5. Railway автоматически начнет деплой

### 4. Настройте переменные окружения
В Railway панели → **Variables** → добавьте:

**Обязательные:**
```
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

**Дополнительные (рекомендуемые):**
```
OPENAI_MODEL=gpt-4.1-mini
MAX_OPTIONS=5
RESPONSE_TIMEOUT=30
LOG_LEVEL=INFO
```

**Для избежания конфликтов (optional):**
```
USE_WEBHOOK=true
WEBHOOK_URL=https://YOUR-RAILWAY-DOMAIN.railway.app
```
*Замените YOUR-RAILWAY-DOMAIN на ваш реальный домен*

### 5. ✅ Готово!
- Бот автоматически запустится
- Health check: `https://your-domain.railway.app/health`
- Попробуйте в Telegram: `/start` и "Пицца или суши?"

---

## 🛠️ Что уже настроено

✅ **Docker конфигурация** - автоматическая сборка  
✅ **Health check endpoint** - мониторинг Railway  
✅ **Структурированные логи** - для отладки  
✅ **Обработка ошибок** - fallback при сбоях OpenAI  
✅ **CI/CD pipeline** - автоматическое тестирование  
✅ **Автодеплой** - каждый git push обновляет бота  

## 🔄 Обновления
Для обновления бота просто отправьте изменения в GitHub:
```bash
git add .
git commit -m "Update bot"
git push
```
Railway автоматически переделойит! 🎉 