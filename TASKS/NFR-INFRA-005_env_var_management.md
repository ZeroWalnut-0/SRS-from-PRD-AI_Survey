---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Infra] NFR-INFRA-005: 전역 환경 변수 관리 및 보안 설정"
labels: 'infrastructure, security, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-INFRA-005] 전역 환경 변수 관리 및 보안 설정
- 목적: 프로젝트 운영에 필요한 민감 정보(API Key, DB 비밀번호 등)를 안전하게 관리하고 배포 환경에 주입한다.

## :link: References (Spec & Context)
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.2.3_C-TEC-005, 006`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `.env.example` 파일 작성 (필요한 변수 목록 명시)
- [ ] Vercel Project Settings 내 Environment Variables 등록:
    - `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
    - `SUPABASE_SERVICE_ROLE_KEY` (Server-side only)
    - `GEMINI_API_KEY`
    - `DATABASE_URL` (Direct Connection)
    - `SLACK_WEBHOOK_URL`
- [ ] `env.ts` (Zod 활용) 등을 통한 환경 변수 유효성 검증(Validation) 코드 추가
- [ ] `.gitignore` 파일 내 `.env*` 패턴 등록 재확인

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: Vercel 배포 환경
- When: 애플리케이션이 구동됨
- Then: 등록된 모든 환경 변수가 `process.env`를 통해 정상적으로 로드되어야 하며, 누락 시 앱 구동이 중단(Panic)되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: `NEXT_PUBLIC_` 접두사가 붙은 변수는 브라우저에 노출되므로 민감 정보를 포함하지 않도록 주의한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 모든 필수 환경 변수가 Vercel 및 로컬에 등록되었는가?
- [ ] 환경 변수 유효성 검사 로직이 적용되었는가?
- [ ] 민감 정보의 소스 코드 유출 가능성이 차단되었는가?

## :construction: Dependencies & Blockers
- Depends on: #NFR-INFRA-003, #NFR-INFRA-004
- Blocks: #BE-PARSE-005, #BE-PAY-001 등
