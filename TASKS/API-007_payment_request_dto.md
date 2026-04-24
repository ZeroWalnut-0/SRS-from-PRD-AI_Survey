---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-007: 결제 요청 API 계약 정의"
labels: 'feature, foundation, api, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [API-007] 결제 요청 API 계약 정의
- 목적: 4종 산출물(ZIP) 다운로드를 위한 결제 세션을 생성하고, PG사(토스페이먼츠 등) 모듈 호출에 필요한 정보를 반환하는 API 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `POST /api/v1/packages/{form_id}/payment`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 DTO 정의: `{ form_id: string, payment_method: string, amount?: number }`
- [ ] 응답 DTO 정의: `{ payment_url: string, session_id: string, order_id: string }`
- [ ] 결제 세션 생성을 위한 PG사 연동 규약 확인 (SDK 또는 API)
- [ ] 에러 코드 정의:
    - 400: 유효하지 않은 결제 요청, 금액 불일치
- [ ] TypeScript 인터페이스 정의 (`types/api/payments.ts`)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 세션 생성 성공
- Given: 조사가 완료된 `form_id`가 존재함
- When: 결제 요청 API를 호출함
- Then: 200 OK와 함께 PG사 결제창 호출에 필요한 `payment_url` 또는 세션 정보를 반환해야 한다.

Scenario 2: 중복 결제 시도 방지
- Given: 이미 결제가 완료된 `form_id`가 주어짐
- When: 다시 결제를 요청함
- Then: 적절한 상태 코드와 함께 이미 결제된 항목임을 안내해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 결제 금액 및 주문 정보는 서버 측에서 생성 및 검증하여 위변조를 방지한다.
- 성능: 결제 세션 생성 및 응답 레이턴시 ≤ 1,000ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] 결제 요청용 DTO가 SRS 규격대로 정의되었는가?
- [ ] PG사 SDK 연동을 위한 필수 필드가 포함되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-006 (ZIP_DATAMAP 테이블)
- Blocks: #BE-PAY-001 (결제 요청 구현), #FE-PAY-002 (결제 모듈 연동)
