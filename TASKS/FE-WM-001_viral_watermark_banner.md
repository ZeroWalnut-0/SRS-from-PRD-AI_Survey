---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-WM-001: 무료 플랜 설문 하단 바이럴 배너 노출 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-WM-001] 무료 플랜 설문 하단 바이럴 배너 노출 구현
- 목적: 무료 사용자가 생성한 설문 폼 하단에 플랫폼 홍보용 바이럴 워터마크("AI로 1분 만에 설문지 만들기")를 상시 노출한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L522)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 무료/유료 플랜 분기 체크 로직 구현
- [ ] 설문 하단 영역 고정 스티키(Sticky) 또는 Footer 배너 UI 디자인 및 배치

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 무료 플랜 설문 접속
- Given: `is_paid_user = false`인 설문 링크로 접속함
- When: 화면 하단으로 스크롤을 내림
- Then: 플랫폼 이동 링크가 걸린 바이럴 배너가 시각적으로 노출된다.

## :gear: Technical & Non-Functional Constraints
- 디자인: 사용자 응답 입력을 가리지 않도록 컴팩트하고 세련된 레이아웃 유지

## :checkered_flag: Definition of Done (DoD)
- [ ] 모바일 뷰포트 하단 가림 현상 유무 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-WM-001
- Blocks: #FE-WM-002
