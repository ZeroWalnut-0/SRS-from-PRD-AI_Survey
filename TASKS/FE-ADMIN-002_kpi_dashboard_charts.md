---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-ADMIN-002: 전체 통계 API 연동 및 KPI 대시보드 데이터 바인딩"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-ADMIN-002] 전체 통계 API 연동 및 KPI 대시보드 데이터 바인딩
- 목적: 시스템 전반의 주요 성과 지표(KPI: 누적 결제 금액, 가입자 수, 설문 전환율 등)를 시각적 차트로 구성해 운영진에게 대시보드로 노출한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.8`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L643)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `Recharts` 라이브러리를 활용한 라인 차트, 바 차트 구성
- [ ] 백엔드 API(`GET /api/v1/admin/stats`) 연동을 통한 데이터 로드

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 차트 렌더링
- Given: 대시보드 페이지 로드
- When: 데이터 패칭 완료
- Then: 최근 30일간의 일별 매출 추이가 꺾은선 그래프로 매핑되어 출력된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 데이터 빈값(Null)일 경우 빈 공간 처리 또는 0 표기 여부

## :construction: Dependencies & Blockers
- Depends on: #FE-ADMIN-001, #API-016
- Blocks: None
