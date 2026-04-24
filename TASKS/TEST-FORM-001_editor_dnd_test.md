---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-FORM-001: 에디터 문항 순서 변경 및 실시간 저장 테스트"
labels: 'test, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-FORM-001] 에디터 문항 순서 변경 및 실시간 저장 테스트
- 목적: 드래그 앤 드롭을 통한 문항 순서 변경이 시각적으로 정확히 반영되고, 서버 DB에 변경된 순서가 정상적으로 저장되는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #FE-FORM-001 (에디터 레이아웃), #BE-FORM-002 (수정 핸들러)

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 1번 문항을 3번 문항 위치로 드래그 시 인덱스 변경 확인
- [ ] 시나리오 2: 순서 변경 직후 페이지 새로고침 시 변경된 순서 유지 확인
- [ ] 시나리오 3: 대량 문항(30개 이상) 순서 변경 시 렌더링 성능 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 5개의 문항이 있는 설문 에디터
- When: 1번 문항을 맨 마지막으로 이동시킨 후 저장함
- Then: 다시 해당 설문을 조회했을 때, 원래 1번이었던 문항이 5번 위치에 존재해야 한다.

## :gear: Technical Constraints
- 도구: Playwright Drag & Drop API 활용

## :checkered_flag: Definition of Done (DoD)
- [ ] 시각적 순서와 DB 저장 데이터의 순서가 완벽히 일치하는가?
- [ ] 순서 변경 시 API 호출 횟수가 효율적으로 관리되는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-001 (에디터 레이아웃)
- Blocks: None
