---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RT-001: 패널사 포스트백 URL 등록 API 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RT-001] 패널사 포스트백 URL 등록 API (`POST /api/v1/routing/postback`)
- 목적: 외부 패널사(Cint/Toluna 등)와의 연동 시, 설문 완료(Success), 스크린아웃(Screenout), 쿼터풀(Quotafull) 상태에 따라 이동할 대상 URL을 등록한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L540)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#10`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L720)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js Route Handler `/app/api/v1/routing/postback/route.ts` 작성
- [ ] Prisma를 통한 `ROUTING_CONFIG` 테이블 레코드 생성 및 업데이트 처리
- [ ] 외부 URL 형식(HTTP/HTTPS)의 데이터 정합성 검증 추가

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 포스트백 URL 정상 등록
- Given: 유효한 3종 URL(Success, Screenout, Quotafull) 데이터가 Body에 전달됨
- When: API가 호출됨
- Then: 201 Created와 함께 라우팅 설정 ID가 반환된다.

## :gear: Technical & Non-Functional Constraints
- 안정성: 잘못된 URL 형식 입력 시 400 Bad Request 반환

## :checkered_flag: Definition of Done (DoD)
- [ ] 라우팅 데이터의 안전한 DB 적재 여부 확인

## :construction: Dependencies & Blockers
- Depends on: #DB-009, #API-012
- Blocks: #BE-RT-002
