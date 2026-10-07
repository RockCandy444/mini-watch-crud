# mini watch · React 감시 대시보드

Flask·React·PostgreSQL로 만든 게시판과 운영 감시 대시보드입니다.
기존 일반 서비스의 게시판을 유지하면서 실제 요청 기록 조회, 운영자 로그인,
관찰 메모 CRUD와 선택 심화 기능 4개를 추가했습니다.

## 시작 자료와 직접 작업한 부분

- 수업 시작 저장소: https://github.com/zeroskill2400/mini-watch
- 기존 CRUD 작업: 이 저장소의 `d26e161` 커밋. `general` 게시판·로그인 판정·요청 전송과 수업 SQL을 이어 사용했습니다.
- 이번 과제: https://classroom.codemit.kr/classes/5/problems/49/submit
- 직접 추가: React·Vite 화면 및 props/state 연결, API 요청 모듈, PostgreSQL 감시 저장소,
  운영자 비밀번호 해시 판정·세션, 메모 CRUD·상태, 검색·집계, SQL·계정 준비 도구, 통합 테스트.
- 직접 수정: 감시 서비스의 메모리 기록을 영구 DB 저장으로 변경하고 Flask 라우터·SQL을 분리했습니다.
  기존 게시판 테스트도 변경된 DB 감시 서비스와 연결해 검증했습니다.

## 필수 기능과 선택 기능

- React 로그인 state → JSON API → DB 계정·해시 검증 → 사용자 이름이 표시되는 대시보드.
- 실제 일반 서비스 요청의 메서드·경로·상태 코드 표시, 기록 및 메모 새로고침.
- 메모 목록·상세·작성·수정·삭제 확인·취소, 성공 후 목록 다시 조회.
- 제목·내용 공백 검사와 400, 없는 번호 및 삭제된 번호의 404, 오류 안내·입력값 보존.
- 빈 목록과 연결 오류 안내, 화면과 API 함수 및 Flask 라우터와 저장소 분리.
- **선택 1:** 경로 검색·응답 코드 필터 및 조건 해제.
- **선택 2:** 현재 조회 목록 전체의 전체 요청·오류 요청 집계. 오류 기준은 HTTP 400 이상입니다.
- **선택 3:** 메모의 `확인 전`·`확인 중`·`완료` 상태 DB 저장.
- **선택 4:** 쿠키 세션으로 새로고침 후 로그인 유지, 메모 API 및 요청 기록 GET 서버 접근 보호.

## 실행 환경

Python 3.11 이상, PostgreSQL 16 이상, Node.js 22.12 이상과 npm, Git이 필요합니다.
아래 명령은 모두 **Windows CMD** 기준입니다. PowerShell에서도 `cmd`를 열면 그대로 실행할 수 있습니다.
PostgreSQL `bin` 폴더가 PATH에 없다면 `psql` 대신 `"C:\Program Files\PostgreSQL\16\bin\psql.exe"`를 사용하세요.

```cmd
git clone https://github.com/RockCandy444/mini-watch-crud.git mini-watch-day04
cd mini-watch-day04
```

기존 프로젝트 폴더를 받은 경우 그 폴더에서 시작합니다. 이하 명령의 루트는 이 폴더입니다.

### 1. DB 생성

PostgreSQL 서버를 실행하고 처음 사용하는 DB만 생성합니다. 기존 `general_db`, `monitor_db`가 있으면 이 단계는 건너뜁니다.

```cmd
psql -h 127.0.0.1 -U postgres -d postgres -f setup\create_databases.sql
```

`setup/create_databases.sql`은 두 DB를 만듭니다. 기존 DB 하나만 있으면 SQL에서 없는 DB의 `CREATE DATABASE` 줄만 실행하세요.
수업의 `monitor/backend/sql/create_database.sql`은 이름과 달리 기존 요청 기록 테이블 SQL입니다.
이번 결과물에서는 반복 실행 가능한 `prepare_monitor.sql`을 아래 준비 스크립트로 실행합니다.

### 2. 일반 게시판 설치·DB 준비

```cmd
cd general
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
notepad .env
```

`.env`에서 본인 PostgreSQL 비밀번호와 DB 정보를 입력하고 저장합니다.
**이미 `.env`가 있으면 복사 명령을 생략하여 기존 설정을 유지합니다.**

```cmd
venv\Scripts\python.exe prepare_db.py
psql -h 127.0.0.1 -U postgres -d general_db -f sql\prepare_users.sql
cd ..
```

`prepare_db.py`는 기존 게시글을 보존하며 `posts` 테이블과 자동 번호를 준비합니다.
기존 일반 게시판 로그인 판정도 시험하려면 `general`에서 `venv\Scripts\python.exe create_user.py`로 별도 계정을 만듭니다.
**감시 화면 운영자 계정은 다음 단계에서 따로 만듭니다.**

### 3. 감시 API 설치·DB·운영자 계정 준비

```cmd
cd monitor\backend
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
notepad .env
```

감시 `.env`는 DB 이름 `monitor_db`, 본인 DB 비밀번호로 설정합니다.
`SECRET_KEY`는 아래 명령으로 만든 값을 복사해 넣고 계속 같은 값으로 유지하세요.
실제 비밀번호나 생성한 키를 Git에 넣지 않습니다.

```cmd
venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
venv\Scripts\python.exe prepare_db.py
venv\Scripts\python.exe create_user.py
cd ..\..
```

`create_user.py`에서 테스트할 운영자 아이디(예: `operator`)와 본인이 사용할 비밀번호를 두 번 입력합니다.
비밀번호는 입력 화면에 표시하지 않고 해시만 DB에 저장합니다. 기존 아이디를 입력하면 기존 계정을 유지합니다.
준비 SQL은 `monitor_users`, `http_events`, `notes`를 만들며 기존 자료를 보존합니다.

