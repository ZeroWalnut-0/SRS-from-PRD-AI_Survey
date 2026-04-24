---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-003: 4종 산출물(Excel, Codebook, PDF) 컴파일 및 ZIP 생성 로직 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-003] 4종 산출물(Excel, Codebook, PDF) 컴파일 및 ZIP 생성 로직 구현
- 목적: 수집된 응답 데이터를 기반으로 엑셀 결과물, 코드북, 원본 PDF, 클린 데이터를 생성하고 이를 하나의 ZIP 파일로 패키징하여 Supabase Storage에 업로드한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3_REQ-FUNC-017`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 기술 스택: `xlsx`, `jszip` 라이브러리 활용

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 데이터 추출: `RESPONSE` 테이블에서 해당 폼의 모든 응답 데이터 페칭
- [ ] 엑셀 생성 로직:
    - `Raw Data`: 응답자별 문항 응답 원본 엑셀 생성
    - `Codebook`: 문항 스키마를 기반으로 변수 설명 및 보기 코드맵 엑셀 생성
- [ ] 파일 패키징:
    - 엑셀 파일들, 원본 업로드 문서(PDF/Word), 클린 데이터 세트를 `jszip`으로 압축
- [ ] Supabase Storage 업로드: 생성된 ZIP 파일을 특정 버킷에 업로드하고 경로 저장
- [ ] 작업 완료 시 `ZIP_DATAMAP.download_url` 필드 갱신

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 산출물 패키징 성공
- Given: 100건의 응답이 수집된 설문
- When: 컴파일러 로직이 실행됨
- Then: 4종의 파일이 포함된 유효한 `.zip` 파일이 생성되고 Storage에 업로드되어야 한다.

Scenario 2: 대량 데이터 처리 성능
- Given: 1,000건 이상의 응답 데이터
- When: 엑셀 생성 및 압축을 수행함
- Then: 서버 타임아웃(10초) 이내에 작업이 완료되거나, 필요 시 비동기(Edge Function)로 처리되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 엑셀 파일 생성 시 메모리 사용량을 최적화한다.
- 정확성: 엑셀 내의 문항 번호와 데이터 값이 `structure_schema`와 정확히 일치해야 한다.
- **4종 산출물 시트 컬럼 스키마:**

| 산출물 | 파일명 | 시트 구성 | 주요 컬럼 |
|---|---|---|---|
| 응답원본 | `raw_responses.xlsx` | Sheet1: 응답데이터 | `resp_id`, `timestamp`, `q_001`~`q_N` (문항별 응답 값), `ip_hash`, `user_agent` |
| 변수가이드 | `variable_guide.xlsx` | Sheet1: 변수목록 | `variable_name` (q_001), `label` (문항 텍스트), `type` (SELECT/TEXT/SCALE), `values` (보기 코드맵) |
| 코드북 | `codebook.xlsx` | Sheet1: 코드맵 | `question_id`, `option_code` (1,2,3...), `option_label` (보기 텍스트), `frequency` (응답 빈도), `percentage` |
| 데이터맵 | `datamap.xlsx` | Sheet1: 클린데이터 | `resp_id`, `q_001_code`~`q_N_code` (코딩된 숫자 값), `quota_group`, `completion_status` |

- 인코딩: UTF-8 with BOM (한글 엑셀 호환성 보장)
- 라이브러리: `exceljs` (스트리밍 모드로 메모리 최적화)

## :checkered_flag: Definition of Done (DoD)
- [ ] 4종 산출물(엑셀 2종, PDF, 데이터세트)이 정상 생성되는가?
- [ ] `jszip`을 이용한 압축 및 파일명 포맷이 정확한가?
- [ ] Supabase Storage 업로드 및 경로 저장이 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-005 (RESPONSE), #BE-PAY-002 (결제 완료)
- Blocks: #BE-PAY-004 (URL 발급)
