---
name: Mock Data Task
about: 개발 시뮬레이션을 위한 Mock 데이터 및 API 작성
title: "[Mock] MOCK-007: 패널 라우팅 포스트백 등록 Mock 데이터"
labels: 'mock, foundation, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-007] 패널 라우팅 포스트백 등록 Mock 데이터
- 목적: 패널사와의 연동에 필요한 파라미터(e.g., `uid`, `status`)를 포함한 성공/실패/쿼터풀 리다이렉트용 URL 샘플을 정의한다.

## :link: References (Spec & Context)
- API 규격: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L662)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 라우팅 URL 3종 데이터 정의 (`success_url`, `screenout_url`, `quotafull_url`)

## :checkered_flag: Definition of Done (DoD)
- [ ] URL 규격 검증 통과

## :construction: Dependencies & Blockers
- Depends on: #API-012, #API-013
- Blocks: None
