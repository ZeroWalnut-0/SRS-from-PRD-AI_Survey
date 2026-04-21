# SRS V0.1 vs V0.2 변경사항 비교 검토 보고서

**작성일:** 2026-04-21  
**비교 대상:**
- **V0.1:** `SRS_v0.1_Opus.md` (Rev 1.1 — C-TEC 스택 전환 적용)
- **V0.2:** `SRS_v0.2_Opus.md` (Rev 1.2 — 무료 인프라 및 MVP 1인 개발 최적화)

---

## 1) 기술 스택의 명확성

V0.1에서 V0.2로 전환하며, 유료 서비스 의존성을 전면 제거하고 **완전 무료(Zero-cost) 인프라**로 단일화한 것이 핵심 변화입니다.

| 검토 항목 | V0.1 (Rev 1.1) | V0.2 (Rev 1.2) | 변경 근거 및 평가 |
|---|---|---|---|
| **Vercel 플랜** | **Pro ($20/월)**, 60초 함수 타임아웃, 1TB 대역폭 | **Hobby (무료)**, 10초 함수 타임아웃, 100GB 대역폭 | MVP 단계에서 월 $20 비용 절감. 10초 타임아웃 제약을 스켈레톤 UI 의무화로 보완 |
| **동시성 제어 / 캐시** | **Vercel KV** (Redis 호환) — 쿼터 카운트 INCR, 파싱 캐시, Rate Limit 카운터 | **Supabase PostgreSQL RPC/Atomic Update** — 모든 동시성 제어를 DB 단일 트랜잭션으로 처리 | Vercel KV(별도 서비스) 의존성 완전 제거. 무료 티어 범위 내 운영 가능성 확보 |
| **쿼터 카운트 연산** | Vercel KV의 `WATCH` / `INCR` 원자적 연산 | Supabase `UPDATE ... SET count = count + 1` 또는 RPC(PL/pgSQL) | 외부 캐시 서버 없이 DB 단일 소스로 무결성 유지. 성능은 소폭 저하 가능하나 50~100명 규모에서 충분 |
| **Rate Limit 구현** | Vercel KV 기반 캐시 카운터 (일일 3,000 req/day) | **Supabase DB 기반 IP 체크 또는 유저별 카운트** (CON-03 명시) | 캐시 서버 비용 0원. ADR-02 결정 사항을 DB 중심으로 재해석 |
| **모니터링 스택** | Vercel Analytics + Slack (3.1에서 `Redis → Vercel KV`로 표기) | Vercel Analytics + Slack (3.1에서 `Redis → Supabase PostgreSQL (Atomic Update)`로 표기) | Redis 관련 참조를 모두 Supabase PostgreSQL로 일원화하여 스택 혼선 제거 |
| **문서 파싱 라이브러리** | `pdf-parse`, `mammoth`, **`hwp.js`** (HWP 전용) | `pdf-parse`, `mammoth`, **`jszip`** (HWPX 전용 — ZIP 해제 후 XML 파싱) | 구형 HWP 바이너리 파서 대신 개방형 HWPX 포맷 파서로 전환. 기술 복잡도 ↓ |
| **컴포넌트 다이어그램 (3.4)** | `QuotaModule` → **`Vercel KV`** 노드 존재, `Vercel KV (Redis 호환 카운터)` 별도 컴포넌트 | `QuotaModule` → **`DB` 직접 연결**, Vercel KV 노드 완전 삭제 | 아키텍처 다이어그램의 기술 스택 일관성 확보 |
| **외부 시스템 목록 (3.1)** | EXT-07: **Vercel KV** 항목 존재 (10개 EXT 항목) | Vercel KV 항목 **완전 삭제**, EXT-08에 RPC 용도 명시 (9개 EXT 항목) | 관리 포인트 1개 감소 |
| **용어 정의 (1.3)** | **Vercel KV** 정의 포함 | Vercel KV 정의 **삭제** | 더 이상 사용하지 않는 용어를 제거하여 문서 정합성 유지 |

