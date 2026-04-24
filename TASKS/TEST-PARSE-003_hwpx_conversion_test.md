---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PARSE-003: HWPX 전환 유도 흐름 및 모달 검증 테스트"
labels: 'test, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PARSE-003] HWPX 전환 유도 흐름 및 모달 검증 테스트
- 목적: 구형 HWP 파일을 업로드했을 때, 시스템이 이를 정확히 감지하고 1초 이내에 HWPX 전환 안내 모달을 띄우는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #FE-PARSE-003 (HWPX 안내 모달)

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: `.hwp` 파일 드래그 앤 드롭 시 모달 노출 확인
- [ ] 시나리오 2: 모달 내 '전환 가이드' 링크 작동 확인
- [ ] 시나리오 3: 모달 닫기 후 파일 선택 초기화 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 구형 `.hwp` 샘플 파일
- When: 업로드 영역에 파일을 드롭함
- Then: 1,000ms 이내에 "HWPX로 저장해 주세요"라는 타이틀의 모달이 화면에 나타나야 한다.

## :gear: Technical Constraints
- 도구: Playwright Component Test

## :checkered_flag: Definition of Done (DoD)
- [ ] 확장자 감지 및 모달 노출 지연 시간이 1초 이내인가?
- [ ] 모달 노출 시 업로드 API 호출이 차단되는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-003 (HWPX 안내 모달), #BE-PARSE-001
- Blocks: None
