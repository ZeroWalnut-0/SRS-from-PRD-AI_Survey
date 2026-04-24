---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-006: ZIP_DATAMAP 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-006] ZIP_DATAMAP 테이블 스키마 및 마이그레이션 작성
- 목적: 결제 상태와 산출물(ZIP 파일)의 다운로드 정보를 관리하기 위한 테이블을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.4_ZIP_DATAMAP`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- Paywall 로직: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.6.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma` 내 `ZipDataMap` 모델 정의
- [ ] 필수 필드 추가: `package_id` (UUID), `form_id` (FK), `payment_cleared`, `pg_transaction_id`, `payment_amount`, `download_url`, `url_expires_at`, `download_count`
- [ ] `ParsedForm` 모델과의 1:1 또는 1:N 관계 설정
- [ ] Prisma Migration 생성 및 실행

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 완료 상태 업데이트
- Given: PG사로부터 결제 성공 신호를 받음
- When: `payment_cleared` 필드를 `true`로 업데이트함
- Then: 해당 레코드의 상태가 즉시 반영되어야 하며, 이후 다운로드 URL 발급이 가능해야 한다.

Scenario 2: 다운로드 횟수 추적
- Given: 유저가 파일을 다운로드함
- When: `download_count`를 1 증가시킴
- Then: 카운트가 정확히 반영되어야 하며, 이를 통해 KPI 측정이 가능해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: `download_url`은 Supabase Storage의 서명된 URL을 저장하며, 만료 시간(`url_expires_at`)을 엄격히 관리한다.
- 무결성: `pg_transaction_id`는 PG사와의 대조를 위해 반드시 저장한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `schema.prisma`에 ZipDataMap 모델이 SRS 명세대로 반영되었는가?
- [ ] 결제 및 다운로드 추적을 위한 필드 구성이 완료되었는가?
- [ ] 마이그레이션이 성공적으로 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM 테이블)
- Blocks: #BE-PAY-002 (결제 콜백 처리), #BE-PAY-005 (다운로드 URL 반환)
