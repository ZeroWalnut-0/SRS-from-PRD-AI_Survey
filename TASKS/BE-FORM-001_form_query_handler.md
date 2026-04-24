---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-FORM-001: 설문 폼 상세 조회 Route Handler 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-FORM-001] 설문 폼 상세 조회 Route Handler 구현
- 목적: 특정 `form_id`에 해당하는 설문 구조(JSON)와 메타데이터를 DB에서 조회하여 반환하는 API 핸들러를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-003_form_retrieval_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-003_form_retrieval_dto.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/forms/[form_id]/route.ts` (GET) 구현
- [ ] Prisma를 이용한 `ParsedForm` 레코드 단일 조회
- [ ] 응답 데이터 구성: `structure_schema`, `viral_watermark_url`, `question_count` 등
- [ ] 존재하지 않는 ID에 대한 404 처리 및 삭제된 폼(Zero-Retention)에 대한 예외 처리
- [ ] 유료 사용 여부에 따른 워터마크 노출 로직 검토

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 유효한 폼 조회
- Given: DB에 존재하는 `form_id`로 요청함
- When: GET 요청이 처리됨
- Then: 200 OK와 함께 파싱된 설문 JSON 구조가 반환되어야 한다.

Scenario 2: 삭제된 폼(24시간 경과) 접근
- Given: `expires_at`이 경과하여 이미 삭제된 레코드의 ID
- When: 조회를 시도함
- Then: 404 Not Found를 반환해야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 폼 조회 레이턴시 ≤ 300ms 달성.
- 보안: 설문 구조 외에 작성자의 개인정보가 유출되지 않도록 필터링한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-003` 규격에 맞는 응답을 반환하는가?
- [ ] DB 조회 로직이 정확하며 예외 처리가 완료되었는가?
- [ ] 워터마크 URL 등 메타데이터가 정확히 포함되는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM), #API-003 (Retrieval DTO)
- Blocks: #FE-FORM-001 (에디터 구현)
