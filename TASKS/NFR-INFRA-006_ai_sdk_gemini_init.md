---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Infra] NFR-INFRA-006: Vercel AI SDK 및 Gemini API 초기 연동 검증"
labels: 'infrastructure, ai, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-INFRA-006] Vercel AI SDK 및 Gemini API 초기 연동 검증
- 목적: Vercel AI SDK를 사용하여 Google Gemini 모델에 대한 기본 호출이 성공하는지 확인하고, 환경 변수 설정을 통해 모델 교체가 용이한 구조인지 검증한다.

## :link: References (Spec & Context)
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3_C-TEC-005, 006`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 기술 스택: `ai` (Vercel AI SDK), `@google/generative-ai`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `ai` 및 관련 프로바이더 패키지 설치
- [ ] `lib/ai.ts` 내에 Gemini 모델 인스턴스 초기화 로직 구현
- [ ] 간단한 텍스트 생성 테스트용 Route Handler 작성 (`/api/test-ai`)
- [ ] 스트리밍 및 비스트리밍(generateText, generateObject) 호출 정상 동작 확인
- [ ] 환경 변수(`AI_MODEL_NAME`)를 통한 모델 버전(예: gemini-1.5-flash) 동적 변경 테스트

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: Gemini API Key 설정 완료
- When: `/api/test-ai`로 "Hello" 메시지를 보냄
- Then: AI 모델로부터 정상적인 응답이 반환되어야 하며, 호출 로그가 Vercel 런타임에 남아야 한다.

## :gear: Technical & Non-Functional Constraints
- 비용: 테스트 호출 시 발생하는 토큰 사용량을 모니터링한다.
- 가용성: API 호출 실패 시의 기본적인 에러 핸들링 패턴을 정의한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] Vercel AI SDK를 통한 Gemini 호출이 성공하는가?
- [ ] 모델 설정을 코드 수정 없이 환경 변수만으로 변경 가능한가?
- [ ] 파싱 로직 개발을 위한 기본 AI 유틸리티가 준비되었는가?

## :construction: Dependencies & Blockers
- Depends on: #NFR-INFRA-005
- Blocks: #BE-PARSE-005 (AI 파싱 로직)
