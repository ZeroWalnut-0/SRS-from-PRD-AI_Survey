---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-003: 설문 응답 수집 Mock API 및 샘플 데이터 작성"
labels: 'feature, foundation, mock, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-003] 설문 응답 수집 Mock API 및 샘플 데이터 작성
- 목적: 설문 응답 제출 기능의 프론트엔드 개발을 지원하기 위해, 응답 데이터(raw_record) 샘플과 제출 API의 Mock 응답을 준비한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.3_RESPONSE`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `raw_record` 샘플 데이터 작성 (문항별 응답값 매핑: `{ "q1": "A", "q2": ["B", "C"], "q3": "텍스트" }`)
- [ ] `POST /api/v1/forms/{form_id}/responses` Mock 핸들러 작성
- [ ] 성공 및 유효성 검사 실패 시나리오 Mock 응답 정의
- [ ] 쿼터 도달 시 리다이렉트 시뮬레이션용 데이터 구성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 응답 제출 성공 테스트
- Given: 설문 폼에서 모든 응답을 입력함
- When: 제출 API를 호출함
- Then: 201 Created 응답과 함께 가상의 `resp_id`를 반환해야 한다.

Scenario 2: 데이터맵 생성을 위한 다량의 응답 시드 데이터 준비
- Given: 100건 이상의 가상 응답 데이터셋을 생성함
- When: 데이터맵 컴파일러 테스트 시 활용함
- Then: 다양한 응답 패턴(결측치 포함 등)이 포함되어 산출물 검증이 가능해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: Mock 데이터 내에 실제 개인정보가 포함되지 않도록 더미 데이터를 사용한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `raw_record`의 표준 포맷 샘플이 작성되었는가?
- [ ] 제출 성공/실패 시의 Mock 핸들러가 작동하는가?
- [ ] 대량 응답 시뮬레이션을 위한 데이터셋이 준비되었는가?

## :construction: Dependencies & Blockers
- Depends on: #API-004 (Response DTO)
- Blocks: #FE-FORM-007 (모바일 폼 렌더링 및 제출), #BE-PAY-003 (산출물 테스트용)
