---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] TEST-F2-001: 설문 라이프사이클 E2E 테스트"
labels: 'feature, test, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-F2-001] 설문 라이프사이클 E2E 테스트
- 목적: 사용자의 설문 제작 전반의 흐름(업로드 → AI 생성 → 편집 → 배포)을 Playwright를 통해 종합 검증한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.3.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L270)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Playwright 테스트 환경 설정 및 테스트 코드 생성
- [ ] 사용자 시나리오 기반 브라우저 자동 조작 스크립트 구현

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 완전한 배포 성공
- Given: 로그인된 사용자
- When: 파일 드롭 후 배포 완료까지 일련의 클릭 이벤트 실행
- Then: 최종 배포 완료 URL 및 QR 코드가 화면에 렌더링된다.

## :gear: Technical & Non-Functional Constraints
- 성능: 외부 API 호출 지연을 고려한 `waitForTimeout` 최적화

## :checkered_flag: Definition of Done (DoD)
- [ ] 헤드리스 브라우저 환경에서 100% 통과

## :construction: Dependencies & Blockers
- Depends on: 프론트/백엔드 핵심 기능 전체
- Blocks: Production 릴리즈
