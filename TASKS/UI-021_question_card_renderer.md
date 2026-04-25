---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] UI-021: 문항 카드 컴포넌트 마크업(객관식, 주관식, 척도형)"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [UI-021] 문항 카드 컴포넌트 마크업
- 목적: 설문지에 들어갈 다양한 형태의 문항(단일 선택, 다중 선택, 단답형, 서술형, 리커트 5점 척도 등)을 시각적으로 구분하여 렌더링한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L837)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 객관식(Radio/Checkbox) 컴포넌트 스타일링
- [ ] 주관식(Input/Textarea) 컴포넌트 스타일링
- [ ] 문항 드래그 핸들러(Grab Icon) UI 추가

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 문항 타입 변경
- Given: 주관식 문항 카드
- When: '객관식'으로 타입 스위칭
- Then: 텍스트 입력창이 라디오 버튼 그룹으로 즉각 변경된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 접근성(ARIA Label) 속성 부여

## :construction: Dependencies & Blockers
- Depends on: #UI-001
- Blocks: #FE-FORM-003
