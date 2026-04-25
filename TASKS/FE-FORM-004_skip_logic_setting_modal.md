---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-004: 스킵 로직(분기문) 설정 모달 컴포넌트 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-004] 스킵 로직 설정 모달 컴포넌트 구현
- 목적: 보기 선택에 따른 설문 분기(예: 1번 보기 선택 시 5번 문항으로 이동) 조건을 설정할 수 있는 시각적 모달을 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L254)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Headless UI 또는 Radix UI Dialog 기반 모달 뼈대 구축
- [ ] 현재 문항의 보기 리스트 추출 및 '이동할 문항' 선택 Select 컴포넌트 연결
- [ ] 무한 루프 방지를 위해 현재 문항보다 앞선 문항으로의 이동 제한 처리

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 분기 설정 저장
- Given: 2번 보기 선택 시 4번 문항으로 스킵 조건 설정
- When: '적용' 버튼 클릭
- Then: 내부 Store 데이터 구조의 해당 보기 속성에 `skipTo: 4`가 올바르게 주입된다.

## :gear: Technical & Non-Functional Constraints
- 무결성: 대상 문항이 삭제되었을 경우 연결된 스킵 로직을 자동으로 해제하는 정화 로직 연동 필수

## :checkered_flag: Definition of Done (DoD)
- [ ] 설정된 로직이 모달을 닫았다 열어도 올바르게 바인딩되어 있는지 확인

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-003
- Blocks: None
