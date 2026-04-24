---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Fallback] NFR-FB-003: Analytics 장애 시 DB 감사 로그 직접 기록 로직"
labels: 'infrastructure, resilience, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-FB-003] Analytics 장애 시 DB 감사 로그 직접 기록 로직
- 목적: Vercel Analytics 또는 GA4 등 외부 분석 도구에 장애가 발생하더라도, 서비스의 핵심 지표 데이터가 유실되지 않도록 Supabase DB의 `AUDIT_LOG` 테이블에 직접 Structured JSON 형태로 이벤트를 기록한다.

## :link: References (Spec & Context)
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.1_EXT-04 Fallback`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 관련 데이터: #DB-010 (AUDIT_LOG)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 외부 Analytics SDK 호출 전후의 에러 래핑(Try-Catch)
- [ ] 호출 실패 시 자동으로 `AUDIT_LOG` 인서트 함수 호출 트리거
- [ ] DB 로그 전용 이벤트 스키마 정의 (Action, Page, UserID, Timestamp 등)
- [ ] 복구 대시보드 UI에서 DB 로그 데이터를 우선 참조하도록 하는 토글 기능(운영자용)

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: Vercel Analytics 스크립트 로드 실패 상황
- When: 사용자가 페이지를 방문하거나 행동을 수행함
- Then: 브라우저 콘솔에 에러가 남지 않아야 하며, 대신 DB의 `AUDIT_LOG` 테이블에 해당 행위 정보가 즉시 저장되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: DB 쓰기 작업이 증가할 수 있으므로 핵심 지표 위주로 선별하여 기록한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 외부 도구 장애 시의 대체 로깅 시스템이 작동하는가?
- [ ] DB에 기록된 데이터가 분석 가능한 정형 데이터인가?
- [ ] 사용자 경험에 지연을 주지 않는가?

## :construction: Dependencies & Blockers
- Depends on: #DB-010, #NFR-MON-001
- Blocks: None
