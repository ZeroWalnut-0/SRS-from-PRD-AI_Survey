---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-007: 모바일 웹 설문 응답 폼 렌더링"
labels: 'feature, frontend, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-007] 모바일 웹 설문 응답 폼 렌더링
- 목적: 응답자가 모바일 기기에서도 원활하게 설문에 참여할 수 있도록 `structure_schema` 기반의 반응형 설문 폼 UI를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.1_REQ-FUNC-008`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 클라이언트 기술: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#3.2_CLI-02`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 디자인 가이드: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#C-TEC-004`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 워터마크 요건: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3_REQ-FUNC-016`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `/app/(survey)/[form_id]/page.tsx` 경로 생성 및 서버 사이드 폼 데이터 페칭
- [ ] `structure_schema` 기반 동적 문항 렌더링 엔진 구현 (단일 선택, 복수 선택, 주관식 등)
- [ ] Tailwind CSS를 활용한 모바일 최적화 반응형 레이아웃 설계
- [ ] `shadcn/ui` 컴포넌트(Radio Group, Checkbox, Input) 기반 문항 UI 구성
- [ ] 설문 제출 처리 로직(Server Action 또는 Route Handler 호출) 연동
- [ ] 무료 사용자의 경우 하단 워터마크 배너 포함 렌더링

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 설문 폼 정상 렌더링
- Given: 유효한 `form_id`와 `structure_schema`가 존재함
- When: 모바일 브라우저로 설문 URL에 접속함
- Then: 모든 문항이 가독성 있게 렌더링되어야 하며, 특히 모바일 뷰포트에서 좌우 스크롤 없이 표시되어야 한다.

Scenario 2: 설문 응답 제출
- Given: 모든 필수 문항에 응답함
- When: [제출] 버튼을 클릭함
- Then: 응답 데이터가 서버로 전송되고, 성공 메시지 또는 리다이렉트가 수행되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: p95 응답 시간 ≤ 1,000ms (REQ-NF-001)
- 접근성: 모바일 터치 타겟 크기(최소 44x44px) 확보 및 웹 접근성 준수
- 비기능: 지연 발생 시 로딩 스켈레톤 UI 적용 (REQ-NF-003)

## :checkered_flag: Definition of Done (DoD)
- [ ] `structure_schema`의 모든 문항 유형이 정상적으로 화면에 표시되는가?
- [ ] 모바일 기기(iPhone, Android) 크롬/사파리에서 레이아웃이 깨지지 않는가?
- [ ] 제출 기능이 백엔드 API(`POST /api/v1/forms/{form_id}/responses`)와 연동되었는가?
- [ ] 하단 워터마크가 (무료 사용자의 경우) 정상적으로 노출되는가?

## :construction: Dependencies & Blockers
- Depends on: #MOCK-002 (Schema 샘플), #MOCK-003 (응답 Mock API)
- Blocks: #BE-FORM-004 (응답 제출 백엔드 구현), #FE-WM-001 (워터마크 구현)
