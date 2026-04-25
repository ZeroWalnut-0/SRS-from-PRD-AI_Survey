---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-005: Vercel AI SDK + Gemini API 연동"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-005] Vercel AI SDK + Gemini API 연동
- 목적: 전처리된 문서 텍스트를 Google Gemini AI 모델에 주입하고, Vercel AI SDK의 `generateObject()`를 활용하여 규격화된 설문 폼 JSON(`structure_schema`)을 자동 생성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L493)
- 제약사항 (CON-05): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L55)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L742)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `@ai-sdk/google` 및 `ai` 패키지 초기화 및 API Key 바인딩
- [ ] 설문 구조 생성을 위한 Zod 스키마(`surveyStructureSchema`) 정의
- [ ] LLM 프롬프트 엔지니어링 (질문 유형 분류: 객관식, 주관식, 척도형 등)
- [ ] `generateObject()` 함수 호출 및 리턴된 JSON 객체 검증
- [ ] AI 주치의 가이드(오류 교정 정보) 동시 추출 로직 추가

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 성공적인 AI 설문 폼 생성
- Given: 전처리 완료된 문자열 데이터가 주어짐
- When: Gemini API에 요청을 전달함
- Then: Zod 규격에 100% 부합하는 `structure_schema` JSON 데이터가 정상 생성된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 전체 LLM 추론 레이턴시 ≤ 8,000ms (Vercel 10초 타임아웃 내 완료)
- 비용: 단건 파싱 당 API 사용량 통제 (원가 ≤ 20원 방어)

## :checkered_flag: Definition of Done (DoD)
- [ ] JSON 스키마 검증 도구(Zod parse) 통과 여부
- [ ] 환경 변수 변경 시 모델(예: Gemini Pro -> Gemini Flash) 전환 정상 동작 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-002, #BE-PARSE-003, #BE-PARSE-004
- Blocks: #BE-PARSE-006, #BE-PARSE-007
