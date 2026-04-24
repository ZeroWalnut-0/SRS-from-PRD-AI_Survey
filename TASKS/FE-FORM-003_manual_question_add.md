---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-003: 수동 문항 추가 및 삭제 기능 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-003] 수동 문항 추가 및 삭제 기능 구현
- 목적: AI가 추출하지 못한 문항을 사용자가 직접 추가하거나, 불필요한 문항을 삭제할 수 있는 기능을 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2_REQ-FUNC-011`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 에디터 하단 또는 문항 사이에 [문항 추가] 플로팅 버튼 구현
- [ ] 문항 삭제(Delete) 아이콘 및 확인 모달 구현
- [ ] 문항 복제(Duplicate) 기능 구현 (기존 문항의 속성을 그대로 복사)
- [ ] 문항 추가/삭제 시 인덱스(ID) 자동 재정렬 로직 구현
- [ ] 실행 취소(Undo) 및 다시 실행(Redo) 기능의 기초 상태 관리 (선택 사항)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 신규 문항 삽입
- Given: 1번 문항과 2번 문항 사이
- When: [+] 버튼을 눌러 문항을 추가함
- Then: 새로운 '단일 선택' 기본형 문항이 2번에 삽입되고 기존 2번 문항은 3번으로 밀려나야 한다.

Scenario 2: 문항 삭제 확인
- Given: 삭제할 문항 선택
- When: 삭제 버튼 클릭 후 확인 모달에서 승인함
- Then: 해당 문항이 목록에서 제거되고 나머지 문항들의 번호가 자동으로 갱신되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 무결성: 모든 문항 삭제 시 "문항이 없습니다" 안내 메시지와 함께 [추가] 유도 UI를 노출한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 문항 추가/삭제/복제 로직이 데이터 모델에 정확히 반영되는가?
- [ ] 인덱스 재정렬이 시각적 번호와 일치하는가?
- [ ] 삭제 시 실수 방지를 위한 확인 단계가 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-001 (에디터 레이아웃)
- Blocks: None
