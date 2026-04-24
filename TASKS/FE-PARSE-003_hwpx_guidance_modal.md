---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PARSE-003: HWPX 전환 안내 모달 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PARSE-003] HWPX 전환 안내 모달 구현
- 목적: 구형 HWP 확장자 파일을 업로드하려는 사용자에게 HWPX 전환 필요성을 안내하고 업로드 절차를 올바르게 유도한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-031`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 제약 사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#CON-01`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `components/parser/HwpConvertModal.tsx` 컴포넌트 생성
- [ ] `.hwp` 파일 감지 시 1초 이내 모달 팝업 로직 구현
- [ ] 모달 내용 구성: "HWPX로 저장하는 방법" 안내 텍스트 및 가이드 이미지/링크
- [ ] 업로드 중단 및 파일 초기화 로직 연동
- [ ] `shadcn/ui` Dialog 컴포넌트 활용

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: .hwp 파일 업로드 시도
- Given: 사용자가 `.hwp` 파일을 선택함
- When: 파일 검증 단계에서 확장자가 감지됨
- Then: 1초 이내에 HWPX 전환 안내 모달이 표시되어야 한다.

Scenario 2: 모달 닫기 및 재시도
- Given: 안내 모달이 표시된 상태
- When: [확인] 버튼을 클릭하거나 모달을 닫음
- Then: 선택되었던 파일이 초기화되고 다시 업로드할 수 있는 상태가 되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 확장자 감지 및 모달 노출까지 레이턴시 ≤ 1,000ms.
- UX: 사용자에게 친절한 톤앤매너로 안내 문구 작성.

## :checkered_flag: Definition of Done (DoD)
- [ ] `.hwp` 확장자 감지 로직이 정확히 작동하는가?
- [ ] 안내 모달이 1초 이내에 정상적으로 팝업되는가?
- [ ] 모달 내 가이드 내용이 SRS 명세대로 포함되었는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-001 (업로드 UI)
- Blocks: #TEST-PARSE-007 (HWP 안내 테스트)
