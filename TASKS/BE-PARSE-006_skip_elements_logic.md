---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-006: 이미지/수식 요소 스킵 처리 및 기록 로직 구현"
labels: 'feature, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-006] 이미지/수식 요소 스킵 처리 및 기록 로직 구현
- 목적: 파싱 과정에서 AI가 처리하기 어려운 비텍스트 요소(이미지, 수식 등)를 식별하여 건너뛰고, 이를 사용자에게 안내하기 위해 `skipped_elements` 목록에 기록한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-007`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2_PARSED_FORM`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 파싱 파이프라인(`BE-PARSE-005`) 내에서 비텍스트 요소 감지 로직 추가
- [ ] 스킵된 요소의 정보(유형, 페이지 번호 또는 문항 인덱스)를 추출
- [ ] 추출된 정보를 JSON 배열 형태로 구성하여 `PARSED_FORM.skipped_elements` 필드에 저장
- [ ] 사용자 안내를 위한 요약 메시지 생성 로직 (예: "이미지 2개, 수식 1개가 제외되었습니다.")

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 복합 요소 포함 문서 파싱
- Given: 이미지 2개와 수식 1개가 포함된 문서가 업로드됨
- When: 파싱 프로세스가 실행됨
- Then: 텍스트 문항은 정상 추출되고, `skipped_elements` 필드에 3개의 요소 정보가 기록되어야 한다.

Scenario 2: 텍스트로만 구성된 문서 파싱
- Given: 이미지나 수식이 없는 순수 텍스트 문서가 업로드됨
- When: 파싱을 완료함
- Then: `skipped_elements` 필드는 `null` 또는 빈 배열(`[]`)로 저장되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 요소 식별 로직이 전체 파싱 시간을 1초 이상 지연시키지 않아야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 이미지/수식 요소 감지 및 스킵 로직이 구현되었는가?
- [ ] `skipped_elements` 데이터가 DB에 올바르게 저장되는가?
- [ ] 프론트엔드에서 안내 메시지를 표시할 수 있는 데이터 구조인가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-005 (AI SDK 연동)
- Blocks: #FE-PARSE-006 (미리보기 화면 노출)
