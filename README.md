# EXAONE Desktop 카탈로그 (테스트)

EXAONE Desktop의 **[Skill] → 찾아보기**, **[MCP 서버] → 찾아보기** 창이 읽어 가는 목록입니다.
앱은 아래 주소의 `catalog.json`을 불러옵니다.

```
https://raw.githubusercontent.com/kidarigun/exaone-catalog/main/catalog.json
```

## 고치는 방법

1. `catalog.src.json`에 항목을 추가하거나 고칩니다. Skill이면 `skills/<id>/SKILL.md`(필요하면 스크립트·참고 파일)도 만듭니다.
2. `python build.py`를 실행합니다. `dist/<id>.zip`과 `catalog.json`(sha256·크기 포함)이 새로 만들어집니다.
3. 커밋하고 푸시하면 몇 분 안에 앱에 반영됩니다.

`catalog.json`은 직접 고치지 말고 항상 `build.py`로 만드세요.

## 형식

### MCP 서버

| 필드 | 설명 |
|---|---|
| `id` | 고유 이름 (영문 소문자·숫자·`-`) |
| `name`, `summary`, `description` | 화면에 보이는 이름과 설명 |
| `category`, `publisher`, `homepage` | 분류, 만든 곳, 안내 페이지 |
| `requires` | 필요한 프로그램: `node`(npx), `uv`(uvx), `python`, `docker` |
| `install.transport` | `stdio`(내 PC에서 실행) 또는 `http`(원격 URL) |
| `install.command`, `install.args`, `install.env` | stdio 서버 실행 방법 |
| `install.url`, `install.headers` | http 서버 주소와 헤더 |
| `inputs` | 설치할 때 사용자에게 받을 값. `{key}`로 args·env·url·headers에 끼워 넣습니다 |
| `safeTools` | 처음부터 승인 없이 실행할 읽기 전용 도구 |

`inputs`의 `type`: `text`, `secret`(비밀번호 칸, 자격 증명 관리자에 저장), `folder`(폴더 선택 창).
선택 입력(`required: false`)을 비워 두면 그 값이 들어간 인자·환경 변수·헤더는 빠집니다.

npm 패키지는 `@2.3.0`처럼 **버전을 고정**하세요. 패키지가 바뀌어도 사용자 PC에서 실행되는 코드가 갑자기 달라지지 않습니다.

### Skill

| 필드 | 설명 |
|---|---|
| `id`, `name`, `summary`, `category`, `publisher` | 화면 표시용 |
| `path` | Skill 폴더 (`skills/<id>`) — `build.py`가 zip으로 묶고 `download`, `sha256`, `size`, `files`, `skillName`을 채웁니다 |
| `requires` | 필요한 프로그램 (예: 스크립트가 있으면 `python`) |

앱은 zip을 받은 뒤 sha256이 맞을 때만 설치합니다.
