---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-007: AI 내러티브 리포트 산출 로직 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-007] AI 내러티브 리포트 산출 로직 구현
- 목적: 수집된 응답 통계 수치를 기반으로 LLM(Gemini)을 호출하여 비즈니스 인사이트 및 종합 소결이 포함된 마크다운 형태의 내러티브 리포트를 자동 생성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#2.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L102)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 문항별 빈도 분석/교차 분석 기초 데이터 추출 쿼리 작성
- [ ] Vercel AI SDK `generateText`를 활용해 데이터 기반 요약 보고서 생성 프롬프트 작성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 보고서 정상 출력
- Given: 응답 100건 데이터셋
- When: 내러티브 생성 API 구동
- Then: "## 1. 핵심 요약..." 형태의 마크다운 텍스트가 3초 이내에 성공적으로 반환된다.

## :gear: Technical & Non-Functional Constraints
- 제한: 10초의 서버리스 타임아웃을 준수하기 위해 배치 연산을 최소화하고 빠른 분석 Prompt 설계

## :checkered_flag: Definition of Done (DoD)
- [ ] 생성된 마크다운의 문맥 정합성 검토

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-003
- Blocks: None
