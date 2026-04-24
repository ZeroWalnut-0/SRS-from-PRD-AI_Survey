---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RT-001: 패널 라우팅 설정 저장 Route Handler 구현"
labels: 'feature, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RT-001] 패널 라우팅 설정 저장 Route Handler 구현
- 목적: 특정 설문에 대한 외부 패널사 포스트백 URL 정보를 수신하여 DB의 `ROUTING_CONFIG` 테이블에 저장 또는 갱신하는 API를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#10`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.7_ROUTING_CONFIG`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/routing/postback/route.ts` 구현
- [ ] 요청 데이터(`success_url`, `screenout_url`, `quotafull_url`)의 형식 검증
- [ ] `RoutingConfig` 테이블에 Upsert (기존 설정이 있으면 수정, 없으면 생성) 로직 구현
- [ ] `form_id` 유효성 및 소유권 확인
- [ ] 저장 완료 후 `routing_id` 반환

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 라우팅 설정 저장 성공
- Given: 3종의 유효한 URL이 포함된 요청
- When: POST 요청이 수행됨
- Then: DB에 해당 설문의 라우팅 설정이 기록되고 200 OK를 반환해야 한다.

Scenario 2: 필수 URL 누락 시 처리
- Given: `success_url`만 포함되고 나머지가 누락된 요청
- When: 저장을 시도함
- Then: 비즈니스 정책에 따라 기본값(자사 감사 페이지)을 넣거나, 400 에러를 반환하여 입력을 유도한다.

## :gear: Technical & Non-Functional Constraints
- 성능: DB 쓰기 작업이므로 레이턴시 ≤ 300ms 유지.
- 보안: 입력된 URL에 대한 XSS 및 삽입 공격 방지를 위한 필터링을 수행한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-012` 규격에 맞는 응답을 반환하는가?
- [ ] DB Upsert 로직이 정확히 작동하는가?
- [ ] `form_id` 관계 맺기가 정상적으로 이루어지는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-009 (ROUTING_CONFIG), #API-012 (Postback DTO)
- Blocks: #BE-RT-002 (리다이렉트 로직 구현)
