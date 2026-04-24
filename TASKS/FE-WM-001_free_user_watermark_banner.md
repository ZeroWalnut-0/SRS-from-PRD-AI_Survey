---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-WM-001: 무료 사용자 설문 폼 워터마크 배너 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-WM-001] 무료 사용자 설문 폼 워터마크 배너 구현
- 목적: 무료 서비스 이용자의 설문 응답 화면 하단에 고정된 워터마크 배너를 노출하여 서비스 홍보 및 유료 전환을 유도한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.3_REQ-FUNC-016`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 디자인 가이드: "Powered by AI Survey" 텍스트 및 로고 포함

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `components/survey/WatermarkBanner.tsx` 컴포넌트 생성
- [ ] 하단 고정(Fixed) 레이아웃 적용: 뷰포트 하단 100% 너비
- [ ] `viral_watermark_url` 존재 여부에 따른 조건부 렌더링 로직 구현
- [ ] 디자인 시스템에 맞는 스타일링 (다크/라이트 모드 대응)
- [ ] 배너가 설문 문항의 마지막 내용을 가리지 않도록 하단 여백(Padding) 추가

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 무료 설문 접근 시 배너 노출
- Given: `viral_watermark_url`이 설정된 무료 설문 폼에 접속함
- When: 화면이 렌더링됨
- Then: 페이지 하단에 "Powered by AI Survey" 워터마크 배너가 고정되어 보여야 한다.

Scenario 2: 유료 설문 접근 시 배너 숨김
- Given: 워터마크 URL이 `null`인 유료 설문 폼에 접속함
- When: 화면이 로드됨
- Then: 하단 배너가 노출되지 않아야 하며, 하단 여백도 최소화되어야 한다.

## :gear: Technical & Non-Functional Constraints
- 성능: 배너 이미지는 SVG 또는 경량화된 자산을 사용하여 로딩 속도에 영향을 주지 않도록 한다.
- UX: 응답자가 배너를 닫을 수 없도록(무료 계정 제약) 구현한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 워터마크 배너가 모든 무료 설문 하단에 정확히 렌더링되는가?
- [ ] 유료 사용자의 경우 배너가 완벽히 제거되는가?
- [ ] 모바일 기기별 하단 고정 위치가 정확한가?

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-007 (모바일 폼), #BE-WM-001 (URL 생성)
- Blocks: #FE-WM-002 (클릭 연동)
