---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-009: ROUTING_CONFIG 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, database, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-009] ROUTING_CONFIG 테이블 스키마 및 마이그레이션 작성
- 목적: 패널 리다이렉션을 위한 외부 연동 URL을 보관하는 `ROUTING_CONFIG` 테이블을 생성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L725)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `RoutingConfig` 모델 선언 (`id`, `form_id`, `success_url`, `screenout_url`, `quotafull_url`)
- [ ] `form_id` 외래키 제약 조건 매핑
- [ ] Prisma Migrate dev 반영

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 모델 반영
- Given: Prisma 스키마 작성 완료
- When: 마이그레이션 수행
- Then: DB 상에 `RoutingConfig` 구조가 정상 구현된다.

## :gear: Technical & Non-Functional Constraints
- 안정성: URL 문자열 길이를 감안하여 `VarChar(512)` 이상의 충분한 데이터 크기 확보

## :checkered_flag: Definition of Done (DoD)
- [ ] 외래키 제약 작동 여부 확인

## :construction: Dependencies & Blockers
- Depends on: #DB-004
- Blocks: #BE-RT-001
