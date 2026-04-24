---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-002: Document 파싱 상태 조회 API 계약 정의"
labels: 'feature, foundation, api, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [API-002] Document 파싱 상태 조회 API 계약 정의
- 목적: 업로드된 문서의 파싱 진행 상태 및 성공 여부를 확인하기 위한 API 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `GET /api/v1/documents/{doc_id}/status`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 파라미터 정의: `doc_id` (Path variable)
- [ ] 응답 DTO 정의: `{ doc_id: string, status: DocumentStatus, parsed_success: boolean, form_id?: string, error_code?: string }`
- [ ] 에러 코드 정의:
    - 404: 존재하지 않는 `doc_id`
- [ ] TypeScript 인터페이스 정의 (`types/api/documents.ts`)
- [ ] 클라이언트 폴링(Polling) 로직을 위한 응답 구조 최적화

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 파싱 완료 상태 조회
- Given: 파싱이 성공적으로 완료된 `doc_id`가 존재함
- When: 상태 조회를 요청함
- Then: `status: 'COMPLETED'`, `parsed_success: true`, 그리고 생성된 `form_id`를 반환해야 한다.

Scenario 2: 파싱 진행 중 조회
- Given: 현재 파서가 작동 중인 `doc_id`가 존재함
- When: 상태 조회를 요청함
- Then: `status: 'PARSING'` 상태를 반환해야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 상태 조회 요청에 대한 응답 시간은 200ms 이내여야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] API 응답 DTO에 `form_id`와 `status`가 포함되었는가?
- [ ] 존재하지 않는 ID에 대한 404 에러 명세가 포함되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #API-001 (Upload DTO), #DB-003 (DOCUMENT 테이블)
- Blocks: #BE-PARSE-008 (상태 조회 구현), #MOCK-002 (Mock 데이터)
