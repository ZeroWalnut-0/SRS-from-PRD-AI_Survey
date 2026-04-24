---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-RL-001: 일일 파싱 한도 제한 미들웨어 구현"
labels: 'feature, backend, security, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-RL-001] 일일 파싱 한도 제한 미들웨어 구현
- 목적: 무료 계정 사용자의 남용을 방지하기 위해 일일 최대 파싱 횟수(3회)를 체크하고 제한한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.6_REQ-FUNC-026`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 비즈니스 정책: 무료 계정 일일 3회 제한 (Phase 1 기준)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `middleware.ts` 또는 API 상위 레이어에 Rate Limit 로직 추가
- [ ] 현재 로그인한 사용자의 당일(KST 기준) `DOCUMENT` 생성 기록 조회
- [ ] 생성 횟수가 3회 이상일 경우 `POST /api/v1/documents/upload` 요청 차단
- [ ] 차단 시 HTTP 429 Too Many Requests 응답 및 안내 메시지 반환
- [ ] 유료 사용자의 경우 해당 한도 체크를 건너뛰는 예외 로직 구현

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 무료 계정 한도 내 요청
- Given: 오늘 파싱을 1회 수행한 무료 사용자
- When: 새로운 문서 업로드를 시도함
- Then: 요청이 수락되고 파싱 프로세스가 시작되어야 한다.

Scenario 2: 한도 초과 요청 차단
- Given: 오늘 이미 3회의 파싱을 완료한 무료 사용자
- When: 4번째 문서 업로드를 시도함
- Then: HTTP 429 에러가 발생하며 "오늘의 파싱 한도를 모두 사용하셨습니다"라는 메시지를 받아야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 한도 체크 쿼리가 전체 API 성능에 영향을 주지 않도록 인덱싱된 필드(`created_at`, `user_id`)를 활용한다.
- 정확성: 서버 시간대(UTC)와 한국 시간대(KST) 차이를 고려하여 날짜 경계선을 명확히 정의한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 일일 3회 제한 로직이 무료 사용자에게 정확히 적용되는가?
- [ ] 유료 사용자는 제한 없이 이용 가능한가?
- [ ] 429 에러 시 프론트엔드에서 적절한 UI(`FE-RL-001`)를 보여주는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-002 (USER), #DB-003 (DOCUMENT)
- Blocks: #TEST-PARSE-008 (한도 테스트)
