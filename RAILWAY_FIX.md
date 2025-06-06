# 🔧 Исправление ошибки BOT_TOKEN в Railway

## ❌ Проблема
```
ValidationError: 1 validation error for Config
bot_token
  Field required [type=missing, input_value={'openai_api_key': 'sk-pr...'}]
```

## 🚨 Причина
В Railway не настроена переменная окружения `BOT_TOKEN`

## ✅ Решение (2 минуты)

### Шаг 1: Получите Telegram Bot Token
1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям для создания бота
4. **Скопируйте токен** - выглядит как `123456789:ABCDEF...`

### Шаг 2: Добавьте переменную в Railway
1. Откройте ваш проект в [Railway Dashboard](https://railway.app/dashboard)
2. Перейдите во вкладку **"Variables"**
3. Нажмите **"New Variable"**
4. Добавьте:
   ```
   Name: BOT_TOKEN
   Value: ВАШ_ТОКЕН_ОТ_BOTFATHER
   ```
5. Нажмите **"Add"**

### Шаг 3: Перезапустите деплой
1. Перейдите во вкладку **"Deployments"**
2. Нажмите **"Redeploy"** или дождитесь автоматического перезапуска

## 📋 Полный список переменных для Railway

Убедитесь, что у вас настроены все эти переменные:

```
BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
MAX_OPTIONS=5
RESPONSE_TIMEOUT=30
LOG_LEVEL=INFO
```

## ✅ Проверка работы

После исправления:
1. Проверьте логи в Railway - не должно быть ошибок
2. Health check: `https://your-domain.railway.app/health`
3. Протестируйте бота в Telegram: `/start` и "Пицца или суши?"

## 🔍 Дополнительная диагностика

Если проблема повторяется, проверьте в Railway Dashboard:

### Variables Tab
- ✅ `BOT_TOKEN` - есть и не пустой
- ✅ `OPENAI_API_KEY` - есть и начинается с `sk-`

### Deployments Tab
- ✅ Последний деплой успешен (зеленый статус)
- ✅ В логах нет ошибок ValidationError

### Settings Tab
- ✅ GitHub репозиторий подключен: `anikitin2507/ideabot`
- ✅ Автодеплой включен

## 🆘 Если не помогло

1. **Проверьте формат токена:**
   - Telegram токен: `123456789:ABCDEF1234567890...`
   - OpenAI ключ: `sk-proj-...` или `sk-...`

2. **Пересоздайте переменные:**
   - Удалите старые переменные
   - Добавьте заново
   - Редеплойте

3. **Проверьте логи:**
   - Railway Dashboard → Deployments → View Logs
   - Найдите детальное сообщение об ошибке

---

🎯 **После исправления бот сразу заработает!** 