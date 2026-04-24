---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-FORM-002: 설문 폼 수정 및 저장 Route Handler 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-FORM-002] 설문 폼 수정 및 저장 Route Handler 구현
- 목적: 사용자가 에디터에서 수정한 설문 구조(JSON)를 수신하여 DB의 `PARSED_FORM` 레코드를 갱신하는 API 핸들러를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3.6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-005_form_edit_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-005_form_edit_dto.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/forms/[form_id]/route.ts` (PUT) 구현
- [ ] 요청 본문(`structure_schema`)의 유효성 검증 (Zod 사용)
- [ ] `ParsedForm` 테이블의 `structure_schema` 필드 업데이트
- [ ] `updated_at` 타임스탬프 갱신
- [ ] 문항 수(`question_count`) 재계산 및 업데이트
- [ ] 수정 권한 확인 (소유자 체크 등)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 설문 수정 성공
- Given: 수정된 설문 문항 JSON 데이터가 준비됨
- When: PUT 요청을 전송함
- Then: 200 OK와 함께 수정 시각을 반환하고, 이후 조회 시 수정된 내용이 반영되어야 한다.

Scenario 2: 유효하지 않은 스키마 전송 시 차단
- Given: 문항 ID가 중복되거나 필수 필드가 누락된 JSON 데이터
- When: 수정을 시도함
- Then: 400 Bad Request를 반환하고 DB 업데이트를 차단해야 한다.

## :gear: Technical & Non-Functional Constraints
- 데이터 무결성: 업데이트 중 에러 발생 시 기존 데이터가 유지되도록 트랜잭션을 적용한다.
- 성능: 수정 요청 처리 레이턴시 ≤ 500ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-005` 규격에 맞는 요청/응답 처리가 완료되었는가?
- [ ] 서버 측 JSON 스키마 유효성 검사가 작동하는가?
- [ ] DB 레코드가 정확히 갱신되는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM), #API-005 (Edit DTO)
- Blocks: #FE-FORM-002 (에디터 수정 연동)
