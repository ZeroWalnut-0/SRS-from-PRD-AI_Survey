---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Mon] NFR-MON-005: 운영자 대시보드 KPI 집계 화면 구현"
labels: 'infrastructure, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-MON-005] 운영자 대시보드 KPI 집계 화면 구현
- 목적: 파싱 완료율, 결제 전환율, 쿼터 상태 등 핵심 비즈니스 지표를 운영자가 시각적으로 파악할 수 있는 전용 관리 도구를 구현한다.

## :link: References (Spec & Context)
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.8_REQ-NF-033~037`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(admin)/dashboard/page.tsx` 운영자 전용 페이지 구현
- [ ] 주요 KPI 카드 UI 구현 (총 파싱 수, 결제 전환율 p95 레이턴시 등)
- [ ] 시간 흐름에 따른 트렌드 차트(Line Chart) 연동
- [ ] 운영자 권한(`BE-RL-002`) 체크 미들웨어 적용
- [ ] 실시간 쿼터 초과 알림 로그 리스트 표시

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 운영자 계정으로 로그인함
- When: 운영자 대시보드에 접속함
- Then: 서비스 전체의 핵심 지표가 시각화되어 노출되어야 하며, 데이터는 1분 이내의 최신성을 유지해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 일반 사용자가 해당 URL에 접근 시 403 Forbidden 처리를 철저히 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 운영에 필요한 핵심 지표가 모두 화면에 포함되었는가?
- [ ] 권한 제어가 정상적으로 작동하는가?
- [ ] 대량 데이터 조회 시 대시보드 로딩 속도가 3초 이내인가?

## :construction: Dependencies & Blockers
- Depends on: #NFR-MON-003, #BE-RL-002
- Blocks: None
