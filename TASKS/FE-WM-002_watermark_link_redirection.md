---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-WM-002: 워터마크 클릭 시 서비스 가입 페이지 리다이렉션 구현"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-WM-002] 워터마크 클릭 시 서비스 가입 페이지 리다이렉션 구현
- 목적: 응답자가 워터마크를 클릭했을 때, UTM 파라미터가 포함된 서비스 소개 또는 가입 페이지로 안전하게 이동시키고 이를 추적한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3_REQ-FUNC-017`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 워터마크 배너 내 `<a>` 태그 또는 클릭 이벤트 핸들러 구현
- [ ] `target="_blank"` 속성을 사용하여 새 탭으로 서비스 페이지 오픈 (설문 중단 방지)
- [ ] 서버 로깅 API(`BE-WM-002`) 호출 연동 (클릭 로그 기록)
- [ ] GA4(Google Analytics) 이벤트 전송 로직 추가 (선택 사항)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 워터마크 클릭 및 새 창 이동
- Given: 설문 응답 중 하단 워터마크를 발견함
- When: 사용자가 워터마크 영역을 클릭함
- Then: 설문 탭은 유지되면서 새 브라우저 탭에 UTM 파라미터가 포함된 서비스 홈페이지가 열려야 한다.

Scenario 2: 클릭 추적 확인
- Given: 워터마크 클릭 이벤트 발생
- When: 서버 측 로그를 확인함
- Then: 해당 클릭에 대한 감사 로그(`AUDIT_LOG`)가 생성되어야 한다.

## :gear: Technical & Non-Functional Constraints
- UX: 클릭 시 설문 폼이 새로고침되거나 데이터가 유실되지 않도록 철저히 격리한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 워터마크 클릭 시 의도한 URL로 정확히 이동하는가?
- [ ] 새 탭 열기 설정이 정상적으로 작동하는가?
- [ ] 클릭 시 서버 로깅 API 호출이 성공하는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-WM-001 (배너 UI), #BE-WM-002 (로그 기록)
- Blocks: None
