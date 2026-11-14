# Google 공식 Workspace MCP 서버 연결 안내

Google이 직접 운영하는 MCP 서버(Gmail, 드라이브, 캘린더, 문서, 시트, 슬라이드, Chat, 연락처)를 Desktop App for LG K-EXAONE에 연결하는 방법입니다.
내 PC에 설치할 프로그램은 없고, 브라우저로 Google 계정에 로그인해 씁니다.

> **아직 개발자 미리보기입니다.** Google이 [Google Workspace Developer Preview Program](https://developers.google.com/workspace/preview) 가입자에게만 열어 두었습니다.
> 가입 전이라면 찾아보기의 **Google Workspace**(커뮤니티 서버, [안내](google-workspace.md))를 쓰세요.
> Google의 원문 안내: [Google Workspace MCP 서버 구성](https://developers.google.com/workspace/guides/configure-mcp-servers?hl=ko)

처음 한 번 Google Cloud 설정이 필요합니다(15분쯤, 무료).

## 1. Developer Preview Program 가입

[Google Workspace Developer Preview Program](https://developers.google.com/workspace/preview) 페이지에서 가입을 신청합니다. 승인된 뒤에 아래 설정을 진행하세요.

## 2. Google Cloud 프로젝트 만들기

1. [Google Cloud 콘솔](https://console.cloud.google.com/projectcreate)에서 새 프로젝트를 만듭니다 (예: `Desktop App for LG K-EXAONE`).
2. 화면 위쪽에서 그 프로젝트가 선택되어 있는지 확인합니다.

## 3. API 켜기

쓸 서비스마다 **일반 API**와 **MCP API** 두 개를 모두 켜야 합니다. 링크를 열어 **사용**을 누르세요.

| 서비스 | 일반 API | MCP API |
|---|---|---|
| Gmail | [gmail.googleapis.com](https://console.cloud.google.com/apis/library/gmail.googleapis.com) | [gmailmcp.googleapis.com](https://console.cloud.google.com/apis/library/gmailmcp.googleapis.com) |
| 드라이브 | [drive.googleapis.com](https://console.cloud.google.com/apis/library/drive.googleapis.com) | [drivemcp.googleapis.com](https://console.cloud.google.com/apis/library/drivemcp.googleapis.com) |
| 캘린더 | [calendar-json.googleapis.com](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com) | [calendarmcp.googleapis.com](https://console.cloud.google.com/apis/library/calendarmcp.googleapis.com) |
| 문서 | [docs.googleapis.com](https://console.cloud.google.com/apis/library/docs.googleapis.com) | [docsmcp.googleapis.com](https://console.cloud.google.com/apis/library/docsmcp.googleapis.com) |
| 시트 | [sheets.googleapis.com](https://console.cloud.google.com/apis/library/sheets.googleapis.com) | [sheetsmcp.googleapis.com](https://console.cloud.google.com/apis/library/sheetsmcp.googleapis.com) |
| 슬라이드 | [slides.googleapis.com](https://console.cloud.google.com/apis/library/slides.googleapis.com) | [slidesmcp.googleapis.com](https://console.cloud.google.com/apis/library/slidesmcp.googleapis.com) |
| Chat | [chat.googleapis.com](https://console.cloud.google.com/apis/library/chat.googleapis.com) | [chatmcp.googleapis.com](https://console.cloud.google.com/apis/library/chatmcp.googleapis.com) |
| 연락처 | [people.googleapis.com](https://console.cloud.google.com/apis/library/people.googleapis.com) | (같은 API) |

Chat은 회사·학교 Google Workspace 계정에서만 쓸 수 있고, Google 안내에 따라 Chat 앱 설정도 해야 합니다.

## 4. 로그인 화면(OAuth 동의 화면) 설정

1. [Google 인증 플랫폼](https://console.cloud.google.com/auth/overview) → **시작하기**.
2. 앱 이름 `Desktop App for LG K-EXAONE`, 지원 이메일은 내 이메일.
3. **대상**: 회사·학교 계정이면 **내부**, 개인 Gmail이면 **외부**.
4. **외부**라면 [대상](https://console.cloud.google.com/auth/audience) 화면의 **테스트 사용자**에 내 이메일을 추가합니다.
5. [데이터 액세스](https://console.cloud.google.com/auth/scopes) → **범위 추가 또는 삭제** → **직접 범위 추가**에 쓸 서비스의 권한을 넣습니다.
   Desktop App for LG K-EXAONE이 요청하는 권한은 다음과 같습니다 (모두 `https://www.googleapis.com/auth/`로 시작):
   - Gmail: `gmail.readonly`, `gmail.compose`
   - 드라이브: `drive.readonly`, `drive.file`
   - 캘린더: `calendar.calendarlist.readonly`, `calendar.events.freebusy`, `calendar.events.readonly`
   - 문서: `drive.readonly`, `drive.file`, `documents.readonly`, `documents`
   - 시트: `drive.readonly`, `drive.file`, `spreadsheets.readonly`, `spreadsheets`
   - 슬라이드: `drive.readonly`, `drive.file`, `presentations.readonly`, `presentations`
   - Chat: `chat.spaces.readonly`, `chat.memberships.readonly`, `chat.messages.readonly`, `chat.messages.create`, `chat.users.readstate`, `chat.users.spacesettings`
   - 연락처: `directory.readonly`, `userinfo.profile`, `contacts.readonly`

## 5. OAuth 클라이언트 만들기 (중요)

1. [클라이언트](https://console.cloud.google.com/auth/clients) → **클라이언트 만들기**.
2. 애플리케이션 유형: **웹 애플리케이션**.
3. **승인된 리디렉션 URI**에 아래 주소를 정확히 추가합니다.
   ```
   http://localhost:45789/oauth2callback
   ```
4. **Use this client for an AI-powered agent**(AI 에이전트용 클라이언트) 옵션을 켭니다. Google은 Workspace MCP 서버를 쓰는 클라이언트에 이 옵션을 요구하며, 이미 만든 클라이언트에서는 나중에 바꾸지 못할 수 있으니 **만들 때 켜세요**.
5. **만들기**를 누르고 **클라이언트 ID**와 **클라이언트 보안 비밀번호**를 복사합니다.

## 6. Desktop App for LG K-EXAONE에서 연결

1. **[MCP 서버] → 찾아보기 → Google 공식 (미리보기)**에서 쓸 서비스(예: Gmail)의 **[연결]**을 누릅니다.
2. 클라이언트 ID와 보안 비밀번호를 넣고 **[연결]** → 브라우저가 열립니다.
3. Google 계정으로 로그인하고 권한을 허락합니다. ("확인되지 않은 앱" 경고가 나오면 **고급 → 이동**. 내가 만든 앱이라 나오는 경고입니다)
4. "로그인 완료" 화면이 나오면 브라우저를 닫고 앱으로 돌아갑니다. **[내 서버]**에서 **연결됨**이 되면 끝입니다.

다른 Google 서비스(드라이브, 캘린더 등)를 추가할 때는 클라이언트 정보를 다시 묻지 않습니다. 새 서비스의 권한을 허락받기 위해 브라우저 로그인만 한 번 더 합니다.

로그인 정보(토큰)는 Windows 자격 증명 관리자에 저장되고, 만료되면 앱이 자동으로 갱신합니다.

## 자주 생기는 문제

| 증상 | 해결 |
|---|---|
| `redirect_uri_mismatch` 오류 | 5-3단계의 리디렉션 URI가 `http://localhost:45789/oauth2callback`과 글자 하나까지 같은지 확인하세요. |
| "액세스 차단됨" | **외부** 대상이면 테스트 사용자에 내 이메일을 추가하세요. |
| 연결 후 HTTP 403 오류 | 3단계의 **MCP API**까지 켰는지, Developer Preview에 가입했는지 확인하세요. |
| "AI-powered agent" 관련 오류 | 5-4단계 옵션을 켠 새 클라이언트를 만들어 서버를 다시 추가하세요. |
| 일주일쯤 지나면 다시 로그인 | **외부 + 테스트** 상태 앱의 로그인은 Google 정책상 7일마다 만료됩니다. MCP 서버 창의 **[로그인]**을 다시 누르세요. |
| "45789번 포트를 열 수 없습니다" | 다른 로그인이 진행 중이거나 다른 프로그램이 그 포트를 씁니다. 잠시 뒤 다시 시도하세요. |

## 연결 끊기

- MCP 서버 창에서 서버의 **로그아웃** 버튼을 누르면 저장된 로그인 정보가 지워집니다.
- [Google 계정 권한](https://myaccount.google.com/connections)에서 `Desktop App for LG K-EXAONE`의 접근 권한도 삭제할 수 있습니다.
