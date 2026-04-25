---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] UI-051: AI Data Bouncer(휴지통) 대시보드 테이블 UI 개발"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [UI-051] AI Data Bouncer 대시보드 테이블 UI 개발
- 목적: 불성실 응답(Speed Trap, Straightlining)으로 분류되어 필터링된 데이터 목록을 표(Table) 형태로 시각화하고 수동 복원 기능을 연결한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L837)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 테이블 헤더: 응답자 ID, 탐지 사유, 응답 시간, 제외 일시, 액션
- [ ] 필터링 위젯: 사유별(Speed/Straight) 다중 선택 필터 구현

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 제외 사유 태그
- Given: Speed Trap으로 걸러진 행
- When: 화면 로드
- Then: 주황색 뱃지(`Speed Trap`)가 상태 열에 명확히 표시된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 체크박스를 통한 다중 선택 및 일괄 복원 UI 동작 검증

## :construction: Dependencies & Blockers
- Depends on: #UI-050, #FE-FORM-008
- Blocks: None
