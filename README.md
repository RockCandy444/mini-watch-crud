# 모아 게시판 · mini-watch CRUD

Flask, Jinja2, PostgreSQL로 만든 게시판입니다. 글 작성·목록·상세 조회·수정·삭제와
입력 오류 안내를 제공하며, 일반 서비스의 요청 기록을 별도 감시 서비스에 전달합니다.

## 시작하기

Python과 PostgreSQL이 필요합니다. PostgreSQL에서 사용할 DB를 먼저 준비하세요.
수업 환경의 기존 `general_db`를 그대로 사용할 수 있습니다.

아래는 프로젝트 루트에서 실행하는 PowerShell 명령입니다.

```powershell
cd general
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env`의 `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`를
본인의 PostgreSQL 접속 정보로 수정하세요. 기존 `.env`가 있다면 복사하지 않고 유지합니다.

```powershell
.\venv\Scripts\python.exe prepare_db.py
.\venv\Scripts\python.exe app.py
```

별도 터미널에서 감시 서버를 실행합니다.

```powershell
cd monitor\backend
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```

- 게시판: http://127.0.0.1:5100/
- 로그인 판정: http://127.0.0.1:5100/login
- 감시 기록: http://127.0.0.1:5200/api/events

기존 `posts(id, title, body)` 데이터와 DB 설정을 유지합니다.
`prepare_db.py`는 테이블이 없으면 생성하고, 자동 번호 설정이 없는 테이블에는
기존 최대 번호 다음부터 시작하는 시퀀스를 연결합니다.

선택 로그인 기능은 기존 수업 `users` 테이블을 사용합니다. 새 DB에서 필요한 경우
`general/sql/prepare_users.sql`을 실행한 뒤 `general/create_user.py`로 테스트 사용자를 만드세요.
비밀번호는 실행 시 입력받아 해시로 저장합니다.

## 구조

```text
general/
  app.py                 앱 생성·등록·실행
  db.py                  PostgreSQL 연결
  post_rules.py          공통 입력 검사
  repositories/          게시글·사용자 SQL
  routes/                Blueprint 및 HTTP 처리
  request_logging.py     감시 서비스 JSON 전송
  templates/             Jinja2 화면
  static/                CSS·JavaScript
  sql/                   DB 준비 SQL
  tests/                 PostgreSQL 및 감시 서비스 통합 검증
monitor/backend/         요청 기록 수집 서비스
```

잘못된 작성·수정은 `400`, 없는 글은 `404`, 저장·수정·삭제 후 이동은 `303`입니다.
삭제 확인 GET은 조회만 하고, 실제 삭제는 POST에서 처리합니다.
기존 `/posts/<번호>` JSON 조회와 `/auth/login` 로그인 판정도 유지합니다.

## 테스트

`general`에서 실행합니다. `.env`로 접속한 PostgreSQL에 테스트용 스키마를
만들었다가 제거하며 기존 게시글·사용자는 변경하지 않습니다.

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 과제 제출

과제 페이지에서 **GitHub 저장소**를 선택하고 이 저장소의 주소를 입력합니다.
DB 비밀번호가 들어 있는 `.env`, 가상환경, 캐시는 Git에서 제외합니다.
자세한 기능과 요구사항은 `CRUD_GUIDE.md`, `TASK_REQUIREMENTS.md`를 참고하세요.

수업 시작 프로젝트: https://github.com/zeroskill2400/mini-watch
