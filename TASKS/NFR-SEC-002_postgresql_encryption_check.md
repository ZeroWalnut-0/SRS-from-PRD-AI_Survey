---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Sec] NFR-SEC-002: PostgreSQL 저장 데이터 암호화(At-rest) 검증"
labels: 'infrastructure, security, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-SEC-002] PostgreSQL 저장 데이터 암호화(At-rest) 검증
- 목적: 물리적 디스크 수준에서의 데이터 암호화가 적용되어 있는지 확인하여, 데이터베이스 서버 탈취 시에도 정보 유출을 방지한다.

## :link: References (Spec & Context)
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.3_REQ-NF-017`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 인프라: Supabase Managed Service 활용

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Supabase 보안 기술 문서를 통해 PostgreSQL 디스크 암호화 정책 확인 (AES-256 적용 여부)
- [ ] Storage 버킷에 저장된 파일들의 물리적 암호화 여부 확인
- [ ] 데이터베이스 백업 파일에 대한 암호화 정책 확인
- [ ] 보안 체크리스트에 해당 항목 증빙 자료(Managed 서비스 설정값 등) 추가

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: Supabase 프로젝트 설정
- When: 인프라 보안 구성을 점검함
- Then: 모든 저장 장치(Storage, Database)에 대해 At-rest Encryption이 활성화되어 있어야 한다.

## :gear: Technical & Non-Functional Constraints
- 컴플라이언스: ISMS 또는 GDPR 수준의 암호화 요건 충족 확인.

## :checkered_flag: Definition of Done (DoD)
- [ ] 저장 데이터 암호화 적용 여부가 확인되었는가?
- [ ] 물리적 유출 시나리오에 대한 방어 대책이 수립되었는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-001 (Prisma 초기화), #NFR-INFRA-004 (Supabase)
- Blocks: None
