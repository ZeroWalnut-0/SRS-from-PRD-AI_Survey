---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-008: QUOTA_CELL 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, database, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-008] QUOTA_CELL 테이블 스키마 및 마이그레이션 작성
- 목적: 교차 쿼터의 각 세그먼트(예: '서울 20대 남성')별 목표치와 현재 상태를 기록하는 하위 셀 테이블을 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L796)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `QuotaCell` 모델 작성 (`id`, `setting_id`, `conditions`, `target_count`, `current_count`, `is_full`)
- [ ] `conditions`를 쿼리하기 편하도록 JsonB 또는 정형 필드 설계 (여기서는 유연성을 위해 JsonB 권장)
- [ ] `is_full` 필드 기본값 `false` 지정

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 셀 레코드 생성
- Given: 쿼터 조건("gender: M, age: 20s")과 목표치 50명이 전달됨
- When: DB에 인서트됨
- Then: 정상 생성되고 `current_count=0`으로 초기화된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 쿼터 판단 시 빈번한 Select/Update가 일어나므로 `setting_id`에 인덱스 적용 필수

## :checkered_flag: Definition of Done (DoD)
- [ ] 교차 테이블 정합성 및 릴레이션 무결성 검증

## :construction: Dependencies & Blockers
- Depends on: #DB-007
- Blocks: #BE-QT-001
