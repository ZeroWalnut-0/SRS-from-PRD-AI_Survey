---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-001: Prisma 스키마 초기화 및 개발 환경 구성"
labels: 'feature, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-001] Prisma 스키마 초기화 및 개발 환경 구성
- 목적: Next.js 프로젝트 내에 Prisma ORM을 설정하고, 로컬(SQLite) 및 운영(Supabase PostgreSQL) 환경을 위한 기초 구성을 완료한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3_C-TEC-003`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 아키텍처 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#Constraints`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Prisma CLI 설치 및 초기화 (`npx prisma init`)
- [ ] `schema.prisma` 파일 내 `datasource` 및 `generator` 설정
- [ ] 로컬 개발용 SQLite 설정 (`provider = "sqlite"`) 및 환경 변수(`DATABASE_URL`) 구성
- [ ] Supabase PostgreSQL 연결 설정 확인 (운영 환경용 프로토콜 확인)
- [ ] Prisma Client 설치 및 기초 디렉토리 구조 생성 (`/prisma`, `/lib/prisma.ts`)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: Prisma 초기화 성공
- Given: Next.js 프로젝트가 생성된 상태
- When: `prisma init` 명령을 실행함
- Then: `prisma/schema.prisma` 파일과 `.env` 파일이 생성되어야 한다.

Scenario 2: Prisma Client 생성 확인
- Given: 기본 스키마가 정의됨
- When: `npx prisma generate`를 실행함
- Then: `node_modules/.prisma/client`에 타입 정의가 생성되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 호환성: SQLite(개발)와 PostgreSQL(운영) 간의 데이터 타입 호환성을 고려하여 스키마를 설계한다.
- 보안: `DATABASE_URL` 등 민감 정보는 반드시 `.env`에서 관리하고 Git에 포함시키지 않는다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `prisma/schema.prisma` 파일이 존재하는가?
- [ ] `npx prisma db push` 또는 `migrate`가 로컬 DB에서 성공하는가?
- [ ] `lib/prisma.ts`에 싱글톤 인스턴스 생성 로직이 포함되었는가?
- [ ] `.env` 파일에 유효한 DB 연결 문자열이 설정되었는가?

## :construction: Dependencies & Blockers
- Depends on: #NFR-INFRA-001 (프로젝트 초기 셋업)
- Blocks: #DB-002 (USER 테이블), #DB-011 (Enum 정의)
