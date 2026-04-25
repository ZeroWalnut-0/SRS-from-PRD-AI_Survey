---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-003: ZIP 5종 산출물 컴파일 로직 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-003] ZIP 5종 산출물 컴파일 로직 구현
- 목적: 설문 응답 데이터와 가이드를 포함한 전문적 형태의 연구 분석용 5대 산출물(ZIP 패키지)을 서버에서 자동 빌드한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L508)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `JSZip` 패키지를 활용한 메모리 상의 아카이브 생성
- [ ] `exceljs`를 사용해 응답 원본 엑셀, 코드북, 데이터맵 등 4종 시트 작성 로직 통합
- [ ] AI 내러티브 리포트(.md) 생성 모듈 병합

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: ZIP 파일 생성
- Given: 응답 수집이 완료된 설문
- When: 컴파일 로직 구동
- Then: 5종의 파일이 포함된 유효한 ZIP 바이너리가 생성된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 생성 속도 5초 이내 완료 여부

## :construction: Dependencies & Blockers
- Depends on: #DB-005, #DB-006
- Blocks: #BE-PAY-004
