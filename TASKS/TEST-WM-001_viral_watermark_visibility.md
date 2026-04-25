---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-WM-001: 무료 사용자 워터마크 배너 렌더링 테스트"
labels: 'test, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-WM-001] 무료 사용자 워터마크 배너 렌더링 테스트
- 목적: 유료 결제를 하지 않은 무료 설문 폼 화면 하단에 "Powered by AI Survey" 배너가 뷰포트 가시성 기준 100% 렌더링되는지 UI를 검증한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L522)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 무료 설문 배포 URL 접속
- [ ] 푸터 영역 내 워터마크 노출 여부 DOM 탐색

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 워터마크 확인
- Given: 무료 사용자 폼
- When: 페이지 로드
- Then: 최하단에 고유 배너 스타일이 정상 출력된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 유료 결제 완료 후 배너가 감춰지는지(Hidden) 교차 테스트

## :construction: Dependencies & Blockers
- Depends on: #FE-WM-001
- Blocks: None
