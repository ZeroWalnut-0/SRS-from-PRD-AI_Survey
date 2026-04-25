---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-FORM-002: 설문 폼 수정(커스텀 빌드) API 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-FORM-002] 설문 폼 수정 API (`PUT /api/v1/forms/{form_id}`)
- 목적: 사용자가 에디터를 통해 문항을 추가/삭제/변경하거나 스킵 로직을 변경한 스키마를 서버 측에서 유효성 검증한 뒤 DB를 갱신한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L493)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L742)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L715)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js API Route Handler `PUT /api/v1/forms/[form_id]/route.ts` 생성
- [ ] Request Body 유효성 검증 (Zod 라이브러리 기반의 `structure_schema` 검증 스키마 설계)
- [ ] 폼 수정을 통한 문항 수 변동 시 `question_count` 재계산 및 `updated_at` 갱신 로직 적용
- [ ] 데이터베이스 트랜잭션 처리 (낙관적 락 적용 또는 원자적 Update)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상적인 폼 스키마 수정
- Given: 정상적인 형태의 JSON 문항 스키마가 Body에 주어짐
- When: `/api/v1/forms/{form_id}`에 PUT 요청을 전송함
- Then: DB의 `structure_schema`가 갱신되고 200 OK를 반환한다.

Scenario 2: 문항 스키마 규격 위반
- Given: 필수 키값이 누락되거나 규격에 맞지 않는 데이터가 주어짐
- When: `/api/v1/forms/{form_id}`에 PUT 요청을 전송함
- Then: 400 Bad Request와 함께 세부 검증 에러 메시지를 반환한다.

## :gear: Technical & Non-Functional Constraints
- 안정성: 데이터 구조 파손 방지를 위해 트랜잭션 롤백 처리 필수
- 보안: 수정 요청에 대한 CSRF 및 비인가 접근 차단(유저 세션 검증)

## :checkered_flag: Definition of Done (DoD)
- [ ] 모든 Acceptance Criteria를 충족하는가?
- [ ] 수정 로직 적용 후 JSON 스키마 무손실 저장이 검증되었는가?
- [ ] Linter 정적 분석 통과 및 API DTO 매핑 확인

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM 스키마), #API-005 (Form 커스텀 빌드 계약)
- Blocks: #FE-FORM-002, #FE-FORM-003
