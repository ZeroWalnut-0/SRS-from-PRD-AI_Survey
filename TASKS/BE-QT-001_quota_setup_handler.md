---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-QT-001: Quota 설정 생성 및 QuotaCell 초기화 핸들러 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-QT-001] Quota 설정 생성 및 QuotaCell 초기화 핸들러 구현
- 목적: 프론트엔드에서 전달받은 쿼터 매트릭스를 기반으로 `QUOTA_SETTING` 레코드를 생성하고, 하위의 `QUOTA_CELL`들을 전개(Expand)하여 초기화한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#8`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.5_QUOTA_SETTING`](#), [`#6.2.6_QUOTA_CELL`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/quotas/route.ts` (POST) 핸들러 구현
- [ ] 요청 본문(`quota_matrix`)의 무결성 검증
- [ ] DB 트랜잭션 처리:
    1. `QUOTA_SETTING` 레코드 생성
    2. 매트릭스를 파싱하여 개별 조합별 `QUOTA_CELL` 레코드 일괄 생성 (Bulk Insert)
- [ ] 기존 쿼터 설정이 있을 경우의 처리 정책 (덮어쓰기 또는 버전 관리) 구현
- [ ] 생성 완료 후 `quota_id` 반환

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 교차 쿼터 초기화 성공
- Given: 성별(2) x 연령(3) x 지역(5)의 총 30개 조합 매트릭스 수신
- When: 쿼터 설정 API를 호출함
- Then: DB에 1개의 `QUOTA_SETTING`과 30개의 `QUOTA_CELL` 레코드가 정확히 생성되어야 한다.

Scenario 2: 유효하지 않은 매트릭스 차단
- Given: 목표 합계가 0이거나 필수 조건이 누락된 매트릭스
- When: 설정을 요청함
- Then: 400 에러를 반환하고 DB에 어떠한 변경사항도 생기지 않아야 한다(트랜잭션 롤백).

## :gear: Technical & Non-Functional Constraints
- 성능: 다량의 셀 생성 시 Bulk Insert를 활용하여 처리 시간을 500ms 이내로 제한한다.
- 원자성: 설정 생성 도중 실패 시 부분 생성되지 않도록 반드시 트랜잭션을 적용한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-010` 규격에 맞는 요청/응답 처리가 완료되었는가?
- [ ] 하위 쿼터 셀들이 매트릭스 구조에 맞게 자동 전개되어 생성되는가?
- [ ] DB 트랜잭션 무결성이 보장되는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-007, #DB-008 (Quota 테이블), #API-010 (Quota DTO)
- Blocks: #BE-QT-003 (쿼터 증가 로직 연동)
