---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-ADMIN-001: 관리자 통계 집계 로직"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-ADMIN-001] 관리자 통계 집계 로직
- 목적: 서비스의 핵심 성과 지표(가입자 수, 전체 설문 생성 건수, ZIP 패키지 유료 결제액 등)를 통합 집계하여 관리자 전용 화면에 송출한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.8`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L657)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Route Handler `/app/api/v1/admin/stats/route.ts` 작성
- [ ] Prisma `groupBy` 및 `count`, `sum` 연산을 활용한 KPI 데이터 쿼리
- [ ] 주기적 캐싱 처리(데이터가 많아질 경우를 대비)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 시스템 KPI 데이터 호출
- Given: 관리자(Admin) 등급의 계정으로 접근함
- When: 통계 데이터 호출 API가 실행됨
- Then: 200 OK와 함께 총 가입자 수 및 결제 지표가 반환된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 복잡한 통계 연산 수행 시 데이터베이스 락(Lock)이 걸리지 않도록 격리 수준 유지

## :checkered_flag: Definition of Done (DoD)
- [ ] 집계 결괏값의 정합성 검증(수동 데이터 검산)

## :construction: Dependencies & Blockers
- Depends on: #DB-010, #BE-RL-002
- Blocks: #FE-ADMIN-002
