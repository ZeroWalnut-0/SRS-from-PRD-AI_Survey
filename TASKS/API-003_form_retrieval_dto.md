---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-003: 설문 폼 조회 API 계약 정의"
labels: 'feature, foundation, api, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [API-003] 설문 폼 조회 API 계약 정의
- 목적: 파싱 완료된 설문 폼의 상세 구조(스키마) 및 메타데이터를 조회하기 위한 API 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `GET /api/v1/forms/{form_id}`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 파라미터 정의: `form_id` (Path variable)
- [ ] 응답 DTO 정의: `{ form_id: string, structure_schema: JSON, viral_watermark_url: string, question_count: number }`
- [ ] 설문 구조화를 위한 `structure_schema` 상세 규격 정의 (Zod 또는 JSON Schema)
- [ ] 에러 코드 정의:
    - 404: 존재하지 않는 `form_id`
- [ ] TypeScript 인터페이스 정의 (`types/api/forms.ts`)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 설문 폼 상세 조회 성공
- Given: 유효한 `form_id`가 존재함
- When: 폼 조회를 요청함
- Then: 200 OK와 함께 파싱된 문항 구조(`structure_schema`)와 워터마크 URL을 반환해야 한다.

Scenario 2: 삭제된 폼 조회 시도
- Given: 24시간이 경과하여 삭제된 `form_id`가 주어짐
- When: 조회를 요청함
- Then: 404 Not Found를 반환해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: `structure_schema` 내에 개인정보나 민감 데이터가 포함되지 않도록 검증한다.
- 성능: 폼 조회 레이턴시 ≤ 300ms 달성.

## :checkered_flag: Definition of Done (DoD)
- [ ] 응답 DTO에 `structure_schema`가 포함되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?
- [ ] 404 에러 케이스 명세가 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM 테이블)
- Blocks: #BE-FORM-001 (폼 조회 구현), #FE-FORM-001 (폼 에디터 구현)
