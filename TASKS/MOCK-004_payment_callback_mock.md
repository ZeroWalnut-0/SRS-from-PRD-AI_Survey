---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-004: 결제 요청/콜백 Mock API 및 시뮬레이션 데이터 작성"
labels: 'feature, foundation, mock, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-004] 결제 요청/콜백 Mock API 및 시뮬레이션 데이터 작성
- 목적: 실제 PG사 연동 전 결제 퍼널과 Paywall UI를 테스트할 수 있도록 결제 세션 생성 및 콜백 응답을 시뮬레이션한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md), [`#6.1_#6`](#)
- 시퀀스 다이어그램: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.2`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `POST /api/v1/packages/{form_id}/payment` Mock 핸들러 작성 (테스트용 `payment_url` 반환)
- [ ] `POST /api/v1/payments/callback` Mock 핸들러 작성
- [ ] PG 성공/실패 시나리오별 응답 데이터셋 작성
- [ ] 결제 완료 후 대시보드 상태 변경을 위한 시뮬레이션 로직 구성
- [ ] Paywall 팝업용 모자이크 처리된 데이터맵 샘플 이미지(더미) 준비

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 성공 시뮬레이션
- Given: 사용자가 결제 버튼을 클릭함
- When: Mock 콜백 API가 호출됨
- Then: `payment_cleared`가 `true`로 변경되고 ZIP 다운로드 버튼이 활성화되어야 한다.

Scenario 2: 결제 실패/이탈 시뮬레이션
- Given: 결제창을 닫거나 잔액 부족이 발생함
- When: 실패 Mock 응답이 수신됨
- Then: 에러 메시지가 표시되고 다운로드가 차단된 상태가 유지되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 신뢰성: 실제 PG사(토스페이먼츠 등)에서 반환하는 JSON 필드 규격과 일치시켜야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 결제 세션 및 콜백 Mock API가 정의되었는가?
- [ ] 성공/실패 시나리오가 프론트엔드에서 테스트 가능한가?
- [ ] Paywall용 샘플 이미지 및 더미 엑셀 파일이 준비되었는가?

## :construction: Dependencies & Blockers
- Depends on: #API-007, #API-008 (결제 DTO)
- Blocks: #FE-PAY-001 (Paywall UI), #FE-PAY-002 (결제 연동)
