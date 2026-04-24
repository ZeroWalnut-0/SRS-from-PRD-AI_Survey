---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-DASH-002: 문항별 기본 통계 차트 및 요약 UI 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-DASH-002] 문항별 기본 통계 차트 및 요약 UI 구현
- 목적: 수집된 설문 응답을 문항별로 집계하여 시각화된 차트(막대, 원형 등)와 수치 요약을 제공함으로써 사용자의 데이터 분석을 돕는다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.6_REQ-FUNC-025`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- UI 라이브러리: `recharts` 또는 `shadcn/ui` chart 컴포넌트

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `app/(dashboard)/forms/[form_id]/stats/page.tsx` 생성
- [ ] 문항 타입별 차트 엔진 구현:
    - 단일/다중 선택: 가로 막대 차트(Bar Chart) 또는 원형 차트(Pie Chart)
    - 척도형: 평균값 및 분포 차트
    - 주관식: 최근 응답 리스트 및 워드클라우드(선택 사항)
- [ ] 응답 요약 카드 구현 (전체 응답 수, 이탈률, 평균 완료 시간)
- [ ] 차트 이미지 다운로드 기능 (선택 사항)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 객관식 문항 통계 시각화
- Given: 100건의 응답이 수집된 객관식 문항
- When: 통계 페이지를 확인함
- Then: 각 선택지별 득표수와 비율(%)이 차트로 표시되어야 한다.

Scenario 2: 데이터 갱신 시 차트 반영
- Given: 통계 화면을 보고 있는 도중 신규 응답이 제출됨
- When: 데이터를 새로고침함
- Then: 변경된 응답 수와 비율이 차트에 즉시 반영되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 대량 응답 집계 데이터 로딩 시 레이턴시 ≤ 500ms.
- 시각화: 색상 대비를 명확히 하여 차트 가독성을 높인다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 모든 문항 유형에 적합한 시각화 차트가 렌더링되는가?
- [ ] 응답 요약 정보가 정확히 계산되어 표시되는가?
- [ ] 반응형 레이아웃이 적용되어 모바일에서도 차트를 볼 수 있는가?

## :construction: Dependencies & Blockers
- Depends on: #BE-DASH-001 (집계 API)
- Blocks: None
