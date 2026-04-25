---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PARSE-002: HWPX 문서 전처리 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PARSE-002] HWPX 문서 전처리 구현
- 목적: HWPX 파일(개방형 한글 포맷)의 압축 구조를 해제하고, XML 노드를 탐색하여 문서 본문 텍스트를 정확하게 추출한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L493)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L725)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] JSZip 라이브러리를 활용한 HWPX 파일 압축 해제 로직 구현
- [ ] `Contents/section0.xml` 파일 위치 탐색 및 로드
- [ ] xml2js 또는 Fast-xml-parser를 이용한 XML 파싱 및 순수 텍스트 노드 추출
- [ ] 추출된 텍스트에서 개행문자 및 불필요한 공백 정규화

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: HWPX 텍스트 추출 성공
- Given: 유효한 HWPX 설문지 초안 파일이 주어짐
- When: 전처리 엔진이 구동됨
- Then: 원본 문항 텍스트들이 손실 없이 하나의 문자열로 병합 추출된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 대용량 XML 파싱 시 Vercel Serverless 메모리 오버플로우 주의
- 호환성: 한컴오피스 표준 HWPX 스펙 준수

## :checkered_flag: Definition of Done (DoD)
- [ ] 전처리 결과 문자열 내 한글 깨짐 현상 유무 확인
- [ ] 텍스트 외 불필요한 XML 태그 100% 정제 여부 검증

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-001 (파일 검증)
- Blocks: #BE-PARSE-005 (Gemini API 연동)
