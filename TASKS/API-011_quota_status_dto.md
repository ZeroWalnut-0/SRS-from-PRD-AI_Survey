---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-011: Quota 충족 상태 조회 API 계약 정의"
labels: 'feature, foundation, api, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [API-011] Quota 충족 상태 조회 API 계약 정의
- 목적: 현재 조사가 진행 중인 쿼터별 목표 대비 달성 현황(카운트)을 실시간으로 확인하기 위한 API 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#9`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `GET /api/v1/quotas/{quota_id}/status`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 파라미터 정의: `quota_id` (Path variable)
- [ ] 응답 DTO 정의: `{ quota_id: string, cells: Array<{ group_key: string, target_count: number, current_count: number, is_full: boolean }> }`
- [ ] 에러 코드 정의:
    - 404: 존재하지 않는 `quota_id`
- [ ] TypeScript 인터페이스 정의 (`types/api/quotas.ts`)
- [ ] 대시보드 시각화를 위한 데이터 구조 최적화

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 현황 조회 성공
- Given: 진행 중인 쿼터 설정(`quota_id`)이 존재함
- When: 상태 조회 API를 호출함
- Then: 200 OK와 함께 각 셀별 목표 수치 및 현재 수집된 응답 수를 반환해야 한다.

Scenario 2: 특정 셀 100% 달성 확인
- Given: 특정 셀의 `current_count`가 `target_count`와 동일함
- When: 상태 조회를 수행함
- Then: 해당 셀의 `is_full` 값이 `true`로 반환되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 실시간 대시보드용이므로 응답 레이턴시 ≤ 200ms를 유지한다.
- 정확성: DB의 최신 카운트를 정확히 반영해야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 쿼터 상태 응답용 DTO가 정의되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?
- [ ] 시각화에 필요한 필드(is_full 등)가 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-008 (QUOTA_CELL 테이블)
- Blocks: #BE-QT-002 (상태 조회 구현), #FE-QT-002 (쿼터 대시보드 구현)
