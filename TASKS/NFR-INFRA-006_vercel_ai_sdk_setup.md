---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] NFR-INFRA-006: Vercel AI SDK + Gemini API 초기 연동 설정"
labels: 'feature, infra, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-INFRA-006] Vercel AI SDK + Gemini API 초기 연동 설정
- 목적: 서버리스 환경에서 최적화된 LLM 연동을 위해 Vercel AI SDK를 프로젝트에 설치하고 Gemini 모델 공급자(Provider) 설정을 완료한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 기술 제약: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L55)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `ai` 및 `@ai-sdk/google` 패키지 설치
- [ ] `google('gemini-1.5-pro-latest')` 인스턴스 생성 유틸 함수 작성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 모델 응답 테스트
- Given: SDK 셋업 완료 및 API Key 설정
- When: 기본 프롬프트 "Hello" 전송
- Then: 정상적으로 텍스트 스트림 또는 JSON 응답이 리턴된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 모듈 로딩 속도 검증

## :construction: Dependencies & Blockers
- Depends on: #NFR-INFRA-005
- Blocks: #BE-PARSE-005
