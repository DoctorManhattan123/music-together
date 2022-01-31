from typing import Optional, Tuple, List

from source import db
from source.models import User, MusicRooms, MusicContent
from source.secrets import get_encrypted_user_secret_from_secret_params, create_encrypted_user_secret_and_params, \
    generate_random_guid


def db_get_user_secret_and_salt_if_exists(username: str) -> Optional[Tuple[str, str]]:
    user_key_row = User.query.filter_by(username=username).first()
    if user_key_row is not None:
        stored_password_hash = user_key_row.secret
        salt = user_key_row.salt
        return stored_password_hash, salt

    return None


def db_create_user_row(username: str, email: str, password: str):
    user_key_row = User.query.filter_by(username=username).first()
    if user_key_row is not None:
        return False
    password_hash, salt = create_encrypted_user_secret_and_params(password=password)

    user_key = User(
        username=username, email=email, salt=salt, secret=password_hash
    )
    db.session.add(user_key)
    db.session.commit()


def db_get_user_by_username(username: str) -> Optional[str]:
    user_key_row = User.query.filter_by(username=username).first()
    if user_key_row is not None:
        return user_key_row.username
    return None


def db_get_user_by_email(email: str) -> Optional[Tuple[str, str]]:
    user_key_row = User.query.filter_by(email=email).first()
    if user_key_row is not None:
        return user_key_row.username
    return None


def db_insert_music_room_for_user(username: str, music_room_name: str) -> Optional[str]:
    music_room_row = MusicRooms.query.filter_by(music_room_name=music_room_name, username=username).first()
    if music_room_row is not None:
        return None
    uuid = generate_random_guid()

    music_room_key = MusicRooms(
        username=username, uuid=uuid, music_room_name=music_room_name
    )
    db.session.add(music_room_key)
    db.session.commit()
    return uuid


def db_get_content_from_room(music_room_name: str) -> Optional[List[str]]:
    content_list = MusicContent.query.filter_by(music_room_name=music_room_name).all()
    if content_list is None or len(content_list) == 0:
        return None
    return [content.content_url for content in content_list]


def db_add_content_to_room(content: str, music_room_name: str, song_name: str, mp3_encoded: str):
    music_content_row = MusicContent.query.filter_by(
        music_room_name=music_room_name,
        content_url=content).first()
    if music_content_row is not None:
        return

    content_key = MusicContent(
        music_room_name=music_room_name,
        content_url=content,
        song_name=song_name,
        mp3_encoded=mp3_encoded
    )
    db.session.add(content_key)
    db.session.commit()


def db_music_room_present_for_user(username: str, music_room_name: str) -> bool:
    music_room_row = MusicRooms.query.filter_by(music_room_name=music_room_name, username=username).first()
    if music_room_row is None:
        return False
    return True


def db_get_music_rooms_from_user(username: str) -> Optional[List[Tuple[str, str]]]:
    music_room_rows = MusicRooms.query.filter_by(username=username).all()
    if len(music_room_rows) == 0:
        return None
    return [(music_room_row.uuid, music_room_row.music_room_name) for music_room_row in music_room_rows]
