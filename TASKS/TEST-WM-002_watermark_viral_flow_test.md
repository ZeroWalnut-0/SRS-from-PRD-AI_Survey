---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-WM-002: 워터마크 클릭 시 바이럴 유입 흐름 검증 테스트"
labels: 'test, backend, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-WM-002] 워터마크 클릭 시 바이럴 유입 흐름 검증 테스트
- 목적: 워터마크 클릭 시 서비스 페이지로의 이동 및 UTM 파라미터 전달, 그리고 서버 측 로그 기록이 연쇄적으로 정상 작동하는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #FE-WM-002 (리다이렉션), #BE-WM-002 (로그 기록)
- 성공 기준: TC-FUNC-017

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 워터마크 클릭 시 새 탭 오픈 및 타겟 URL 확인
- [ ] 시나리오 2: 타겟 URL에 `utm_source=watermark` 포함 여부 확인
- [ ] 시나리오 3: 클릭 직후 DB `AUDIT_LOG` 테이블에 클릭 이벤트 생성 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 무료 설문 폼 화면
- When: 워터마크 배너를 클릭함
- Then: 서비스 메인 페이지가 열려야 하며, 서버 로그에는 해당 클릭을 발생시킨 `form_id`가 정확히 기록되어야 한다.

## :gear: Technical Constraints
- 도구: Playwright (URL 검증) + API Test (Log 체크)

## :checkered_flag: Definition of Done (DoD)
- [ ] 바이럴 추적을 위한 파라미터가 유실 없이 전달되는가?
- [ ] 서버 측 클릭 통계 기록이 정확히 수행되는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-WM-002 (워터마크 리다이렉션)
- Blocks: None
