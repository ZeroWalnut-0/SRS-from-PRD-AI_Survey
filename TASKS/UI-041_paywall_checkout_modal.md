---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] UI-041: Paywall 결제 유도 모달 UI 개발"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [UI-041] Paywall 결제 유도 모달 UI 개발
- 목적: 최종 ZIP 산출물 다운로드를 위해 사용자가 결제 버튼을 눌렀을 때, 가격 정책(9,900원) 및 혜택을 명확히 명시하고 결제 수단을 선택하게 하는 팝업 창을 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L837)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 상품명("설문 분석 데이터맵 패키지") 및 최종 결제 금액 표시
- [ ] Toss API 호출을 위한 '토스페이로 결제하기' 버튼 및 약관 동의 체크박스 배치

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 모달 오픈
- Given: 다운로드 버튼 클릭
- When: 미결제 상태인 경우
- Then: 결제 유도 모달이 팝업 애니메이션과 함께 중앙에 노출된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] ESC 키 입력 시 모달이 정상적으로 닫히는지(Cancel) 확인

## :construction: Dependencies & Blockers
- Depends on: #UI-001, #FE-PAY-001
- Blocks: None
