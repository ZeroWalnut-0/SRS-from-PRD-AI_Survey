---
name: UI/UX Task
about: 관리자 통계 시각화 화면 구현
title: "[UI] FE-ADMIN-002: 시스템 결제 및 파싱 통계 시각화 대시보드 뷰 구현"
labels: 'frontend, admin, ui'
assignees: ''
---

## :dart: Summary
- 목적: 백엔드에서 제공하는 통계 데이터를 운영자가 직관적으로 이해할 수 있도록 차트와 지표 카드로 시각화한다.

## :link: References (Spec & Context)
- SRS 문서: `§4.2.8 REQ-NF-033 ~ 037`
- 관련 API: `API-016`, `BE-ADMIN-001`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 핵심 지표 카드(Metric Cards) 구현:
    - 총 매출, 활성 문서 수, 평균 파싱 시간, 결제 전환율
- [ ] 시계열 차트 구현 (Recharts 또는 유사 라이브러리):
    - 일별 업로드 수 vs 결제 완료 수 추이 그래프
- [ ] 데이터 테이블 구현:
    - 최근 발생한 결제 내역 및 파싱 실패 로그 리스트

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 통계 데이터 렌더링
- Given: `BE-ADMIN-001`을 통해 통계 데이터가 응답됨
- When: 관리자 통계 페이지 로드 시
- Then: 지표 카드가 실제 수치와 일치하게 노출되고 차트가 정상적으로 그려져야 한다.

## :gear: Technical & Non-Functional Constraints
- UX: 데이터 로딩 시 스켈레톤 UI를 적용하여 답답함을 최소화함.
- 접근성: 차트 데이터의 가독성을 위해 명확한 범례와 툴팁 제공.

## :checkered_flag: Definition of Done (DoD)
- [ ] 지표 카드와 차트가 정상적으로 렌더링되는가?
- [ ] 실시간 데이터(또는 새로고침) 연동이 원활한가?

## :construction: Dependencies & Blockers
- Depends on: `FE-ADMIN-001`, `BE-ADMIN-001`
- Blocks: None
