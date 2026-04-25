---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-RET-001: 24시간 후 데이터 영구 삭제 스케줄러 테스트"
labels: 'test, automation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-RET-001] 24시간 후 데이터 영구 삭제 테스트
- 목적: Vercel Cron에 의해 매시간 구동되는 정리 작업이, 생성된 지 24시간이 지난 무료 플랜 데이터를 DB 및 Storage에서 완벽히 영구 삭제(Hard Delete)하는지 확인한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L538)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 25시간 전 생성된 더미 데이터 셋업
- [ ] 삭제 크론 라우트(`GET /api/v1/cron/cleanup`) 수동 트리거
- [ ] DB 레코드 및 스토리지 파일 존재 여부 조회

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 영구 삭제
- Given: 24시간 경과된 파일
- When: 크론 실행
- Then: 해당 데이터가 복구 불가능하게 완전 삭제된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 삭제 대상이 아닌(23시간 경과 등) 파일은 보존되었는지 교차 검증

## :construction: Dependencies & Blockers
- Depends on: #BE-RET-001, #BE-RET-002
- Blocks: None