### 4. 프론트엔드 설치

```cmd
cd monitor\frontend
npm ci
cd ..\..
```

`package-lock.json`을 포함했습니다. Vite의 `/api` 프록시는 `http://127.0.0.1:5200`으로 연결되며 Host를 유지하여
같은 출처의 세션 요청을 처리합니다. 프론트엔드는 DB 비밀번호나 별도의 `.env` 설정이 필요하지 않습니다.

### 5. 세 서비스를 별도 CMD 창에서 실행

각 창은 프로젝트 루트에서 시작합니다. 감시 API를 먼저 실행하면 게시판의 첫 요청부터 수집됩니다.

**창 1 · 감시 API**

```cmd
cd monitor\backend
venv\Scripts\python.exe app.py
```

**창 2 · 일반 게시판**

```cmd
cd general
venv\Scripts\python.exe app.py
```

**창 3 · React 대시보드**

```cmd
cd monitor\frontend
npm run dev
```

- 일반 게시판: http://127.0.0.1:5100/
- 감시 API 상태: http://127.0.0.1:5200/health
- React 감시 화면: **http://127.0.0.1:5173/**

주소의 `127.0.0.1`을 통일해 사용하고 방금 만든 감시 운영자 계정으로 로그인합니다.
일반 게시판의 정상 글과 `/board/999999`에 접속한 뒤 감시 화면의 `기록 새로고침`을 눌러 결과를 비교합니다.
세 서비스는 각 터미널에서 Ctrl+C로 종료합니다. DB 자료는 서버를 종료해도 남습니다.

## 환경 변수

두 서비스 각각 `.env.example`을 제공합니다.

| 값 | 용도 |
| --- | --- |
| DB_HOST | PostgreSQL 주소, 로컬은 127.0.0.1 |
| DB_PORT | PostgreSQL 포트, 기본 5432 |
| DB_NAME | 일반은 general_db, 감시는 monitor_db |
| DB_USER | PostgreSQL 접속 계정 |
| DB_PASSWORD | 해당 DB 계정의 실제 비밀번호, Git 제외 |
| SECRET_KEY | 감시 세션 서명용 임의 키, Git 제외. 새로고침·서버 재실행 시 같은 값 사용 |
| MONITOR_URL | 일반 서비스의 요청 전송 주소. 기본 http://127.0.0.1:5200/api/events |

감시 서비스의 개별 설정을 실행 환경에서 덮어쓸 때는 `MONITOR_DB_HOST`처럼 `MONITOR_` 접두사를 사용합니다.
키를 설정하지 않으면 실행 때 임의 키를 생성하므로 서버 재실행 후에는 다시 로그인해야 합니다.
`POST /api/events`는 일반 서비스가 자동 기록을 보낼 수 있도록 로그인 없이 수집합니다.
`GET /api/events`와 메모 API 전체는 비로그인 요청을 401로 차단합니다.

## 구조

```text
general/                         기존 Flask·Jinja2 게시판, 요청 전송 유지
monitor/
  backend/
    app.py                       앱 설정·Blueprint 연결·실행
    db.py                        psycopg DB 연결
    routes/                      인증·기록·메모 HTTP 처리
    repositories/                사용자·기록·메모 SQL
    sql/prepare_monitor.sql      테이블 준비
    prepare_db.py, create_user.py DB 준비 및 해시 계정 생성
    tests/                       실제 PostgreSQL 통합 검증
  frontend/
    src/App.jsx                  로그인 전후 화면 연결
    src/components/              state·props 화면 구성
    src/api/                     fetch 요청 모듈
    src/style.css                반응형 공통 스타일
    vite.config.js               /api 프록시
setup/create_databases.sql        새 환경 DB 생성
```

목록 항목에는 DB 번호를 React key로 사용합니다. 저장·수정 요청이 실패하면 폼을 유지하고 완료 안내를 표시하지 않습니다.
수정 취소와 삭제 확인을 여는 동작은 DB를 변경하지 않으며 삭제 확인에서 확정한 경우에만 DELETE 요청을 보냅니다.

## 테스트와 통합 확인 결과

프로젝트 루트에서 감시 API 테스트를 실행합니다.

```cmd
monitor\backend\venv\Scripts\python.exe -m unittest discover -s monitor\backend\tests -v
cd general
venv\Scripts\python.exe -m unittest discover -s tests -v
cd ..
cd monitor\frontend
npm run build
cd ..\..
```

2026-10-07 실제 PostgreSQL에서 **감시 테스트 6개, 기존 게시판 테스트 10개 모두 통과**, React 빌드 성공.
테스트는 임시 스키마를 만들었다 제거하며 운영 데이터를 수정하지 않습니다. 테스트 DB 계정에 스키마 생성 권한이 필요합니다.

브라우저에서도 실패·성공 로그인, 게시판 실제 200·404 기록 수집, 검색·필터·집계,
메모 작성·상세·수정 취소·공백 오류·수정 저장·상태 저장, 삭제 취소·삭제 확정,
새로고침 후 세션과 DB 자료 유지, 로그아웃을 확인했습니다.
자세한 API와 검증 결과는 `DASHBOARD_GUIDE.md`, 이전 게시판 설명은 `CRUD_GUIDE.md`를 참고하세요.

## Git 제출

필수 기능 20개와 선택 기능 4개를 구현했습니다. 강의실에서 **GitHub 저장소**를 선택하고
`https://github.com/RockCandy444/mini-watch-crud`를 입력합니다.
실제 `.env`, 비밀번호·토큰, 가상환경, `node_modules`, 빌드·캐시는 `.gitignore`로 제외했습니다.
