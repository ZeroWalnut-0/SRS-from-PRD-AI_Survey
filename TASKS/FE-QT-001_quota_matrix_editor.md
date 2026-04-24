---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-QT-001: 교차 쿼터 설정 매트릭스 에디터 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-QT-001] 교차 쿼터 설정 매트릭스 에디터 구현
- 목적: 성별, 연령, 지역 등 다양한 조건이 결합된 복합 쿼터(할당)를 시각적으로 설정하고 엑셀 업로드를 통해 일괄 등록할 수 있는 인터페이스를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4_REQ-FUNC-018`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- UI 컴포넌트: `TanStack Table` (복합 헤더 테이블)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(dashboard)/forms/[form_id]/quota/page.tsx` 생성
- [ ] 쿼터 변수(성별, 연령, 지역 등) 선택 및 조합 생성 UI 구현
- [ ] 교차 쿼터 매트릭스 테이블 구현 (문항별 응답 제한 수치 입력 가능)
- [ ] 쿼터 설정 엑셀 업로드/다운로드 기능 연동
- [ ] 설정된 쿼터 데이터 저장 API (`POST /api/v1/quotas`) 호출

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 매트릭스 생성
- Given: 성별(2종)과 연령(3종) 변수를 선택함
- When: [매트릭스 생성] 버튼을 클릭함
- Then: 2x3 형태의 총 6개 셀이 포함된 입력 테이블이 생성되어야 한다.

Scenario 2: 엑셀 기반 일괄 설정
- Given: 미리 정의된 쿼터 양식 엑셀 파일
- When: 파일을 업로드함
- Then: 테이블의 각 셀에 엑셀 데이터가 정확히 매핑되어 채워져야 한다.

## :gear: Technical & Non-Functional Constraints
- UX: 복잡한 쿼터 구조에서도 데이터 입력 실수를 줄이기 위해 '합계 자동 계산' 기능을 제공한다.
- 성능: 100개 이상의 셀을 가진 매트릭스에서도 입력 지연이 없어야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 교차 쿼터 설정 테이블이 의도대로 렌더링되는가?
- [ ] 엑셀 업로드/다운로드 로직이 정상 작동하는가?
- [ ] 설정된 데이터가 서버로 정확히 전송되는가?

## :construction: Dependencies & Blockers
- Depends on: #MOCK-006 (쿼터 Mock), #API-010 (Quota DTO)
- Blocks: #BE-QT-001 (쿼터 설정 구현)
