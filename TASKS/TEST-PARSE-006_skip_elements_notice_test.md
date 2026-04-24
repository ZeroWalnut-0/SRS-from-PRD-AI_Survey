---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PARSE-006: 이미지/수식 스킵 및 알림 기록 검증 테스트"
labels: 'test, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PARSE-006] 이미지/수식 스킵 및 알림 기록 검증 테스트
- 목적: 복잡한 요소(이미지, 수식 등)가 포함된 문서를 파싱할 때, 해당 요소를 안전하게 건너뛰고 이를 사용자에게 정확히 고지하는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-PARSE-006 (스킵 로직), #FE-PARSE-006 (미리보기 화면)
- 성공 기준: TC-FUNC-007

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 이미지가 포함된 문항 파싱 시 이미지 제외 텍스트만 추출 확인
- [ ] 시나리오 2: 수식이 포함된 문항의 스킵 여부 및 `skipped_elements` 기록 확인
- [ ] 시나리오 3: 미리보기 화면에서 "건너뛴 요소" 배너 노출 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 이미지 2개와 수식 1개가 포함된 테스트용 HWPX 문서
- When: 파싱 프로세스를 실행함
- Then: `PARSED_FORM.structure_schema` 내에 3개의 스킵 항목이 기록되어야 하며, 미리보기 화면에 관련 안내가 표시되어야 한다.

## :gear: Technical Constraints
- 도구: Jest (Integration Test)

## :checkered_flag: Definition of Done (DoD)
- [ ] 스킵된 요소의 개수와 위치 정보가 정확히 기록되는가?
- [ ] 스킵 안내 UI가 사용자에게 명확히 전달되는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-006 (스킵 요소 기록)
- Blocks: None
