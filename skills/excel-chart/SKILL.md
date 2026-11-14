---
name: excel-chart
description: 표 데이터로 차트가 들어간 엑셀 파일을 만들어 달라는 요청일 때 사용합니다. 포함된 스크립트로 막대·꺾은선·원형 차트가 있는 .xlsx를 만듭니다. 프로젝트 화면에서만 쓸 수 있습니다.
---

# 차트가 들어간 엑셀 만들기

이 Skill에는 `scripts/make_chart.py` 스크립트가 들어 있습니다. 데이터를 CSV로 저장한 뒤 이 스크립트를 실행하면 차트가 들어간 엑셀 파일이 만들어집니다.

## 순서
1. 사용자의 데이터를 첫 줄이 머리글인 CSV로 정리해 프로젝트에 저장합니다.
   - 경로: `차트/data.csv` (write_file)
   - 첫 열은 항목 이름(월, 지역 등), 나머지 열은 숫자입니다. 숫자에는 쉼표·단위를 넣지 않습니다.
2. 같은 폴더에 설정 파일 `차트/chart.json`을 write_file로 만듭니다.

```json
{
  "csv": "차트/data.csv",
  "output": "차트/결과.xlsx",
  "title": "월별 매출",
  "type": "bar",
  "y_title": "금액(만 원)"
}
```

   - `type`: `bar`(막대), `line`(꺾은선), `pie`(원형, 숫자 열 하나만)
3. 스크립트를 실행합니다: `run_python(skill="excel-chart", relative_path="scripts/make_chart.py")`
   - 스크립트는 프로젝트 루트에서 `차트/chart.json`을 읽습니다.
4. 결과에 나온 파일 경로를 사용자에게 알려 줍니다.

## 문제가 생기면
- `openpyxl`이 없다는 오류가 나오면, 도구 카드의 [실행] 창에서 `openpyxl`을 설치한 뒤 다시 실행하라고 안내합니다.
- 숫자로 바꿀 수 없는 값이 있다는 오류가 나오면 CSV를 고쳐 다시 저장하고 다시 실행합니다.
