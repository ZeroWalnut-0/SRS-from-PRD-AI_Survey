---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-001: 문서 업로드 성공/실패 Mock API 및 샘플 데이터 작성"
labels: 'feature, foundation, mock, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-001] 문서 업로드 성공/실패 Mock API 및 샘플 데이터 작성
- 목적: 백엔드 로직이 완성되기 전 프론트엔드에서 업로드 기능을 테스트할 수 있도록 Mock 응답과 테스트용 샘플 파일(HWPX, Word, PDF)을 준비한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 태스크 리스트: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/06_TASK_LIST.md#MOCK-001`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/06_TASK_LIST.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 테스트용 샘플 파일 확보: `sample.hwpx`, `sample.docx`, `sample.pdf` (50문항 이내 구성)
- [ ] 에러 케이스용 샘플 파일 확보: 손상된 파일, 암호화된 PDF 등
- [ ] `POST /api/v1/documents/upload`에 대한 Mock 핸들러 작성
- [ ] 상태별 Mock 응답 정의:
    - 성공: `{ "doc_id": "mock-uuid-123", "status": "PARSING" }`
    - 실패(한도초과): `{ "error_code": "RATE_LIMIT_EXCEEDED", "message": "일일 한도 초과" }`
- [ ] 프론트엔드에서 활용 가능한 Mock Service Worker(MSW) 또는 Next.js API Route 기반 Mock 구성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 성공 케이스 Mock 테스트
- Given: 프론트엔드에서 샘플 파일을 업로드함
- When: Mock API가 호출됨
- Then: 200 OK와 함께 미리 정의된 `doc_id`가 반환되어야 한다.

Scenario 2: 에러 케이스 Mock 테스트
- Given: 업로드 지연 또는 실패 상황을 시뮬레이션함
- When: Mock API가 호출됨
- Then: 429 또는 400 에러와 함께 지정된 에러 메시지가 화면에 표시되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 유지보수: 실제 API 연동 시 환경 변수 조작만으로 Mock을 끌 수 있어야 한다.
- 데이터: 샘플 데이터는 실제 설문 문항의 형태(객관식, 주관식 등)를 골고루 포함해야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 테스트용 3종(HWPX, Word, PDF) 샘플 파일이 준비되었는가?
- [ ] 성공/실패 시나리오에 대한 Mock 응답이 구성되었는가?
- [ ] 프론트엔드 코드에서 Mock 데이터를 성공적으로 가져올 수 있는가?

## :construction: Dependencies & Blockers
- Depends on: #API-001 (Upload DTO)
- Blocks: #FE-PARSE-001 (업로드 UI 구현)
