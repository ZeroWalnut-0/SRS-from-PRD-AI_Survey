---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PAY-002: PG사(토스페이먼츠) 결제 SDK 연동 및 팝업 구현"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PAY-002] PG사(토스페이먼츠) 결제 SDK 연동 및 팝업 구현
- 목적: 토스페이먼츠 결제창을 연동하여 사용자가 신용카드, 계좌이체 등으로 실제 결제를 진행할 수 있는 기능을 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 가이드: [토스페이먼츠 개발자 센터](https://docs.tosspayments.com/)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 토스페이먼츠 클라이언트 SDK 설치 및 초기화
- [ ] `components/payment/PaymentButton.tsx` 구현:
    - 클릭 시 서버 API(`API-007`)를 호출하여 주문 정보(OrderId) 수신
    - 토스페이먼츠 결제창(`requestPayment`) 호출
- [ ] 결제 성공/실패 시의 Redirect 경로 설정 (`successUrl`, `failUrl`)
- [ ] 결제 창 로딩 중 상태 처리 (Loading Spinner)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제창 호출 성공
- Given: Paywall 모달에서 결제 버튼을 클릭함
- When: SDK가 정상 작동함
- Then: 토스페이먼츠 표준 결제창(모달 또는 팝업)이 화면에 표시되어야 한다.

Scenario 2: 결제 중단/실패 처리
- Given: 사용자가 결제창을 임의로 닫거나 카드 승인이 거절됨
- When: `failUrl`로 리다이렉트되거나 SDK 에러가 반환됨
- Then: 적절한 안내 메시지를 표시하고 다시 결제할 수 있는 상태로 복구되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 클라이언트 측 결제 정보는 최소한으로 유지하며, 최종 검증은 반드시 서버에서 수행한다.
- 가용성: 모바일 환경에서의 결제창 팝업/리다이렉트 흐름을 최적화한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 토스페이먼츠 결제창이 정상적으로 호출되는가?
- [ ] 주문 정보 연동(`API-007`)이 완료되었는가?
- [ ] 성공/실패 시의 페이지 전환 로직이 구현되었는가?

## :construction: Dependencies & Blockers
- Depends on: #API-007 (결제 요청 DTO), #FE-PAY-001 (Paywall UI)
- Blocks: #BE-PAY-002 (결제 콜백 처리)
