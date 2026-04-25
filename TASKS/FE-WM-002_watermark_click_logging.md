---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-WM-002: 워터마크 클릭 시 GA4 이벤트 로깅 구현"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-WM-002] 워터마크 클릭 시 GA4 이벤트 로깅 구현
- 목적: 바이럴 워터마크 배너의 클릭 효율을 측정하여 신규 유입 깔때기(Funnel) 지표를 수집한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L522)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `gtag` 또는 GA4 React Wrapper 모듈 연동
- [ ] 워터마크 링크 클릭 이벤트 리스너 추가

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 배너 클릭
- Given: 무료 설문 하단 배너가 활성화됨
- When: 배너를 클릭하여 랜딩 페이지로 이동함
- Then: GA4 콘솔의 실시간(Real-time) 이벤트에 `click_watermark`가 기록된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 구글 애널리틱스 디버그 뷰(DebugView) 정상 전송 검증

## :construction: Dependencies & Blockers
- Depends on: #FE-WM-001
- Blocks: None
