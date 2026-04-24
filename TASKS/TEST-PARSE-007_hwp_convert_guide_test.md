---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PARSE-007: .hwp 파일 업로드 시 전환 유도 흐름 테스트"
labels: 'test, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PARSE-007] .hwp 파일 업로드 시 전환 유도 흐름 테스트
- 목적: 구형 HWP 파일을 업로드했을 때 시스템이 이를 차단하고 HWPX 전환 유도 모달을 1초 이내에 띄우는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #FE-PARSE-003 (HWPX 안내 모달)
- 성공 기준: TC-FUNC-031

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: `.hwp` 파일 업로드 시 즉각적인 확장자 감지 확인
- [ ] 시나리오 2: HWPX 전환 안내 모달의 텍스트 및 링크 유효성 확인
- [ ] 시나리오 3: 모달 노출 지연 시간 측정 (≤ 1,000ms)

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 구형 `.hwp` 확장자 파일
- When: 업로드 영역에 파일을 드롭함
- Then: 1초 이내에 "HWPX로 저장해 주세요" 모달이 나타나야 하며, 업로드 서버 요청은 발생하지 않아야 한다.

## :gear: Technical Constraints
- 도구: Playwright (E2E Test)

## :checkered_flag: Definition of Done (DoD)
- [ ] 확장자 기반 필터링이 클라이언트 측에서 즉시 작동하는가?
- [ ] 모달 노출 타이밍이 성능 요건을 충족하는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-003, #BE-PARSE-001
- Blocks: None
