---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-007: 파싱 완료 후 상태 갱신"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-007] 파싱 완료 후 상태 갱신
- 목적: 파싱 파이프라인의 모든 단계가 성공적으로 완료되었을 때, DB의 문서 처리 상태를 갱신하여 클라이언트가 완료 시점을 인지하게 한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L379)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L725)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 데이터베이스 내 `DOCUMENT.parsed_success` 필드를 `true`로 업데이트
- [ ] `DOCUMENT.status` 값을 `COMPLETED`로 영속화
- [ ] 예외/실패 시 `status`를 `FAILED`로 전환하고 적합한 `error_code` 기록

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 상태 갱신 정상 처리
- Given: 파싱 JSON이 성공적으로 저장됨
- When: 상태 업데이트 트랜잭션이 수행됨
- Then: DB 조회를 통해 해당 `doc_id`의 `status`가 `COMPLETED`로 변경된 것을 확인한다.

## :gear: Technical & Non-Functional Constraints
- 안정성: 상태 갱신 실패 시 전체 파이프라인의 원자성 보장(필요 시 DB Transaction 활용)

## :checkered_flag: Definition of Done (DoD)
- [ ] 상태 갱신 API 호출 결과 통합 테스트 통과

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005, #BE-PARSE-006
- Blocks: #FE-PARSE-002 (파싱 대기 상태 폴링 로직)
