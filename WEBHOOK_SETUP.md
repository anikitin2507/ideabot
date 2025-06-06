# ⚡ Быстрое переключение на Webhook

## 🚨 СЕЙЧАС: Конфликт polling продолжается
```
TelegramConflictError: terminated by other getUpdates request
```

## ✅ РЕШЕНИЕ: Webhook за 2 минуты

### Шаг 1: Railway Dashboard
1. https://railway.app/dashboard
2. Выберите ваш проект

### Шаг 2: Найдите домен
**Settings → Domains** → скопируйте URL
Формат: `https://ideabot-production-XXXX.up.railway.app`

### Шаг 3: Добавьте переменные
**Variables → Add Variable:**

```
USE_WEBHOOK=true
WEBHOOK_URL=https://ideabot-production-XXXX.up.railway.app
```

*Замените XXXX на ваш реальный домен!*

### Шаг 4: Сохранить
Railway автоматически переделоит с webhook!

## 🎯 Результат

**До (polling):**
```
❌ Failed to fetch updates - TelegramConflictError
❌ Sleep for X seconds and try again
❌ Бесконечные конфликты
```

**После (webhook):**
```
✅ Starting Decision Bot mode=webhook
✅ Webhook set url=https://your-domain/webhook  
✅ Webhook server started on port 8000
✅ Никаких конфликтов - НАВСЕГДА!
```

## 🔍 Проверка работы

1. **Логи:** Railway → Deployments → Logs (зеленый статус)
2. **Health:** `https://your-domain.railway.app/health`
3. **Telegram:** Найдите бота → `/start` → `Пицца или суши?`

---

⚡ **Webhook = Конец всех конфликтов polling!** 🎉 