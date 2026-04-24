---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-RT-001: 외부 패널사 라우팅 설정 UI 구현"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-RT-001] 외부 패널사 라우팅 설정 UI 구현
- 목적: 외부 패널 플랫폼(엠브레인, 한국리서치 등) 연동을 위해 응답 결과별(성공, 스크린아웃, 쿼터풀) 리다이렉트 URL을 입력하고 관리하는 화면을 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.5_REQ-FUNC-023`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- API 명세: [`/Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-012_routing_postback_dto.md`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/TASKS/API-012_routing_postback_dto.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(dashboard)/forms/[form_id]/routing/page.tsx` 생성
- [ ] 상태별 URL 입력 폼 구현:
    - 조사 성공 시 (Success URL)
    - 조건 미달 시 (Screenout URL)
    - 정원 초과 시 (QuotaFull URL)
- [ ] 패널사별 파라미터(PID, UID 등) 치환자 가이드 안내 문구 추가
- [ ] 설정값 저장 API (`POST /api/v1/routing/postback`) 연동
- [ ] 현재 설정된 라우팅 정보 조회 및 표시

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 라우팅 링크 등록
- Given: 외부 패널사로부터 받은 3종의 링크가 준비됨
- When: 각 항목에 URL을 입력하고 [저장]을 클릭함
- Then: DB에 설정이 기록되고, 이후 응답 시 해당 링크로의 리다이렉트가 가능해져야 한다.

Scenario 2: URL 유효성 검증
- Given: 잘못된 형식(예: `abc.com`)의 URL을 입력함
- When: 저장을 시도함
- Then: "유효한 URL 형식이 아닙니다"와 같은 경고 메시지가 노출되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 보안: 입력된 URL이 악성 사이트 등으로 유도되지 않도록 기본적인 화이트리스트 검증 로직을 검토한다.
- UX: 설정이 없는 경우 "자사 응답 수집 모드"임을 명시하여 혼선을 방지한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 상태별 3종 URL 입력 및 저장 기능이 정상 작동하는가?
- [ ] URL 형식 유효성 검사가 서버/클라이언트 모두에서 수행되는가?
- [ ] 저장된 설정값이 대시보드에 정확히 표시되는가?

## :construction: Dependencies & Blockers
- Depends on: #MOCK-007 (라우팅 Mock), #API-012 (Postback DTO)
- Blocks: #BE-RT-001 (라우팅 핸들러 구현)
