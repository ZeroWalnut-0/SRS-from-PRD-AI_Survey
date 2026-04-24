---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] DB-009: ROUTING_CONFIG 테이블 스키마 및 마이그레이션 작성"
labels: 'feature, foundation, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [DB-009] ROUTING_CONFIG 테이블 스키마 및 마이그레이션 작성
- 목적: 외부 패널사 연동을 위한 상태별 리다이렉트 URL 정보를 저장하고 관리하는 테이블을 정의한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#6.2.7_ROUTING_CONFIG`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 패널 라우팅 요건: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.5_REQ-FUNC-023`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `prisma/schema.prisma` 내 `RoutingConfig` 모델 정의
- [ ] 필수 필드 추가: `routing_id` (UUID), `form_id` (FK), `success_url`, `screenout_url`, `quotafull_url`
- [ ] `ParsedForm` 모델과의 1:1 관계 설정
- [ ] Prisma Migration 생성 및 실행

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 라우팅 설정 저장
- Given: 패널사로부터 제공받은 상태별 포스트백 URL이 존재함
- When: `RoutingConfig` 테이블에 데이터를 삽입함
- Then: 각 상태(Success, Screenout, QuotaFull)에 대응하는 URL이 정확히 저장되어야 한다.

Scenario 2: 리다이렉트 시 URL 조회
- Given: 응답자가 설문을 종료함
- When: 해당 설문의 `form_id`로 라우팅 설정을 조회함
- Then: 저장된 URL을 즉시 반환하여 리다이렉트를 수행할 수 있어야 한다.

## :gear: Technical & Non-Functional Constraints
- 데이터 무결성: URL 형식에 대한 기본적인 유효성 검증을 포함한다.
- 성능: 리다이렉트 지연을 최소화하기 위해 조회가 최적화되어야 한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] `schema.prisma`에 RoutingConfig 모델이 SRS 명세대로 반영되었는가?
- [ ] 마이그레이션이 성공적으로 완료되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-004 (PARSED_FORM 테이블)
- Blocks: #BE-RT-001 (라우팅 등록 API), #BE-RT-002 (리다이렉트 로직)
