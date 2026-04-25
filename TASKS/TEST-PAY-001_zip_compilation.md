---
name: Test Task
about: AC 기반의 구체적인 테스트 명세
title: "[Test] TEST-PAY-001: ZIP 5종 산출물 생성 검증 테스트"
labels: 'test, foundation, priority:high'
assignees: ''
---

## :dart: Summary
- 기능명: [TEST-PAY-001] ZIP 5종 산출물 생성 테스트
- 목적: 설문 수집 완료 후 생성되는 ZIP 파일 내에 필수 5대 구성 요소(응답 엑셀, 변수가이드, 코드북, 데이터맵, 할당표) 및 AI 내러티브 리포트가 정상 압축되어 있는지 검증한다.

## :link: References (Spec & Context)
- 요구사항: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#L503)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] ZIP 패키지 생성 API 호출
- [ ] 응답 바이너리를 디스크에 풀어서 파일 목록 및 내용 검사

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 5종 파일 존재
- Given: 유료 결제 완료 상태
- When: ZIP 다운로드
- Then: 압축 해제 시 `data_map.xlsx`, `codebook.pdf` 등의 파일이 온전히 존재한다.

## :checkered_flag: Definition of Done (DoD)
- [ ] 엑셀 파일이 손상되지 않고(Excel Viewer로 열림) 열리는지 체크

## :construction: Dependencies & Blockers
- Depends on: #BE-PAY-003
- Blocks: None
