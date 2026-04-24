---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-PARSE-004: 파싱 한도 및 정확도 안내 모달 구현"
labels: 'feature, frontend, priority:low'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-PARSE-004] 파싱 한도 및 정확도 안내 모달 구현
- 목적: 업로드 전 AI 파싱의 기술적 한계(표/이미지 등)를 안내하고, 최적화된 템플릿 사용을 권장하여 사용자 기대를 관리한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.6_REQ-FUNC-027`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 리스크 대응: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#1.4.1_ADR-02`](#)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] `components/parser/PreUploadGuide.tsx` 컴포넌트 생성
- [ ] 업로드 화면 진입 시 또는 파일 선택 전 가이드 모달 노출 (쿠키 기반 '다시 보지 않기' 옵션 검토)
- [ ] 내용 구성: "표, 이미지, 수식 파싱 정확도 한계 안내" 및 "AI 최적화 템플릿 다운로드" 버튼
- [ ] 일일 파싱 한도(3회) 안내 문구 포함
- [ ] `shadcn/ui` 컴포넌트 활용

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 업로드 전 안내 확인
- Given: 사용자가 설문 생성 대시보드에 진입함
- When: 업로드 영역을 클릭하거나 접근함
- Then: 파싱 정확도 한계 및 템플릿 안내 모달이 노출되어야 한다.

Scenario 2: 템플릿 다운로드
- Given: 안내 모달이 노출된 상태
- When: [AI 최적화 템플릿 다운로드] 버튼을 클릭함
- Then: 준비된 샘플 문서 파일이 다운로드되어야 한다.

## :gear: Technical & Non-Functional Constraints
- UX: 잦은 모달 노출로 인한 피로도를 고려하여 닫기 로직을 간결하게 유지한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 파싱 정확도 한계 안내 문구가 포함되었는가?
- [ ] AI 최적화 템플릿 다운로드 링크가 정상 작동하는가?
- [ ] 디자인 시스템에 맞는 UI로 구현되었는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-PARSE-001 (업로드 UI)
- Blocks: None