> **[핵심 판단]** V0.2는 Vercel KV(Redis)를 단일 장애 포인트(SPOF)이자 비용 요소로 식별하고, Supabase PostgreSQL로 모든 상태를 통합하여 **관리 포인트를 최소화**한 올바른 전환입니다. 다만 DB 기반 원자적 연산은 Redis 대비 레이턴시가 높을 수 있으므로, 트래픽 증가 시 성능 모니터링이 필수적입니다.

---

## 2) MVP 목표 및 가치전달 조정 내용

V0.1의 '소규모 프로덕션 수준' 목표에서 V0.2는 **'1인 개발자의 PMF 검증용 린(Lean) MVP'**로 명확히 피벗했습니다.

| 검토 항목 | V0.1 (Rev 1.1) | V0.2 (Rev 1.2) | 변경 근거 및 평가 |
|---|---|---|---|
| **문서 제목** | `Software Requirements Specification (SRS)` | `SRS - V0.2 (무료 인프라 및 MVP 1인 개발 최적화)` | 문서 목적(무료 인프라, 1인 개발)이 제목에서 즉시 드러남 |
| **지원 문서 포맷 (IS-01)** | **HWP**/Word/PDF (구형 바이너리 HWP 포함) | **HWPX**(개방형 한글)/Word/PDF (구형 HWP는 **V2.0으로 연기**) | 구형 HWP 파싱의 기술 복잡도를 제거하여 MVP 개발 리드타임 단축 |
| **Out-of-Scope 항목** | 5개 항목 (OS-01~05) | **6개 항목** (OS-01~06) — `구형 바이너리 HWP 파싱 (V2.0 연기)` 신규 추가 | 기존 IS-01(HWP)을 OS로 이관하고 HWPX로 대체. 스코프 명확화 |
| **HWP 업로드 안내 UX** | 별도 안내 없음 | **REQ-FUNC-031 신규 추가**: `.hwp` 확장자 업로드 시 1초 이내 HWPX 전환 안내 모달 | 사용자가 구형 HWP를 업로드해도 혼란 없이 대처할 수 있는 안내 UX 보장 |
| **CON-01 기술 제약** | HWP 내부 복잡 표/수식 파싱 정밀도 한계 | **HWPX(.hwpx) 기반 정형 텍스트 파싱에 한정** + HWPX 전환 가이드 UX 필수 포함 | 제약 범위를 좁혀 개발 범위를 현실적으로 조정 |
| **월간 인프라 예산 (CON-02)** | **무료~최대 100,000원** (Vercel Pro 포함) | **완전 무료 (0원) 지향** | 1인 개발자의 초기 자본 부담을 0원으로 제거 |
| **비용 테이블 합계** | **27,000 ~ 57,000 KRW** (Vercel Pro $20 포함) | **0 KRW** (전 항목 무료) | 비용 감축률 ▼85% → **▼100%**로 극적 전환 |
| **p95 응답 시간 (REQ-NF-001)** | **≤ 300ms** (동시 1,000명 기준) | **≤ 1,000ms** (무료 티어 기준) | Vercel Hobby의 Cold Start를 반영한 현실적 완화 |
| **스켈레톤 UI (REQ-NF-003)** | 요구사항 없음 | **스켈레톤 UI 의무화** 명시 | Cold Start로 인한 지연을 사용자 체감 품질 저하 없이 흡수 |
| **가용성/SLA (REQ-NF-008)** | **월 99.9% 이상** (다운타임 ≤ 43.8분) | **Best-effort** (무료 티어 제공자 정책 준수) | SLA 보장 불가한 무료 플랜의 현실 인정 |
| **동시 접속자 (REQ-NF-029)** | **1,000명 이상** (DB 데드락 없이 처리) | **50~100명 수준** | MVP 초기 트래픽 규모에 맞춘 현실적 하향 조정 |
| **쿼터 데드락 방지 (REQ-FUNC-020)** | Vercel KV 기반 INCR (동시 1,000명+ 트래픽 스파이크) | **Supabase DB 단일 트랜잭션 및 RPC** | 동접 50~100명으로 하향됨에 따라 DB 수준에서도 충분히 처리 가능 |
| **ADR-02 Rate Limit 전략** | 캐시 서버 구축을 통한 해시 기반 중복 비용 절감 | **Supabase DB 기반 IP/유저 카운트** (별도 캐시 서버 불가 명시) | 캐시 = 비용이므로 제거, DB 직접 조회로 대체 |
| **ASM-06 (가정)** | Vercel **Pro** 플랜($20/월), **60초** 타임아웃 충분 가정 | Vercel **Hobby(무료)**, **10초** 타임아웃 내 파싱 가능 가정 | 타임아웃 6배 감소에 대한 아키텍처 대응이 전반에 반영됨 |
| **ASM-08 (가정)** | Vercel KV Free 티어(3,000 req/day) 충분 가정 | **Supabase PostgreSQL 트랜잭션/원자적 연산에 전적 의존** | Vercel KV 의존 완전 제거, DB 단일 소스 원칙으로 전환 |

