---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] API-009: ZIP 패키지 다운로드 API 계약 정의"
labels: 'feature, foundation, api, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [API-009] ZIP 패키지 다운로드 API 계약 정의
- 목적: 결제가 완료된 사용자가 산출물(ZIP)을 안전하게 다운로드할 수 있도록 Supabase Storage의 서명된 URL을 제공하는 API 규격을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#7`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 엔드포인트: `GET /api/v1/packages/{package_id}/download`

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 요청 파라미터 정의: `package_id` (Path variable)
- [ ] 응답 DTO 정의: `{ presigned_url: string, expires_at: string }`
- [ ] 결제 여부 검증 로직 명세 (`payment_cleared === true`)
- [ ] 에러 코드 정의:
    - 403: 결제가 완료되지 않은 요청
    - 404: 존재하지 않거나 이미 삭제된 패키지
- [ ] TypeScript 인터페이스 정의 (`types/api/packages.ts`)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 완료 후 다운로드 URL 발급
- Given: `payment_cleared: true`인 패키지가 존재함
- When: 다운로드 API를 호출함
- Then: 200 OK와 함께 유효기간이 있는 Supabase Storage 서명 URL을 반환해야 한다.

Scenario 2: 결제 미완료 상태에서 접근
- Given: 아직 결제되지 않은 패키지 ID로 접근함
- When: 다운로드 URL을 요청함
- Then: 403 Forbidden을 반환하고 접근을 차단해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 서명된 URL의 유효기간은 최소한(예: 5분)으로 설정하여 유출 위험을 방지한다.
- 성능: URL 발급 레이턴시 ≤ 200ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] 다운로드 응답 DTO가 정의되었는가?
- [ ] 결제 여부 체크 로직 명세가 포함되었는가?
- [ ] TypeScript 타입 정의가 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-006 (ZIP_DATAMAP), #BE-PAY-002 (결제 콜백)
- Blocks: #BE-PAY-005 (다운로드 구현), #FE-PAY-004 (다운로드 시작 UI)
