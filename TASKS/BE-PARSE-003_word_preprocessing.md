---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-003: Word(.docx) 문서 전처리 및 텍스트 추출 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-003] Word(.docx) 문서 전처리 및 텍스트 추출 구현
- 목적: 업로드된 Microsoft Word 파일에서 텍스트 데이터를 추출하여 AI 파서(Gemini)가 처리할 수 있는 정제된 입력값으로 변환한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-006`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 기술 스택: `mammoth` 라이브러리 활용 (REQ-FUNC-006)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `mammoth` 라이브러리 설치 및 연동
- [ ] Word 파일(`.docx`)로부터 텍스트 추출 로직 구현:
    - 텍스트 본문 추출
    - 표(Table) 데이터의 텍스트 변환 방식 결정 (정렬 유지를 위한 처리)
- [ ] 불필요한 메타데이터 또는 서식 정보 제거 (정제 프로세스)
- [ ] 추출된 텍스트의 크기 검증 (AI 모델 입력 제한 확인)
- [ ] 추출 실패 시 예외 처리 및 에러 로깅

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 일반 텍스트 Word 문서 추출
- Given: 텍스트로만 구성된 `.docx` 파일이 주어짐
- When: `mammoth`를 통해 텍스트를 추출함
- Then: 모든 문항 내용이 누락 없이 평문(Plain Text) 형태로 반환되어야 한다.

Scenario 2: 표가 포함된 Word 문서 추출
- Given: 설문 문항이 표 내부에 작성된 Word 파일이 주어짐
- When: 텍스트 추출을 수행함
- Then: 표의 구조는 깨지더라도 각 셀의 텍스트 데이터는 순차적으로 추출되어 문맥이 유지되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 텍스트 추출 프로세스 레이턴시 ≤ 2,000ms.
- 정확성: 특수 기호나 서식 태그가 텍스트에 포함되지 않도록 정제한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `mammoth`를 이용한 텍스트 추출 로직이 구현되었는가?
- [ ] 추출된 텍스트가 AI 파서의 입력값으로 적합한 포맷인가?
- [ ] 예외 케이스(파일 손상 등)에 대한 처리가 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-001 (서버 검증)
- Blocks: #BE-PARSE-005 (AI SDK 연동)
