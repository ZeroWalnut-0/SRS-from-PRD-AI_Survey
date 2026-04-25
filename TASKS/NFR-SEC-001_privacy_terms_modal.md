---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] NFR-SEC-001: 개인정보 취급방침 약관 동의 팝업 UI 구현"
labels: 'feature, security, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-SEC-001] 개인정보 취급방침 약관 동의 팝업 UI 구현
- 목적: 설문 참여 전, 수집되는 개인정보(비식별 IP 등)에 대해 법적 규제 준수를 위한 동의 절차를 거친다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 제약사항 (CON-02): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L55)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 설문 진입 시 최우선으로 노출될 모달 컴포넌트 작성
- [ ] 동의 체크박스 해제 시 '설문 시작' 버튼 비활성화 로직

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 비동의 상태
- Given: 약관 미동의 상태
- When: 설문 시작 시도
- Then: 에러 툴팁이 출력되며 진입이 불허된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 동의 상태 세션 스토리지 기록 확인

## :construction: Dependencies & Blockers
- Depends on: #FE-SURV-001
- Blocks: None
