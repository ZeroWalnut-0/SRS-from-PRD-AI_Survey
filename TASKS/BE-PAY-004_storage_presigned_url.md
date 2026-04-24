---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] BE-PAY-004: Supabase Storage 서명된 URL 발급 핸들러 구현"
labels: 'feature, backend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [BE-PAY-004] Supabase Storage 서명된 URL 발급 핸들러 구현
- 목적: 결제가 완료된 사용자에게만 유효기간이 짧은(예: 5분) 보안 다운로드 URL을 발급하여 산출물의 무단 유출을 방지한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.1_#7`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 보안 요건: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#REQ-NF-021`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/api/v1/packages/[package_id]/download/route.ts` 구현
- [ ] 권한 검증: `ZIP_DATAMAP.payment_cleared === true` 여부 확인
- [ ] Supabase SDK (`createSignedUrl`)를 사용하여 전용 다운로드 링크 생성
- [ ] URL 유효기간 설정 (Short-lived, 예: 300초)
- [ ] 응답 데이터 구성: `{ presigned_url, expires_at }`

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 정상 URL 발급
- Given: 결제가 완료된 유효한 패키지 ID로 요청함
- When: 핸들러가 실행됨
- Then: 200 OK와 함께 즉시 다운로드 가능한 서명된 URL이 반환되어야 한다.

Scenario 2: 미결제 접근 차단
- Given: 결제되지 않은 패키지 ID로 URL 요청
- When: 권한 검증이 실행됨
- Then: 403 Forbidden을 반환하고 URL 생성을 거부해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 서명된 URL이 타인에게 공유되더라도 단시간 내에 만료되도록 설정한다.
- 성능: URL 발급 레이턴시 ≤ 200ms.

## :checkered_flag: Definition of Done (DoD)
- [ ] `API-009` 규격에 맞는 응답을 반환하는가?
- [ ] 결제 여부에 따른 접근 제어가 완벽히 작동하는가?
- [ ] 서명된 URL의 유효기간이 의도대로 설정되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-006 (ZIP_DATAMAP), #BE-PAY-003 (ZIP 생성)
- Blocks: #FE-PAY-004 (다운로드 UI 연동)
