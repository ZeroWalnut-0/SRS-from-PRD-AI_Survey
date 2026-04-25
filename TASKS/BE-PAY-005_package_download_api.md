---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-005: ZIP 다운로드 Route Handler 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-005] ZIP 다운로드 Route Handler 구현
- 목적: `GET /api/v1/packages/{package_id}/download` 엔드포인트의 비즈니스 로직을 작성하여 미결제자의 불법 다운로드를 차단한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#7`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L751)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] DB `ZIP_DATAMAP` 테이블의 `payment_cleared` 플래그 유효성 검사
- [ ] 미결제 시 403 Forbidden HTTP 응답 반환

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 완료자 다운로드 요청
- Given: `payment_cleared = true` 상태
- When: 다운로드 API 호출
- Then: HTTP 200과 함께 서명된 URL이 반환된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 존재하지 않는 패키지 ID에 대한 404 에러 처리

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-004, #API-009
- Blocks: None
