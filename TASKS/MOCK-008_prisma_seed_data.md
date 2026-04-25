---
name: Mock Data Task
about: 개발 시뮬레이션을 위한 Mock 데이터 및 API 작성
title: "[Mock] MOCK-008: Prisma DB Seed 데이터 작성"
labels: 'mock, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-008] Prisma DB Seed 데이터 작성
- 목적: 개발 환경을 초기화할 때, `npx prisma db seed` 명령어를 통해 전체 테이블에 유기적으로 연결된 가상의 관계형 데이터(USER -> DOCUMENT -> PARSED_FORM 등)를 일괄 주입한다.

## :link: References (Spec & Context)
- DB 스키마: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L761)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/seed.ts` 작성
- [ ] 외래키(FK) 제약 조건을 준수하는 생성 순서 설계

## :checkered_flag: Definition of Done (DoD)
- [ ] 명령어 실행 후 데이터베이스에 레코드들이 정상적으로 생성되는지 검증

## :construction: Dependencies & Blockers
- Depends on: #DB-002 ~ #DB-010
- Blocks: None
