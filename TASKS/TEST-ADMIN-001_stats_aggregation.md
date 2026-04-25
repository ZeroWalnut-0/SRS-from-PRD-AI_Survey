---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-ADMIN-001: 어드민 통계 데이터 집계 정합성 테스트"
labels: 'test, foundation, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-ADMIN-001] 어드민 통계 집계 정합성 테스트
- 목적: 전체 매출액, 총 응답자 수, 수집 완료율 등의 핵심 비즈니스 지표가 DB 레코드 합계와 정확하게 일치하는지 검증한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.7`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L467)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 테스트 결제 완료 데이터(9,900원 3건) 주입
- [ ] `GET /api/v1/admin/stats` 호출 결과의 `total_revenue`가 29,700원인지 검사

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 매출 집계
- Given: 3건의 성공 결제
- When: 통계 조회
- Then: JSON 응답의 `total_revenue`가 정확히 29,700으로 표기된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 취소/환불 건이 포함되었을 때 매출 차감이 정상 적용되는지 검증

## :construction: Dependencies & Blockers
- Depends on: #API-016, #BE-ADMIN-001
- Blocks: None
