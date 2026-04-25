---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-FORM-003: 설문 폼 배포 API 구현"
labels: 'feature, backend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-FORM-003] 설문 폼 배포 API (`POST /api/v1/forms/{form_id}/publish`)
- 목적: 설문 폼의 개발/수정 단계를 마감하고 응답 수집을 개시하기 위해 상태를 `PUBLISHED`로 전환하며, 접근 가능한 최종 설문 URL을 생성한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L493)
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L742)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L716)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Next.js API Route Handler 생성 (`/app/api/v1/forms/[form_id]/publish/route.ts`)
- [ ] DB 레코드 접근 및 `DOCUMENT.status`를 `COMPLETED`에서 `PUBLISHED`(수집중) 상태로 변경
- [ ] 최종 응답 수집 링크 생성 (`/survey/[form_id]`) 및 QR 코드 이미지 생성 라이브러리 연동
- [ ] 응답 DTO 구성 (`{ survey_url, qr_code }`)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상적인 폼 배포
- Given: 유효한 `form_id`가 제공됨
- When: 해당 API로 POST 요청을 보냄
- Then: 상태값이 `PUBLISHED`로 변경되고, 설문 URL과 QR 코드가 200 OK와 함께 반환된다.

## :gear: Technical & Non-Functional Constraints
- 보안: 비인가 배포 방지(설문 소유자 본인 세션 확인 필수)
- 가용성: 배포 완료 시 동시 접속 대응을 위한 무상태(Stateless) 설계 유지

## :checkered_flag: Definition of Done (DoD)
- [ ] 모든 AC 충족 및 통합 배포 테스트 성공
- [ ] 생성된 설문 링크가 모바일 뷰포트에서 정상 접속되는지 확인

## :construction: Dependencies & Blockers
- Depends on: #DB-004, #API-006
- Blocks: #FE-FORM-006
