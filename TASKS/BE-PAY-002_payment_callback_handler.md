---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-002: 결제 완료 콜백 및 최종 승인 처리 핸들러 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-002] 결제 완료 콜백 및 최종 승인 처리 핸들러 구현
- 목적: PG사(토스페이먼츠)로부터 수신된 결제 완료 신호를 검증하고, 서버 간 통신을 통해 최종 승인을 완료한 뒤 DB의 결제 상태를 업데이트한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 가이드: [토스페이먼츠 결제 승인 API](https://docs.tosspayments.com/reference#%EA%B2%B0%EC%A0%9C-%EC%8A%B9%EC%9D%B8)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/payments/callback/route.ts` 구현
- [ ] 토스페이먼츠 API 연동 (Secret Key 기반 호출)
- [ ] 결제 승인 검증 프로세스:
    - `paymentKey`, `orderId`, `amount` 대조 확인
    - PG사 승인 API (`/v1/payments/confirm`) 호출
- [ ] DB 상태 갱신: `ZIP_DATAMAP.payment_cleared = true`, `pg_transaction_id` 저장
- [ ] `AUDIT_LOG` 기록 (결제 성공 여부 및 트랜잭션 정보)
- [ ] 산출물 생성 큐(Queue) 또는 비동기 작업(`BE-PAY-003`) 트리거

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 최종 승인 성공
- Given: PG사로부터 유효한 결제 완료 파라미터가 수신됨
- When: 서버에서 승인 API를 호출하고 성공 응답을 받음
- Then: DB의 결제 상태가 즉시 업데이트되고 사용자에게 성공 응답을 반환해야 한다.

Scenario 2: 금액 위변조 감지
- Given: 요청된 주문 금액과 PG사에서 승인하려는 금액이 다름
- When: 검증 로직이 실행됨
- Then: 승인을 중단하고 400 에러를 반환하며 부정 결제 시도로 로그를 기록해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: Secret Key는 서버 측 환경 변수(`TOSS_SECRET_KEY`)로 엄격히 관리한다.
- 무결성: 멱등성을 보장하여 중복 콜백 발생 시에도 안전하게 처리한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-008` 규격에 맞는 콜백 처리가 완료되었는가?
- [ ] PG사 서버 간 승인 통신이 정상 작동하는가?
- [ ] DB 상태 갱신 및 에러 핸들링이 완벽한가?

## :construction: Dependencies & Blockers
- Depends on: #DB-006 (ZIP_DATAMAP), #API-008 (Payment Callback DTO)
- Blocks: #BE-PAY-003 (ZIP 파일 생성), #FE-PAY-003 (성공 화면)
