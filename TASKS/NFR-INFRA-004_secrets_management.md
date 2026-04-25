---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] NFR-INFRA-004: 환경변수(Secrets) 중앙 관리 시스템 구성"
labels: 'feature, infra, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-INFRA-004] 환경변수 중앙 관리 시스템 구성
- 목적: API Key, DB Password 등의 민감 정보를 안전하게 통제하기 위해 Vercel 및 Supabase 관리 콘솔에 환경변수를 등록하고 관리한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- 제약사항 (CON-03): [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L55)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Vercel Environment Variables 설정 화면에 Gemini, TossPayments Key 등록
- [ ] 로컬 개발용 `.env.local` 템플릿 파일 생성

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 소스코드 노출 방지
- Given: 개발 서버 기동
- When: 코드베이스 내 API Key 검색
- Then: 하드코딩된 문자열 없이 `process.env.GEMINI_API_KEY` 형태로만 호출된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 빌드 시 환경변수 주입 성공 확인

## :construction: Dependencies & Blockers
- Depends on: None
- Blocks: #DB-001, #BE-PARSE-005
