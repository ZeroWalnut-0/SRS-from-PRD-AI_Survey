---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-006: 설문 최종 배포 확인 모달 컴포넌트 구현"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-006] 설문 최종 배포 확인 모달 컴포넌트 구현
- 목적: 설문 배포 후에는 문항 수정이 불가하므로, 사용자에게 최종 경고와 동의를 받아 배포 요청을 확정한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L270)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 배포 확인 다이얼로그 마크업
- [ ] '배포 후 수정이 불가능함에 동의합니다' 체크박스 컴포넌트 구현
- [ ] 체크 시에만 '최종 배포' 활성화되는 버튼 제어 로직

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 동의 전 배포 시도 차단
- Given: 동의 체크박스가 해제되어 있음
- When: 배포 버튼을 클릭하려고 함
- Then: 버튼이 비활성화(`disabled`)되어 클릭되지 않는다.

## :gear: Technical & Non-Functional Constraints
- 안정성: 중복 클릭 방지(Debounce / Loading State) 적용

## :checkered_flag: Definition of Done (DoD)
- [ ] 성공적인 배포 API 연동 및 완료 화면 전환 확인

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-005, #API-006
- Blocks: None
