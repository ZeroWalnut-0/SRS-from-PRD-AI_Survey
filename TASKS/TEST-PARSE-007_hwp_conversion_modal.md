---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-PARSE-007: HWPX 전환 안내 모달 노출 테스트"
labels: 'test, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-PARSE-007] HWPX 전환 안내 모달 노출 테스트
- 목적: 사용자가 실수로 구버전 `.hwp` 파일을 드롭했을 때, 시스템이 즉시 차단하고 "HWPX로 변환해 주세요" 안내 모달을 띄우는지 클라이언트 로직을 테스트한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L477)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Cypress 또는 Playwright를 이용한 `.hwp` 드래그 앤 드롭 시뮬레이션
- [ ] 모달 창의 DOM 가시성(Visibility) 체크

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 확장자 오류 감지
- Given: 메인 업로드 영역
- When: `test.hwp` 파일 드롭
- Then: 파일 업로드가 중단되고 안내 팝업이 활성화된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 모달 닫기 버튼 클릭 시 초기 상태로 복귀 검증

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-003
- Blocks: None
