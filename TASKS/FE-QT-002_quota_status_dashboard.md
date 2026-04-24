---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-QT-002: 실시간 쿼터 충족 현황 대시보드 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-QT-002] 실시간 쿼터 충족 현황 대시보드 구현
- 목적: 조사가 진행됨에 따라 각 쿼터별 목표 대비 현재 응답 수집 현황을 시각적으로 모니터링할 수 있는 대시보드를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4_REQ-FUNC-018`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-011_quota_status_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-011_quota_status_dto.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `components/quota/QuotaDashboard.tsx` 컴포넌트 생성
- [ ] 쿼터 상태 데이터 페칭 로직 구현 (자동 갱신/Polling 기능 포함)
- [ ] 시각화 요소 구현:
    - 각 셀별 진행률 바 (Progress Bar)
    - 쿼터 달성(Full) 시 시각적 강조 (색상 변경 등)
- [ ] 전체 진행 상황 요약 정보 표시 (전체 목표 대비 총 응답 수)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 실시간 상태 반영
- Given: 조사가 진행되어 DB 카운트가 증가함
- When: 대시보드 화면이 열려 있거나 갱신됨
- Then: 별도의 새로고침 없이(또는 짧은 주기로) 바 차트의 길이가 늘어나야 한다.

Scenario 2: 쿼터 풀(Full) 상태 감지
- Given: 특정 연령대 쿼터가 100% 충족됨
- When: 대시보드를 확인함
- Then: 해당 셀의 상태가 '완료'로 표시되고 시각적으로 확연히 구분되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 다수의 사용자가 대시보드를 조회할 때 서버 부하를 최소화하기 위해 효율적인 폴링 전략을 사용한다.
- UX: 데이터 로딩 시 스켈레톤 UI를 사용하여 사용자 경험을 개선한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 쿼터별 진행률이 시각적으로 정확히 표현되는가?
- [ ] 실시간 데이터 갱신 로직이 연동되었는가?
- [ ] 쿼터 달성 시의 알림/표시 처리가 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #MOCK-006 (쿼터 Mock), #BE-QT-002 (상태 조회 구현)
- Blocks: None
