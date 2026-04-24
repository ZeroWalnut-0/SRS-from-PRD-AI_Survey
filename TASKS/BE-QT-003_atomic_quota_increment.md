---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-QT-003: 응답 제출 시 쿼터 카운트 원자적 증가 로직"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-QT-003] 응답 제출 시 쿼터 카운트 원자적 증가 로직
- 목적: 다수의 응답자가 동시에 설문을 제출할 때 발생할 수 있는 Race Condition을 방지하고, 목표 쿼터를 초과하지 않도록 DB 수준에서 원자적(Atomic)으로 카운트를 업데이트한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4_REQ-FUNC-019`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 동시성 제어 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#REQ-FUNC-020`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 시퀀스 다이어그램: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.6_QUOTA_CELL`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Supabase PostgreSQL에서 카운트 업데이트를 처리할 RPC(Stored Procedure) 함수 작성
- [ ] SQL 로직: `UPDATE QUOTA_CELL SET current_count = current_count + 1 WHERE cell_id = $1 AND current_count < target_count`
- [ ] 업데이트 성공 시 `true`, 실패(이미 쿼터 도달) 시 `false`를 반환하도록 설계
- [ ] `lib/services/quota.ts`에서 Prisma의 `$queryRaw` 또는 RPC 호출 인터페이스 구현
- [ ] 응답 제출 서비스(`BE-FORM-004`)와의 트랜잭션 연동
- [ ] 쿼터 도달 시 즉시 `is_full=true` 갱신 로직 추가

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상적인 쿼터 증가
- Given: 특정 쿼터 셀의 `current_count`가 10, `target_count`가 20인 상태
- When: 설문 응답이 제출되어 쿼터 증가 로직이 실행됨
- Then: `current_count`가 11로 증가하고, 성공 응답을 반환해야 한다.

Scenario 2: 쿼터 도달 시 차단
- Given: 특정 쿼터 셀의 `current_count`가 20, `target_count`가 20인 상태 (이미 도달)
- When: 새로운 설문 응답 제출이 시도됨
- Then: 카운트가 증가하지 않아야 하며, 쿼터 도달 에러(또는 리다이렉트 지시)가 발생해야 한다.

## :gear: Technical & Non-Functional Constraints
- 안정성: Supabase RPC 또는 트랜잭션을 사용하여 Race Condition 오차율 1% 이내 보장 (REQ-NF-013)
- 성능: 쿼터 연산 레이턴시 ≤ 1초 (REQ-NF-006)
- 모니터링: 연산 지연 시 Slack Webhook 발송 연계 (REQ-FUNC-021)

## :checkered_flag: Definition of Done (DoD)
- [ ] DB 레벨에서 원자적 증가가 보장되는 SQL/RPC 함수가 작성되었는가?
- [ ] 동시성 테스트(부하 테스트) 시 쿼터 초과 응답자가 발생하지 않는가?
- [ ] 쿼터 도달 시 `is_full` 필드가 즉시 업데이트되는가?
- [ ] 실패 시 적절한 예외 처리 및 로깅이 수행되는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-012 (RPC 함수 정의), #BE-FORM-004 (응답 제출 서비스)
- Blocks: #TEST-QT-002 (쿼터 오차율 테스트), #BE-QT-004 (쿼터 도달 알림)
