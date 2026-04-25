---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-WM-002: 워터마크 클릭 및 UTM 추적 테스트"
labels: 'test, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-WM-002] 워터마크 클릭 및 UTM 추적 테스트
- 목적: 응답자가 하단 워터마크를 클릭해 서비스 랜딩 페이지로 넘어올 때, `utm_source=watermark` 파라미터가 정상적으로 전송 및 기록되는지 확인한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L522)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 배너 클릭 이벤트 발생
- [ ] 이동된 URL의 쿼리 스트링(Query String) 검증

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: UTM 파라미터
- Given: 워터마크 노출 화면
- When: 배너 터치/클릭
- Then: `https://aisurvey.net/?utm_source=watermark`로 리다이렉트된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] GA4 및 DB AUDIT_LOG에 `WATERMARK_CLICK` 이벤트 적재 확인

## :construction: Dependencies & Blockers
- Depends on: #FE-WM-002, #BE-WM-002
- Blocks: None
