---
name: Mock Data Task
about: 개발 시뮬레이션을 위한 Mock 데이터 및 API 작성
title: "[Mock] MOCK-006: 쿼터 설정/조회 Mock 데이터 작성"
labels: 'mock, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-006] 쿼터 설정/조회 Mock 데이터 작성
- 목적: 교차 쿼터(성별 2개 x 연령대 5개 x 지역 3개 = 30개 셀)를 구성하는 복잡한 JSON 매트릭스 구조 샘플을 작성하여 프론트엔드 쿼터 대시보드 연동을 돕는다.

## :link: References (Spec & Context)
- API 규격: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L662)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `quota_matrix` 구조 설계 및 30개 셀의 `target_count` 임의 할당
- [ ] `GET /api/v1/quotas/{quota_id}/status` API용 진행률 업데이트 Mock 데이터 추가

## :checkered_flag: Definition of Done (DoD)
- [ ] 쿼터 달성률 게이지 UI에 데이터 바인딩 정상 작동

## :construction: Dependencies & Blockers
- Depends on: #API-010, #API-011
- Blocks: #FE-QT-001, #FE-QT-002
