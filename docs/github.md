# GitHub MCP 서버 연결 안내

Desktop App for LG K-EXAONE에서 내 GitHub 저장소의 코드, 커밋, 이슈, 풀 리퀘스트를 조회하거나 새로 만드는 설정입니다.

## 연결 방식 고르기

**[MCP 서버] → 찾아보기 → GitHub** 분류에서 목적에 맞는 방식을 고르세요.

| 항목 | 실행 방식 | 로그인 방법 | 할 수 있는 일 |
|---|---|---|---|
| **GitHub** (권장) | GitHub 공식 원격 서버 | 개인 액세스 토큰(PAT) | 저장소·코드·이슈·PR 조회 + 파일 수정·이슈·PR 만들기 |
| **GitHub (읽기 전용)** | GitHub 공식 원격 서버 | 개인 액세스 토큰(PAT) | 저장소·코드·이슈·PR 읽기만 가능 |
| **GitHub (브라우저 로그인)** | GitHub 공식 원격 서버 | 브라우저 OAuth 로그인 | 저장소·코드·이슈·PR 조회 + 만들기 |
| **GitHub (내 PC에서 실행)** | 내 PC Node.js (`npx`) | 개인 액세스 토큰(PAT) | 원격 서버 대신 내 PC에서 GitHub API 직접 호출 |

- 읽기 도구(검색, 파일·이슈·PR·커밋 조회 등)는 승인 없이 바로 실행되고, **파일 수정·이슈·PR 작성·병합 같은 작업은 실행할 때마다 승인 창**이 나옵니다.
- **GitHub (읽기 전용)**은 원격 읽기 전용 주소(`/mcp/readonly`)를 쓰므로 실수로 저장소를 바꿀 염려 없이 코드 검토용으로 쓰기에 안전합니다.

---

## 방법 1: 개인 액세스 토큰(PAT)으로 연결하기 (권장, 2분)

**GitHub**, **GitHub (읽기 전용)**, **GitHub (내 PC에서 실행)**에서 씁니다.

1. [GitHub Personal access tokens (Fine-grained tokens)](https://github.com/settings/personal-access-tokens/new) 페이지를 열고 로그인합니다.
   - 또는 기존 방식인 [Tokens (classic)](https://github.com/settings/tokens/new)에서 `repo`, `read:org`, `read:user` 권한을 선택해 만들어도 됩니다.
2. **Token name**에 `Desktop App for LG K-EXAONE` 등을 적고, 만료 기한(**Expiration**)을 고릅니다.
3. **Repository access**에서 이 앱이 접근할 저장소를 고릅니다 (**Only select repositories**로 필요한 저장소만 고르거나 **All repositories**).
4. **Permissions → Repository permissions**에서 필요한 권한을 켭니다.
   - 읽기만 쓸 경우: **Contents** (`Read-only`), **Issues** (`Read-only`), **Pull requests** (`Read-only`), **Metadata** (`Read-only`)
   - 파일 수정·이슈·PR 생성까지 쓸 경우: **Contents** (`Read and write`), **Issues** (`Read and write`), **Pull requests** (`Read and write`), **Metadata** (`Read-only`)
5. **Generate token**을 누르고 화면에 나온 토큰(`github_pat_...` 또는 `ghp_...`)을 복사합니다. (페이지를 닫으면 다시 볼 수 없습니다.)
6. 앱의 **[MCP 서버] → 찾아보기 → GitHub**에서 **[연결]**을 누르고 복사한 토큰을 붙여 넣습니다.
   - 입력한 토큰은 설정 파일이 아니라 **Windows 자격 증명 관리자**에 암호화되어 저장됩니다.

> **팁 (GitHub CLI `gh` 사용자):** 이 PC에 이미 `gh auth login`으로 로그인되어 있다면 PowerShell에서 `gh auth token`을 실행해 나온 값(`gho_...`)을 바로 넣어 테스트할 수도 있습니다.

---

## 방법 2: OAuth 앱(브라우저 로그인)으로 연결하기

개인 액세스 토큰을 직접 넣는 대신 브라우저에서 GitHub 계정으로 로그인해 연결하는 방식입니다. 처음 한 번 GitHub에 OAuth App을 등록해야 합니다.

1. [GitHub Developer settings → OAuth Apps](https://github.com/settings/developers)로 이동해 **New OAuth App**을 누릅니다.
2. 아래 값을 입력하고 **Register application**을 누릅니다.
   - **Application name**: `Desktop App for LG K-EXAONE`
   - **Homepage URL**: `https://github.com/kidarigun/k-exaone-desktop`
   - **Authorization callback URL** (중요):
     ```
     http://localhost:45789/oauth2callback
     ```
3. 생성된 화면에서 **Client ID**를 복사하고, **Generate a new client secret**을 눌러 **Client Secret**도 복사합니다.
4. 앱의 **[MCP 서버] → 찾아보기 → GitHub (브라우저 로그인) → [연결]**을 눌러 Client ID와 Client Secret을 입력합니다.
5. **[내 서버]** 탭에서 해당 서버의 **[로그인]**을 누르면 브라우저가 열립니다. 권한을 확인하고 **Authorize**를 누르면 "로그인 완료" 화면과 함께 연결됩니다.

---

## 자주 생기는 문제

| 증상 | 해결 |
|---|---|
| HTTP 401 인증 오류 | 토큰이 잘못되었거나 만료되었습니다. 새 토큰을 발급해 서버의 **[편집]**에서 다시 넣거나, 브라우저 로그인 서버는 **[로그인]**을 다시 누르세요. |
| 조직(Organization) 저장소가 보이지 않음 (HTTP 403) | 조직 정책상 Fine-grained PAT나 OAuth App 승인이 필요할 수 있습니다. 조직 관리자에게 승인을 요청하거나 **Tokens (classic)**에서 조직 권한(`read:org`)과 SSO 승인을 켜세요. |
| `npx` 명령을 찾을 수 없음 (**내 PC에서 실행**) | Node.js가 필요합니다. **[MCP 서버]** 창의 **[자동 설치]** 버튼을 눌러 Node.js를 설치하거나 공식 원격 서버(**GitHub**)를 쓰세요. |
| "45789번 포트를 열 수 없습니다" (OAuth 로그인) | 다른 로그인이 진행 중이거나 다른 프로그램이 45789 포트를 쓰고 있습니다. 잠시 뒤 다시 시도하세요. |
| `redirect_uri` 불일치 오류 (OAuth 로그인) | OAuth App의 **Authorization callback URL**이 `http://localhost:45789/oauth2callback`과 글자 하나까지 같은지 확인하세요. |

---

## 연결 끊기

- 앱의 **[MCP 서버]** 창에서 서버 스위치를 끄거나 **삭제**하면 저장된 토큰과 로그인 정보가 Windows 자격 증명 관리자에서 함께 삭제됩니다.
- GitHub 계정의 [Personal access tokens](https://github.com/settings/tokens) 또는 [Authorized OAuth Apps](https://github.com/settings/applications)에서도 토큰이나 접근 권한을 언제든 회수할 수 있습니다.
