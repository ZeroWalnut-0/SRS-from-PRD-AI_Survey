---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-002: USER 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, database, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-002] USER 테이블 스키마 및 마이그레이션 작성
- 목적: 서비스 사용자 정보를 저장하는 핵심 테이블인 `USER` 스키마를 선언한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L725)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `schema.prisma` 내 `User` 모델 선언 (id, email, password_hash, role, created_at, updated_at)
- [ ] Role 필드를 Enum 타입(`USER`, `PAID`, `ADMIN`)으로 정의
- [ ] Prisma migration 커맨드를 이용해 로컬/원격 DB에 테이블 반영

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 마이그레이션 수행 성공
- Given: Prisma User 모델이 올바르게 작성됨
- When: `npx prisma migrate dev` 실행 시
- Then: DB에 `User` 테이블이 정상 생성된다.

## :gear: Technical & Non-Functional Constraints
- 무결성: `email` 컬럼에 고유 인덱스(Unique Index) 설정 필수

## :checkered_flag: Definition of Done (DoD)
- [ ] Prisma Client에서 `prisma.user.create()` 호출 가능 여부 확인

## :construction: Dependencies & Blockers
- Depends on: #DB-001
- Blocks: #BE-AUTH-001, #BE-RL-001
