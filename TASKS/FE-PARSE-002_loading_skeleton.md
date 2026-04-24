---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PARSE-002: 파싱 대기 로딩 스켈레톤 UI 구현"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PARSE-002] 파싱 대기 로딩 스켈레톤 UI 구현
- 목적: 문서 업로드 후 AI 파싱이 진행되는 동안 사용자에게 진행 상태를 시각적으로 전달하여 체감 대기 시간을 줄인다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.2.1_REQ-NF-003`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 성능 요건: 10초 이상 지연 시 연장 표시 (REQ-NF-003)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `components/parser/ParsingSkeleton.tsx` 컴포넌트 생성
- [ ] 설문 폼 미리보기 형태의 스켈레톤 애니메이션 구현
- [ ] 파싱 단계별 안내 메시지 로직 구현 (예: "텍스트를 분석 중입니다...", "설문 문항을 구성 중입니다...")
- [ ] 10초 경과 시 "조금만 더 기다려 주세요, 거의 완료되었습니다" 등 연장 표시 로직 추가
- [ ] 파싱 상태 API (`GET /api/v1/documents/{doc_id}/status`) 폴링 연동

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 파싱 중 스켈레톤 노출
- Given: 문서 업로드가 완료되고 `PARSING` 상태임
- When: 화면이 전환됨
- Then: 실제 데이터 대신 스켈레톤 UI가 표시되어야 한다.

Scenario 2: 지연 시 안내 메시지 변경
- Given: 파싱이 시작된 지 10초가 경과함
- When: 여전히 `PARSING` 상태인 경우
- Then: 사용자에게 추가 대기를 요청하는 메시지가 화면에 노출되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 스켈레톤 컴포넌트 자체의 렌더링은 즉각적이어야 한다.
- 애니메이션: 부드러운 Pulse 효과를 적용하여 시스템이 작동 중임을 알린다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 스켈레톤 UI가 디자인 시스템에 맞게 구현되었는가?
- [ ] 파싱 상태 API 폴링 로직이 정상적으로 연동되었는가?
- [ ] 10초 경과 시 연장 메시지 표시 로직이 작동하는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-001 (업로드 UI), #MOCK-002 (상태 조회 Mock)
- Blocks: #FE-PARSE-006 (미리보기 화면 전환)