> **[핵심 판단]** V0.2는 "무조건 무료로 시작하여 PMF를 검증한 뒤 스케일업한다"는 린 스타트업 전략에 완벽히 부합합니다. 성능 목표의 완화(300ms→1,000ms, 1,000명→100명)는 스켈레톤 UI와 Best-effort 가용성 정책으로 보완되어 있어 사용자 경험에 미치는 영향은 제한적입니다.

---

## 3) 기타 차이점

위 두 가지 관점에 속하지 않는 세부적 변경사항들입니다.

| 검토 항목 | V0.1 (Rev 1.1) | V0.2 (Rev 1.2) | 변경 근거 및 평가 |
|---|---|---|---|
| **문서 메타 — Tech Stack** | `Next.js App Router + Vercel + Supabase + Gemini API` | `+ **Vercel Hobby** + **Supabase Free** + Gemini API` | 티어(무료)를 메타데이터에 명시하여 문서만으로 비용 구조 파악 가능 |
| **Purpose (1.1)** | AI 기반 문서(**HWP**/Word/PDF) → 설문 변환 | AI 기반 문서(**HWPX**/Word/PDF) → 설문 변환 | 도입부부터 HWPX 중심 스코프를 명확히 선언 |
| **3.6.1 파싱 시퀀스 — 전처리** | `pdf-parse/mammoth/**hwp.js**` | `**jszip(HWPX)** / pdf-parse / mammoth` | hwp.js → jszip으로 명시적 전환 |
| **3.6.3 쿼터 시퀀스** | `participant KV as Vercel KV`, Handler↔KV 통신 | KV participant **삭제**, Handler→DB 직접 Atomic Update | 외부 캐시 의존 제거, DB 직접 통신으로 단순화 |
| **6.3.1 상세 시퀀스 — participant** | `Redis Cache`, `OCR Engine`, `DataDog APM` | Redis/OCR **삭제**, DataDog → **`Vercel Analytics / Slack`** | 유료 외부 도구 참조 모두 제거 |
| **6.3.1 — 캐시 로직** | 해시 기반 캐시 조회 → 캐시 히트/미스 분기 → form_id 캐시 저장 | **캐시 관련 로직 전체 삭제** — 유효한 파일이면 바로 DB + Parser | 코드 복잡도 ↓, 관리 포인트 ↓ |
| **6.3.1 — 문서 타입 분기** | `HWP → OCR: HWP 전용 추출` / `Word → OCR: DOCX 추출` / `PDF → OCR: PDF OCR` | `HWPX → Parser: jszip XML 파싱` / `Word → Parser: mammoth` / `PDF → Parser: pdf-parse` | OCR 외부 엔진 의존 제거, Parser 내부 라이브러리로 단순화 |
| **6.3.1 — 성능 경고** | `Monitor→Monitor: 성능 경고 로그` | `Monitor→Monitor: 성능 경고 로그 **(스켈레톤 UI 노출 연장)**` | Cold Start 대응 UX를 시퀀스 다이어그램에도 반영 |
| **6.3.3 쿼터 상세 시퀀스** | `Redis: WATCH/INCR`, `Monitor→Slack` 체인 | **Redis 삭제**, `DB: Atomic Update/RPC`, `Note: Supabase DB 단일 트랜잭션` | 동시성 제어의 DB 내재화, 외부 캐시 동기화 이슈 근본 제거 |
| **6.3.6 커스텀 빌드 시퀀스** | `Cache as Redis Cache`, `DataDog APM`, 캐시 무효화 로직 | **Cache 삭제**, `Vercel Analytics / Slack`, 캐시 무효화 삭제 | 커스텀 빌드 플로우에서도 캐시 의존 제거, Slack 알림 일원화 |
| **REQ-FUNC-006 구현 방식** | `hwp.js`로 HWP 전처리 → Gemini API | **`jszip` ZIP 해제 → `section0.xml` XML 파싱** → Gemini API | HWPX 파싱 방식을 구체적으로 명시, 즉시 구현 착수 가능 |
| **REQ-FUNC-031 (신규)** | 해당 없음 | 구형 HWP 확장자 업로드 시 **1초 이내 안내 모달** | OS-01(HWP 연기)에 대한 사용자 안내 보완 |
| **5.2 추적 매트릭스 — p95** | `≤ 300ms` | `≤ **1,000ms**` | 본문과 일치하도록 동기화 |
| **5.2 추적 매트릭스 — SLA** | `SLA ≥ 99.9%` | `**제공자 가용성 준수 (Best-effort)**` | 무료 티어 대응 현실 반영 |
| **5.2 추적 매트릭스 — 인프라** | `≤ 100,000 KRW` | `= **0 KRW**` | 완전 무료 목표 명확 반영 |
| **ERD — ZIP_DATAMAP** | `s3_download_url` | `**download_url**` | AWS S3 → Supabase Storage 전환을 필드명에 반영 |
| **Class Diagram — ZipDatamap** | `s3DownloadUrl` | `**downloadUrl**` | ERD 변경에 맞춰 도메인 객체 필드명 동기화 |

