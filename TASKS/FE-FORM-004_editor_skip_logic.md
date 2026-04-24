---
name: Feature Task
about: SRS 기반의 구체적인 개발 태스크 명세
title: "[Feature] FE-FORM-004: 문항 스킵 로직(Skip Logic) 설정 UI 구현"
labels: 'feature, frontend, priority:medium'
assignees: ''
---

## :dart: Summary
- 기능명: [FE-FORM-004] 문항 스킵 로직(Skip Logic) 설정 UI 구현
- 목적: 특정 문항의 응답 값에 따라 다음 문항으로 건너뛰거나 설문을 종료하는 분기 로직을 설정할 수 있는 인터페이스를 구현한다.

## :link: References (Spec & Context)
> :bulb: AI Agent & Dev Note: 작업 시작 전 아래 문서를 반드시 먼저 Read/Evaluate 할 것.
- SRS 문서: [`/Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md#4.1.2_REQ-FUNC-014`](file:///Users/hodogood/SRS-from-PRD-AI_Survey/05_SRS_v1.md)
- 데이터 모델: `logic_rules` 필드 (JSON)

## :white_check_mark: Task Breakdown (실행 계획)
- [ ] 우측 속성 설정 창 내 '로직 설정' 섹션 구현
- [ ] 조건부 이동(Jump to) UI 구현: "만약 [응답값]이 [A]라면 -> [X번 문항]으로 이동"
- [ ] 스크린아웃(Screenout) 처리 옵션 추가: "설문 종료(탈락)" 선택 시 외부 라우팅 연동 준비
- [ ] 순환 참조(Circular Reference) 방지 검증 로직 구현 (이전 문항으로 이동 금지 등)
- [ ] 시각적인 로직 흐름 표시 (선택 사항: 다이어그램 또는 텍스트 요약)

## :test_tube: Acceptance Criteria (BDD/GWT)
Scenario 1: 기본 스킵 로직 설정
- Given: 1번 문항(객관식) 선택
- When: "1번 보기 선택 시 5번 문항으로 이동" 로직을 설정함
- Then: `structure_schema`의 해당 문항 데이터에 로직 규칙이 정확히 저장되어야 한다.

Scenario 2: 유효하지 않은 이동 차단
- Given: 5번 문항 선택
- When: "2번 문항으로 이동(역방향)" 로직을 시도함
- Then: 클라이언트 측에서 경고 메시지를 노출하고 설정을 차단해야 한다.

## :gear: Technical & Non-Functional Constraints
- 무결성: 설문 응답 엔진(FE-FORM-007)에서 해당 로직을 해석할 수 있는 표준 형식을 유지한다.
- **`logic_rules` JSON 스키마 (FE↔BE 공유 계약):**
```json
{
  "logic_rules": [
    {
      "rule_id": "rule_uuid",
      "source_question_id": "q_003",
      "condition": {
        "operator": "EQUALS",        // EQUALS | NOT_EQUALS | CONTAINS | IN
        "value": "1"                 // 선택한 보기 코드 또는 값
      },
      "action": {
        "type": "JUMP_TO",           // JUMP_TO | SCREENOUT | END_SURVEY
        "target_question_id": "q_007" // JUMP_TO인 경우만 필수
      }
    }
  ]
}
```
- 유효성: `target_question_id`는 반드시 `source_question_id`보다 후순위여야 한다 (순환 참조 방지).

## :checkered_flag: Definition of Done (DoD)
- [ ] 조건부 문항 이동 설정 UI가 정상 작동하는가?
- [ ] 스크린아웃(종료) 처리 로직 설정이 가능한가?
- [ ] 설정된 로직 데이터가 `structure_schema`에 올바르게 저장되는가?

## :construction: Dependencies & Blockers
- Depends on: #FE-FORM-002 (문항 편집)
- Blocks: #FE-FORM-007 (모바일 폼 렌더링 내 로직 처리)
