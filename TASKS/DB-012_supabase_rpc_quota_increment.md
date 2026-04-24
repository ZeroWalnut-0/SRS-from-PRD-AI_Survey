---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-012: 쿼터 카운트 원자적 증가를 위한 Supabase RPC 함수 작성"
labels: 'feature, backend, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-012] 쿼터 카운트 원자적 증가를 위한 Supabase RPC 함수 작성
- 목적: 동시 응답자가 많은 상황에서도 정확한 쿼터 카운팅을 보장하기 위해, 데이터베이스 수준에서 원자적(Atomic) 증가 및 조건 체크를 수행하는 PL/pgSQL 함수를 작성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 기술 스택 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#C-TEC-008`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md) (Supabase RPC 활용)
- 동시성 요건: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4_REQ-FUNC-020`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Supabase SQL Editor 또는 마이그레이션 스크립트를 통해 `increment_quota_cell` 함수 작성
- [ ] 함수 로직 설계:
    1. `cell_id`를 파라미터로 수신
    2. 해당 셀의 `current_count`가 `target_count`보다 작은지 확인
    3. 조건 충족 시 `current_count`를 1 증가시키고 `true` 반환
    4. 조건 미충족(쿼터 도달) 시 증가시키지 않고 `false` 반환
- [ ] 쿼터 도달 시 `is_full` 필드를 자동으로 `true`로 갱신하는 로직 포함
- [ ] Prisma Client에서 해당 RPC를 호출할 수 있도록 `$queryRaw` 또는 전용 인터페이스 준비

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 원자적 증가 성공
- Given: 특정 쿼터 셀의 잔여 쿼터가 존재함
- When: `increment_quota_cell` 함수를 호출함
- Then: DB 레벨에서 즉시 카운트가 증가하고 `true`를 반환해야 한다.

Scenario 2: 동시성 상황에서의 오차율 0% 확인
- Given: 다수의 세션이 동시에 동일한 `cell_id`에 대해 함수를 호출함
- When: 호출 횟수가 `target_count`를 초과함
- Then: 최종 `current_count`는 정확히 `target_count`와 일치해야 하며, 그 이상의 증가는 차단되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 해당 함수는 응답 제출 시마다 호출되므로 실행 시간이 100ms 이내여야 한다.
- 무결성: 로우 레벨 락(Row-level Lock) 또는 단일 업데이트 트랜잭션을 사용하여 동시성을 보장한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] PL/pgSQL 함수 스크립트가 작성되었는가?
- [ ] Supabase Dashboard에서 함수가 정상적으로 등록되었는가?
- [ ] 테스트 호출 시 성공/실패 케이스가 의도대로 동작하는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-008 (QUOTA_CELL 테이블)
- Blocks: #BE-QT-003 (쿼터 카운트 연동), #TEST-QT-003 (동시성 테스트)
