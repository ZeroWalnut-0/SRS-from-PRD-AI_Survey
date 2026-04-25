---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-004: PARSED_FORM 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, database, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-004] PARSED_FORM 테이블 스키마 및 마이그레이션 작성
- 목적: AI 분석을 통해 추출된 설문의 구조 및 JSON 형태의 문항 데이터 스키마(`structure_schema`)를 영속화한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L742)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `ParsedForm` 모델 선언 (`id`, `doc_id`, `structure_schema`, `viral_watermark_url`, `skipped_elements`, `question_count` 등)
- [ ] JSON 데이터를 무손실로 저장하기 위한 PostgreSQL `JsonB` 타입 컬럼 활용 설정
- [ ] DB 마이그레이션 반영

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: JSON 데이터 삽입 테스트
- Given: 규격화된 JSON 문항 객체가 주어짐
- When: `structure_schema` 컬럼에 인서트함
- Then: 온전한 JSON 타입으로 데이터가 저장되고 파싱 없이 바로 조회된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 유연한 쿼리를 위해 JsonB 데이터 구조의 최적화 유지

## :checkered_flag: Definition of Done (DoD)
- [ ] Prisma Client DTO 객체 매핑 검증 완료

## :construction: Dependencies & Blockers
- Depends on: #DB-003
- Blocks: #BE-FORM-001, #BE-FORM-002
