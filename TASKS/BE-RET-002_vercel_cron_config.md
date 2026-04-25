---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RET-002: Vercel Cron 설정 및 수동 삭제 npm script 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RET-002] Vercel Cron 설정 및 수동 삭제 npm script 구현
- 목적: Vercel의 Serverless 환경에서 삭제 스케줄러가 매시간 구동되도록 `vercel.json` 구성을 완료하고, 비상시 관리자가 실행할 Fallback 커맨드를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L168)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 프로젝트 루트의 `vercel.json` 파일에 `crons` 속성 추가 (매시간 동작 표현식)
- [ ] `package.json`에 `npm run cleanup` 수동 트리거용 CLI 명령어 구성
- [ ] 외부 트리거를 방지하기 위한 Cron Route Handler 인증 체크 구현 (Vercel 헤더 기반 검증)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 외부 비인가 크론 트리거 차단
- Given: Vercel Cron 시스템 외의 일반 브라우저가 크론 API 주소로 직접 접근
- When: GET 요청이 인입됨
- Then: 401 Unauthorized로 접근이 거부된다.

## :gear: Technical & Non-Functional Constraints
- 인프라: Vercel Hobby 무료 플랜 크론 실행 횟수 및 한도 준수

## :checkered_flag: Definition of Done (DoD)
- [ ] `vercel.json` 문법 에러 검사 통과

## :construction: Dependencies & Blockers
- Depends on: #BE-RET-001
- Blocks: None
