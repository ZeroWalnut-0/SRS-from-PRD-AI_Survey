---
name: Feature/Logic Task
about: 관리자 통계 집계 로직 구현
title: "[Feature/Query] BE-ADMIN-001: 시스템 전반 결제 및 파싱 통계 집계 로직 구현"
labels: 'backend, admin, logic'
assignees: ''
---

## :dart: Summary
- 목적: `DOCUMENT`, `RESPONSE`, `ZIP_DATAMAP`, `AUDIT_LOG` 테이블을 참조하여 시스템 운영에 필요한 핵심 지표를 산출하는 백엔드 로직을 구현한다.

## :link: References (Spec & Context)
- SRS 문서: `§4.2.8 REQ-NF-033 ~ 037`
- 관련 API: `API-016`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] [Query] 전체 파싱 통계 산출:
    - `total`: 전체 문서 수
    - `completed`: `status = 'COMPLETED'` 수
    - `failed`: `status = 'FAILED'` 수
- [ ] [Query] 결제 통계 산출:
    - `total_revenue`: `payment_cleared = true`인 금액 합계
    - `conversion_count`: 결제 완료 건수
- [ ] [Query] 일자별 추이 집계: 최근 30일간의 일일 업로드 및 결제량 그룹화 (Prisma `groupBy`)
- [ ] [Logic] 관리자 권한(`role === 'ADMIN'`) 검증 미들웨어 연동

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 통계 데이터 정확성 검증
- Given: DB에 100건의 문서와 10건의 결제 데이터가 존재함
- When: 관리자 통계 API를 호출하면
- Then: 반환된 `total_documents`가 100, `conversion_rate`가 10%로 계산되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 복잡한 조인 연산 시 타임아웃(10초)을 피하기 위해 인덱스(`status`, `created_at`) 활용 필수.
- 정확도: 결제 데이터는 `payment_cleared` 필드뿐만 아니라 `pg_transaction_id` 존재 여부도 교차 검증.

## :checkered_flag: Definition of Done (DoD)
- [ ] Prisma를 활용한 통계 쿼리가 정상 작동하는가?
- [ ] 관리자가 아닌 사용자의 접근이 차단되는가?

## :construction: Dependencies & Blockers
- Depends on: `API-016`, `DB-010`
- Blocks: `FE-ADMIN-002`
