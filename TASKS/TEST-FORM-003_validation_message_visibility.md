---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-FORM-003: 필수 응답 미입력 유효성 검사 테스트"
labels: 'test, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-FORM-003] 필수 응답 유효성 검사 테스트
- 목적: 응답자가 필수(Required) 문항을 누락하고 제출을 시도할 때, 브라우저 스크롤이 해당 문항으로 이동하며 경고 메시지가 가시적으로 노출되는지 검증한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L287)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 필수 문항 1개가 포함된 설문 화면 로드
- [ ] 입력 없이 '다음' 또는 '제출' 버튼 클릭 시뮬레이션
- [ ] 에러 스타일(Red Border) 및 메시지 노출 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 필수 누락 차단
- Given: 미입력 상태
- When: 제출 버튼 클릭
- Then: 폼 제출이 중단되고, "필수 항목입니다" 문구가 노출된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 접근성(Aria-invalid) 속성이 올바르게 부여되는지 확인

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-007
- Blocks: None
