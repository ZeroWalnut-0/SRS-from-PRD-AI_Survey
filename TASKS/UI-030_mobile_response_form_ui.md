---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] UI-030: 모바일 최적화 설문 응답 폼 렌더러 마크업"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [UI-030] 모바일 최적화 설문 응답 폼 렌더러 마크업
- 목적: 실제 설문 참여자가 모바일 기기(스마트폰)로 접속했을 때, 한 화면에 1문항씩 집중하여 응답할 수 있도록 깔끔한 카드 스와이프 스타일의 UI를 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- UI 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L837)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 100vh(화면 꽉 참) 기준의 문항 카드 중앙 정렬 레이아웃
- [ ] 문항 전환 시 좌우 슬라이딩 애니메이션(Framer Motion) 적용

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 모바일 뷰포트 대응
- Given: 모바일 해상도
- When: 응답자가 '다음' 버튼 터치
- Then: 부드러운 애니메이션과 함께 다음 문항 카드가 화면 중앙으로 슬라이드 인 된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 모바일 가상 키보드가 올라왔을 때 레이아웃 깨짐 방지(Viewport Fit) 확인

## :construction: Dependencies & Blockers
- Depends on: #UI-001, #FE-FORM-007
- Blocks: None
