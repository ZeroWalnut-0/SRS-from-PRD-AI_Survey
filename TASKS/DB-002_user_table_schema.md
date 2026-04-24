---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-002: USER 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-002] USER 테이블 스키마 및 마이그레이션 작성
- 목적: 서비스 사용자 정보를 저장하고 관리하기 위한 기초 데이터 테이블을 설계하고 Prisma 마이그레이션 스크립트를 작성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.9_ERD`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델 상세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 기술 스택 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#C-TEC-003`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma` 파일 내 `User` 모델 정의
- [ ] 필수 필드 추가: `user_id` (UUID), `email` (Unique), `name`, `is_paid_user` (Boolean), `created_at` (Timestamp)
- [ ] 관계 설정: `DOCUMENT`, `AUDIT_LOG` 테이블과의 1:N 관계 정의
- [ ] Prisma Migration 생성 (`npx prisma migrate dev --name init_user_table`)
- [ ] 로컬 SQLite 및 Supabase PostgreSQL 호환성 체크

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: User 테이블 생성 확인
- Given: Prisma 스키마가 정의됨
- When: 마이그레이션 스크립트를 실행함
- Then: DB 내에 `User` 테이블이 생성되고, 지정된 모든 컬럼(user_id, email 등)이 존재해야 한다.

Scenario 2: 이메일 중복 제약 조건 확인
- Given: 특정 이메일로 가입된 유저가 존재함
- When: 동일한 이메일로 새로운 유저 레코드를 삽입하려고 시도함
- Then: DB 레벨에서 Unique 제약 조건 위반 에러가 발생해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 이메일 필드는 인덱싱 처리하여 조회 성능을 확보한다.
- 호환성: Prisma Client Type Generation이 정상적으로 수행되어야 한다.
- 규정: Zero-Retention 정책을 고려하여, 향후 삭제 시 연쇄 삭제(Cascade) 또는 비식별화 로직을 검토한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `schema.prisma`에 User 모델이 SRS 규격대로 반영되었는가?
- [ ] 마이그레이션 파일이 `prisma/migrations/` 디렉토리에 생성되었는가?
- [ ] `npx prisma generate` 명령어가 에러 없이 실행되는가?
- [ ] DB 도구(Prisma Studio 등)를 통해 테이블 구조가 확인되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-001 (Prisma 초기화)
- Blocks: #DB-003 (DOCUMENT 테이블 생성), #BE-RL-001 (인증/한도 제한 구현)
