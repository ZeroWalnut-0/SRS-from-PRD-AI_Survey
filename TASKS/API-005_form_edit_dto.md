---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-005: 설문 폼 수정 API 계약 정의"
labels: 'feature, foundation, api, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [API-005] 설문 폼 수정 API 계약 정의
- 목적: 파싱된 설문 구조를 사용자가 수동으로 수정(문항 추가/삭제/순서 변경 등)하기 위한 API 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3.6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `PUT /api/v1/forms/{form_id}`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 DTO 정의: `{ structure_schema: JSON }`
- [ ] 응답 DTO 정의: `{ form_id: string, updated_at: string }`
- [ ] 서버 측 스키마 유효성 검증 로직 명세 (순환 참조 체크 등)
- [ ] 에러 코드 정의:
    - 400: 잘못된 스키마 구조, 데이터 타입 불일치
- [ ] TypeScript 인터페이스 정의 (`types/api/forms.ts`)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 설문 문항 수정 성공
- Given: 수정된 `structure_schema`가 준비됨
- When: `PUT /api/v1/forms/{form_id}`로 요청함
- Then: 200 OK와 함께 수정된 시각을 반환해야 하며, DB에 즉시 반영되어야 한다.

Scenario 2: 잘못된 스키마 형식 제출
- Given: 필수 필드가 누락된 JSON 스키마가 주어짐
- When: 수정을 요청함
- Then: 400 Bad Request와 함께 유효성 검사 에러 목록을 반환해야 한다.

## :gear: Technical & Non-Functional Constraints
- 원자성: 스키마 업데이트 중 에러 발생 시 기존 데이터가 유지되도록 트랜잭션을 고려한다.
- 성능: 수정 요청 처리 레이턴시 ≤ 500ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] 수정용 요청/응답 DTO가 정의되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?
- [ ] 유효성 검사 실패 케이스에 대한 명세가 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM 테이블)
- Blocks: #BE-FORM-002 (폼 수정 구현), #FE-FORM-001 (폼 에디터 구현)
