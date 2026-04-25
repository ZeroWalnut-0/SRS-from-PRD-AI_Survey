---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-QT-004: 자연어 프롬프트 API 호출 및 할당표 자동 생성 결과 상태 반영"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-QT-004] 자연어 프롬프트 API 호출 및 할당표 자동 생성 결과 상태 반영
- 목적: 사용자가 "전국 20대 500명 표본" 등 자연어 지시문 입력 시, AI가 통계청 비례 데이터를 가공해 쿼터 셀을 자동 생성해 주는 컴포넌트를 연동한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L514)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 'AI로 할당표 자동 생성' 입력 텍스트 영역 UI
- [ ] 생성 버튼 클릭 시 자연어 텍스트를 백엔드로 발송 및 결과 JSON 바인딩

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 자연어로 쿼터 생성
- Given: 프롬프트 입력창에 조건 입력
- When: '생성' 클릭
- Then: 로딩 완료 후 쿼터 매트릭스에 조건별 셀 데이터가 자동 생성된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] API 통신 에러 시 로딩 원복

## :construction: Dependencies & Blockers
- Depends on: #FE-QT-001, #BE-QT-006
- Blocks: None
