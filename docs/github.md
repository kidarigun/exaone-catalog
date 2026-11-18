# GitHub MCP 서버 연결 안내

Desktop App for LG K-EXAONE에서 내 GitHub 저장소의 코드, 커밋, 이슈, 풀 리퀘스트를 조회하거나 새로 만드는 설정입니다.

## 연결 방식 한눈에 비교

**[MCP 서버] → 찾아보기 → GitHub** 분류에서 목적에 맞는 방식을 고르세요.

| 항목 | 인증 방식 | 특징 |
|---|---|---|
| **GitHub (GitHub App 인증)** (권장) | GitHub App (`Iv23li...`) | 저장소·권한 세밀하게 선택, 토큰 만료 시 자동 갱신 |
| **GitHub (GitHub App 인증 · 읽기 전용)** | GitHub App (`Iv23li...`) | 위와 같지만 읽기 전용 주소(`/mcp/readonly`)만 사용 |
| **GitHub (OAuth App 인증)** | OAuth App (`Ov23li...`) | 권한 세부 설정 없이 Callback URL만으로 가장 간단히 등록 |
| **GitHub (개인 액세스 토큰)** | 개인 액세스 토큰(PAT) | 브라우저 로그인 설정 없이 토큰 복사만으로 연결 |
| **GitHub (개인 액세스 토큰 · 읽기 전용)** | 개인 액세스 토큰(PAT) | 읽기 전용 주소(`/mcp/readonly`)만 사용 |
| **GitHub (내 PC에서 실행)** | 개인 액세스 토큰(PAT) | 원격 서버 대신 내 PC Node.js(`npx`)로 직접 실행 |

- 읽기 도구(검색, 파일·이슈·PR·커밋 조회 등)는 승인 없이 바로 실행되고, **파일 수정·이슈·PR 작성·병합 같은 작업은 실행할 때마다 승인 창**이 나옵니다.

---

## 방법 1: GitHub App으로 등록해 연결하기 (권장)

GitHub 공식 문서에서 권장하는 인증 앱 방식입니다. 내가 허용할 저장소와 권한(읽기/쓰기)만 지정할 수 있고, 브라우저 로그인 후 토큰이 만료되면 앱이 자동으로 갱신합니다.

### 1. GitHub App 만들기

