---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] TEST-F1-004: Gemini API 누락 문항 처리 로직 테스트"
labels: 'feature, test, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-F1-004] Gemini API 누락 문항 처리 로직 테스트
- 목적: AI가 문항 추출 시 특정 영역을 누락(Skip) 처리했을 때, 시스템이 이를 인지하고 프론트엔드 에디터에 경고 배지를 올바르게 표시하는지 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L225)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] AI 모킹 데이터를 통해 `skipped_elements`에 임의의 영역 정보 주입
- [ ] 폼 에디터 진입 시 해당 누락 영역 경고 모달 팝업 여부 검증

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 누락 문항 경고 확인
- Given: 누락 요소가 포함된 파싱 결과
- When: 사용자가 설문 편집 화면에 진입함
- Then: "AI가 분석하지 못한 2개의 영역이 있습니다." 알림이 발생한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 경고 렌더링 상태값 검증 완료

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-006
- Blocks: None
