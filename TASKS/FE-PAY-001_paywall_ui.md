---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PAY-001: Paywall(결제 유도) 팝업 및 데이터 미리보기 UI 구현"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PAY-001] Paywall(결제 유도) 팝업 및 데이터 미리보기 UI 구현
- 목적: 조사 완료 후 산출물(ZIP) 다운로드를 유도하기 위해, 결제 필요성을 안내하고 일부 데이터를 블러(Blur) 처리하여 미리 보여주는 Paywall UI를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 비즈니스 정책: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3_REQ-FUNC-017`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `components/payment/PaywallModal.tsx` 컴포넌트 생성
- [ ] 데이터 미리보기 섹션 구현:
    - 엑셀 결과물의 상위 3개 행만 노출
    - 나머지 행 및 상세 지표는 블러 처리 또는 모자이크 이미지로 대체
- [ ] 산출물 패키지 구성 안내 (엑셀, 코드북, 원본 PDF, 클린 데이터)
- [ ] 결제 가격(예: 29,000원) 및 혜택 강조 문구 추가
- [ ] [결제하고 다운로드하기] 버튼 연동

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 유도 모달 노출
- Given: 설문 응답 수집이 완료되고 사용자가 결과 다운로드를 시도함
- When: 아직 결제되지 않은 상태(`payment_cleared: false`)인 경우
- Then: 즉시 Paywall 모달이 팝업되어야 한다.

Scenario 2: 데이터 블러 처리 확인
- Given: 미리보기 영역에 실제 수집 데이터 샘플이 로드됨
- When: 화면을 확인함
- Then: 상위 3행을 제외한 나머지 영역은 읽을 수 없도록 시각적 처리가 되어 있어야 한다.

## :gear: Technical & Non-Functional Constraints
- UX: 결제에 대한 거부감을 줄이기 위해 산출물의 가치를 시각적으로 명확히 전달한다.
- 보안: 프론트엔드에서의 블러 처리는 시각적 장치일 뿐이며, 실제 전체 데이터는 결제 완료 전까지 클라이언트에 전송하지 않는다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Paywall 모달이 디자인 시스템에 맞게 구현되었는가?
- [ ] 데이터 미리보기 및 블러 처리 효과가 적용되었는가?
- [ ] 결제 프로세스로 넘어가는 버튼이 정상 작동하는가?

## :construction: Dependencies & Blockers
- Depends on: #MOCK-004 (결제 Mock), #FE-FORM-006 (대시보드)
- Blocks: #FE-PAY-002 (결제 연동)
