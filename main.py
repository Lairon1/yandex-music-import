import yandex_music
import time
import os


def read_tracks(filename):
    """Считывает список треков из файла"""
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def find_track(client, track_name):
    """Ищет трек в Яндекс Музыке"""
    search_result = client.search(track_name, type_="track")
    if search_result.tracks:
        return search_result.tracks.results[0]  # Берем первый найденный трек
    return None


def get_or_create_playlist(client, playlist_name):
    """Получает или создает плейлист"""
    user = client.me
    playlists = client.users_playlists_list(user.account.uid)

    for playlist in playlists:
        if playlist.title == playlist_name:
            return playlist  # Если плейлист найден, возвращаем его

    # Если нет, создаем новый
    return client.users_playlists_create(playlist_name)


def add_tracks_to_playlist(client, playlist, tracks):
    """Добавляет найденные треки в плейлист"""
    track_ids = []
    not_found_tracks = []

    for track in tracks:
        found_track = find_track(client, track)
        if found_track:
            track_ids.append(f"{found_track.id}:{found_track.albums[0].id}")
            print(f"✅ Найдено: {track}")
        else:
            print(f"❌ Не найдено: {track}")
            not_found_tracks.append(track)

        time.sleep(1)  # Задержка, чтобы не получить блокировку

    if track_ids:
        client.users_playlists_insert_tracks(
            kind=playlist.kind, track_ids=track_ids
        )
        print(f"🎵 Треки добавлены в плейлист: {playlist.title}")

    if not_found_tracks:
        print("\n⚠️ Не удалось найти следующие треки:")
        for track in not_found_tracks:
            print(f"- {track}")


def main():
    print("🎵 Импорт Яндекс Музыки: Инициализация...")

    # Ввод данных от пользователя
    token = input("Введите ваш токен Яндекс Музыки: ").strip()
    file_path = input("Введите путь к файлу со списком музыки: ").strip()

    # Проверка существования файла
    if not os.path.exists(file_path):
        print(f"❌ Ошибка: Файл {file_path} не найден!")
        return

    client = yandex_music.Client(token).init()
    tracks = read_tracks(file_path)

    # Получаем список плейлистов пользователя
    user = client.me
    playlists = client.users_playlists_list(user.account.uid)

    print("\nВаши плейлисты:")
    for i, playlist in enumerate(playlists, 1):
        print(f"{i}. {playlist.title}")

    print(f"{len(playlists) + 1}. ➕ Новый плейлист")

    # Выбор плейлиста
    choice = int(input("\nВыберите номер плейлиста: "))
    if choice == len(playlists) + 1:
        playlist_name = input("Введите название нового плейлиста: ")
        playlist = get_or_create_playlist(client, playlist_name)
    else:
        playlist = playlists[choice - 1]

    add_tracks_to_playlist(client, playlist, tracks)


if __name__ == "__main__":
    print("✅ Все модули успешно импортированы!")
    main()
