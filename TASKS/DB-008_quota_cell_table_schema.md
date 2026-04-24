---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-008: QUOTA_CELL 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-008] QUOTA_CELL 테이블 스키마 및 마이그레이션 작성
- 목적: 쿼터 매트릭스의 각 개별 셀(예: "서울-남성-20대")에 대한 목표치와 현재 응답수를 관리하는 테이블을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.6_QUOTA_CELL`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 동시성 제어 요건: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4_REQ-FUNC-020`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma` 내 `QuotaCell` 모델 정의
- [ ] 필수 필드 추가: `cell_id` (UUID), `quota_id` (FK), `group_key`, `gender`, `age_range`, `region`, `target_count`, `current_count`, `is_full`
- [ ] `QuotaSetting` 모델과의 1:N 관계 설정
- [ ] Prisma Migration 생성 및 실행

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 셀 생성
- Given: 교차 쿼터 설정이 완료됨
- When: 각 조건 조합별로 `QuotaCell` 레코드를 생성함
- Then: `target_count`가 정확히 설정되어야 하며, 초기 `current_count`는 0이어야 한다.

Scenario 2: 목표 도달 상태 확인
- Given: `current_count`가 `target_count`에 도달함
- When: 시스템이 이를 감지함
- Then: `is_full` 필드가 `true`로 업데이트되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 쿼터 카운트 조회가 빈번하므로 `group_key`와 `quota_id` 조합에 인덱스를 추가한다.
- 무결성: 동시성 제어를 위해 `current_count`는 원자적 연산으로 업데이트되어야 함을 고려하여 설계한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `schema.prisma`에 QuotaCell 모델이 SRS 명세대로 반영되었는가?
- [ ] 마이그레이션이 성공적으로 수행되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-007 (QUOTA_SETTING 테이블)
- Blocks: #DB-012 (RPC 함수 작성), #BE-QT-003 (원자적 증가 로직)
