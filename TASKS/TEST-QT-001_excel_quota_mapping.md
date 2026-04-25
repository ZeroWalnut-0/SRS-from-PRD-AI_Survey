---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-QT-001: 엑셀 업로드 교차 쿼터 반영 테스트"
labels: 'test, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-QT-001] 엑셀 업로드 교차 쿼터 반영 테스트
- 목적: 관리자가 쿼터 할당 엑셀 파일을 업로드했을 때, 이를 서버에서 파싱하여 `QUOTA_SETTING` 및 `QUOTA_CELL` 구조로 완벽히 매핑 및 저장하는지 확인한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L528)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 2x3x2 교차 쿼터(총 12개 셀) 엑셀 샘플 업로드
- [ ] `QUOTA_CELL` 테이블 레코드 수 및 `target_count` 값 대조

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 셀 생성 일치
- Given: 12개 조건의 엑셀 할당표
- When: 업로드 API 실행
- Then: DB에 정확히 12개의 셀 레코드가 타겟 수량과 일치하게 생성된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 복잡한 연령대(e.g., 20-29) 문자열 파싱 유효성 검사

## :construction: Dependencies & Blockers
- Depends on: #BE-QT-001
- Blocks: None
