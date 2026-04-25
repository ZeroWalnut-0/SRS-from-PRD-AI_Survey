---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-002: POST /api/v1/payments/callback 결제 승인 처리"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-002] PG 결제 콜백 Route Handler 구현
- 목적: 토스페이먼츠로부터 결제 승인 완료 Webhook 또는 Redirect 응답을 받아, 최종 결제 상태를 확정하고 다운로드 권한을 부여한다.

## :link: References (Spec & Context)
- 기술 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L461)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 전달받은 `paymentKey`, `orderId`, `amount` 검증 로직 구현
- [ ] `ZIP_DATAMAP.payment_cleared = true` 및 `pg_transaction_id` 저장

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 승인 완료
- Given: PG사 성공 페이로드 수신
- When: 금액 검증 일치
- Then: `payment_cleared` 상태가 `true`로 변경된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 결제 실패 시 `payment_cleared`가 `false`로 유지되는지 검증

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-001, #API-008
- Blocks: #BE-PAY-003
