---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RT-002: 패널 리다이렉트 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RT-002] 패널 리다이렉트 구현 (`GET /api/v1/routing/redirect/{resp_id}`)
- 목적: 응답자의 최종 상태(성공/스크린아웃/쿼터풀)를 판별하여 패널사가 지정한 HTTP 302 외부 링크로 사용자를 리다이렉트한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L540)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#11`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L721)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] API Route Handler `/app/api/v1/routing/redirect/[resp_id]/route.ts` 작성
- [ ] `RESPONSE` 및 `ROUTING_CONFIG` 조회 로직 구현
- [ ] 응답자 상태(Success/Screenout/Quotafull) 판별 조건문 작성
- [ ] Next.js `redirect()` 또는 `Response.redirect()`를 이용한 HTTP 302 처리

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상 응답자 리다이렉트
- Given: `Success` 상태의 응답자 ID가 주어짐
- When: 리다이렉트 엔드포인트로 접근함
- Then: 지정된 성공 포스트백 URL로 HTTP 302 리다이렉트된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 지연으로 인한 이탈을 막기 위해 리다이렉트 처리 ≤ 500ms 준수

## :checkered_flag: Definition of Done (DoD)
- [ ] 브라우저 환경에서의 HTTP 302 응답 및 Location 헤더 검증

## :construction: Dependencies & Blockers
- Depends on: #BE-RT-001
- Blocks: #BE-RT-003
