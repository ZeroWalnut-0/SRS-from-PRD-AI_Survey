---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-001: 결제 요청 세션 생성 및 OrderID 발급 핸들러 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-001] 결제 요청 세션 생성 및 OrderID 발급 핸들러 구현
- 목적: 프론트엔드에서 결제 시작 시, 서버 측에서 고유한 주문 번호(OrderID)를 생성하고 PG사에 전달할 기초 정보를 준비하여 응답한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.4_ZIP_DATAMAP`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/packages/[form_id]/payment/route.ts` 구현
- [ ] 주문 정보 생성 로직:
    - UUID 기반 고유 `order_id` 생성
    - 상품 명칭(예: "[AI Survey] {설문제목} 데이터 패키지") 확정
    - 결제 금액 확정 (현재 고정가 29,000원)
- [ ] `ZIP_DATAMAP` 레코드 생성 또는 업데이트 (`payment_cleared = false`)
- [ ] PG사 연동에 필요한 클라이언트 키 및 주문 데이터 응답

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 세션 생성 성공
- Given: 설문 수집이 완료된 `form_id`로 요청함
- When: 서버 핸들러가 실행됨
- Then: DB에 미결제 상태의 주문 레코드가 생성되고, 200 OK와 함께 `order_id`가 반환되어야 한다.

Scenario 2: 중복 결제 시도 감지
- Given: 이미 결제 완료된 건에 대해 다시 세션을 생성하려고 함
- When: 검증 로직이 실행됨
- Then: 400 Bad Request와 함께 이미 결제된 상품임을 안내해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 결제 금액(`amount`)은 반드시 서버 측 환경 변수 또는 DB 설정을 참조하여 클라이언트 변조를 방지한다.
- 성능: 세션 생성 레이턴시 ≤ 300ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-007` 규격에 맞는 주문 응답이 반환되는가?
- [ ] DB에 주문 내역이 정확히 기록되는가?
- [ ] 서버 측 결제 금액 검증 로직이 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-006 (ZIP_DATAMAP), #API-007 (Payment Request DTO)
- Blocks: #FE-PAY-002 (SDK 연동)
