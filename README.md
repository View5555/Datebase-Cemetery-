# Datebase-Cemetery-

# 🪦 Cemetery Database App

Веб-приложение на Flask для хранения информации об умерших. Поддерживает регистрацию пользователей, добавление и поиск записей, экспорт и резервное копирование.

## 🌐 Демо

Проект развернут на Render:  
🔗 [https://datebase-cemetery-cemetery-app.onrender.com](https://datebase-cemetery-cemetery-app.onrender.com)

---

## 📦 Функциональность

- 👤 Регистрация и вход пользователей
- 👨‍💼 Роли: `user` и `admin`
- ➕ Admin может добавлять, редактировать и удалять записи
- 🔍 Поиск по фамилии
- 📄 Экспорт базы в Excel
- 🔐 База данных на SQLite (users.db)
- 🌍 Деплой на Render.com

---
## 📃 Лицензия


---

## ✅ Как использовать

1. Создай новый файл: `README.md`
2. Вставь туда содержимое выше
3. Подстрой ссылки под себя
4. Закоммить:

## 🗂 Структура проекта

.
├── app.py                 # Главный файл Flask-приложения
├── requirements.txt       # Зависимости проекта
├── users.db               # SQLite база данных
├── templates/             # HTML-шаблоны
├── static/                # Стили
└── Procfile / render.yaml # Настройка для Render

## 🧪 Логин по умолчанию

```bash
Логин: admin
Пароль: admin123

