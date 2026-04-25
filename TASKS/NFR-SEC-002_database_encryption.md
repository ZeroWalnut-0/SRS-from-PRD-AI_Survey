---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] NFR-SEC-002: 데이터 암호화 저장(Encryption at Rest) 적용"
labels: 'feature, security, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-SEC-002] 데이터 암호화 저장(Encryption at Rest) 적용
- 목적: Supabase 데이터베이스의 저장 데이터가 물리 디스크 레벨에서 암호화되어 보관되는지 설정 상태를 검증하고 유지한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 제약사항 (CON-02): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L55)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Supabase AWS/GCP 인프라의 기본 EBS/디스크 암호화 정책(AES-256) 활성화 확인
- [ ] 민감 컬럼(예: User PII가 생길 경우)에 대한 별도 애플리케이션 암호화 고려

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 인프라 보안 준수
- Given: 데이터베이스 물리 설정 조회
- When: TDE(Transparent Data Encryption) 상태 점검
- Then: Enabled 상태임을 공식 확인한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 설정 리포트 작성 및 검토

## :construction: Dependencies & Blockers
- Depends on: #DB-001
- Blocks: None
