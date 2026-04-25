---
name: API Contract Task
about: API Endpoint 명세 및 계약 정의
title: "[API] API-013: GET /api/v1/routing/redirect/{resp_id} 계약 정의"
labels: 'api-contract, foundation, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [API-013] 패널 리다이렉트 API 계약 정의
- 목적: 설문 응답이 완료되거나, 스크린아웃/쿼터풀 발생 시 패널 공급사가 지정한 URL로 자동 리다이렉트하기 위한 HTTP 302 명세를 정의한다.

## :link: References (Spec & Context)
- API 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L662)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `GET /api/v1/routing/redirect/{resp_id}` 엔드포인트 규격 확정
- [ ] 응답 코드: 302 Found (Location 헤더 포함)
- [ ] 에러 코드: 404 (존재하지 않는 응답자), 500 (서버 오류)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상 리다이렉트
- Given: 유효한 `{resp_id}` 및 성공(Success) 상태
- When: API 호출
- Then: HTTP 302 상태 코드와 함께 등록된 `success_url`로 이동한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] OpenAPI Spec(Swagger 등)에 해당 규격 반영

## :construction: Dependencies & Blockers
- Depends on: #DB-009
- Blocks: #BE-RT-002
