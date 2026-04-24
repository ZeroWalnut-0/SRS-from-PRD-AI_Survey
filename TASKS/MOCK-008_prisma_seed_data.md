---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-008: Prisma DB Seed 스크립트 작성"
labels: 'feature, foundation, database, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-008] Prisma DB Seed 스크립트 작성
- 목적: 개발 및 테스트 환경에서 즉시 사용 가능한 전체 도메인 데이터를 일괄적으로 생성하는 Seed 스크립트를 작성하여 개발 효율성을 극대화한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2_전체_Entity`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/seed.ts` 파일 생성 및 설정
- [ ] 기초 데이터 인서트 로직 구현:
    - User (일반/유료) 10명
    - Document & ParsedForm (각 상태별) 20건
    - Response 데이터 500건 (다양한 설문에 분산)
    - QuotaSetting & QuotaCell 5세트
    - ZipDataMap (결제 완료/미완료) 10건
    - AuditLog 100건
- [ ] `package.json`에 `prisma.seed` 스크립트 등록 (`ts-node prisma/seed.ts`)
- [ ] 실행 시 기존 데이터를 초기화(Truncate/Delete)하는 옵션 추가

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: Seed 스크립트 실행 성공
- Given: 빈 DB 또는 기존 DB가 존재함
- When: `npx prisma db seed` 명령을 실행함
- Then: 에러 없이 완료되어야 하며, 모든 테이블에 명세된 수량의 데이터가 적재되어야 한다.

Scenario 2: 데이터 무결성 및 관계 확인
- Given: Seed 데이터가 적재됨
- When: `ParsedForm`을 조회하여 연관된 `Document`를 확인하거나, `QuotaCell`을 조회함
- Then: 외래 키(FK) 관계가 정확히 매핑되어 데이터 탐색이 가능해야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 전체 데이터 적재 시간이 10초 이내여야 한다.
- 유지보수: 스키마 변경 시 Seed 스크립트도 쉽게 업데이트할 수 있도록 도메인별 함수로 모듈화한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `prisma/seed.ts` 파일이 작성되었는가?
- [ ] 전체 테이블에 대한 샘플 데이터 생성 로직이 포함되었는가?
- [ ] `npx prisma db seed` 실행 시 데이터 무결성 에러가 없는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-002 ~ #DB-010 (모든 DB 테이블)
- Blocks: 전체 도메인의 기능 구현 및 수동 테스트 환경 구축
