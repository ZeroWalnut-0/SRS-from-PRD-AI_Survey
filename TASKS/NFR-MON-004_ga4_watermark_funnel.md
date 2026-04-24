---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Mon] NFR-MON-004: GA4 연동 및 워터마크 바이럴 퍼널 분석 설정"
labels: 'infrastructure, monitoring, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [NFR-MON-004] GA4 연동 및 워터마크 바이럴 퍼널 분석 설정
- 목적: Google Analytics 4를 연동하여 워터마크를 통한 유입부터 서비스 가입까지의 전환 퍼널을 분석한다.

## :link: References (Spec & Context)
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.5_REQ-NF-028`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] Google Analytics 4 속성 생성 및 측정 ID 발급
- [ ] Next.js Script 태그를 활용한 GA4 기본 스니펫 삽입
- [ ] Custom Event 정의: `watermark_click`, `signup_from_viral`
- [ ] UTM 파라미터(`utm_source=watermark`) 자동 트래킹 확인
- [ ] GA4 대시보드 내 전환 퍼널(Exploration) 보고서 구성

## :test_tube: Acceptance Criteria (BDD/GWT)
- Given: 사용자가 워터마크를 통해 진입하여 가입함
- When: GA4 실시간 보고서를 확인함
- Then: `watermark_click` 이벤트와 함께 유입 소스가 `watermark`로 정확히 잡혀야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: GDPR 준수를 위해 사용자 IP 마스킹 설정을 확인한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] GA4 트래킹 코드가 모든 페이지에 삽입되었는가?
- [ ] 워터마크 클릭 이벤트가 정상적으로 전송되는가?
- [ ] 바이럴 효과를 측정할 수 있는 퍼널 보고서가 준비되었는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-WM-002
- Blocks: None
