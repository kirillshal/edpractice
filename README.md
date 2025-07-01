# Image Processing App

Приложение для обработки изображений с функциями:
- Просмотр цветовых каналов
- Обрезка изображения
- Вращение изображения
- Рисование кругов

## Требования
- Python 3.8+
- Установленные зависимости (см. ниже)

## Установка

1. Клонировать репозиторий:
```bash
git clone https://github.com/kirillshal/edpractice.git
cd edpractice
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Запустить приложение:
```bash
python app.py
```

## Использование
1. Загрузите изображение (кнопка "Upload Image" или "Capture from Webcam")
2. Используйте инструменты:
   - "Show Channel" - просмотр цветовых каналов
   - "Set Crop Area" - обрезка по координатам
   - "Rotate" - вращение на заданный угол
   - "Add Circle" - рисование красного круга
3. "Reset Image" - сброс к исходному изображению

## Разработка
Для установки dev-зависимостей:
```bash
pip install -r requirements-dev.txt
```# edpractice