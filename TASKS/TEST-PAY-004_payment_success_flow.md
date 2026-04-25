---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-PAY-004: 결제 성공 및 서명 URL 발급 테스트"
labels: 'test, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-PAY-004] 결제 성공 및 서명 URL 발급 테스트
- 목적: PG사로부터 승인 완료 응답을 받았을 때, DB의 `payment_cleared` 상태가 즉시 `true`로 바뀌고, ZIP 파일 다운로드를 위한 Supabase 서명 URL이 발급되는지 E2E로 검증한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L503)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Toss Payments 결제 승인 Webhook 수신 모킹 스크립트 작성
- [ ] `/api/v1/payments/callback` 엔드포인트에 성공 페이로드 전송
- [ ] DB 검증: `ZIP_DATAMAP` 테이블의 `payment_cleared=true` 및 `pg_transaction_id` 적재 확인
- [ ] Supabase Storage API 연동: 다운로드 서명(Presigned) URL 생성 로직 유닛 테스트
- [ ] 만료 시간(60분) 설정 준수 여부 검증

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 승인 및 권한 획득
- Given: 유료 데이터맵(9,900원) 결제 세션이 열려있음
- When: PG사로부터 정상 승인 Webhook이 서버에 도달함
- Then: 유저 화면에 '결제 완료' 토스트가 뜨며, 다운로드 링크가 활성화된다.

Scenario 2: 서명 URL 유효성
- Given: 발급된 Presigned URL
- When: 60분 이내에 접속 시
- Then: 엑셀 및 PDF가 포함된 ZIP 파일이 정상 다운로드된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 실제 결제 테스트 모드(Test Secret Key)를 통한 PG사 연동 E2E 테스트 1회 통과
- [ ] 만료된 URL로 접근 시 403 에러가 발생하는지 확인

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-002, #BE-PAY-004
- Blocks: None

