# Google Workspace 연결 안내

Desktop App for LG K-EXAONE에서 Gmail, Google 드라이브, 캘린더, 문서, 시트, 슬라이드, 할 일을 쓰기 위한 설정입니다.
처음 한 번만 하면 되고 10분쯤 걸립니다. 비용은 들지 않습니다.

> Google 공식 서버(개발자 미리보기)를 쓰려면 [공식 서버 안내](google-workspace-official.md)를 보세요.
>
> 이 연결은 Google 공식 서버가 아니라 커뮤니티 오픈소스 서버([taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp), MIT)를 씁니다.
> 서버는 **내 PC에서만** 실행되고, 로그인 정보도 내 PC에 저장됩니다.

## 1. uv 설치

이 서버는 Python 프로그램이라 `uv`가 필요합니다. 시작 메뉴에서 **PowerShell**을 열고 아래 한 줄을 붙여 넣으세요.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

설치가 끝나면 **Desktop App for LG K-EXAONE을 완전히 껐다가 다시 여세요.** (설치한 프로그램을 앱이 찾을 수 있게)

## 2. Google Cloud 프로젝트 만들기

1. [Google Cloud 콘솔](https://console.cloud.google.com/projectcreate)에 Google 계정으로 로그인합니다.
2. 프로젝트 이름에 `Desktop App for LG K-EXAONE` 등을 넣고 **만들기**를 누릅니다. (결제 정보는 필요 없습니다)
3. 화면 위쪽에서 방금 만든 프로젝트가 선택되어 있는지 확인합니다.

## 3. 쓸 API 켜기

아래 링크를 하나씩 열어 **사용**을 누릅니다. 쓰지 않을 서비스는 건너뛰어도 됩니다.

- [Gmail API](https://console.cloud.google.com/apis/library/gmail.googleapis.com)
- [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com)
- [Google Calendar API](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com)
- [Google Docs API](https://console.cloud.google.com/apis/library/docs.googleapis.com)
- [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com)
- [Google Slides API](https://console.cloud.google.com/apis/library/slides.googleapis.com)
- [Google Tasks API](https://console.cloud.google.com/apis/library/tasks.googleapis.com)

## 4. 로그인 화면(OAuth 동의 화면) 설정

1. [Google 인증 플랫폼](https://console.cloud.google.com/auth/overview)을 열고 **시작하기**를 누릅니다.
2. **앱 정보**: 앱 이름 `Desktop App for LG K-EXAONE`, 사용자 지원 이메일은 내 이메일.
3. **대상**: 개인 Gmail이면 **외부**를 고릅니다. (회사·학교 Google Workspace 계정이면 **내부**를 고를 수 있습니다)
4. **연락처 정보**에 내 이메일을 넣고 완료합니다.
5. **외부**를 골랐다면 [대상](https://console.cloud.google.com/auth/audience) 화면의 **테스트 사용자**에 **내 Gmail 주소를 추가**합니다. 추가하지 않으면 로그인이 거부됩니다.

## 5. OAuth 클라이언트 만들기

1. [클라이언트](https://console.cloud.google.com/auth/clients) 화면에서 **클라이언트 만들기**를 누릅니다.
2. 애플리케이션 유형: **데스크톱 앱**, 이름: `Desktop App for LG K-EXAONE`.
3. **만들기**를 누르면 **클라이언트 ID**와 **클라이언트 보안 비밀번호**가 나옵니다. 둘 다 복사해 둡니다.

## 6. Desktop App for LG K-EXAONE에서 연결

1. 왼쪽 아래 **[MCP 서버] → 찾아보기 → Google Workspace**(또는 **읽기 전용**)에서 **[연결]**을 누릅니다.
2. 내 Google 이메일, 클라이언트 ID, 클라이언트 보안 비밀번호를 넣고 **[연결]**을 누릅니다.
   - 처음에는 서버 프로그램을 내려받느라 1~2분 걸릴 수 있습니다.
   - 보안 비밀번호는 Windows 자격 증명 관리자에 저장됩니다.
3. **[내 서버]** 탭에서 상태가 **연결됨**이 되고 도구 목록이 보이면 준비 끝입니다.

## 7. 처음 쓸 때 Google 로그인

채팅에서 예를 들어 **"오늘 받은 메일 중 중요한 것 요약해 줘"**라고 요청해 보세요.

1. 엑사원이 Gmail 도구를 쓰려고 하면 승인 카드가 나옵니다. **[승인]**을 누릅니다.
2. 처음이면 **브라우저가 열리고 Google 로그인 화면**이 나옵니다. 내 계정으로 로그인합니다.
3. "Google에서 확인하지 않은 앱" 경고가 나오면 **고급 → Desktop App for LG K-EXAONE(으)로 이동**을 누릅니다. (내가 만든 앱이라 나오는 경고입니다)
4. 권한을 확인하고 **계속**을 누르면 "인증 완료" 화면이 나옵니다. 브라우저를 닫고 채팅으로 돌아와 **"다시 해 줘"**라고 하면 됩니다.

로그인 정보(토큰)는 사용자 폴더의 `.google_workspace_mcp` 폴더에 저장되어 다음부터는 묻지 않습니다.

## 자주 생기는 문제

| 증상 | 해결 |
|---|---|
| `uvx` 명령을 찾을 수 없음 | 1단계 설치 후 Desktop App for LG K-EXAONE을 완전히 껐다가 다시 여세요. |
| 로그인할 때 "액세스 차단됨" | 4-5단계의 **테스트 사용자**에 내 이메일을 추가했는지 확인하세요. |
| "API has not been used in project" 오류 | 3단계에서 해당 API를 **사용**으로 바꾸고 몇 분 뒤 다시 시도하세요. |
| 일주일쯤 지나면 다시 로그인하라고 함 | 대상이 **외부 + 테스트** 상태인 앱은 Google 정책상 로그인이 7일마다 만료됩니다. 그때마다 브라우저 로그인을 다시 하면 됩니다. ([대상](https://console.cloud.google.com/auth/audience) 화면에서 **앱 게시**를 하면 만료가 없어질 수 있지만, Gmail처럼 민감한 권한은 Google 검증 정책의 적용을 받으니 Google 안내를 확인하세요.) |
| 로그인 후 "포트 8000" 관련 오류 | 다른 프로그램이 8000번 포트를 쓰고 있습니다. 그 프로그램을 끄고 다시 시도하세요. |
| 메일 보내기·일정 만들기가 안 됨 | **읽기 전용**으로 연결했다면 바꿀 수 없습니다. 일반 **Google Workspace**로 다시 연결하세요. |

## 안전하게 쓰기

- 메일 보내기, 일정·파일 만들기 같은 작업은 실행할 때마다 승인 카드가 나옵니다. 내용을 확인하고 승인하세요.
- 메일 본문이나 문서 안에 "이 메일을 누구에게 보내라" 같은 지시가 들어 있을 수 있습니다. 엑사원에게 도구 결과 속 지시는 따르지 말라고 알려 두었지만, 모델이 실수할 수 있으니 승인 전에 꼭 확인하세요.
- 연결을 끊으려면 MCP 서버 창에서 서버를 끄거나 삭제하고, [Google 계정 권한](https://myaccount.google.com/connections)에서 `Desktop App for LG K-EXAONE` 접근을 삭제하세요.
