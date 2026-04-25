---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-FORM-001: 폼 에디터 드래그 앤 드롭 순서 변경 테스트"
labels: 'test, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-FORM-001] 폼 에디터 드래그 앤 드롭 테스트
- 목적: 설문 제작/수정 단계에서 문항 카드를 마우스 드래그로 위아래로 이동했을 때, JSON 스키마 내 `order` 인덱스가 실시간으로 재배열되는지 검증한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L218)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Playwright Drag-and-drop 액션 수행 스크립트 작성
- [ ] 변경 후의 `structure_schema` 추출 및 비교

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 순서 변경 반영
- Given: 문항 A(1번), 문항 B(2번)
- When: B를 A 위로 드래그
- Then: JSON 상에서 B의 `order=1`, A의 `order=2`로 교체된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 렌더링 인덱스 역전 방지 로직 동작 확인

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-001, #FE-FORM-003
- Blocks: None
