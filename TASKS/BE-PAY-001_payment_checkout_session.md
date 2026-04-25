---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-001: POST /api/v1/packages/{form_id}/payment 결제 세션 생성"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-001] 결제 요청 Route Handler 구현
- 목적: 유저가 데이터맵 다운로드를 위해 결제를 시도할 때, Toss Payments에 보낼 주문 ID를 생성하고 임시 결제 상태를 기록한다.

## :link: References (Spec & Context)
- 기술 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L461)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 주문 번호(`orderId`) UUID 생성 및 `ZIP_DATAMAP` 레코드 생성 (결제 전)
- [ ] 토스페이먼츠 API 연동용 Secret Key 로드 및 응답 데이터 구성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 세션 생성 성공
- Given: 결제 요청
- When: 유효한 `form_id`
- Then: `orderId`, `amount: 9900`이 포함된 JSON을 반환한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] DB에 임시 레코드 저장이 정상적으로 이루어졌는지 검증

## :construction: Dependencies & Blockers
- Depends on: #DB-006, #API-007
- Blocks: #FE-PAY-002
