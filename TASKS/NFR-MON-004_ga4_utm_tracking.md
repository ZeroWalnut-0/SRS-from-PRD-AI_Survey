---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] NFR-MON-004: GA4 연동(Next.js Script 태그 + utm 파라미터 트래킹)"
labels: 'feature, nfr, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-MON-004] GA4 연동 및 utm 파라미터 트래킹
- 목적: 마케팅 성과 측정을 위해 바이럴 워터마크 및 외부 광고를 통한 유입 경로별 퍼널 전환율을 Google Analytics 4로 전송한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.5`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L617)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `next/script`를 이용한 GA4 GTAG 글로벌 주입
- [ ] 랜딩 페이지 접근 시 URL `utm_source`, `utm_campaign` 파싱 후 GA4 이벤트 전송

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 워터마크 유입 트래킹
- Given: `utm_source=watermark` 링크로 유입
- When: 회원가입 또는 결제 완료
- Then: GA4 이벤트 콘솔에 해당 유입의 결제 전환 기록이 정상 수집된다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 쿠키 동의 정책 준수 확인

## :construction: Dependencies & Blockers
- Depends on: #FE-WM-002
- Blocks: None
