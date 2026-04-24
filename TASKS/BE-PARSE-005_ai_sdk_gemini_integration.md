---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-005: Vercel AI SDK + Gemini API 연동"
labels: 'feature, backend, ai, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-005] Vercel AI SDK + Gemini API 연동
- 목적: 업로드된 문서에서 추출된 텍스트를 Google Gemini API로 전달하여, 구조화된 설문 스키마(JSON)로 변환하고 DB에 저장한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-002`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 기술 스택: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#C-TEC-005`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 시퀀스 다이어그램: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2_PARSED_FORM`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Vercel AI SDK (`ai` 패키지) 및 Google Gemini Provider (`@ai-sdk/google`) 설치
- [ ] `lib/services/parser.ts` 내 `generateObject()` 함수 구현
- [ ] 설문 구조화를 위한 Zod 스키마 정의 (`question_title`, `options`, `question_type` 등)
- [ ] Gemini API 호출용 프롬프트 엔지니어링 (정밀도 향상을 위한 Few-shot 포함)
- [ ] 파싱 결과를 `PARSED_FORM` 테이블에 저장하는 비즈니스 로직 구현
- [ ] 10초 타임아웃 이내 처리를 위한 최적화 (Vercel Serverless 제약 고려)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상적인 문서 파싱 및 JSON 생성
- Given: 전처리된 텍스트(문서 내용)가 주어짐
- When: `generateObject()`를 통해 Gemini API에 파싱을 요청함
- Then: 정의된 Zod 스키마를 준수하는 JSON 객체가 반환되고 DB에 저장되어야 한다.

Scenario 2: 파싱 실패 시 예외 처리
- Given: 비정상적이거나 의미를 알 수 없는 텍스트가 주어짐
- When: 파싱을 시도함
- Then: 적절한 에러 로그를 남기고, 사용자에게 파싱 실패 안내를 제공(FAILED 상태 갱신)해야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 전체 파싱 레이턴시 ≤ 15초 (SRS REQ-NF-002 준수)
- 비용: Gemini Free Tier 쿼터 범위 내 운영 (REQ-NF-021)
- 인프라: 환경 변수로 Gemini API Key를 관리하며, Vercel AI SDK 표준을 준수하여 모델 교체가 용이해야 함.

## :checkered_flag: Definition of Done (DoD)
- [ ] `generateObject()` 호출을 통해 구조화된 JSON이 성공적으로 생성되는가?
- [ ] 결과 데이터가 `PARSED_FORM` 테이블에 올바르게 Insert 되는가?
- [ ] 50문항 규모의 샘플 문서 파싱이 10초 내외로 완료되는가?
- [ ] API Key 등 민감 정보가 환경 변수로 관리되고 있는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-002 (HWPX 전처리), #BE-PARSE-003 (Word 전처리), #BE-PARSE-004 (PDF 전처리), #DB-004 (PARSED_FORM 테이블)
- Blocks: #BE-PARSE-006 (스킵 요소 기록), #TEST-PARSE-001 (기능 테스트)
