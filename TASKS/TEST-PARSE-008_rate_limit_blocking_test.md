---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PARSE-008: 일일 파싱 한도 초과(429) 차단 테스트"
labels: 'test, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PARSE-008] 일일 파싱 한도 초과(429) 차단 테스트
- 목적: 무료 사용자가 일일 3회 파싱 한도를 초과하여 요청할 경우 서버에서 정확히 차단하고 에러를 반환하는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-RL-001 (한도 미들웨어)
- 성공 기준: TC-FUNC-026

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 3회까지의 정상 파싱 수행 확인
- [ ] 시나리오 2: 4회째 요청 시 HTTP 429 응답 확인
- [ ] 시나리오 3: 유료 사용자의 경우 4회 이상 요청 시에도 성공 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 오늘 이미 3번의 파싱을 완료한 무료 사용자 계정
- When: 4번째 파싱 API를 호출함
- Then: 서버는 HTTP 429 상태 코드를 반환해야 하며, DB에 새로운 문서 레코드가 생성되지 않아야 한다.

## :gear: Technical Constraints
- 도구: API Integration Test (Supertest)

## :checkered_flag: Definition of Done (DoD)
- [ ] Rate Limit 정책이 무료/유료 등급에 따라 차별적으로 적용되는가?
- [ ] 429 에러 응답 시 사용자 안내 메시지가 포함되어 있는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-RL-001 (한도 미들웨어)
- Blocks: None
