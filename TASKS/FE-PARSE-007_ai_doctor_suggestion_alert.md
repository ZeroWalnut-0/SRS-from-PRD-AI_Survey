---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PARSE-007: AI 주치의 제안 Alert 데이터 수신 및 자동 교정 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PARSE-007] AI 주치의 제안 Alert 데이터 수신 및 자동 교정 구현
- 목적: AI가 분석한 설문 설계상의 오류(예: 중복 문항, 편향된 보기) 제안 사항을 사용자에게 시각적 경고(Alert) 배지로 알리고, 수락 시 자동 일괄 적용한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L225)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 문항 카드 우상단 'AI 주치의 제안' 배지 UI 구현
- [ ] 배지 클릭 시 상세 제안 사유 및 '적용하기' 버튼이 담긴 팝오버/모달 노출
- [ ] 적용 시 상태 스토어의 문항 데이터를 즉시 치환하는 로직 연결

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: AI 제안 수락
- Given: "3번 문항 보기가 상호 배타적이지 않습니다." 경고 노출 중
- When: '적용하기' 버튼 클릭
- Then: 3번 문항의 보기가 AI가 추천한 수정본으로 즉각 업데이트된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 상태 롤백(되돌리기) 기능 정상 작동 여부

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-006, #BE-PARSE-005
- Blocks: None
