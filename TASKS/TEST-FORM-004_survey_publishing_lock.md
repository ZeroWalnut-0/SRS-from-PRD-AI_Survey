---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-FORM-004: 배포 후 설문 수정 잠금 테스트"
labels: 'test, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-FORM-004] 배포 후 설문 수정 잠금 테스트
- 목적: 설문이 '배포(PUBLISHED)' 상태로 전환된 이후에는, 데이터 무결성을 위해 문항 수정, 삭제, 추가 요청이 백엔드 단에서 403/400 에러로 원천 차단되는지 확인한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L218)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 상태가 `PUBLISHED`인 폼 준비
- [ ] `PUT /api/v1/forms/{id}`로 구조 변경 요청 전송 후 응답 분석

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 배포 후 수정 불가
- Given: 배포 완료된 설문
- When: 문항 수정 API 호출
- Then: HTTP 400 에러와 함께 "배포된 설문은 수정할 수 없습니다" 반환

## :checkered_flag: Definition of Done (DoD)
- [ ] 프론트엔드 에디터 UI에서도 수정 버튼이 비활성화(Disabled) 처리되는지 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-FORM-002
- Blocks: None
