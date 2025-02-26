import logging
from yandex_music import Client


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler("yandex_music.log"), logging.StreamHandler()]
    )


def get_token():
    return input("Введите ваш токен Яндекс.Музыки: ").strip()


def get_file_path():
    return input("Введите путь к файлу с названиями треков: ").strip()


def get_playlist_choice(client):
    playlists = client.users_playlists_list()
    if playlists:
        logging.info("Список доступных плейлистов:")
        for i, playlist in enumerate(playlists):
            logging.info(f"{i + 1}. {playlist.title} ({playlist.track_count} треков)")

        choice = input("Введите номер плейлиста или 0 для создания нового: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(playlists):
                return playlists[choice - 1].kind, playlists[choice - 1].title

    new_name = input("Введите название нового плейлиста: ")
    new_playlist = client.users_playlists_create(new_name)
    return new_playlist.kind, new_name


def search_track(client, track_name):
    search_result = client.search(track_name, type_='track')
    tracks = search_result.tracks.results if search_result.tracks else []
    return tracks[0] if tracks else None


def add_track_to_playlist(client, playlist_id, track):
    playlist = client.users_playlists(kind=playlist_id)
    revision = playlist.revision
    client.users_playlists_insert_track(
        kind=playlist_id, track_id=track.id, album_id=track.albums[0].id, revision=revision
    )


def main():
    setup_logger()

    token = get_token()
    client = Client(token).init()

    file_path = get_file_path()
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            track_names = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error("Файл не найден.")
        return

    playlist_id, playlist_name = get_playlist_choice(client)
    logging.info(f"Используем плейлист: {playlist_name}")

    for track_name in track_names:
        logging.info(f"Ищем трек: {track_name}")
        track = search_track(client, track_name)

        if track:
            add_track_to_playlist(client, playlist_id, track)
            logging.info(f"Добавлен: {track.title} - {track.artists[0].name}")
        else:
            logging.warning(f"Трек не найден: {track_name}")

    logging.info("Завершено!")


if __name__ == "__main__":
    main()
