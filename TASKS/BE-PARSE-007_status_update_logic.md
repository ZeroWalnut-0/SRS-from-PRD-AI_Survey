---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-007: 파싱 완료 후 DOCUMENT 상태 갱신 로직 구현"
labels: 'feature, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-007] 파싱 완료 후 DOCUMENT 상태 갱신 로직 구현
- 목적: AI 파싱 파이프라인의 최종 단계에서 `DOCUMENT` 테이블의 상태를 업데이트하여, 클라이언트가 파싱 완료를 인지하고 화면을 전환할 수 있도록 한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.1_DOCUMENT`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 파싱 성공 시 처리:
    - `DOCUMENT.parsed_success = true` 업데이트
    - `DOCUMENT.status = 'COMPLETED'` 업데이트
- [ ] 파싱 실패 시 처리:
    - `DOCUMENT.parsed_success = false` 업데이트
    - `DOCUMENT.status = 'FAILED'` 업데이트
    - 에러 코드 및 상세 사유 기록
- [ ] 전체 과정을 단일 트랜잭션 또는 원자적 연산으로 처리하여 데이터 무결성 보장

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 파싱 성공 시 상태 전이 확인
- Given: AI 파싱 작업이 성공적으로 종료됨
- When: 상태 갱신 함수가 호출됨
- Then: DB의 해당 `doc_id` 레코드의 `status`가 `COMPLETED`로 변경되어야 한다.

Scenario 2: 예외 발생 시 실패 기록
- Given: 파싱 도중 타임아웃 또는 API 에러가 발생함
- When: 캐치된 에러를 처리함
- Then: `status`가 `FAILED`로 변경되고, 프론트엔드에서 에러 모달을 띄울 수 있는 에러 정보가 저장되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 상태 갱신 DB 요청은 100ms 이내에 완료되어야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 성공/실패에 따른 상태 전이 로직이 완벽히 구현되었는가?
- [ ] 에러 발생 시의 로그 기록이 정확한가?
- [ ] 마이그레이션된 `DocumentStatus` Enum을 올바르게 사용하는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005 (AI SDK 연동), #DB-003 (DOCUMENT 테이블)
- Blocks: #BE-PARSE-008 (상태 조회 API)
