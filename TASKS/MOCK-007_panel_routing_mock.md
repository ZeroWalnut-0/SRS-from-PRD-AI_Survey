---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-007: 패널 라우팅 포스트백/리다이렉트 Mock API 작성"
labels: 'feature, foundation, mock, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-007] 패널 라우팅 포스트백/리다이렉트 Mock API 작성
- 목적: 외부 패널사 연동 및 리다이렉트 설정을 테스트하기 위해, 가상의 포스트백 링크와 리다이렉트 동작을 시뮬레이션한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#10`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md), [`#6.1_#11`](#)
- 시퀀스 다이어그램: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.3`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `POST /api/v1/routing/postback` Mock 핸들러 작성
- [ ] `GET /api/v1/routing/redirect/{resp_id}` Mock 핸들러 작성 (HTTP 302 시뮬레이션)
- [ ] 가상의 패널사 랜딩 페이지(Success, Screenout, QuotaFull 각 1종) 구성
- [ ] 리다이렉트 실패 시의 에러 페이지 Mock 구성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 패널 리다이렉션 흐름 테스트
- Given: 설문 응답 결과가 'SUCCESS'로 기록됨
- When: Mock 리다이렉트 API를 호출함
- Then: 브라우저가 정의된 가상 패널 성공 페이지로 이동해야 한다.

Scenario 2: 리다이렉트 URL 미설정 시나리오
- Given: 라우팅 설정이 없는 폼에 대해 리다이렉트를 시도함
- When: Mock API를 호출함
- Then: 404 또는 500 에러와 함께 안내 메시지가 표시되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 인프라: 리다이렉션 테스트를 위해 로컬 환경에서도 작동하는 가상 외부 도메인 시뮬레이션이 필요하다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 상태별 가상 포스트백 URL 세트가 준비되었는가?
- [ ] HTTP 302 리다이렉트 동작이 Mock에서 시뮬레이션되는가?
- [ ] 라우팅 설정 UI와의 연동 테스트가 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #API-012, #API-013 (Routing DTO)
- Blocks: #FE-RT-001 (라우팅 세팅 UI), #BE-RT-002 (리다이렉트 구현)
