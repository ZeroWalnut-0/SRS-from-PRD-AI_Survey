---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-PARSE-006: 이미지/수식 요소 스킵 기록 테스트"
labels: 'test, foundation, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-PARSE-006] 이미지/수식 요소 스킵 기록 테스트
- 목적: 문서 내 텍스트가 아닌 이미지나 수식 객체가 있을 경우, 에러 중단 없이 해당 요소를 패스하고 `skipped_elements` 메타데이터에 정확히 기록하는지 테스트한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L477)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 사진 1장이 포함된 한글 파일 업로드
- [ ] 파싱 결과 JSON 내 `skipped_elements` 배열 조회

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 이미지 스킵
- Given: 이미지가 포함된 문서
- When: 파싱 완료
- Then: `skipped_elements`에 `["image"]` 항목이 존재한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 누락 요소 안내 문구가 화면에 정상 출력되는지 검증

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-006
- Blocks: None
