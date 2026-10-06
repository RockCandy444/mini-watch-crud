from getpass import getpass

from werkzeug.security import generate_password_hash

from db import connect_db


if __name__ == "__main__":
    username = input("만들 사용자 이름 [student]: ").strip() or "student"
    password = getpass("비밀번호: ")
    if not password.strip():
        raise SystemExit("비밀번호를 입력해 주세요.")
    with connect_db() as conn:
        result = conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING",
            (username, generate_password_hash(password)),
        )
        if result.rowcount == 1:
            print(f"{username} 계정을 만들었습니다.")
        else:
            print(f"{username} 계정이 이미 있습니다. 기존 계정을 유지합니다.")
