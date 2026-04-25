---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-RT-001: 패널사 포스트백 링크 등록 테스트"
labels: 'test, foundation, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-RT-001] 패널사 포스트백 링크 등록 테스트
- 목적: 관리자가 어드민 페이지에서 패널 공급사 전용 3종 URL을 등록하고 저장했을 때, 특수문자(?, & 등)가 깨지지 않고 DB에 안전하게 저장되는지 확인한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.4.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L377)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 다양한 쿼리 파라미터가 섞인 긴 URL을 등록하는 API 요청
- [ ] DB에서 추출한 URL과 원본 URL의 문자열 일치 여부 비교

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: URL 인코딩 유지
- Given: 복잡한 URL 문자열
- When: 저장 요청
- Then: 변형 및 유실 없이 원본 그대로 DB에 기록된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] XSS 방지 필터링을 거친 후에도 정상 동작하는지 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-RT-001
- Blocks: None
