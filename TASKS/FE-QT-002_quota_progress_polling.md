---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-QT-002: 쿼터 진행률 데이터 실시간 폴링 및 차트/게이지 데이터 매핑"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-QT-002] 쿼터 진행률 데이터 실시간 폴링 및 차트 데이터 매핑
- 목적: 설문이 진행되는 동안 각 쿼터 셀별 수집 현황을 실시간으로 갱신하여 대시보드에 시각화한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L514)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] SWR 또는 React Query를 활용한 10초 주기 실시간 데이터 폴링 구현
- [ ] 수신된 셀별 데이터(`current_count / target_count`)를 원형 프로그레스 바에 매핑

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 실시간 데이터 갱신
- Given: 쿼터 모니터링 페이지 오픈 중
- When: 새로운 응답이 적재되어 서버 카운트가 올라감
- Then: 새로고침 없이 10초 이내에 화면의 게이지가 증가한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 백그라운드 탭 전환 시 불필요한 폴링 중단 기능 검증

## :construction: Dependencies & Blockers
- Depends on: #FE-QT-001, #API-011
- Blocks: None
