# posts CRUD 과제 요구사항

출처: https://classroom.codemit.kr/classes/5/problems/48/submit

## 필수 기술과 기존 프로젝트

- Python, Flask, Jinja2, PostgreSQL, HTML, CSS, Git을 사용한다.
- 수업의 `mini-watch/general`에서 작업한다.
- 기존 `db.py`의 `connect_db()`, DB 접속 설정, SQL, 연습 파일, 로그인 코드, 감시 서비스를 유지한다.
- 게시글 데이터는 `posts(id, title, body)`이며 번호는 PostgreSQL 시퀀스로 자동 생성한다.
- `.env`와 `python-dotenv`로 DB 접속 정보를 읽고 `psycopg.connect()`로 연결한다.
- Python 가상환경과 `requirements.txt`로 실행 환경을 관리한다.

## 경로와 화면

| 요청 | 경로 | 템플릿 | 처리 |
| --- | --- | --- | --- |
| GET | `/` | `index.html` | 번호 오름차순 목록, 번호·제목, 상세 링크, 새 글 작성 링크 |
| GET | `/board/<int:post_id>` | `detail.html` | 번호·제목·본문, 목록·수정·삭제 링크 |
| GET, POST | `/board/new` | `new.html` | 빈 작성 폼, 저장 후 새 글 상세로 303 이동 |
| GET, POST | `/board/<int:post_id>/edit` | `edit.html` | 기존 값 표시, 수정 후 상세로 303 이동 |
| GET, POST | `/board/<int:post_id>/delete` | `delete.html` | GET은 확인만, POST로 삭제 후 목록으로 303 이동 |
| 오류 요청 | 별도 경로 없음 | `error.html` | 없는 게시글은 404 |

빈 목록에서는 `등록된 게시글이 없습니다.`를 표시한다.
삭제 확인 화면에는 글 제목, 확인 문구, `삭제 확인` 버튼과 `취소` 링크가 있어야 한다.
취소하면 해당 글 상세로 돌아간다.

## 입력과 DB 처리

- 작성·수정은 공통 함수로 제목·본문의 앞뒤 공백을 제거하고 빈 값 또는 공백뿐인 값을 거부한다.
- 오류 시 입력했던 값을 폼에 다시 표시하고 HTTP 400을 반환한다. DB는 변경하지 않는다.
- 작성은 `INSERT ... RETURNING id`로 생성된 번호를 받는다.
- 수정·삭제는 해당 번호만 변경하며 대상이 없으면 404를 반환한다.
- GET 요청이나 폼 편집만으로 DB를 변경하지 않는다.
- 저장 뒤 상세를 새로고침해도 중복 저장되지 않는다.
- 삭제한 글의 상세·수정·삭제 주소는 모두 404를 반환한다.
- SQL에는 `%s`와 매개변수를 사용한다.
- `conn.execute()`, `fetchall()`, `fetchone()`을 사용한다.
- 저장소 함수는 데이터 또는 `None`을 반환하고 HTTP 응답은 라우터에서 결정한다.

## 역할 분리

| 파일/폴더 | 역할 |
| --- | --- |
| `general/app.py` | 앱 생성·설정·Blueprint 및 요청 기록 등록·서버 실행 |
| `general/db.py` | 공통 DB 연결 함수 |
| `general/post_rules.py` | 작성·수정 공통 입력 검사 |
| `general/repositories/posts.py` | `find_post()` 및 목록·작성·수정·삭제 SQL |
| `general/routes/posts.py` | Blueprint, HTTP 요청 및 응답 |
| `general/request_logging.py` | 요청 기록 및 `requests`를 사용한 감시 서버 JSON 전송 |
| `general/templates/` | 각 화면의 Jinja2 HTML |
| `general/static/style.css` | 공통 CSS |
| `general/sql/` | DB 준비 SQL |
| `monitor/backend/` | 기존 감시 서비스 |

`routes`와 `repositories`에는 `__init__.py`를 둔다.
`general`에서 `python app.py`로 실행할 수 있어야 한다.

## 검증과 제출

- 목록 → 작성 → 상세 → 수정 → 상세 → 삭제 확인 → 취소 → 상세 → 삭제 확인 → 삭제 → 목록 흐름을 확인한다.
- 제목·본문 각각에 빈 값과 공백만 입력하여 400과 DB 보존을 확인한다.
- 존재하지 않는 번호의 상세·수정·삭제 GET/POST를 확인한다.
- SQL 매개변수 전달과 HTML 자동 이스케이프를 확인한다.
- 서버를 재실행해도 PostgreSQL 데이터가 유지되는지 확인한다.
- 감시 서비스가 실제 게시글 요청 기록 JSON을 수집하는지 확인한다.
- 모듈 분리 후 동일 기능이 동작하는지 확인한다.
- 구현을 Git에 커밋하고 작업 내용이 드러나는 메시지를 작성한다.
- 제출은 ZIP 또는 GitHub 저장소 형식을 고를 수 있다.

## 선택 기능

기존 로그인 파일은 유지한다. `/login`에서 `fetch()`로 `/auth/login`에
아이디·비밀번호 JSON을 POST하는 판정 화면 연결은 선택 실습이다.
세션 유지, 로그아웃, 게시글 접근 제한은 이번 과제 범위에 포함되지 않는다.
