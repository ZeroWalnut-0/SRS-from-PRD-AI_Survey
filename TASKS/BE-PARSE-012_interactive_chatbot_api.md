---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-012: 대화형 챗봇 API 스트리밍 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-012] 대화형 챗봇 API 스트리밍 구현
- 목적: 유저가 대화창을 통해 추가 문항 생성을 요청할 경우, 기존 폼 구조를 인텍스트로 넘겨 실시간 스트리밍 형태로 업데이트한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L245)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js Route Handler 스트리밍 응답(SSE) 구성
- [ ] Vercel AI SDK `streamText` 함수와 Gemini API 통합

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 챗봇 지시 수행
- Given: 사용자의 "객관식 1문항 더 만들어줘" 발화
- When: API 호출
- Then: 청크 단위로 문항 생성 정보가 스트리밍되어 브라우저로 전송된다.

## :gear: Technical & Non-Functional Constraints
- 보안: 악의적인 프롬프트 주입(Prompt Injection) 방지 필터 적용

## :checkered_flag: Definition of Done (DoD)
- [ ] 데이터 전송 완료(END) 신호 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-011
- Blocks: #FE-PARSE-009
