---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-QT-004: 쿼터 도달 자동 감지 및 Slack Webhook 알림 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-QT-004] 쿼터 도달 자동 감지 및 Slack Webhook 알림 구현
- 목적: 특정 쿼터 셀의 응답이 목표치(target_count)에 도달했을 때, 이를 실시간으로 감지하여 `is_full` 상태를 갱신하고 관리자에게 알림을 발송한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4_REQ-FUNC-022`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 태스크 리스트: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/06_TASK_LIST.md#L153`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/06_TASK_LIST.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `BE-QT-003` (원자적 증가) 수행 후 `current_count >= target_count` 여부 체크 로직 추가
- [ ] 조건 충족 시 `QUOTA_CELL.is_full = true` 갱신 트랜잭션 수행
- [ ] Slack Webhook 통합 모듈(`lib/slack.ts`) 구현
- [ ] 쿼터 도달 메시지 템플릿 작성 (설문명, 쿼터명, 완료 시각 포함)
- [ ] 비동기 방식으로 Slack 알림 발송 트리거

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 도달 감지 및 DB 갱신
- Given: 특정 쿼터의 `target_count`가 100이고 `current_count`가 99임
- When: 마지막 1건의 응답이 제출되어 카운트가 100이 됨
- Then: 해당 `QUOTA_CELL`의 `is_full` 필드가 `true`로 자동 변경되어야 한다.

Scenario 2: Slack 알림 발송
- Given: 쿼터가 가득 참(`is_full = true`)
- When: 알림 발송 로직이 실행됨
- Then: 연동된 Slack 채널로 "[Quota Full] 설문 A의 '남성-20대' 쿼터가 마감되었습니다" 메시지가 전송되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 무결성: DB 갱신과 카운트 체크는 반드시 원자적(Atomic)으로 이루어져야 한다.
- 가용성: Slack API 장애가 본 설문 응답 과정에 영향을 주지 않도록 예외 처리(Try-Catch)를 철저히 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 쿼터 도달 시 `is_full` 상태가 지연 없이 반영되는가?
- [ ] Slack 알림 메시지가 정확한 내용을 담고 있는가?
- [ ] 알림 발송 로직이 비동기로 처리되어 응답 레이턴시에 영향을 주지 않는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-QT-003 (원자적 증가), #NFR-INFRA-005 (환경 변수)
- Blocks: #TEST-QT-005 (도달 검증 테스트)
