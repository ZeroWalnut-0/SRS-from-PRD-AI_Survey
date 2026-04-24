---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-002: HWPX 문서 전처리 및 텍스트 추출 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-002] HWPX 문서 전처리 및 텍스트 추출 구현
- 목적: 업로드된 HWPX(Hancom Office XML) 파일의 구조를 분석하여 파싱에 필요한 텍스트 노드를 추출하고 정제한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-006`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 태스크 리스트: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/06_TASK_LIST.md#L94`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/06_TASK_LIST.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `jszip` 라이브러리를 사용하여 HWPX 파일(ZIP 포맷) 압축 해제
- [ ] `Contents/section0.xml` (또는 하위 섹션) 파일 접근 및 XML 파싱
- [ ] `<hp:t>` 태그 내의 텍스트 노드 추출 로직 구현
- [ ] 개행 처리 및 불필요한 메타데이터 필터링
- [ ] 추출된 텍스트 데이터를 AI 파서(`BE-PARSE-005`)의 입력값으로 전달

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 표준 HWPX 문서 텍스트 추출
- Given: 텍스트가 포함된 정상적인 HWPX 파일이 업로드됨
- When: 전처리 로직이 실행됨
- Then: 원본 문서의 모든 텍스트 내용이 순차적인 문자열 형태로 추출되어야 한다.

Scenario 2: 다중 섹션 문서 처리
- Given: 여러 개의 섹션(section0.xml, section1.xml ...)으로 구성된 HWPX 파일
- When: 압축 해제 및 텍스트 추출을 수행함
- Then: 모든 섹션의 텍스트가 순서대로 병합되어 반환되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 1MB 이하 HWPX 전처리 시간 ≤ 2,000ms.
- 메모리: 서버리스 환경의 메모리 제약을 고려하여 대용량 XML 스트리밍 처리 검토.

## :checkered_flag: Definition of Done (DoD)
- [ ] HWPX 파일 구조 분석 및 텍스트 추출 성공률 100% (텍스트만 있는 경우)?
- [ ] `jszip`을 통한 안전한 파일 접근이 보장되는가?
- [ ] 추출된 데이터가 AI 모델의 컨텍스트 윈도우 내에 들어오는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-001 (서버 검증)
- Blocks: #BE-PARSE-005 (AI SDK 연동)
