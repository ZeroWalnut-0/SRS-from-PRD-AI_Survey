---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-PARSE-004: 비정상 파일 업로드 예외 처리 테스트"
labels: 'test, foundation, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-PARSE-004] 비정상 파일 업로드 예외 처리 테스트
- 목적: 암호화된 파일, 손상된 바이너리, 혹은 허용되지 않은 확장자(e.g., `.exe`) 업로드 시 400 Bad Request 에러가 정상적으로 반환되는지 확인한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L477)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 암호가 걸린 `.docx` 파일 업로드 요청
- [ ] 상태 코드 400 확인 및 에러 메시지 검증

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 암호화 파일 차단
- Given: 패스워드 잠금 파일
- When: 업로드 시도
- Then: 400 에러와 함께 "암호화된 파일은 지원하지 않습니다" 메시지가 출력된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] DB `DOCUMENT.status`가 `FAILED`로 기록되었는지 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-PARSE-001
- Blocks: None
