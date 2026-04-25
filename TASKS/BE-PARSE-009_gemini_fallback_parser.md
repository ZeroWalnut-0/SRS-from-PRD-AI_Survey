---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-009: Gemini API 장애 시 대체 파서(Fallback) 구현"
labels: 'feature, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-009] Gemini API 장애 시 대체 파서 구현
- 목적: 외부 거대언어모델(LLM) 서비스 장애 시에도 설문 변환 시스템의 가용성을 보장하기 위해 정규표현식 기반의 로컬 대체 파싱 경로를 구축한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- Fallback 정책: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L145)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Gemini API 호출부 `try-catch` 래핑
- [ ] 에러 캐칭 시 순수 텍스트를 "Q.", "1)", "①" 등의 정규식 패턴으로 문항 분할하는 JS 알고리즘 작성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: LLM API 503 Service Unavailable 발생
- Given: Gemini 서버 다운
- When: 문서 변환 시도
- Then: 예외가 터지지 않고 Fallback 알고리즘에 의해 정형화된 폼 스키마가 생성된다.

## :gear: Technical & Non-Functional Constraints
- 한계점: 척도형 등 복잡한 로직은 파싱되지 못할 수 있으므로 사용자에게 사전 고지 필요

## :checkered_flag: Definition of Done (DoD)
- [ ] Fallback 전환 로깅 기록 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005
- Blocks: None
