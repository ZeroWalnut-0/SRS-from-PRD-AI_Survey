---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-007: QUOTA_SETTING 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, database, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-007] QUOTA_SETTING 테이블 스키마 및 마이그레이션 작성
- 목적: 설문별로 정의된 교차 쿼터 관리의 최상위 설정 메타데이터 테이블을 생성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L785)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `QuotaSetting` 모델 선언 (`id`, `form_id`, `total_quota`, `created_at`, `updated_at`)
- [ ] 설문 폼 테이블과의 1:1 관계 지정
- [ ] Prisma DB Migration 반영

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 1:1 제약 확인
- Given: 이미 쿼터가 설정된 `form_id`
- When: 동일 `form_id`로 추가 생성 시도
- Then: 유니크 제약조건 에러로 중복 생성이 차단된다.

## :gear: Technical & Non-Functional Constraints
- 안정성: 고아 레코드 방지를 위해 Cascade Delete(연쇄 삭제) 제약 추가 검토

## :checkered_flag: Definition of Done (DoD)
- [ ] 모델 관계 정의 이상 유무 확인

## :construction: Dependencies & Blockers
- Depends on: #DB-004
- Blocks: #DB-008, #BE-QT-001
