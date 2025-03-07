# Yandex Music Playlist Importer

Этот скрипт позволяет импортировать музыку в плейлист Яндекс.Музыки по названиям треков из текстового файла.

## Установка и запуск

1. Установите зависимости:
   ```sh
   pip install yandex-music
   ```
2. Запустите скрипт:
   ```sh
   python script.py
   ```

## Получение токена Яндекс.Музыки

   * Перейдите по ссылке: https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d
   * Разрешите доступ к сервису.
   * Скопируйте полученный токен из url.

## Использование

1. Введите токен Яндекс.Музыки при запуске скрипта.
2. Укажите путь к файлу с названиями треков (каждый трек на новой строке).
3. Выберите существующий плейлист или создайте новый.
4. Скрипт попытается найти и добавить все треки в плейлист.

## Логирование

Все действия записываются в файл `yandex_music.log`.

## Импорт плейлиста из ВКонтакте

Вы можете экспортировать плейлист из ВКонтакте в текстовый файл с помощью [этого инструмента](https://github.com/fivemru/export-vk-playlist-to-file).

