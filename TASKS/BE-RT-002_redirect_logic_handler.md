---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RT-002: 상태별 리다이렉트 로직 핸들러 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RT-002] 상태별 리다이렉트 로직 핸들러 구현
- 목적: 응답자의 `resp_id`를 기반으로 해당 조사의 결과 상태(성공/스크린아웃/쿼터풀)를 판단하고, 사전에 설정된 패널사 URL로 최종 리다이렉트(HTTP 302)를 수행한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#11`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 시퀀스 다이어그램: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.3`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/routing/redirect/[resp_id]/route.ts` 구현
- [ ] `resp_id`를 통한 응답자 상태(`routing_status`) 조회
- [ ] 해당 설문의 `ROUTING_CONFIG` 조회
- [ ] 상태에 따른 타겟 URL 매핑:
    - SUCCESS -> `success_url`
    - SCREENOUT -> `screenout_url`
    - QUOTAFULL -> `quotafull_url`
- [ ] URL 내의 파리미터(예: `uid={resp_id}`) 치환 로직 구현
- [ ] HTTP 302 Redirect 응답 반환

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 성공한 응답자 리다이렉트
- Given: `routing_status`가 `SUCCESS`인 응답자
- When: 리다이렉트 API 호출
- Then: `Location` 헤더에 `success_url`이 포함된 302 응답을 받아야 한다.

Scenario 2: 라우팅 설정이 없는 경우의 폴백
- Given: 패널사 연동을 하지 않은 일반 설문 응답자
- When: 리다이렉트를 시도함
- Then: 시스템 기본 "조사 완료 안내" 페이지로 이동시켜야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 리다이렉트 지연은 이탈로 이어지므로 DB 조회 및 판단 로직을 200ms 이내에 처리한다 (REQ-NF-012).
- 정확성: 응답자의 상태와 매핑되는 URL이 어긋나지 않도록 철저히 검증한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-013` 규격에 맞는 리다이렉트 처리가 완료되었는가?
- [ ] 상태별 URL 매핑 및 파라미터 치환 로직이 정확한가?
- [ ] 설정 미비 시의 폴백 페이지 연결이 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-005 (RESPONSE), #DB-009 (ROUTING_CONFIG), #API-013 (Redirect DTO)
- Blocks: None
