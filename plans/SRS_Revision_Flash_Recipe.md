요청하신 대로 HWPX 지원 및 안내 UX 반영 사항을 포함하여 전체 작업 계획서를 업데이트했습니다. 이 내용을 그대로 복사해서 AI에게 전달하시면 됩니다.

---

# AI 프롬프트용 SRS V0.2 업데이트 작업 계획서

이 문서는 기존 `SRS_v0.1_Opus.md` 원본을 AI(Cursor, Gemini 등)에게 입력하여 **완전 무료 인프라(Vercel Hobby + Supabase Free) 및 1인 바이브코딩 최적화 버전(V0.2)**으로 자동 수정하도록 지시하기 위한 '프롬프트 플랜'입니다.

아래의 각 Step 블록을 복사하여 원본 SRS 문서와 함께 AI에게 순차적으로 명령(Prompt)하시면 됩니다.

### 💡 [사전 주입] 시스템 프롬프트 (System Prompt)
**목적:** AI가 수정 작업을 시작하기 전에 지켜야 할 절대 원칙을 부여합니다.

> **[AI 입력용 프롬프트]**
> 너는 지금부터 3년 차 IT 기획자이자 1인 풀스택 개발자(바이브코딩 활용)를 돕는 수석 아키텍트야. 
> 내가 제공하는 [원본 SRS 문서]를 분석하고, 내가 지시하는 '수정 요건'에 맞춰 SRS V0.2로 업데이트해 줘. 
> 
> **[업데이트 절대 원칙]**
> 1. 기존 문서의 ISO/IEC/IEEE 29148:2018 목차 구조와 마크다운 포맷팅(표, Mermaid 다이어그램 등)을 완벽하게 유지할 것.
> 2. 추가/수정되는 내용은 기술적으로 모순이 없어야 하며, '완전 무료 인프라(Vercel Hobby, Supabase Free)' 환경에서 1인 개발자가 구현 가능한 현실적인 스펙으로 작성할 것.

---

### 🛠️ [Step 1] 스코프 및 제약사항 수정 (Scope & Constraints)
**목적:** 구형 바이너리 HWP 파싱을 제외하되, XML 기반의 HWPX 지원을 명문화하고 사용자 안내 UX를 추가하며, 무료 인프라 제약을 명시합니다.

> **[AI 입력용 프롬프트]**
> 문서의 **1.2 Scope** 및 **1.4 Assumptions** 부분을 아래 요건에 맞게 수정해 줘.
> 
> * **In-Scope (IS-01):** HWP를 "HWPX(개방형 한글 포맷)"으로 변경하고, "Word(.docx), PDF, HWPX 텍스트 기반 파싱"으로 스코프를 확정할 것.
> * **Out-of-Scope:** "구형 바이너리 HWP 비정형 문서 파싱 (V2.0으로 연기)" 항목을 명시적으로 추가할 것.
> * **Constraints (CON-01):** "HWP 파일 업로드 시, 한컴오피스에서 'HWPX로 저장' 기능을 사용하도록 안내하는 사용자 가이드 UX 필수 포함"이라는 제약사항을 추가할 것.
> * **Constraints (CON-03 등):** 일일 파싱 횟수 제한(Rate Limit)을 "Supabase DB 기반 IP 체크 또는 유저별 카운트"로 명시. (별도 캐시 서버 불가)
> * **Assumptions:** >   * Vercel 플랜을 'Pro($20)'에서 'Hobby(무료)'로 변경. (Serverless Function 타임아웃 10초 제약 명시)
>   * Vercel KV(Redis) 사용 가정을 완전히 삭제하고, 모든 상태와 카운트는 Supabase PostgreSQL(Free)에 의존하는 것으로 변경.

---

### 🛠️ [Step 2] 아키텍처 및 시스템 인터페이스 수정 (Architecture)
**목적:** Vercel KV(Redis)를 제거하고 DB 직접 제어로 단일화합니다.

> **[AI 입력용 프롬프트]**
> 문서의 **3.1 External Systems** 및 **3.4 Component Diagram**을 아래 요건에 맞게 수정해 줘.
> 
> * **External Systems:** 'Vercel KV' 항목을 완전히 삭제.
> * **동시성 제어 대안:** Vercel KV 대신 "Supabase PostgreSQL의 RPC(Remote Procedure Call) 기능 또는 `UPDATE ... SET count = count + 1` 쿼리를 통한 원자적(Atomic) 연산"으로 교체.
> * **Mermaid 다이어그램 (3.4):** 아키텍처 구성도에서 Vercel KV(Redis 호환 카운터) 노드를 삭제하고, QuotaModule이 Supabase DB와 직접 통신하도록 화살표 수정.

