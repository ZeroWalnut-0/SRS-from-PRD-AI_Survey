---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-FORM-004: 설문 응답 제출 API 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-FORM-004] 설문 응답 제출 API (`POST /api/v1/forms/{form_id}/responses`)
- 목적: 응답자 데이터(문항 답변)를 수신하여 유효성(AI Data Bouncer)을 검증하고, IP 해싱을 거쳐 DB에 안전하게 저장한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L508)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L756)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L714)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js API Route Handler `/app/api/v1/forms/[form_id]/responses/route.ts` 구축
- [ ] 요청 IP 추출 및 SHA-256 해시 적용 (`ip_hash` 생성으로 개인정보 비식별화)
- [ ] AI Data Bouncer 로직 연동 (500ms 이내 매크로 및 찍기성 불성실 응답 탐지)
- [ ] 쿼터 상태 확인 및 `RESPONSE` 테이블에 데이터 일괄 저장

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상 응답 제출
- Given: 규격에 맞는 답변 데이터가 전달됨
- When: API에 POST 요청을 전송함
- Then: 201 Created 상태와 함께 생성된 `resp_id`가 반환된다.

Scenario 2: AI Data Bouncer에 의한 불성실 응답 마킹
- Given: 1초 이내에 모든 답변을 작성하는 등 기계적 패턴의 응답이 주어짐
- When: 응답 제출 API가 호출됨
- Then: `quota_status`가 `SCREENOUT` 또는 `SUSPECT`로 기록된다.

## :gear: Technical & Non-Functional Constraints
- 성능: AI Data Bouncer 분석을 포함하여 p95 응답 속도 500ms 이내 유지
- 보안: 개인정보(IP 등) 평문 저장 전면 금지 및 마스킹 필수

## :checkered_flag: Definition of Done (DoD)
- [ ] DB 내 `raw_record` JSON 구조 일치 확인
- [ ] 부하 테스트 시 동시 접속 처리 능력 검증(Atomic/RPC 적용 확인)

## :construction: Dependencies & Blockers
- Depends on: #DB-005, #API-004
- Blocks: #BE-PAY-003 (ZIP 산출물 컴파일)
