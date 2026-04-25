---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-005: 설문 폼 실시간 미리보기(Preview) 화면 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-005] 설문 폼 실시간 미리보기 화면 구현
- 목적: 설문 작성자가 배포 전 응답자의 화면을 데스크톱 및 모바일 뷰포트로 가상 체험할 수 있는 샌드박스 영역을 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L267)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 에디터 우측 또는 탭 영역에 미리보기 뷰어 설계
- [ ] 데스크톱/모바일 해상도 토글 스위치 배치
- [ ] 현재 작성 중인 문항 데이터를 실시간으로 반영하는 컴포넌트 바인딩

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 에디터 수정 사항 반영
- Given: 에디터에서 1번 문항 질문을 '수정 전'에서 '수정 후'로 변경함
- When: 실시간 미리보기 화면을 주시함
- Then: 별도 새로고침 없이 미리보기 화면의 텍스트도 즉시 변경된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 불필요한 리렌더링 방지를 위해 React.memo 활용

## :checkered_flag: Definition of Done (DoD)
- [ ] 뷰포트 전환 시 레이아웃 틀어짐 유무 검사

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-002, #FE-FORM-003
- Blocks: #FE-FORM-006
