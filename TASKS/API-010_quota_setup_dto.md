---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-010: Quota 설정 API 계약 정의"
labels: 'feature, foundation, api, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [API-010] Quota 설정 API 계약 정의
- 목적: 특정 설문에 대한 교차 쿼터(성별×연령×지역 등) 목표치를 설정하고 DB에 반영하기 위한 API 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#8`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `POST /api/v1/quotas`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 DTO 정의: `{ form_id: string, quota_matrix: JSON }`
- [ ] 응답 DTO 정의: `{ quota_id: string, status: string }`
- [ ] 쿼터 매트릭스 유효성 검증 규칙 정의 (각 셀의 목표치 합계 등)
- [ ] 에러 코드 정의:
    - 400: 잘못된 쿼터 형식, 존재하지 않는 문항 참조
- [ ] TypeScript 인터페이스 정의 (`types/api/quotas.ts`)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 설정 성공
- Given: 유효한 쿼터 매트릭스 JSON이 준비됨
- When: `POST /api/v1/quotas`로 요청함
- Then: 201 Created와 함께 생성된 `quota_id`를 반환해야 한다.

Scenario 2: 이미 진행 중인 조사에 쿼터 수정 시도
- Given: 이미 응답 수집이 시작된 폼의 쿼터를 대폭 수정함
- When: 요청을 전송함
- Then: 경고 또는 에러를 반환하여 데이터 일관성을 보호해야 함 (정책에 따라 결정).

## :gear: Technical & Non-Functional Constraints
- 데이터: 쿼터 매트릭스는 유연한 확장을 위해 JSONB 타입을 고려한 구조로 정의한다.
- 성능: 쿼터 생성 및 DB 트랜잭션 처리 레이턴시 ≤ 500ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] 쿼터 설정 요청/응답 DTO가 정의되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?
- [ ] 쿼터 매트릭스의 데이터 구조가 확정되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-007 (QUOTA_SETTING), #DB-008 (QUOTA_CELL)
- Blocks: #BE-QT-001 (쿼터 설정 구현), #FE-QT-001 (쿼터 설정 UI)
