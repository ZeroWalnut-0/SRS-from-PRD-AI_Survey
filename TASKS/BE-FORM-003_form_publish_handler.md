---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-FORM-003: 설문 배포 상태 전환 Route Handler 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-FORM-003] 설문 배포 상태 전환 Route Handler 구현
- 목적: 작성이 완료된 설문을 배포 상태(`PUBLISHED`)로 전환하고, 응답 수집을 시작할 수 있도록 관련 설정을 갱신하는 API 핸들러를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2_REQ-FUNC-016`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-006_form_publish_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-006_form_publish_dto.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/forms/[form_id]/publish/route.ts` 구현
- [ ] 설문 상태 변경: `Document.status`를 `PUBLISHED`로 업데이트 (또는 별도 배포 테이블 관리)
- [ ] 고유 설문 응답 URL 생성 로직 구현
- [ ] QR 코드 생성 라이브러리 연동 및 이미지 데이터 생성
- [ ] 배포 시점 기록 (`published_at`)
- [ ] 빈 폼 배포 차단 (문항 수 확인)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상 배포 성공
- Given: 문항 작성이 완료된 설문 폼
- When: 배포 API를 호출함
- Then: 200 OK와 함께 고유 URL 및 QR 코드 정보를 반환해야 한다.

Scenario 2: 배포 중단 처리
- Given: 현재 배포 중인 설문
- When: 배포 중단(삭제/상태변경) 요청을 보냄
- Then: 상태가 변경되어 더 이상 응답을 제출할 수 없어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 배포 처리 및 응답 반환까지 레이턴시 ≤ 500ms.
- 인프라: QR 코드는 Supabase Storage에 저장하거나 Base64 형태로 반환한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-006` 규격에 맞는 응답을 반환하는가?
- [ ] 설문 상태가 정확히 전이되는가?
- [ ] 고유 URL 및 QR 코드가 유효하게 생성되는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM), #API-006 (Publish DTO)
- Blocks: #FE-FORM-006 (배포 화면 연동)
