---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PAY-004: ZIP 산출물 다운로드 시작 및 프로그레스 UI 구현"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PAY-004] ZIP 산출물 다운로드 시작 및 프로그레스 UI 구현
- 목적: 사용자가 다운로드 버튼을 클릭했을 때 서명된 URL을 받아 실제 파일 다운로드를 시작하고, 대용량 파일의 경우 진행 상태를 표시한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#7`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-009_zip_download_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-009_zip_download_dto.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] [ZIP 다운로드] 버튼 이벤트 핸들러 구현
- [ ] `GET /api/v1/packages/{package_id}/download` API 호출 및 `presigned_url` 수신
- [ ] 브라우저 다운로드 트리거 로직 구현 (숨겨진 `<a>` 태그 활용 등)
- [ ] 다운로드 중 상태 표시 (Button Loading, Toast 알림 등)
- [ ] 다운로드 완료 또는 실패 시 후속 알림 처리

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 파일 다운로드 시작
- Given: 결제가 완료된 유효한 패키지 ID
- When: 다운로드 버튼을 클릭함
- Then: 서버로부터 서명된 URL을 받고, 브라우저 다운로드 관리자에 `.zip` 파일이 추가되어야 한다.

Scenario 2: URL 만료 또는 에러 시 재시도
- Given: API 호출 중 네트워크 에러가 발생함
- When: 다운로드에 실패함
- Then: 에러 토스트를 표시하고, 사용자가 다시 클릭하여 신규 URL을 받을 수 있도록 유도한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 서명된 URL은 1회용 또는 짧은 유효기간을 가지므로, 클릭 시점에 실시간으로 발급받아야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 서명된 URL 기반의 실제 파일 다운로드가 정상 작동하는가?
- [ ] 다운로드 요청 시의 로딩 UI가 적절히 표시되는가?
- [ ] 에러 핸들링 및 재시도 로직이 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #API-009 (Download DTO), #FE-PAY-003 (성공 화면)
- Blocks: None
