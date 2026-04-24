---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-006: 쿼터 설정/조회 Mock API 및 샘플 데이터 작성"
labels: 'feature, foundation, mock, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-006] 쿼터 설정/조회 Mock API 및 샘플 데이터 작성
- 목적: 복잡한 교차 쿼터(성별×연령×지역) 설정 및 실시간 모니터링 대시보드 개발을 지원하기 위해 Mock 데이터를 준비한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#8`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md), [`#6.1_#9`](#)
- 쿼터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.6_QUOTA_CELL`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 교차 쿼터 매트릭스 샘플 JSON 작성 (예: 2x3x5 구조의 복합 할당)
- [ ] `POST /api/v1/quotas` Mock 핸들러 작성
- [ ] `GET /api/v1/quotas/{quota_id}/status` Mock 핸들러 작성
- [ ] 대시보드 시각화용 실시간 카운트 변동 시뮬레이션 데이터 구성 (일부 셀이 Full인 케이스 포함)
- [ ] 쿼터 설정용 샘플 엑셀 파일 작성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 쿼터 모니터링 대시보드 렌더링
- Given: 다양한 충족률을 가진 쿼터 상태 Mock 데이터가 주어짐
- When: 대시보드 화면을 로드함
- Then: 각 셀별 진행률 바(Progress Bar) 및 Full 상태 표시가 시각적으로 정확히 표현되어야 한다.

Scenario 2: 쿼터 엑셀 업로드 시뮬레이션
- Given: 샘플 엑셀 파일을 업로드함
- When: Mock API가 성공 응답을 반환함
- Then: 업로드된 내용이 대시보드에 즉시 반영된 것처럼 표시되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 대시보드 실시간 갱신 테스트를 위해 Mock 데이터의 지연 시간(Latency)을 의도적으로 조정(예: 100ms)할 수 있어야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 복합 교차 쿼터 매트릭스 샘플이 준비되었는가?
- [ ] 충족 상태별(진행 중, 완료 등) Mock 데이터가 구성되었는가?
- [ ] 쿼터 대시보드 시각화 컴포넌트와의 데이터 정렬이 확인되었는가?

## :construction: Dependencies & Blockers
- Depends on: #API-010, #API-011 (Quota DTO)
- Blocks: #FE-QT-001 (쿼터 설정 UI), #FE-QT-002 (쿼터 모니터링)
