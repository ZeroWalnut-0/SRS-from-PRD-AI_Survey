---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-011: Enum 타입 정의 및 Prisma 매핑"
labels: 'feature, foundation, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-011] Enum 타입 정의 및 Prisma 매핑
- 목적: 시스템 전반에서 공통으로 사용되는 상태 값 및 범주형 데이터를 Enum 타입으로 정의하여 데이터 일관성을 확보한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.10_Enum_Definitions`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma` 내 전역 Enum 정의:
    - `FileType`: HWP, PDF, WORD
    - `DocumentStatus`: PENDING, PARSING, COMPLETED, FAILED
    - `QuotaStatus`: ACTIVE, FULL, SCREENOUT
    - `RoutingStatus`: SUCCESS, SCREENOUT, QUOTAFULL, PENDING
    - `Gender`: M, F, OTHER
- [ ] 각 모델(Document, Response 등)에 해당 Enum 타입 적용
- [ ] Prisma Migration 생성 및 실행

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 잘못된 상태 값 삽입 차단
- Given: `DocumentStatus`가 Enum으로 정의됨
- When: 정의되지 않은 문자열(예: "UNKNOWN")을 상태 값으로 삽입하려고 시도함
- Then: DB 또는 ORM 레벨에서 유효성 검증 에러가 발생해야 한다.

Scenario 2: Enum 타입 코드 활용
- Given: Prisma Client가 생성됨
- When: 애플리케이션 코드에서 Enum 타입을 사용함
- Then: IDE 자동완성 및 타입 체크가 정상적으로 동작해야 한다.

## :gear: Technical & Non-Functional Constraints
- 호환성: SQLite는 Native Enum을 지원하지 않으므로 Prisma가 문자열로 매핑함을 인지한다. PostgreSQL 배포 시에는 Native Enum을 사용하도록 설정한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] SRS에 명시된 모든 Enum 타입이 `schema.prisma`에 정의되었는가?
- [ ] 각 모델의 상태 필드에 Enum 타입이 올바르게 매핑되었는가?
- [ ] 마이그레이션이 성공적으로 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-001 (Prisma 초기화)
- Blocks: #DB-003, #DB-005, #DB-008 등 Enum 사용 모델들
