---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-RET-001: 24시간 후 자동 데이터 영구 삭제 검증 테스트"
labels: 'test, backend, security, priority:high'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-RET-001] 24시간 후 자동 데이터 영구 삭제 검증 테스트
- 목적: 서비스 정책에 따라 생성 후 24시간이 경과한 문서 파일과 관련 DB 정보가 스케줄러에 의해 완전히 삭제되는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-RET-001 (삭제 스케줄러)
- 성공 기준: TC-FUNC-029

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: `expires_at`이 지난 데이터가 스케줄러 호출 시 삭제되는지 확인
- [ ] 시나리오 2: 삭제 후 Storage 버킷에 실제 파일이 존재하지 않는지 확인
- [ ] 시나리오 3: `AUDIT_LOG`에 삭제 작업 요약 기록 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 만료 시각이 1시간 지난 테스트 데이터 5건
- When: `/api/v1/cron/cleanup`을 수동 호출함
- Then: 대상 문서 5건의 레코드가 DB에서 제거되어야 하며, 연결된 Storage 파일도 404 상태여야 한다.

## :gear: Technical Constraints
- 도구: Supertest + Supabase Storage SDK

## :checkered_flag: Definition of Done (DoD)
- [ ] 데이터 삭제 프로세스가 명시된 만료 조건을 정확히 따르는가?
- [ ] 영구 삭제 후 복구가 불가능한 상태임을 확인하였는가?
- [ ] 연관된 모든 파편 데이터(Form, Response 등)가 함께 정리되는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-RET-001 (삭제 스케줄러)
- Blocks: None
