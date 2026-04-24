---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-005: RESPONSE 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-005] RESPONSE 테이블 스키마 및 마이그레이션 작성
- 목적: 응답자가 제출한 설문 응답 데이터와 관련 메타데이터(IP 해시, 쿼터 상태 등)를 저장하는 테이블을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.3_RESPONSE`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 보안 요건: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.3_REQ-NF-017`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md) (IP 비식별화)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma` 내 `Response` 모델 정의
- [ ] 필수 필드 추가: `resp_id` (UUID), `form_id` (FK), `user_agent`, `raw_record` (JSON), `quota_status` (Enum), `quota_group` (JSON), `routing_status` (Enum), `ip_hash`
- [ ] `ParsedForm` 모델과의 1:N 관계 설정
- [ ] Prisma Migration 생성 및 실행

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 설문 응답 저장
- Given: 응답자가 설문을 제출함
- When: `Response` 테이블에 데이터를 삽입함
- Then: 응답 내용(JSON)과 응답자 식별 정보(해시된 IP 등)가 정확히 저장되어야 한다.

Scenario 2: IP 비식별화 확인
- Given: 응답자의 실제 IP 주소가 수집됨
- When: `ip_hash` 필드에 저장함
- Then: 평문 IP가 아닌 해싱된 문자열로 저장되어 개인정보를 보호해야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: `ip_hash`는 SHA-256 등 단방향 암호화를 사용하여 저장한다.
- 데이터: `raw_record`는 대량의 응답 데이터를 수용할 수 있도록 JSON 타입으로 정의한다.
- 성능: 특정 폼에 대한 응답 조회가 빈번하므로 `form_id` 인덱스를 추가한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `schema.prisma`에 Response 모델이 SRS 명세대로 반영되었는가?
- [ ] IP 해싱 처리를 위한 필드 구성이 완료되었는가?
- [ ] 마이그레이션이 성공적으로 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM 테이블), #DB-011 (Enum 정의)
- Blocks: #BE-FORM-004 (응답 제출 로직), #BE-PAY-003 (ZIP 산출물 생성)
