---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-001: 문서 파일 서버 측 검증 및 DOCUMENT 레코드 생성"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-001] 문서 파일 서버 측 검증 및 DOCUMENT 레코드 생성
- 목적: 업로드된 파일의 물리적 유효성(확장자, 크기, 암호화, 손상 여부)을 서버에서 최종 검증하고, 파싱 프로세스 추적을 위한 `DOCUMENT` 레코드를 DB에 생성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-005`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.1_DOCUMENT`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/documents/upload/route.ts` 핸들러 구현
- [ ] 파일 수신 및 임시 저장 로직 (Vercel 환경 제약 고려)
- [ ] 서버 측 유효성 검증:
    - 매직 넘버(Magic Number) 기반 실제 파일 형식 검증 (HWPX, Word, PDF)
    - 파일 크기 재검증 (5MB 상한)
    - 암호화 여부 체크 (PDF/Word 라이브러리 활용)
- [ ] `DOCUMENT` 레코드 초기 생성: `status='PARSING'`, `file_hash` 계산 및 저장
- [ ] 검증 실패 시 `status='FAILED'` 업데이트 및 에러 응답 반환

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 유효한 파일 업로드
- Given: 2MB의 정상적인 `.docx` 파일이 업로드됨
- When: 서버 검증 로직이 실행됨
- Then: DB에 `DOCUMENT` 레코드가 생성되고 200 OK와 함께 `doc_id`를 반환해야 한다.

Scenario 2: 암호화된 PDF 업로드
- Given: 비밀번호가 걸린 PDF 파일이 업로드됨
- When: 서버 측 검증을 수행함
- Then: 파싱이 불가능하므로 400 에러를 반환하고 DB에 실패 사유를 기록해야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 서버 측 검증 및 DB 레코드 생성까지 레이턴시 ≤ 1,000ms.
- 무결성: 동일 파일 중복 업로드 방지를 위한 `file_hash` 중복 체크 로직 검토.

## :checkered_flag: Definition of Done (DoD)
- [ ] 서버 측 파일 검증 로직이 SRS 명세를 충족하는가?
- [ ] `DOCUMENT` 테이블에 레코드가 의도대로 생성되는가?
- [ ] 에러 발생 시 상세 사유가 DB와 응답에 포함되는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-003 (DOCUMENT 테이블), #API-001 (Upload DTO)
- Blocks: #BE-PARSE-002 (HWPX 전처리), #BE-PARSE-003 (Word 전처리)