---

### 🛠️ [Step 3] 기능 및 비기능 요구사항 현실화 (Functional & NFR)
**목적:** 무료 서버 환경에 맞춰 목표 성능치와 기능을 현실적인 수준으로 하향하고, HWPX 처리 방식을 구체화합니다.

> **[AI 입력용 프롬프트]**
> 문서의 **4.1 Functional Requirements** 와 **4.2 Non-Functional Requirements**를 아래 요건에 맞게 수정해 줘.
> 
> * **F1 (REQ-FUNC-001, 006):** 지원 포맷을 HWPX, Word, PDF로 변경할 것. REQ-FUNC-006의 구현 방식에서 HWPX의 경우 "`jszip` 라이브러리로 압축을 해제한 후, XML 파서를 활용하여 `Contents/section0.xml` 파일 내의 텍스트 노드를 추출하는 방식"으로 명시할 것.
> * **F1 (신규 추가):** 구형 HWP 확장자 업로드 시 "문서를 HWPX로 다른 이름으로 저장한 후 업로드해 주세요"라는 안내 모달이 1초 이내에 뜨도록 요구사항 추가.
> * **F4 (REQ-FUNC-020):** 쿼터 카운트 연산 시 DB 데드락 방지 로직을 'Vercel KV'에서 'Supabase DB 단일 트랜잭션 및 RPC 활용'으로 변경.
> * **성능 (REQ-NF-001~007):** Vercel Hobby의 Cold Start(초기 구동 지연)를 감안하여, API 응답 시간 기준을 완화 (예: p95 응답 시간 300ms -> 1,000ms 이하, 폼 렌더링 10초 이내 보장 불가 시 '로딩 스켈레톤 UI 적용 의무화' 추가).
> * **가용성 (REQ-NF-008):** "SLA 월 99.9% 보장" 조항을 삭제하고 "Vercel 및 Supabase 무료 티어 서비스 제공자의 가용성 정책을 베스트 에포트(Best-effort)로 준수"로 완화.
> * **확장성 (REQ-NF-029):** 동시 접속자 처리 기준을 "1,000명"에서 MVP 현실 수준인 "동시 접속 50~100명"으로 하향 조정.
> * **비용 (REQ-NF-022):** MVP 월간 인프라 예산을 "무료~최대 10만원"에서 **"완전 무료(0원, PG사 수수료 제외)"**로 변경.

---

### 🛠️ [Step 4] 시퀀스 다이어그램 및 시나리오 갱신 (Sequence Diagrams)
**목적:** 변경된 아키텍처에 맞춰 통신 흐름 다이어그램을 재작성합니다.

> **[AI 입력용 프롬프트]**
> 문서의 **3.6 Interaction Sequences**와 **6.3 Detailed Interaction Models**의 Mermaid 다이어그램을 아래 요건에 맞춰 재작성해 줘.
> 
> * **모든 다이어그램:** `participant KV as Vercel KV` 및 Redis 관련 캐시/조회 로직 노드를 전부 삭제할 것.
> * **6.3.3 동적 쿼터 제어 시퀀스:** 패널 접속 시 Redis에서 `WATCH/INCR` 하던 로직을 지우고, API Server가 Supabase DB에 직접 `Atomic Update 쿼리`를 날려서 잔여 쿼터를 확인하고 증감시키는 흐름으로 그릴 것.
> * **6.3.1 파싱 시퀀스:** OCR Engine에서 구형 HWP 분기 처리를 삭제하고, HWPX 분기(ZIP 해제 및 XML 파싱)를 반영할 것.

---

### 🛠️ [Step 5] 전체 정합성 검증 및 출력 (Final Polish)
**목적:** 충돌하는 내용이 없는지 마무리 검수를 지시합니다.

> **[AI 입력용 프롬프트]**
> 지금까지 지시한 Step 1~4의 내용을 바탕으로 전체 문서를 다시 한번 훑어보고, 아래 사항들을 점검한 뒤 **마크다운 전문(Full Text)을 출력해 줘.**
> 
> 1. 문서 앞부분의 요약(Executive Summary)이나 KPI 지표(동접 1,000명 등)에 여전히 과거 스펙이 남아있지 않은지 확인할 것.
> 2. `C-TEC` 기술 스택 정의 부분에서 무료 인프라 지향성이 잘 드러나는지 확인할 것.
> 3. 출력 결과물의 제목은 `# Software Requirements Specification (SRS) - V0.2 (무료 인프라 및 MVP 1인 개발 최적화)`로 설정할 것.