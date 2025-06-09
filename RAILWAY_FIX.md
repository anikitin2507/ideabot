# �� Исправление ошибки API_KEY в Railway

## ❌ Проблема
```
ValidationError: 1 validation error for Config
api_key
  Field required [type=missing, input_value={'bot_token': '123456...'}]
```

## 🚨 Причина
В Railway не настроена переменная окружения `API_KEY`

## ✅ Решение (2 минуты)

### Шаг 1: Получите API ключ
1. Перейдите на [openrouter.ai](https://openrouter.ai)
2. Войдите или зарегистрируйтесь
3. Перейдите в раздел "API Keys"
4. Создайте новый ключ
5. **Скопируйте ключ**

### Шаг 2: Добавьте переменную в Railway
1. Откройте ваш проект в [Railway Dashboard](https://railway.app/dashboard)
2. Перейдите во вкладку **"Variables"**
3. Нажмите **"New Variable"**
4. Добавьте:
   ```
   Name: API_KEY
   Value: ВАШ_КЛЮЧ_ОТ_OPENROUTER
   ```
5. Нажмите **"Add"**

### Шаг 3: Перезапустите деплой
1. Перейдите во вкладку **"Deployments"**
2. Нажмите **"Redeploy"** или дождитесь автоматического перезапуска

## 📋 Полный список переменных для Railway

Убедитесь, что у вас настроены все эти переменные:

```
BOT_TOKEN=your_telegram_bot_token_here
API_KEY=your_openrouter_api_key_here
API_TYPE=openrouter
API_BASE=https://openrouter.ai/api/v1
MODEL=gpt-4.1-mini
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
- ✅ `API_KEY` - есть и не пустой

### Deployments Tab
- ✅ Последний деплой успешен (зеленый статус)
- ✅ В логах нет ошибок ValidationError

### Settings Tab
- ✅ GitHub репозиторий подключен: `anikitin2507/ideabot`
- ✅ Автодеплой включен

## 🆘 Если не помогло

1. **Проверьте формат токена:**
   - Telegram токен: `123456789:ABCDEF1234567890...`
   - OpenRouter ключ: должен быть действительным

2. **Пересоздайте переменные:**
   - Удалите старые переменные
   - Добавьте заново
   - Редеплойте

3. **Проверьте логи:**
   - Railway Dashboard → Deployments → View Logs
   - Найдите детальное сообщение об ошибке

---

🎯 **После исправления бот сразу заработает!** 