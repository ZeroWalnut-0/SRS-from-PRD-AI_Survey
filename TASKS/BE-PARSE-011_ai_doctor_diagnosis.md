---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-011: AI 주치의 진단 로직 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-011] AI 주치의 진단 로직 구현
- 목적: 파싱이 완료된 설문 데이터 구조를 LLM을 이용해 재검토하여, 설문 조사 품질을 저해할 수 있는 논리적 모순점을 분석 및 제안한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L225)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 진단용 프롬프트 템플릿(System Prompt) 정립
- [ ] Gemini API 호출 로직 구현 및 응답 데이터 구조화(JSON)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 편향 문항 진단
- Given: 파싱된 문항 중 "우리 제품이 최고인데 동의하십니까?" 존재
- When: 진단 API 구동
- Then: "문항 유도 편향성" 지적 메시지가 결과 객체에 포함된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 진단 실패 시 로깅 및 무응답 예외 처리

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005
- Blocks: #FE-PARSE-007
