---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Test] TEST-QT-001: 교차 쿼터 설정 유효성 및 매트릭스 정합성 테스트"
labels: 'test, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 테스트명: [TEST-QT-001] 교차 쿼터 설정 유효성 및 매트릭스 정합성 테스트
- 목적: 사용자가 입력한 복합 쿼터 조건(성별 x 연령 등)이 DB에 누락 없이 전개(Expand)되어 저장되는지 검증한다.

## :link: References (Spec & Context)
- 관련 태스크: #BE-QT-001 (쿼터 설정 핸들러)

## :white_check_mark: Test Scenarios
- [ ] 시나리오 1: 성별(2) x 연령(3) 조합 시 6개의 쿼터 셀 생성 확인
- [ ] 시나리오 2: 엑셀 일괄 업로드 시 데이터 매핑 정확성 확인
- [ ] 시나리오 3: 쿼터 변수 이름 중복 또는 특수문자 포함 시 처리 확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 성별(남/여)과 연령(20대/30대/40대) 변수 매트릭스
- When: 설정을 저장함
- Then: `QUOTA_CELL` 테이블에 총 6개의 레코드가 생성되어야 하며, 각 레코드의 `group_key`가 조합 이름과 일치해야 한다.

## :gear: Technical Constraints
- 도구: API Integration Test (Prisma 조회 병행)

## :checkered_flag: Definition of Done (DoD)
- [ ] 쿼터 셀 전개 로직이 수학적으로 정확한가?
- [ ] 엑셀 데이터와의 1:1 매핑이 완벽한가?

## :construction: Dependencies & Blockers
- Depends on: #BE-QT-001 (쿼터 설정)
- Blocks: None
