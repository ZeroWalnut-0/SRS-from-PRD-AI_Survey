---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-006: 설문 배포 API 계약 정의"
labels: 'feature, foundation, api, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [API-006] 설문 배포 API 계약 정의
- 목적: 작성이 완료된 설문 폼을 배포 상태로 전환하고, 응답 수집을 위한 고유 URL 및 QR 코드를 생성하기 위한 API 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.3.6`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `POST /api/v1/forms/{form_id}/publish`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 파라미터 정의: `form_id` (Path variable)
- [ ] 응답 DTO 정의: `{ survey_url: string, qr_code_url: string, published_at: string }`
- [ ] 설문 상태 변경 로직 명세 (`PENDING` -> `PUBLISHED`)
- [ ] 에러 코드 정의:
    - 400: 문항이 없는 빈 폼 배포 시도
    - 404: 존재하지 않는 `form_id`
- [ ] TypeScript 인터페이스 정의 (`types/api/forms.ts`)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 설문 배포 성공
- Given: 최소 1개 이상의 문항이 포함된 설문 폼이 준비됨
- When: 배포 API를 호출함
- Then: 200 OK와 함께 고유한 설문 참여 URL(`survey_url`)을 반환해야 한다.

Scenario 2: 배포 후 상태 확인
- Given: 설문 배포가 완료됨
- When: 설문 상태를 조회함
- Then: 상태가 `PUBLISHED`로 변경되어 있어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 배포 처리 및 URL 생성 레이턴시 ≤ 500ms.
- 인프라: QR 코드는 외부 라이브러리 또는 Supabase Edge Function을 활용하여 생성함을 고려한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 배포 API의 요청/응답 DTO가 정의되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?
- [ ] 배포 성공 시 반환될 URL 형식이 확정되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM 테이블)
- Blocks: #BE-FORM-003 (배포 구현), #FE-FORM-006 (배포 화면 구현)
