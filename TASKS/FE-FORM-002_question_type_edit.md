---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-002: 문항 타입 변경 및 옵션 편집 UI 구현"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-002] 문항 타입 변경 및 옵션 편집 UI 구현
- 목적: 개별 문항의 유형(객관식 ↔ 주관식 ↔ 척도형 등)을 변경하고, 객관식 문항의 선택지(Option)를 추가/삭제/수정할 수 있는 기능을 제공한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2_REQ-FUNC-011`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: `structure_schema` JSON 규격

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 문항 유형 선택용 `Select` 컴포넌트 구현 (단일 선택, 다중 선택, 주관식 단답/장문, 5점 척도 등)
- [ ] 선택지(Option) 관리 UI 구현:
    - [추가] 버튼 클릭 시 새로운 옵션 행 생성
    - [삭제] 버튼 클릭 시 해당 옵션 삭제
    - [순서 변경] 선택지 내 드래그 앤 드롭
- [ ] 문항 제목(Title) 및 안내 문구(Description) 실시간 편집 로직 구현
- [ ] 필수 응답 여부(Required) 토글 스위치 추가

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 객관식 옵션 수정
- Given: 3개의 선택지가 있는 단일 선택 문항
- When: 4번째 선택지를 추가하고 텍스트를 입력함
- Then: 내부 `structure_schema` 데이터에 4번째 옵션이 즉시 반영되어야 한다.

Scenario 2: 문항 유형 변경 시 데이터 변환
- Given: 객관식 문항(선택지 포함)
- When: 주관식으로 유형을 변경함
- Then: 기존 선택지 데이터는 유지(또는 경고 후 삭제)되면서 입력 폼이 텍스트 영역으로 전환되어야 한다.

## :gear: Technical & Non-Functional Constraints
- UX: 'Enter' 키 입력 시 자동으로 다음 선택지 행이 생성되도록 하여 편집 편의성을 높인다.
- 무결성: 최소 1개 이상의 선택지가 있어야 하는 등의 제약 조건을 실시간으로 검증한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 모든 지원 문항 유형으로의 상호 전환이 가능한가?
- [ ] 선택지 편집 로직이 데이터 모델과 정확히 연동되는가?
- [ ] 실시간 유효성 검사(제목 누락 등)가 작동하는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-001 (에디터 레이아웃)
- Blocks: #BE-FORM-002 (수정 API 연동)
