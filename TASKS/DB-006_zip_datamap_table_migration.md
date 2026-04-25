---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-006: ZIP_DATAMAP 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, database, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-006] ZIP_DATAMAP 테이블 스키마 및 마이그레이션 작성
- 목적: 유료 플랜 고객에게 제공되는 최종 산출물(ZIP 패키지: 5대 데이터 맵 포함)의 다운로드 권한 및 결제 상태를 관리한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 데이터 모델 (ERD): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.4`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L771)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `ZipDatamap` 모델 생성 (`id`, `form_id`, `payment_id`, `zip_url`, `is_purchased`, `file_integrity_hash`)
- [ ] 파일 무결성 검증을 위한 해시 문자열 저장 필드 구성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 결제 전/후 다운로드 권한 필터링
- Given: 구매되지 않은 `ZipDatamap` 레코드
- When: `is_purchased` 확인
- Then: False를 확인하여 다운로드를 제한할 수 있는 구조임을 검증한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 클라우드 스토리지 URL 유출 방지 체계와 호환되도록 설계

## :checkered_flag: Definition of Done (DoD)
- [ ] 필드 결락 여부 검사

## :construction: Dependencies & Blockers
- Depends on: #DB-004
- Blocks: #BE-PAY-001
