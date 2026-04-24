---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-005: 다운로드 횟수 카운팅 및 로깅 구현"
labels: 'feature, backend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-005] 다운로드 횟수 카운팅 및 로깅 구현
- 목적: 사용자가 산출물을 다운로드할 때마다 횟수를 기록하고 로그를 남겨, 서비스 이용 현황 분석 및 어뷰징 방지에 활용한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.4_ZIP_DATAMAP`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: `download_count` 필드

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 다운로드 URL 발급 핸들러(`BE-PAY-004`) 내에 카운트 증가 로직 추가
- [ ] `ZIP_DATAMAP.download_count` 필드 원자적 증가 (Atomic Increment)
- [ ] `AUDIT_LOG` 테이블에 다운로드 이벤트 기록:
    - action: `DOWNLOAD_PACKAGE`
    - details: `{ package_id, user_id, timestamp }`
- [ ] 비정상적으로 잦은 다운로드 시도 시 알림 또는 제한 로직 검토

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 다운로드 횟수 증가 확인
- Given: 현재 `download_count`가 0임
- When: 다운로드 URL을 성공적으로 발급받음
- Then: DB의 `download_count`가 1로 증가해야 한다.

Scenario 2: 감사 로그 기록 확인
- Given: 사용자가 파일을 다운로드함
- When: `AUDIT_LOG` 테이블을 조회함
- Then: 누가, 언제, 어떤 패키지를 받았는지에 대한 로그가 정확히 생성되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 로그 기록 및 카운트 증가 작업이 메인 다운로드 흐름을 방해하지 않도록 비동기로 처리하거나 최적화한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 다운로드 시 `download_count`가 정확히 증가하는가?
- [ ] `AUDIT_LOG`에 관련 상세 정보가 남는가?
- [ ] 다수의 다운로드 요청 시에도 카운트 정합성이 유지되는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-004 (URL 발급), #DB-010 (AUDIT_LOG)
- Blocks: None
