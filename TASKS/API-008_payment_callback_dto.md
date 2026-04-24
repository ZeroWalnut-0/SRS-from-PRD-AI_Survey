---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-008: 결제 콜백 API 계약 정의"
labels: 'feature, foundation, api, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [API-008] 결제 콜백 API 계약 정의
- 목적: PG사로부터 결제 완료 결과를 수신(Webhook 또는 Redirect 콜백)하여 결제 상태를 업데이트하기 위한 API 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서르 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `POST /api/v1/payments/callback`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 DTO 정의: `{ session_id: string, status: string, pg_transaction_id: string, amount: number }` (PG사 규격 준수)
- [ ] 응답 DTO 정의: `{ result: string, message?: string }`
- [ ] 결제 검증(Verification) 프로세스 명세 (금액 대조 등)
- [ ] 에러 코드 정의:
    - 400: 잘못된 서명, 금액 불일치, 이미 처리된 트랜잭션
- [ ] TypeScript 인터페이스 정의 (`types/api/payments.ts`)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 성공 콜백 처리
- Given: PG사로부터 결제 성공 신호가 수신됨
- When: 서버에서 금액 검증 및 서명 확인을 수행함
- Then: DB의 `payment_cleared` 상태를 `true`로 갱신하고 200 OK를 반환해야 한다.

Scenario 2: 위조된 결제 요청 감지
- Given: 요청된 금액과 실제 결제 금액이 다른 콜백이 수신됨
- When: 검증 로직을 실행함
- Then: 400 Bad Request를 반환하고 로그(Audit Log)를 남겨야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: PG사의 IP 화이트리스팅 또는 서명 검증(HMAC 등)을 반드시 수행한다.
- 무결성: 멱등성(Idempotency)을 보장하여 중복 콜백 처리를 방지한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 결제 콜백 수신용 DTO가 PG사 규격에 맞게 정의되었는가?
- [ ] 서버 측 검증 로직에 대한 명세가 포함되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-006 (ZIP_DATAMAP 테이블), #DB-010 (AUDIT_LOG)
- Blocks: #BE-PAY-002 (결제 콜백 구현), #BE-PAY-003 (ZIP 산출물 생성)
