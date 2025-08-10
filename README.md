###  Бот для записи

Небольшой Telegram‑бот на aiogram 3 для записи пользователей в базу и синхронизации данных с Google Sheets.

### Возможности
- **Регистрация**: бот собирает ФИО и номер телефона; ник Telegram подтягивается автоматически
- **Хранение**: данные сохраняются в SQLite (`database/registrs.db`)
- **Синхронизация**: фоновая задача добавляет новые записи в Google Sheets, не перезаписывая уже существующие
- **Валидация телефона**: проверка, что введённые символы — только цифры

### Требования
- Python 3.11+

### Установка
1) Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2) Подготовить окружение:
   - Создать файл `.env` и указать токен бота:
     ```env
     BOT_T=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     ```
   - Секреты Google (service account):
     - Рекомендуемый способ — переменные окружения (`GOOGLE_...`, см. ниже) или локальный файл `.secrets/cred.json` (не попадает в git).
     - Поддерживается также fallback-файл `sheets/cred.json` для локальной разработки, но он игнорируется git.

   Важно: ключи не должны попадать в репозиторий. Файлы в `.secrets/` и `sheets/cred.json` игнорируются `.gitignore`.

### Запуск
```bash
python main.py
```

При запуске инициализируется база и стартует фоновая синхронизация c Google Sheets (раз в ~5 минут). Новые записи из БД дозаписываются в таблицу, а не затирают её.

### Как начать регистрацию
- Откройте бота по дип‑ссылке вида: `https://t.me/<ваш_бот>?start=reg`
- Нажмите кнопку «Записаться» и следуйте инструкциям

### Конфигурация синхронизации
- Идентификатор таблицы и листа задаются через переменные окружения или дефолты в `sheets/sync.py`:
  - `GSHEET_ID` — id таблицы
  - `GSHEET_DATA_SHEET` — лист с данными (по умолчанию `Sheet1`)
  - `GSHEET_META_SHEET` — лист для метаданных (по умолчанию `meta`)
- Заголовки столбцов: `name`, `phone`, `usrname`

### Конфигурация Google Service Account (любой из способов)
1) Через переменные окружения:
   ```env
   GOOGLE_TYPE=service_account
   GOOGLE_PROJECT_ID=...
   GOOGLE_PRIVATE_KEY_ID=...
   GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   GOOGLE_CLIENT_EMAIL=...
   GOOGLE_CLIENT_ID=...
   GOOGLE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
   GOOGLE_TOKEN_URI=https://oauth2.googleapis.com/token
   GOOGLE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
   GOOGLE_CLIENT_X509_CERT_URL=...
   GOOGLE_UNIVERSE_DOMAIN=googleapis.com
   ```
2) Через файл `.secrets/cred.json` (безопасный локальный путь, игнорируется git).
3) В качестве fallback — `sheets/cred.json` (не рекомендуется для продакшн).

### Полезно знать
- Виртуальное окружение `.venv/` исключено в `.gitignore`
- Для логирования используйте уровни логера вместо `print`


