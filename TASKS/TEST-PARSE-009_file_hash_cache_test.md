---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PARSE-009: 파일 해시 기반 중복 요청 캐시 검증 테스트"
labels: 'test, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PARSE-009] 파일 해시 기반 중복 요청 캐시 검증 테스트
- 목적: 동일한 파일을 다시 업로드했을 때, AI 파싱을 재실행하지 않고 기존에 저장된 결과를 즉시 반환하는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-PARSE-010 (파일 해시 캐시)
- 성공 기준: TC-FUNC-028

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 신규 파일 업로드 시 AI 파싱 로직 실행 여부 확인
- [ ] 시나리오 2: 동일 파일 재업로드 시 AI 호출 없이 즉시 COMPLETED 상태 반환 확인
- [ ] 시나리오 3: 내용이 1바이트라도 바뀐 경우 신규 파싱 실행 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 이미 파싱이 완료된 `A.hwpx` 파일 (해시값 `H1`)
- When: 다시 동일한 `A.hwpx` 파일을 업로드함
- Then: `DOCUMENT` 테이블의 `doc_id`는 새로 생성되되, `PARSED_FORM`은 기존 레코드를 참조하거나 데이터를 즉시 복사하여 응답 속도가 1초 이내여야 한다.

## :gear: Technical Constraints
- 도구: API Performance Test + Mocking (AI 호출 횟수 감시)

## :checkered_flag: Definition of Done (DoD)
- [ ] 동일 파일 감지 로직(SHA-256)이 정확히 작동하는가?
- [ ] 캐시 히트 시 AI API 호출이 발생하지 않는 것을 확인하였는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-010 (파일 해시 캐시)
- Blocks: None
