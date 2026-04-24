---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-008: 파싱 상태 조회 Route Handler 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-008] 파싱 상태 조회 Route Handler 구현
- 목적: 클라이언트의 폴링 요청에 응답하여 특정 문서의 현재 파싱 상태(`PENDING`, `PARSING`, `COMPLETED`, `FAILED`)를 반환하는 API를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-004`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-002_document_status_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-002_document_status_dto.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/documents/[doc_id]/status/route.ts` 구현
- [ ] Path 파라미터(`doc_id`)를 통한 DB 조회 로직 구현
- [ ] 응답 데이터 구성:
    - `doc_id`, `status`, `parsed_success`
    - 완료 시 `form_id` 포함
    - 실패 시 `error_code` 포함
- [ ] 존재하지 않는 ID 요청 시 404 에러 처리

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 진행 중 상태 조회 성공
- Given: 파싱이 진행 중인 `doc_id`가 DB에 존재함
- When: `GET /api/v1/documents/{doc_id}/status` 요청을 보냄
- Then: 200 OK와 함께 `status: 'PARSING'` 응답을 받아야 한다.

Scenario 2: 완료 상태 조회 시 form_id 확인
- Given: 파싱이 완료된 `doc_id`가 존재함
- When: 상태 조회를 요청함
- Then: `status: 'COMPLETED'`와 함께 유효한 `form_id`를 반환해야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: DB 단일 조회 요청이므로 레이턴시 ≤ 100ms 달성.
- 가용성: 폴링 부하를 고려하여 효율적인 쿼리를 작성한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-002` 규격에 맞는 응답을 반환하는가?
- [ ] `form_id` 연동 조회가 정확히 이루어지는가?
- [ ] 404 등 에러 핸들링이 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-003 (DOCUMENT), #API-002 (Status DTO)
- Blocks: #FE-PARSE-002 (로딩 UI 연동)
