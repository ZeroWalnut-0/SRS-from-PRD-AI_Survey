---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-WM-001: 무료 사용자 설문 폼 워터마크 렌더링 검증 테스트"
labels: 'test, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-WM-001] 무료 사용자 설문 폼 워터마크 렌더링 검증 테스트
- 목적: 무료 계정으로 생성된 설문 폼의 모든 페이지 하단에 워터마크 배너가 예외 없이 100% 노출되는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #FE-WM-001 (배너 UI)
- 성공 기준: TC-FUNC-016

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 무료 사용자가 생성한 설문 링크 접속 시 하단 배너 확인
- [ ] 시나리오 2: 설문 응답 중 문항을 넘길 때마다 배너가 계속 유지되는지 확인
- [ ] 시나리오 3: 다양한 해상도(데스크탑, 모바일)에서 배너의 가시성 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: `viral_watermark_url`이 포함된 무료 설문 폼
- When: 설문의 모든 단계(시작, 본문, 완료)를 탐색함
- Then: 모든 화면 하단에 "Powered by AI Survey" 배너가 고정되어 표시되어야 한다.

## :gear: Technical Constraints
- 도구: Playwright (Visual Regression Test 또는 Selector 체크)

## :checkered_flag: Definition of Done (DoD)
- [ ] 워터마크 노출률이 100%인가?
- [ ] 다른 UI 요소(다음 버튼 등)와 겹치지 않는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-WM-001 (워터마크 배너)
- Blocks: None