1. [GitHub Apps 등록 페이지](https://github.com/settings/apps/new)를 열고 로그인합니다.
2. **GitHub App name**에 고유한 이름을 적습니다 (예: `exaone-desktop-내아이디`).
3. **Homepage URL**에 `https://github.com/kidarigun/k-exaone-desktop`을 입력합니다.
4. **Callback URL** (중요)에 아래 주소를 글자 하나까지 정확히 입력합니다.
   ```
   http://localhost:45789/oauth2callback
   ```
   - **Expire user authorization tokens**는 켜 두어도 됩니다(앱이 갱신 토큰으로 자동 갱신합니다).
5. **Webhook** 항목의 **Active** 체크를 **해제**합니다.
6. **Permissions → Repository permissions**에서 필요한 권한을 고릅니다.
   - 읽기만 쓸 경우: **Contents** (`Read-only`), **Issues** (`Read-only`), **Pull requests** (`Read-only`), **Metadata** (`Read-only`)
   - 파일 수정·이슈·PR 생성까지 쓸 경우: **Contents** (`Read and write`), **Issues** (`Read and write`), **Pull requests** (`Read and write`), **Metadata** (`Read-only`)
7. 아래쪽 **Where can this GitHub App be installed?**는 **Only on this account**를 고른 뒤 **Create GitHub App**을 누릅니다.

### 2. Client ID·Client Secret 확인 및 앱 설치

1. 생성된 앱 화면 위쪽의 **Client ID**(`Iv23li...` 형태)를 복사합니다.
2. **Client secrets** 항목에서 **Generate a new client secret**을 눌러 생성된 비밀 값을 복사합니다. (페이지를 벗어나면 다시 볼 수 없습니다.)
3. 왼쪽 메뉴에서 **Install App**을 누르고, 내 계정의 **Install**을 눌러 앱이 접근할 저장소(**All repositories** 또는 **Only select repositories**)를 지정해 설치를 마칩니다.

### 3. Desktop App for LG K-EXAONE에서 연결

1. **[MCP 서버] → 찾아보기 → GitHub**에서 **GitHub (GitHub App 인증)** (또는 **읽기 전용**)의 **[연결]**을 누릅니다.
2. 복사한 **Client ID**와 **Client Secret**을 넣고 **[연결]**을 누릅니다.
3. 브라우저가 열리면 권한을 확인하고 **Authorize**를 누릅니다.
4. "로그인 완료" 화면이 나오면 브라우저를 닫고 앱으로 돌아갑니다. **[내 서버]**에서 **연결됨**이 되면 준비 끝입니다.

---

## 방법 2: OAuth App으로 등록해 연결하기 (간편한 브라우저 로그인)

저장소별 세부 권한 설정 없이 Callback URL만으로 빠르게 인증 앱을 등록하고 싶을 때 씁니다.

1. [OAuth Apps 등록 페이지](https://github.com/settings/applications/new)를 엽니다.
2. 아래 값을 입력하고 **Register application**을 누릅니다.
   - **Application name**: `Desktop App for LG K-EXAONE`
   - **Homepage URL**: `https://github.com/kidarigun/k-exaone-desktop`
   - **Authorization callback URL** (중요):
     ```
     http://localhost:45789/oauth2callback
     ```
3. 생성된 화면에서 **Client ID**(`Ov23li...`)를 복사하고, **Generate a new client secret**을 눌러 **Client Secret**도 복사합니다.
4. 앱의 **[MCP 서버] → 찾아보기 → GitHub (OAuth App 인증) → [연결]**을 눌러 입력한 뒤, 브라우저에서 **Authorize**를 눌러 로그인합니다.

---

## 방법 3: 개인 액세스 토큰(PAT)으로 연결하기

인증 앱 등록 없이 토큰 한 줄로 연결할 때 씁니다. **GitHub (개인 액세스 토큰)**, **읽기 전용**, **내 PC에서 실행**에서 씁니다.

1. [Personal access tokens (Fine-grained tokens)](https://github.com/settings/personal-access-tokens/new) 페이지를 열고 로그인합니다.
   - 또는 기존 방식인 [Tokens (classic)](https://github.com/settings/tokens/new)에서 `repo`, `read:org`, `read:user` 권한을 선택해 만들어도 됩니다.
2. **Token name**과 만료 기한(**Expiration**)을 적고, **Repository access**에서 허용할 저장소를 고릅니다.
3. **Permissions → Repository permissions**에서 **Contents**, **Issues**, **Pull requests**, **Metadata** 권한을 고르고 **Generate token**을 누릅니다.
4. 복사한 토큰(`github_pat_...` 또는 `ghp_...`)을 앱의 **[연결]** 칸에 붙여 넣습니다. (토큰은 **Windows 자격 증명 관리자**에 저장됩니다.)

> **팁 (GitHub CLI `gh` 사용자):** 이 PC에 이미 `gh auth login`으로 로그인되어 있다면 PowerShell에서 `gh auth token`을 실행해 나온 값(`gho_...`)을 바로 넣어 쓸 수도 있습니다.

---

## 자주 생기는 문제

| 증상 | 해결 |
|---|---|
| GitHub App 로그인 후 저장소가 보이지 않음 | GitHub App의 **Install App** 메뉴에서 내 계정과 대상 저장소에 앱을 설치했는지(2-3단계) 확인하세요. |
| `redirect_uri` 불일치 오류 (인증 앱 로그인) | 앱 설정의 Callback URL이 `http://localhost:45789/oauth2callback`과 글자 하나까지 같은지 확인하세요. |
| 조직(Organization) 저장소가 보이지 않음 (HTTP 403) | 조직 관리자의 OAuth/GitHub App 또는 PAT 승인이 필요할 수 있습니다. 조직 설정의 Third-party access / Personal access tokens 정책을 확인하세요. |
| HTTP 401 인증 오류 | 토큰이 잘못되었거나 만료되었습니다. PAT는 **[편집]**에서 새 토큰으로 바꾸고, 인증 앱은 **[로그인]**을 다시 누르세요. |
| `npx` 명령을 찾을 수 없음 (**내 PC에서 실행**) | Node.js가 필요합니다. **[MCP 서버]** 창의 **[자동 설치]** 버튼으로 설치하거나 원격 서버 항목을 쓰세요. |
| "45789번 포트를 열 수 없습니다" | 다른 로그인이 진행 중이거나 다른 프로그램이 45789 포트를 쓰고 있습니다. 잠시 뒤 다시 시도하세요. |

---

## 연결 끊기

- 앱의 **[MCP 서버]** 창에서 서버의 **로그아웃** 또는 **삭제**를 누르면 저장된 토큰과 인증 정보가 Windows 자격 증명 관리자에서 삭제됩니다.
- GitHub 계정의 [Authorized GitHub Apps](https://github.com/settings/apps/authorizations), [Authorized OAuth Apps](https://github.com/settings/applications), [Personal access tokens](https://github.com/settings/tokens)에서도 접근 권한을 언제든 취소할 수 있습니다.
