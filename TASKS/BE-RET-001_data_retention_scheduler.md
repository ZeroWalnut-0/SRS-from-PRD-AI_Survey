---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RET-001: Zero-Retention 자동 데이터 삭제 스케줄러 구현"
labels: 'feature, backend, security, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RET-001] Zero-Retention 자동 데이터 삭제 스케줄러 구현
- 목적: 개인정보 보호 및 저장 공간 효율화를 위해, 만료 시간(`expires_at`)이 지난 문서 파일과 관련 DB 레코드를 자동으로 영구 삭제한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.7_REQ-FUNC-029`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 기술 스택: Vercel Cron Jobs, Supabase Storage API

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `/api/v1/cron/cleanup` 엔드포인트 구현
- [ ] 만료된 레코드 조회: `DOCUMENT.expires_at <= NOW()`
- [ ] 연관 데이터 삭제 순서 정의:
    1. Supabase Storage 내 원본 파일 및 ZIP 패키지 삭제
    2. `DOCUMENT`, `PARSED_FORM`, `ZIP_DATAMAP` 등 DB 레코드 삭제 (또는 비식별화)
- [ ] 삭제 완료 후 `AUDIT_LOG`에 요약 정보(삭제된 문서 수 등) 기록
- [ ] 실패 건에 대한 로깅 및 관리자 알림(Slack) 연동

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 만료 문서 자동 삭제
- Given: `expires_at`이 현재 시각보다 이전인 문서 10건이 존재함
- When: 클린업 스케줄러가 실행됨
- Then: 해당 10건의 DB 레코드와 Storage 파일이 모두 삭제되어야 하며, 이후 조회 시 404가 발생해야 한다.

Scenario 2: 미만료 문서 보존
- Given: 아직 만료되지 않은(24시간 이내) 문서
- When: 스케줄러가 실행됨
- Then: 해당 문서는 삭제되지 않고 안전하게 보존되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 클린업 API는 외부에서 직접 호출할 수 없도록 시크릿 토큰(`CRON_SECRET`) 검증을 거쳐야 한다.
- 신뢰성: 파일 삭제 실패 시 DB 레코드를 남겨두어 재시도가 가능하도록 트랜잭션 관리를 수행한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 만료 데이터 선별 및 삭제 로직이 정확한가?
- [ ] Storage 파일과 DB 데이터 간의 정합성이 유지되는가?
- [ ] 삭제 프로세스가 감사 로그에 정확히 기록되는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-003, #DB-010, #NFR-INFRA-004 (Storage)
- Blocks: #BE-RET-002 (Cron 설정)
