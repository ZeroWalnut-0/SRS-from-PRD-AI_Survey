---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-004: 설문 응답 제출 API 계약 정의"
labels: 'feature, foundation, api, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [API-004] 설문 응답 제출 API 계약 정의
- 목적: 응답자가 작성한 설문 데이터를 수집하고 저장하기 위한 API의 요청/응답 규격 및 DTO를 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `POST /api/v1/forms/{form_id}/responses`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 DTO 정의: `{ resp_id: string, user_agent: string, raw_record: JSON, quota_group?: JSON }`
- [ ] 응답 DTO 정의: `{ resp_id: string, status: string, redirect_url?: string }`
- [ ] 에러 코드 정의:
    - 400: 유효하지 않은 응답 형식
    - 429: 쿼터 도달로 인한 제출 차단 (필요 시)
- [ ] TypeScript 인터페이스 정의 (`types/api/responses.ts`)
- [ ] 응답 무결성 검증을 위한 Zod 스키마 작성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 설문 응답 성공적 제출
- Given: 유효한 응답 데이터가 준비됨
- When: `POST /api/v1/forms/{form_id}/responses`로 요청함
- Then: 201 Created와 함께 생성된 `resp_id`를 반환해야 한다.

Scenario 2: 필수 문항 누락 시 에러
- Given: 필수 응답 항목이 누락된 데이터가 주어짐
- When: 제출을 요청함
- Then: 400 Bad Request와 함께 누락된 항목 정보를 반환해야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: p95 응답 시간 ≤ 1,000ms (REQ-NF-001)
- 보안: 응답자의 IP는 서버 측에서 해싱 처리되므로 DTO에 직접 포함하지 않는다.

## :checkered_flag: Definition of Done (DoD)
- [ ] API 요청/응답 DTO가 SRS 규격대로 정의되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?
- [ ] 에러 케이스 명세가 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-005 (RESPONSE 테이블)
- Blocks: #BE-FORM-004 (응답 제출 구현), #FE-FORM-007 (모바일 폼 렌더링)
