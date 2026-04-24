---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-005: 실시간 모바일 미리보기 팝업 구현"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-005] 실시간 모바일 미리보기 팝업 구현
- 목적: 에디터에서 편집 중인 설문이 실제 응답자의 모바일 기기에서 어떻게 보이는지 실시간으로 확인하여 디자인 및 문구 오차를 줄인다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2_REQ-FUNC-012`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- UI 프레임: 아이폰/안드로이드 가상 베젤(Frame) UI

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 에디터 상단 [미리보기] 버튼 구현 및 모달/드로워 연동
- [ ] 모바일 뷰 시뮬레이터 UI 구현:
    - 360x800 규격의 Iframe 또는 Container 구성
    - 실제 모바일 렌더링 엔진(`FE-FORM-007`) 재사용
- [ ] 에디터 내 데이터 변경 시 미리보기 화면 실시간 갱신(Sync) 로직 구현
- [ ] 가로/세로 모드 전환 기능 (선택 사항)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 미리보기 실행
- Given: 설문 편집 중
- When: [미리보기] 버튼을 클릭함
- Then: 화면 중앙에 모바일 형태의 팝업이 뜨고 현재 편집 중인 내용이 그대로 노출되어야 한다.

Scenario 2: 실시간 동기화 확인
- Given: 미리보기 팝업이 띄워진 상태
- When: 에디터에서 문항 제목을 수정함
- Then: 미리보기 화면 내의 문항 제목도 지연 없이(≤ 300ms) 업데이트되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 미리보기 화면 갱신 시 불필요한 네트워크 요청 없이 클라이언트 상태를 직접 참조한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 모바일 기기 프레임 내에서 설문이 정상 렌더링되는가?
- [ ] 에디터 상태값과 실시간 동기화가 이루어지는가?
- [ ] 실제 모바일 응답 폼(`FE-FORM-007`)의 로직이 미리보기에서도 동일하게 작동하는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-001 (에디터), #FE-FORM-007 (모바일 폼 렌더링)
- Blocks: None
