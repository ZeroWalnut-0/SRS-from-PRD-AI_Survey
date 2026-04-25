---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PARSE-003: 파일 확장자·크기 클라이언트 검증 로직 구현"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PARSE-003] 파일 확장자·크기 클라이언트 검증 로직 구현
- 목적: 서버 부하를 방지하기 위해 파일 선택 단계에서 유효하지 않은 파일을 1차 필터링한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.2.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L208)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] HTML File API를 이용한 크기 체크
- [ ] 확장자(extension) 추출 및 허용 목록 대조

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 비정상 확장자 업로드 차단
- Given: `.png` 이미지 파일이 선택됨
- When: 파일 업로드를 시도함
- Then: 모달 경고창을 띄우며 진행을 막는다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 사용자 안내 문구 출력 확인

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-001
- Blocks: None
