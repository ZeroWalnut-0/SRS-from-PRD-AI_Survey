---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-007: QUOTA_SETTING 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-007] QUOTA_SETTING 테이블 스키마 및 마이그레이션 작성
- 목적: 특정 설문에 대한 쿼터(할당) 설정 전반을 관리하기 위한 테이블을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.5_QUOTA_SETTING`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 쿼터 요건: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4_REQ-FUNC-018`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma` 내 `QuotaSetting` 모델 정의
- [ ] 필수 필드 추가: `quota_id` (UUID), `form_id` (FK), `quota_matrix` (JSON), `is_active`
- [ ] `ParsedForm` 모델과의 1:1 관계 설정
- [ ] Prisma Migration 생성 및 실행

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 설정 저장
- Given: 엑셀 파싱 등을 통해 도출된 쿼터 매트릭스가 존재함
- When: `QuotaSetting` 테이블에 데이터를 삽입함
- Then: JSON 형식의 매트릭스가 정확히 저장되어야 하며, 해당 설문(`form_id`)과 연동되어야 한다.

Scenario 2: 쿼터 활성화 상태 제어
- Given: 쿼터 설정이 존재함
- When: `is_active` 필드를 변경함
- Then: 설문 응답 수집 시 쿼터 적용 여부가 이 필드에 의해 제어되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 데이터: `quota_matrix`는 복잡한 교차 쿼터 구조를 수용할 수 있도록 JSON 타입으로 정의한다.
- 무결성: 한 설문 당 하나의 활성 쿼터 설정을 권장한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `schema.prisma`에 QuotaSetting 모델이 SRS 명세대로 반영되었는가?
- [ ] 마이그레이션이 성공적으로 수행되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM 테이블)
- Blocks: #DB-008 (QUOTA_CELL 테이블), #BE-QT-001 (쿼터 설정 생성)
