---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RET-002: Vercel Cron 설정 및 수동 삭제 스크립트 작성"
labels: 'feature, backend, devops, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RET-002] Vercel Cron 설정 및 수동 삭제 스크립트 작성
- 목적: `BE-RET-001`에서 구현한 삭제 엔드포인트를 매시간 자동으로 호출하도록 설정하고, 비상시를 대비한 수동 삭제 도구를 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.1_EXT-09`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 인프라 가이드: `vercel.json` Cron 구성법

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `vercel.json` 파일에 `crons` 배열 정의
- [ ] 매 정각(Hourly)마다 `/api/v1/cron/cleanup` 호출 스케줄 설정
- [ ] 로컬 개발 환경에서 실행 가능한 수동 클린업 npm script 작성 (`scripts/cleanup.ts`)
- [ ] 배포 파이프라인에서 Cron 설정 유효성 검사 절차 추가

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정기 호출 확인
- Given: Vercel에 프로젝트 배포 완료
- When: 정시(예: 13:00)가 됨
- Then: Vercel 로그에 `GET /api/v1/cron/cleanup` 호출 기록과 성공 응답이 확인되어야 한다.

Scenario 2: 수동 스크립트 실행
- Given: 터미널 환경
- When: `npm run db:cleanup` 명령을 수행함
- Then: 만료된 데이터 삭제 프로세스가 즉시 가동되고 결과가 출력되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 가용성: Cron 호출 실패 시 Vercel 알림 또는 Slack 알림을 통해 즉각 인지할 수 있도록 한다.
- 보안: 수동 스크립트 실행 시 운영 DB 접근 권한 관리에 유의한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `vercel.json` 내 Cron 설정이 올바르게 구성되었는가?
- [ ] 수동 클린업 도구가 정상 작동하는가?
- [ ] 자동 삭제 주기가 비즈니스 요건(매시간)을 충족하는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-RET-001 (삭제 핸들러)
- Blocks: None
