---
name: Mock Data Task
about: 개발 시뮬레이션을 위한 Mock 데이터 및 API 작성
title: "[Mock] MOCK-003: 설문 응답 수집 Mock 데이터 작성"
labels: 'mock, foundation, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-003] 설문 응답 수집 Mock 데이터 작성
- 목적: 백엔드 데이터베이스 적재 로직 완성 전, 데이터맵 컴파일러를 테스트하기 위한 100명 분의 가상 설문 응답 `raw_record` 데이터를 생성한다.

## :link: References (Spec & Context)
- API 규격: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L662)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `POST /api/v1/forms/{form_id}/responses` 요청 바디(Body) 규격에 맞춘 시드 데이터 작성
- [ ] 다양한 조건(성별, 연령)을 가진 더미 유저 데이터 매핑

## :checkered_flag: Definition of Done (DoD)
- [ ] JSON 파일 유효성 검증 통과

## :construction: Dependencies & Blockers
- Depends on: #API-004
- Blocks: #BE-PAY-003
