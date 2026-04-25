---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] TEST-F1-002: DOCX 파서 텍스트 추출 정확도 테스트"
labels: 'feature, test, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-F1-002] DOCX 파서 텍스트 추출 정확도 테스트
- 목적: Word(.docx) 파일에서 문항 본문과 보기 리스트가 깨짐 없이 추출되는지 유닛 테스트한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.2.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L222)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `mammoth` 라이브러리 변환 결과물 테스트 케이스 작성
- [ ] 불필요한 XML 태그 제거 후 순수 텍스트만 정제되는지 검증

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: DOCX 파싱 결과물 검증
- Given: DOCX 기반 테스트 데이터셋
- When: 파서 구동
- Then: JSON 변환용 원천 텍스트가 정상 빌드된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `npm run test` 무에러 통과

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-003
- Blocks: None
