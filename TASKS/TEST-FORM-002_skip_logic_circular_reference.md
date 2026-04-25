---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-FORM-002: 조건부 분기 순환 참조 차단 테스트"
labels: 'test, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-FORM-002] 조건부 분기 순환 참조 차단 테스트
- 목적: 설문 로직 설계 시 문항 A가 B로 가고, B가 다시 A로 돌아오는 형태의 무한 루프(순환 참조) 분기가 설정될 경우, 저장 전 유효성 검사에서 이를 감지해 차단하는지 E2E 및 알고리즘 레벨에서 테스트한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L218)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] DAG(Directed Acyclic Graph) 판별 알고리즘 유닛 테스트 작성
- [ ] 순환 참조(A -> B -> A)가 포함된 악의적 `structure_schema` 페이로드 생성
- [ ] `POST /api/v1/forms/{id}` API 호출 및 400 Bad Request 응답 검증
- [ ] 프론트엔드 테스트: 순환 참조 생성 시 "순환 논리가 발생했습니다" 경고 툴팁 노출 여부 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 순환 참조 차단
- Given: 문항 1번의 분기 조건이 2번을 가리키고, 2번의 조건이 1번을 가리킴
- When: 설문 '저장' 또는 '배포' 버튼 클릭
- Then: 저장 프로세스가 중단되고, UI 상에 에러 하이라이트가 표시된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 3개 이상의 문항이 얽힌 복합 순환(A -> B -> C -> A) 구조도 완벽히 차단하는지 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-FORM-002, #FE-FORM-004
- Blocks: None

