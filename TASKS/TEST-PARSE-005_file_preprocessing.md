---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-PARSE-005: 파일 타입별 전처리 분기 테스트"
labels: 'test, foundation, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-PARSE-005] 파일 타입별 전처리 분기 테스트
- 목적: HWPX(jszip), Word(mammoth), PDF(pdf-parse) 각각의 라이브러리가 올바른 확장자에 매핑되어 바이너리를 텍스트로 추출해내는지 검증한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L477)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 동일한 설문 내용이 담긴 HWPX, DOCX, PDF 3종 파일 준비
- [ ] 각각의 텍스트 추출 결과 문자열 비교

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 전처리 일관성
- Given: 3가지 타입의 파일
- When: 텍스트 추출
- Then: 추출된 문자열에서 핵심 키워드(e.g., "만족도")가 모두 검출된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 각 전처리 모듈 단위 유닛 테스트 통과

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-002, #BE-PARSE-003, #BE-PARSE-004
- Blocks: None
