---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PARSE-008: 커스텀 에디터 모드 전역 상태 연동 및 인라인 AI 명령 전송"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PARSE-008] 커스텀 에디터 모드 전역 상태 연동 및 인라인 AI 명령 전송
- 목적: 사용자가 문항 편집 영역에서 텍스트 형태로 AI에게 지시(예: "이 문항을 5점 척도로 바꿔줘")를 내릴 수 있는 인터페이스와 상태 제어를 담당한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L245)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 문항 카드별 'AI에게 요청하기' 인라인 입력 필드 구현
- [ ] 명령 전송 시 로딩 스피너 표시 및 업데이트된 문항 상태 수신 대기

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 인라인 명령 실행
- Given: 2번 문항 아래 AI 입력창 활성화
- When: "보기 순서를 무작위로 섞어줘" 입력 후 엔터
- Then: 로딩 후 2번 문항의 보기 배치가 변경된다.

## :gear: Technical & Non-Functional Constraints
- UX: AI 응답 대기 중 해당 문항에 대한 유저의 수동 편집 접근 일시 차단

## :checkered_flag: Definition of Done (DoD)
- [ ] 인라인 API 호출 에러 핸들링 검증

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-007
- Blocks: #FE-PARSE-009
