---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-PARSE-005: Fallback 파싱 경로 동작 검증 테스트"
labels: 'test, backend, resilience, priority:medium'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-PARSE-005] Fallback 파싱 경로 동작 검증 테스트
- 목적: 메인 AI 엔진 장애 시 로컬 라이브러리 기반의 Fallback 로직이 정상적으로 작동하여 서비스 연속성을 유지하는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-PARSE-009 (Fallback 경로)
- 가용성 요건: 서비스 치명률 0.5% 이하 유지

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: Gemini API 호출 강제 실패 시뮬레이션
- [ ] 시나리오 2: Fallback 엔진을 통한 순수 텍스트 추출 결과 확인
- [ ] 시나리오 3: Fallback 결과물의 데이터 무결성(텍스트 누락 여부) 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: Gemini API Key를 의도적으로 잘못 설정하거나 호출을 차단함
- When: 문서 파싱을 시도함
- Then: 시스템이 에러를 뱉지 않고 Fallback 모드로 전환되어야 하며, 최소한 원본 문서의 텍스트가 DB에 저장되어야 한다.

## :gear: Technical Constraints
- 도구: Mocking (Gemini API 호출 가로채기)

## :checkered_flag: Definition of Done (DoD)
- [ ] AI 장애 상황에서도 파싱 프로세스가 "성공(Fallback)"으로 종료되는가?
- [ ] Fallback 실행 시 `AUDIT_LOG`에 기록이 남는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-002, #BE-PARSE-003, #BE-PARSE-004
- Blocks: None
