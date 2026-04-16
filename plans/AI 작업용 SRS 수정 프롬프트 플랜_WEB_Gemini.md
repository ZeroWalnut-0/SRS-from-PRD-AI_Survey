📝 Step 1: 글로벌 컨텍스트 및 Scope 조정 (1. Introduction 수정)
목적: AI에게 1인 개발 및 $0 예산이라는 핵심 제약사항을 주입하고, Scope를 대폭 쳐내도록 지시합니다.

Plaintext
[System Role]
너는 1인 개발자를 위해 현실적이고 실행 가능한 소프트웨어 아키텍처와 요구사항을 설계하는 '시니어 테크니컬 PM'이야.
현재 첨부된 `SRS_v0.1_Opus.md` 문서를 기반으로, "1인 개발"과 "예산 0원(서버리스 무료 티어 활용)"이라는 조건에 맞춰 문서를 전면 수정해야 해.

[Task 1: 1. Introduction 섹션 수정]
다음 지침에 따라 '1. Introduction' 섹션을 수정해줘.

1. '1.2.1 In-Scope' 수정:
   - IS-01에서 HWP를 삭제하고 "Word/PDF 비정형 문서 파싱"으로 한정해.
   - IS-05(쿼터 세팅), IS-06(패널사 라우팅)을 완전히 삭제해.
2. '1.2.2 Out-of-Scope' 수정:
   - OS-06, OS-07을 추가해서 "HWP 파싱(Phase 2로 연기)", "동적 쿼터 및 패널사 라우팅(Phase 2로 연기)"을 명시해.
3. '1.2.3 Constraints (제약사항)' 수정:
   - CON-02(비용)를 "MVP 기간 내 월간 인프라 운영 예산 0원 (Vercel, Supabase 등 Serverless Free Tier 적극 활용)"으로 변경해.
   - CON-05를 삭제하고 "비용 0원을 위해 LLM API의 무료 티어(Gemini Flash 등)를 활용"하는 내용으로 대체해.
📝 Step 2: 인프라 아키텍처 및 시스템 컨텍스트 변경 (3. System Context 수정)
목적: 유료/엔터프라이즈급 인프라(AWS, DataDog 등)를 무료/BaaS 생태계로 교체하도록 지시합니다.

Plaintext
[Task 2: 3. System Context and Interfaces 섹션 수정]
비용 0원 달성을 위해 외부 시스템 및 아키텍처를 서버리스 기반으로 교체해줘.

1. '3.1 External Systems' 수정:
   - EXT-02 (AWS S3) -> "Supabase Storage (또는 Cloudflare R2) / 무료 티어 활용"으로 변경.
   - EXT-03 (패널사) -> 전면 삭제.
   - EXT-04, EXT-05 (DataDog, PagerDuty) -> 전면 삭제.
   - EXT-06 (Slack) -> "서버 에러 및 주요 알림용 Slack Webhook"으로 유지.
   - EXT-09 (Redis) -> "Upstash (Serverless Redis) / Rate Limit 및 캐시용"으로 변경.
2. '3.3 API Overview' 및 '3.4 Interaction Sequences' 수정:
   - 쿼터(Quota) 및 라우팅(Routing)과 관련된 모든 API 엔드포인트와 시퀀스 다이어그램(3.4.3)을 완전히 삭제해.
📝 Step 3: 모순 해결을 위한 기능/비기능 요구사항 현실화 (4. Specific Requirements 수정)
목적: 1인 개발자가 절대 구현할 수 없는 기능과, 무료 서버에서 불가능한 성능 지표를 현실적으로 하향 조정합니다.

Plaintext
[Task 3: 4. Specific Requirements 전면 수정]
무료 서버리스 환경의 기술적 한계(콜드 스타트, 커넥션 제한)를 반영하여 모순을 해결해줘.

1. '4.1 Functional Requirements' 수정:
   - F1 (REQ-FUNC-001 ~ 007): HWP 관련 내용을 모두 삭제하고 PDF/Word만 남겨. 데이터 손실률(1% 미만) 조건을 "핵심 문항 텍스트 인식률 90% 이상"으로 완화해.
   - F4, F5 (REQ-FUNC-018 ~ 025): 쿼터 및 외부 패널사 라우팅 요구사항을 통째로 삭제해.
2. '4.2 Non-Functional Requirements' (가장 중요) 수정:
   - REQ-NF-001 (성능): p95 300ms 이하를 "p95 2,000ms 이하 (서버리스 콜드 스타트 허용)"로 변경해.
   - REQ-NF-008 (가용성): SLA 99.9%를 "Best Effort (의존하는 BaaS 무료 티어 가용성에 따름)"로 변경해.
   - REQ-NF-018 (보안): 24시간 내 영구 삭제를 "Edge Cron Job을 활용한 일 단위 일괄 삭제"로 단순화해.
   - REQ-NF-021, 022 (비용): 단건 원가 20원, 월 500 USD를 "월 운영비 0원 (Free Tier 한도 내 방어)"로 수정해.
   - REQ-NF-024, 025, 026 (모니터링): DataDog/PagerDuty 관련 내용을 지우고 "Slack Webhook을 통한 주요 에러 로깅"으로 축소해.
   - REQ-NF-029 (확장성): 동시 접속 1,000명을 "동시 접속 50~100명 처리 (Supabase 무료 티어 커넥션 한계 반영)"로 하향 조정해.
📝 Step 4: 부록 및 데이터 모델 정리 (5. Traceability & 6. Appendix 수정)
목적: 삭제된 기능들의 흔적(DB 테이블, API 명세 등)을 문서 끝까지 추적해서 깔끔하게 지워냅니다.

Plaintext
[Task 4: 5. Traceability Matrix 및 6. Appendix 정리]
앞서 삭제한 요구사항(HWP, 쿼터, 라우팅, 유료 모니터링)의 흔적을 부록에서도 지워줘.

1. '5. Traceability Matrix' 수정:
   - 삭제된 REQ-FUNC 및 REQ-NF ID들을 매트릭스 테이블에서 모두 제거해.
2. '6.1 API Endpoint List' 수정:
   - /quotas, /routing 관련 엔드포인트(8번~11번)를 모두 삭제해.
3. '6.2 Entity & Data Model' 수정:
   - 6.2.5 QUOTA_SETTING, 6.2.6 QUOTA_CELL, 6.2.7 ROUTING_CONFIG 테이블 명세를 완전히 삭제해.
   - RESPONSE 테이블에서 quota_status, quota_group, routing_status 필드를 삭제해.
4. 다이어그램 및 시퀀스 수정:
   - 6.3.3 동적 쿼터 제어 및 패널 라우팅 상세 흐름도를 완전히 삭제해.

위의 모든 지시사항을 반영하여 완벽한 마크다운 형태의 `[수정본] SRS_v0.1_Opus_Diet.md` 전체 문서를 출