> **[정합성 검토 결과]** V0.2는 문서 전반(메타데이터, 제약사항, 가정, 외부 시스템, 컴포넌트, 시퀀스, NFR, 추적 매트릭스, ERD, 클래스 다이어그램)에 걸쳐 변경 사항이 **일관되게 반영**되어 있습니다. 다만, 아래 잔여 이슈는 후속 정비가 필요합니다:
> - 6.3.4 삭제 스케줄러의 `AWS S3` 참조 → `Supabase Storage`로 변경 필요
> - 6.4.2 KPI 측정 체계의 `DataDog APM` / `Amplitude` 참조 → `Vercel Analytics / Slack`으로 변경 필요

---

## 종합 평가

| 평가 축 | 결론 |
|---|---|
| **비용 최적화** | ✅ 월 인프라 비용 0원 달성. 1인 개발자의 자본 진입 장벽 완전 제거 |
| **기술 스택 단순화** | ✅ 외부 의존성 1개(Vercel KV) 제거, 관리 포인트 감소, DB 단일 소스 원칙 달성 |
| **MVP 현실성** | ✅ 동접 50~100명, p95 1,000ms, 10초 타임아웃 내 파싱으로 현실적 스펙 설정 |
| **사용자 경험 보완** | ✅ 스켈레톤 UI 의무화, HWPX 전환 안내 모달 등 성능 완화에 따른 UX 대응 포함 |
| **문서 정합성** | ⚠️ 대부분 일관되나, 일부 잔여 참조(6.3.4 AWS S3, 6.4.2 DataDog/Amplitude) 후속 정비 필요 |

---

*End of Report*
