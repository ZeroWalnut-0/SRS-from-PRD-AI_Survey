---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-012: 패널사 포스트백 URL 등록 API 계약 정의"
labels: 'feature, foundation, api, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [API-012] 패널사 포스트백 URL 등록 API 계약 정의
- 목적: 외부 패널사 연동 시 응답 결과(성공, 스크린아웃, 쿼터풀)에 따라 리다이렉트할 외부 URL을 등록하기 위한 API 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#10`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `POST /api/v1/routing/postback`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 DTO 정의: `{ form_id: string, success_url: string, screenout_url: string, quotafull_url: string }`
- [ ] 응답 DTO 정의: `{ routing_id: string, status: string }`
- [ ] URL 형식 유효성 검증 규칙 정의
- [ ] 에러 코드 정의:
    - 400: 잘못된 URL 형식
- [ ] TypeScript 인터페이스 정의 (`types/api/routing.ts`)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 포스트백 링크 등록 성공
- Given: 외부 패널사의 가이드에 따른 URL들이 준비됨
- When: `POST /api/v1/routing/postback`으로 등록 요청함
- Then: 201 Created와 함께 생성된 `routing_id`를 반환해야 한다.

Scenario 2: 잘못된 URL 형식 제출
- Given: 프로토콜(`http://` 등)이 누락된 잘못된 URL을 전송함
- When: 등록을 요청함
- Then: 400 Bad Request를 반환하고 수정을 요구해야 한다.

## :gear: Technical & Non-Functional Constraints
- 데이터: 저장 전 URL에 특수문자나 공격 코드가 포함되지 않았는지 검증한다.
- 성능: 등록 요청 처리 레이턴시 ≤ 300ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] 라우팅 등록 요청/응답 DTO가 정의되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?
- [ ] 상태별 3가지 URL 필드가 모두 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-009 (ROUTING_CONFIG 테이블)
- Blocks: #BE-RT-001 (라우팅 등록 구현), #FE-RT-001 (라우팅 세팅 UI)
