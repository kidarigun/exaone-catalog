# Desktop App for LG K-EXAONE 카탈로그 (테스트)

> [Desktop App for LG K-EXAONE](https://github.com/kidarigun/k-exaone-desktop)용 목록입니다. 앱과 이 목록 모두 LG AI연구원이 만들거나 보증하지 않은 **비공식 프로젝트**입니다.

Desktop App for LG K-EXAONE의 **[Skill] → 찾아보기**, **[MCP 서버] → 찾아보기** 창이 읽어 가는 목록입니다.
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
| `install.oauth` | 원격 서버 로그인: `clientId`, `clientSecret`(`{key}` 사용 가능), `scopes`, `authorizationEndpoint`, `tokenEndpoint`, `extraParams`, `group`. 엔드포인트를 비우면 앱이 서버에서 찾고, `clientId`를 비우면 자동 등록을 시도합니다. 같은 `group`의 서버는 클라이언트 정보와 로그인을 함께 씁니다. 앱의 리디렉션 URI는 `http://localhost:45789/oauth2callback`입니다 |
| `inputs` | 설치할 때 사용자에게 받을 값. `{key}`로 args·env·url·headers에 끼워 넣습니다 |
| `safeTools` | 처음부터 승인 없이 실행할 읽기 전용 도구 |
| `guide` | 처음 설정이 필요한 서버의 단계별 안내 페이지 (예: `docs/google-workspace.md`) — 연결 창에 [설정 안내 열기] 버튼이 나옵니다 |
| `note`, `license` | "이 앱에서 알아 둘 점"과 라이선스 표시 |

`inputs`의 `type`: `text`, `secret`(비밀번호 칸, 자격 증명 관리자에 저장), `folder`(폴더 선택 창).
선택 입력(`required: false`)을 비워 두면 그 값이 들어간 인자·환경 변수·헤더는 빠집니다.

npm 패키지는 `@2.3.0`처럼 **버전을 고정**하세요. 패키지가 바뀌어도 사용자 PC에서 실행되는 코드가 갑자기 달라지지 않습니다.

### Skill

| 필드 | 설명 |
|---|---|
| `id`, `name`, `summary`, `category`, `publisher` | 화면 표시용 |
| `path` | Skill 폴더 (`skills/<id>`) — `build.py`가 zip으로 묶고 `download`, `sha256`, `size`, `files`, `skillName`을 채웁니다 |
| `requires` | 필요한 프로그램 (예: 스크립트가 있으면 `python`) |
| `source` | 다른 GitHub 저장소의 Skill을 옮겨 올 때: `{"repo": "anthropics/skills", "commit": "<40자리 커밋>", "path": "skills/docx"}` — `path` 대신 씁니다 |
| `license`, `note` | 라이선스 표시와 "이 앱에서 알아 둘 점" 안내 |

### Claude 공식 Skill

`anthropics/skills` 저장소의 Skill 18개를 커밋 `1780c5e`로 고정해 옮겨 왔습니다 (모두 Apache-2.0).
zip에는 원본 LICENSE.txt와 함께 출처를 적은 `SOURCE.md`, 저장소의 `THIRD_PARTY_NOTICES.md`를 넣습니다.
LICENSE 파일이 없는 `doc-coauthoring`은 넣지 않았습니다. 원본을 새 버전으로 바꾸려면 `commit`만 바꾸고 `build.py`를 다시 실행하세요.

### Superpowers Skill

`obra/superpowers` 저장소의 Skill 15개를 커밋 `22f0b46`으로 고정해 옮겨 왔습니다 (모두 MIT).
zip에는 저장소 루트의 원본 `LICENSE`와 함께 출처를 적은 `SOURCE.md`를 넣습니다.

앱은 zip을 받은 뒤 sha256이 맞을 때만 설치합니다.
