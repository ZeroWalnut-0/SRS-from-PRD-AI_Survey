---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-003: Word(.docx) 문서 전처리 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-003] Word(.docx) 문서 전처리 구현
- 목적: Mammoth 라이브러리를 사용하여 Word 문서(.docx)의 서식을 제외한 본문 순수 텍스트를 추출한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L493)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `mammoth` npm 패키지 설치 및 연동
- [ ] 파일 버퍼를 Mammoth 라이브러리에 전달하여 Raw Text 추출 로직 작성
- [ ] Word의 스타일(제목, 본문 등) 정보를 무시하고 텍스트 데이터만 선별

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: DOCX 텍스트 추출 성공
- Given: 유효한 `.docx` 파일이 제공됨
- When: Mammoth 전처리가 실행됨
- Then: 문서 내부의 설문 문항 및 보기 데이터가 정상 텍스트로 전환된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 텍스트 변환 레이턴시 p95 ≤ 2,000ms 달성

## :checkered_flag: Definition of Done (DoD)
- [ ] Mammoth 변환 시 발생하는 경고(Warning) 로그 기록 및 모니터링
- [ ] 추출된 데이터가 UTF-8 포맷으로 유효한지 검증

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-001 (파일 검증)
- Blocks: #BE-PARSE-005 (Gemini API 연동)
