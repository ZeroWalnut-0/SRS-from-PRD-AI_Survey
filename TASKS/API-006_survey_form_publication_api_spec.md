---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-006: POST /api/v1/forms/{form_id}/publish 규격 정의"
labels: 'feature, api-spec, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [API-006] POST /api/v1/forms/{form_id}/publish 규격 정의
- 목적: 설문 배포 완료 시 응답자용 URL과 QR 코드를 반환할 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L716)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] URL 및 QR Base64 데이터를 포함하는 Response DTO 작성
- [ ] Swagger 연동

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 출력 규격 적합성
- Given: 배포 성공 결과 객체
- When: 타입 확인 시
- Then: `survey_url` 필드가 필수 포함된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Swagger 테스트 통과

## :construction: Dependencies & Blockers
- Depends on: #DB-004
- Blocks: #BE-FORM-003, #FE-FORM-006
