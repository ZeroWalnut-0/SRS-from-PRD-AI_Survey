---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] MOCK-002: 파싱 완료 상태 조회 Mock API 및 스키마 샘플 작성"
labels: 'feature, foundation, mock, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [MOCK-002] 파싱 완료 상태 조회 Mock API 및 스키마 샘플 작성
- 목적: 파싱 완료 후 생성되는 `structure_schema`의 샘플 데이터를 작성하고, 상태 조회 및 폼 데이터 페칭을 위한 Mock API를 구성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md), [`#6.1_#3`](#)
- 데이터 모델: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2_PARSED_FORM`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `structure_schema` 샘플 JSON 작성 (다양한 문항 유형 포함: 단일/복수 선택, 주관식, 척도형 등)
- [ ] `GET /api/v1/documents/{doc_id}/status` Mock 핸들러 작성 (PENDING -> COMPLETED 시뮬레이션)
- [ ] `GET /api/v1/forms/{form_id}` Mock 핸들러 작성
- [ ] 워터마크 URL 샘플(`utm_source=watermark` 포함) 정의
- [ ] 파싱 과정 중 발생할 수 있는 '건너뛴 요소(skipped_elements)' 샘플 데이터 포함

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 파싱 진행 상태 시뮬레이션
- Given: 상태 조회 API를 연속 호출함
- When: 처음 2회는 `PARSING`, 3회째는 `COMPLETED`를 반환하도록 설정함
- Then: 프론트엔드의 폴링 및 로딩 UI가 정상적으로 동작함을 확인해야 한다.

Scenario 2: 대량 문항 스키마 렌더링 테스트
- Given: 50개 이상의 문항이 포함된 샘플 스키마를 로드함
- When: 폼 미리보기 화면을 렌더링함
- Then: 스크롤 및 렌더링 성능이 보장되며 모든 문항이 정상 표시되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 데이터 무결성: 샘플 JSON은 실제 프론트엔드 렌더링 엔진에서 요구하는 Zod 스키마를 완벽히 준수해야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 복합 문항 유형이 포함된 `structure_schema` 샘플이 작성되었는가?
- [ ] 파싱 상태 전이(PARSING -> COMPLETED)가 Mock에서 시뮬레이션되는가?
- [ ] 워터마크가 포함된 폼 조회 Mock 데이터가 준비되었는가?

## :construction: Dependencies & Blockers
- Depends on: #API-002, #API-003 (DTO 정의)
- Blocks: #FE-PARSE-002 (로딩 UI), #FE-PARSE-006 (미리보기 화면)
