---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-004: PARSED_FORM 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-004] PARSED_FORM 테이블 스키마 및 마이그레이션 작성
- 목적: AI에 의해 파싱된 설문 구조(JSON)와 관련 설정을 저장하는 테이블을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2_PARSED_FORM`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 시퀀스 다이어그램: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma` 내 `ParsedForm` 모델 정의
- [ ] 필수 필드 추가: `form_id` (UUID), `doc_id` (FK), `structure_schema` (JSON), `question_count`, `skipped_elements` (JSON), `viral_watermark_url`, `is_paid_user`
- [ ] `Document` 모델과의 1:1 관계 설정
- [ ] Prisma Migration 생성 및 실행

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 파싱 결과 저장
- Given: AI 파서로부터 생성된 JSON 스키마가 존재함
- When: `ParsedForm` 테이블에 데이터를 삽입함
- Then: JSON 데이터가 손상 없이 저장되어야 하며, 관련 `doc_id`와의 관계가 유지되어야 한다.

Scenario 2: 워터마크 URL 확인
- Given: 무료 사용자의 폼이 생성됨
- When: `viral_watermark_url` 필드를 확인함
- Then: UTM 파라미터(`utm_source=watermark`)가 포함된 올바른 URL이 저장되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 데이터 타입: `structure_schema` 및 `skipped_elements`는 Prisma의 `Json` 타입을 사용하여 유연성을 확보한다.
- 성능: 폼 조회 빈도가 높으므로 `form_id` 조회가 최적화되어야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `schema.prisma`에 ParsedForm 모델이 SRS 규격대로 반영되었는가?
- [ ] `structure_schema` 필드가 복잡한 JSON 구조를 수용할 수 있도록 설정되었는가?
- [ ] 마이그레이션이 성공적으로 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-003 (DOCUMENT 테이블)
- Blocks: #BE-PARSE-005 (AI SDK 연동), #BE-FORM-001 (폼 조회 API)
