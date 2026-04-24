---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-001: 설문 에디터 레이아웃 및 문항 목록 렌더링"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-001] 설문 에디터 레이아웃 및 문항 목록 렌더링
- 목적: 파싱된 설문 데이터를 기반으로 문항들을 시각화하고, 드래그 앤 드롭으로 순서를 변경하거나 개별 문항을 선택할 수 있는 메인 에디터 화면을 구축한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2_REQ-FUNC-011`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- UI 컴포넌트: `dnd-kit` (드래그 앤 드롭), `shadcn/ui` (ScrollArea, Card)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(dashboard)/forms/[form_id]/edit/page.tsx` 생성
- [ ] 에디터 3단 레이아웃 구현:
    - 좌측: 문항 네비게이터 (Thumbnail/Index)
    - 중앙: 메인 캔버스 (문항 상세 내용 렌더링)
    - 우측: 문항 속성 설정 (로직, 필수 여부 등)
- [ ] `dnd-kit`을 활용한 문항 순서 변경(Reorder) 로직 구현
- [ ] 현재 선택된 문항 강조(Highlight) 처리 및 상태 관리

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 문항 순서 변경 테스트
- Given: 3개의 문항이 포함된 설문 에디터
- When: 1번 문항을 3번 문항 아래로 드래그함
- Then: 화면상에서 즉시 순서가 변경되어야 하며, 내부 데이터 모델의 `index` 정보가 갱신되어야 한다.

Scenario 2: 대량 문항 렌더링 성능
- Given: 100개 이상의 문항이 포함된 설문
- When: 에디터 페이지를 로드함
- Then: 가상 스크롤(Virtual Scroll) 등을 활용하여 초기 렌더링 및 스크롤 성능이 부드러워야 한다.

## :gear: Technical & Non-Functional Constraints
- 유지보수: 문항 타입별 렌더러를 컴포넌트로 분리하여 확장성을 확보한다.
- 성능: 문항 이동 시 불필요한 전체 리렌더링을 방지한다 (React.memo 활용).

## :checkered_flag: Definition of Done (DoD)
- [ ] 에디터 3단 레이아웃이 디자인대로 구현되었는가?
- [ ] 문항 순서 변경(Dnd) 기능이 정상 작동하는가?
- [ ] 선택된 문항에 대한 상태 관리가 정확히 이루어지는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-006 (미리보기 화면), #MOCK-002 (스키마 샘플)
- Blocks: #FE-FORM-002 (문항 수정), #FE-FORM-003 (문항 추가)
