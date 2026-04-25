---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RL-001: 인증 및 Rate Limit 미들웨어 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RL-001] 인증 및 Rate Limit 미들웨어 구현
- 목적: 무료 플랜 유저 및 비로그인 접속자의 악의적인 서버 요청을 방지하고, 일일 파싱 제한(3회)을 수행한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L548)
- 제약사항 (CON-03): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L55)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js `middleware.ts` 파일 생성/확장
- [ ] 요청 클라이언트의 IP 추출 및 유저 토큰 검증
- [ ] DB의 `AUDIT_LOG` 또는 파싱 카운트를 집계하여 일일 3회 도달 체크
- [ ] 초과 시 429 Too Many Requests 에러 반환

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 일일 파싱 4회째 요청
- Given: 오늘 이미 3번의 문서 파싱을 성공적으로 마침
- When: 4번째 파일 업로드를 시도함
- Then: 429 에러 코드와 한도 초과 안내가 표시된다.

## :gear: Technical & Non-Functional Constraints
- 보안: IP 스푸핑(Spoofing) 방지를 위한 신뢰할 수 있는 헤더(X-Forwarded-For) 검사

## :checkered_flag: Definition of Done (DoD)
- [ ] 3회 차단 검증 테스트 통과

## :construction: Dependencies & Blockers
- Depends on: #DB-002, #DB-010
- Blocks: None
