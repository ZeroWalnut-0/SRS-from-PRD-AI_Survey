# SRS V0.1 vs V0.2 변경사항 비교 검토 보고서

**작성일:** 2026-04-21  
**비교 대상:**
- **V0.1:** `SRS_v0.1_Opus.md` (Rev 1.1 — C-TEC 스택 전환 적용)
- **V0.2:** `SRS_v0.2_Opus.md` (Rev 1.2 — 무료 인프라 및 MVP 1인 개발 최적화)

---

## 1) 기술 스택의 명확성

V0.1에서 V0.2로 전환하며, 유료 서비스 의존성을 전면 제거하고 **완전 무료(Zero-cost) 인프라**로 단일화한 것이 핵심 변화입니다.

| # | 검토 항목 | V0.1 (Rev 1.1) | V0.2 (Rev 1.2) | 변경 근거 및 평가 |
|---|---|---|---|---|
| 1 | **Vercel 플랜** | **Pro ($20/월)** — 60초 함수 타임아웃, 1TB 대역폭 | **Hobby (무료)** — 10초 함수 타임아웃, 100GB 대역폭 | MVP 단계에서 월 $20 비용 절감. 10초 타임아웃은 스켈레톤 UI 의무화로 보완 |
| 2 | **동시성 제어 / 캐시** | **Vercel KV** (Redis 호환) — 쿼터 INCR, 파싱 캐시, Rate Limit 카운터 | **Supabase PostgreSQL RPC/Atomic Update** — DB 단일 트랜잭션으로 전체 처리 | Vercel KV 의존성 완전 제거. 무료 티어 범위 내 운영 확보 |
| 3 | **쿼터 카운트 연산** | Vercel KV의 `WATCH` / `INCR` 원자적 연산 | Supabase `UPDATE ... SET count = count + 1` 또는 RPC(PL/pgSQL) | 외부 캐시 없이 DB 단일 소스로 무결성 유지 |
| 4 | **Rate Limit 구현** | Vercel KV 기반 캐시 카운터 | **Supabase DB 기반 IP 체크 또는 유저별 카운트** (CON-03 명시) | 캐시 서버 비용 0원. ADR-02를 DB 중심으로 재해석 |
| 5 | **문서 파싱 라이브러리** | `pdf-parse`, `mammoth`, **`hwp.js`** | `pdf-parse`, `mammoth`, **`jszip`** (HWPX ZIP 해제 → XML 파싱) | 구형 HWP 바이너리 파서 → 개방형 HWPX 파서 전환. 기술 복잡도 ↓ |
| 6 | **컴포넌트 다이어그램 (§3.4)** | `QuotaModule` → `Vercel KV` 노드 존재 | `QuotaModule` → `DB` 직접 연결, **Vercel KV 노드 삭제** | 아키텍처 다이어그램 일관성 확보 |
| 7 | **외부 시스템 목록 (§3.1)** | EXT-07: **Vercel KV** 존재 (10개 항목) | Vercel KV **삭제**, EXT-08에 RPC 용도 명시 (9개 항목) | 관리 포인트 1개 감소 |
| 8 | **삭제 스케줄러 (§6.3.4)** | `participant S3 as AWS S3` | `participant Storage as **Supabase Storage**` | AWS 의존 제거, Supabase 단일 스토리지로 통일 |
| 9 | **KPI 측정 경로 (§6.4.2)** | `Amplitude 대시보드`, `DataDog APM` | **`Prisma 쿼리 대시보드`**, **`Vercel Analytics + AUDIT_LOG`** | 유료 분석 도구 제거, DB 직접 집계 + 무료 도구로 대체 |
| 10 | **용어 정의 (§1.3)** | **Vercel KV** 정의 포함 | Vercel KV 정의 **삭제** | 미사용 용어 제거로 문서 정합성 유지 |

> **핵심 판단:** V0.2는 Vercel KV(Redis)를 SPOF이자 비용 요소로 식별하고, Supabase PostgreSQL로 모든 상태를 통합하여 **관리 포인트를 최소화**했습니다. 단, DB 기반 원자적 연산은 Redis 대비 레이턴시가 높을 수 있으므로 트래픽 증가 시 성능 모니터링이 필수적입니다.

---

## 2) MVP 목표 및 가치전달 조정 내용

V0.1의 '소규모 프로덕션 수준' 목표에서 V0.2는 **'1인 개발자의 PMF 검증용 린(Lean) MVP'**로 명확히 피벗했습니다.

| # | 검토 항목 | V0.1 (Rev 1.1) | V0.2 (Rev 1.2) | 변경 근거 및 평가 |
|---|---|---|---|---|
| 1 | **문서 제목** | `Software Requirements Specification (SRS)` | `SRS - V0.2 (**무료 인프라 및 MVP 1인 개발 최적화**)` | 문서 목적이 제목에서 즉시 드러남 |
| 2 | **Purpose (§1.1)** | AI 기반 문서(**HWP**/Word/PDF) | AI 기반 문서(**HWPX**/Word/PDF) | 도입부부터 HWPX 중심 스코프 선언 |
| 3 | **지원 포맷 (IS-01)** | **HWP**/Word/PDF (구형 바이너리 HWP 포함) | **HWPX**(개방형)/Word/PDF (구형 HWP → **V2.0 연기**) | 기술 복잡도 제거, MVP 리드타임 단축 |
| 4 | **Out-of-Scope** | 5개 항목 (OS-01~05) | **6개 항목** — `구형 바이너리 HWP 파싱 (V2.0 연기)` 추가 | OS-01 신규 추가로 스코프 명확화 |
| 5 | **CON-01 기술 제약** | HWP 내부 복잡 표/수식 파싱 한계 | **HWPX(.hwpx) 기반 정형 텍스트 한정** + 전환 가이드 UX 필수 | 제약 범위를 좁혀 개발 범위 현실화 |
| 6 | **CON-02 월간 예산** | 무료 ~ 최대 **100,000원** | **완전 무료 (0원) 지향** | 1인 개발자 자본 부담 완전 제거 |
| 7 | **비용 테이블 합계** | **27,000 ~ 57,000 KRW** | **0 KRW** (전 항목 무료) | 비용 감축률 ▼85% → **▼100%** |
| 8 | **p95 응답 시간 (REQ-NF-001)** | ≤ **300ms** (동시 1,000명 기준) | ≤ **1,000ms** (무료 티어 기준) | Hobby Cold Start 반영 현실적 완화 |
| 9 | **스켈레톤 UI (REQ-NF-003)** | 언급 없음 | **스켈레톤 UI 의무화** 명시 | Cold Start 지연을 UX로 흡수하는 설계 |
| 10 | **가용성/SLA (REQ-NF-008)** | 월 **99.9%** (다운타임 ≤ 43.8분) | **Best-effort** (무료 제공자 정책 준수) | SLA 보장 불가한 무료 플랜 현실 인정 |
| 11 | **동시 접속자 (REQ-NF-029)** | **1,000명 이상** | **50~100명** | MVP 초기 트래픽 규모에 맞춤 |
| 12 | **쿼터 데드락 방지 (REQ-FUNC-020)** | Vercel KV INCR (1,000명+ 스파이크) | **Supabase DB 단일 트랜잭션 및 RPC** | 동접 하향에 따라 DB 수준에서 충분 |
| 13 | **ADR-02 Rate Limit** | 캐시 서버 구축으로 해시 기반 중복 절감 | **DB 기반 IP/유저 카운트** (캐시 서버 불가 명시) | 캐시 = 비용이므로 제거 |
| 14 | **ASM-06 (가정)** | Vercel **Pro** ($20), **60초** 타임아웃 | Vercel **Hobby** (무료), **10초** 타임아웃 | 타임아웃 6배 감소 → 파이프라인 최적화 필요 |
| 15 | **ASM-08 (가정)** | Vercel KV Free (3,000 req/day) 충분 | **Supabase PostgreSQL 트랜잭션에 전적 의존** | Vercel KV 의존 완전 제거, DB 단일 소스 |

> **핵심 판단:** V0.2는 "무조건 무료로 시작하여 PMF 검증 후 스케일업"이라는 린 스타트업 전략에 완벽히 부합합니다. 성능 목표 완화(300ms→1,000ms, 1,000명→100명)는 스켈레톤 UI와 Best-effort 정책으로 보완됩니다.

---

## 3) 기타 차이점

위 두 관점에 속하지 않는 세부적 변경사항들입니다.

| # | 검토 항목 | V0.1 (Rev 1.1) | V0.2 (Rev 1.2) | 변경 근거 및 평가 |
|---|---|---|---|---|
| 1 | **Tech Stack 메타데이터** | `Next.js + Vercel + Supabase + Gemini API` | `Next.js + **Vercel Hobby** + **Supabase Free** + Gemini API` | 티어(무료)를 메타데이터에 명시 |
| 2 | **§3.6.1 파싱 전처리** | `pdf-parse/mammoth/**hwp.js**` | `**jszip(HWPX)** / pdf-parse / mammoth` | hwp.js → jszip 명시적 전환 |
| 3 | **§3.6.3 쿼터 시퀀스** | `participant KV as Vercel KV`, Handler↔KV 통신 | KV **삭제**, Handler→DB 직접 Atomic Update | 외부 캐시 의존 제거 |
| 4 | **§6.3.1 상세 participant** | `Redis Cache`, `OCR Engine`, `DataDog APM` | Redis/OCR **삭제**, DataDog → `Vercel Analytics / Slack` | 유료 외부 도구 참조 전면 제거 |
| 5 | **§6.3.1 캐시 로직** | 해시 기반 캐시 조회 → 히트/미스 분기 → 캐시 저장 | **캐시 로직 전체 삭제** | 코드 복잡도 ↓, 관리 포인트 ↓ |
| 6 | **§6.3.1 문서 타입 분기** | `HWP→OCR 전용 추출` / `Word→OCR` / `PDF→OCR` | `HWPX→Parser: jszip XML` / `Word→Parser: mammoth` / `PDF→Parser: pdf-parse` | OCR 엔진 의존 제거, 내부 라이브러리로 단순화 |
| 7 | **§6.3.1 성능 경고** | `성능 경고 로그` | `성능 경고 로그 **(스켈레톤 UI 노출 연장)**` | Cold Start 대응 UX를 시퀀스에도 반영 |
| 8 | **§6.3.3 쿼터 상세** | `Redis: WATCH/INCR`, `Monitor→Slack` 체인 | **Redis 삭제**, `DB: Atomic Update/RPC`, `Note: Supabase 단일 트랜잭션` | 동시성 제어 DB 내재화 |
| 9 | **§6.3.4 삭제 스케줄러** | `participant S3 as AWS S3` | `participant Storage as **Supabase Storage**` | AWS 의존 완전 제거 |
| 10 | **§6.3.6 커스텀 빌드** | `Redis Cache`, `DataDog APM`, 캐시 무효화 로직 | **Cache 삭제**, `Vercel Analytics / Slack`, 캐시 무효화 삭제 | 커스텀 빌드 플로우 단순화 |
| 11 | **REQ-FUNC-006 구현** | `hwp.js`로 HWP 전처리 → Gemini API | `jszip` ZIP 해제 → `section0.xml` XML 파싱 → Gemini API | HWPX 파싱 방식 구체적 명시 |
| 12 | **REQ-FUNC-031 (신규)** | 해당 없음 | .hwp 업로드 시 **1초 이내 HWPX 전환 안내 모달** | OS-01(HWP 연기)에 대한 사용자 안내 보완 |
| 13 | **§5.2 추적 — p95** | `≤ 300ms` | `≤ **1,000ms**` | 본문과 동기화 |
| 14 | **§5.2 추적 — SLA** | `SLA ≥ 99.9%` | `**제공자 가용성 준수 (Best-effort)**` | 무료 티어 현실 반영 |
| 15 | **§5.2 추적 — 인프라** | `≤ 100,000 KRW` | `= **0 KRW**` | 완전 무료 목표 명확 반영 |
| 16 | **ERD — ZIP_DATAMAP** | `s3_download_url` | `**download_url**` | AWS S3 → Supabase Storage 필드명 반영 |
| 17 | **Class Diagram — ZipDatamap** | `s3DownloadUrl` | `**downloadUrl**` | ERD와 도메인 객체 필드명 동기화 |

> **정합성 검토 결과:** V0.2는 문서 전반(메타데이터, 제약사항, 가정, 외부 시스템, 컴포넌트, 시퀀스 다이어그램, NFR, 추적 매트릭스, ERD, 클래스 다이어그램, KPI 측정 체계)에 걸쳐 변경 사항이 **일관되게 반영**되어 있습니다. 잔여 정합성 이슈는 없습니다.

---

## 종합 평가

| 평가 축 | 결론 |
|---|---|
| **비용 최적화** | ✅ 월 인프라 비용 **0원** 달성. 1인 개발자의 자본 진입 장벽 완전 제거 |
| **기술 스택 단순화** | ✅ 외부 의존성 1개(Vercel KV) 제거, DB 단일 소스 원칙 달성, 관리 포인트 최소화 |
| **MVP 현실성** | ✅ 동접 50~100명, p95 1,000ms, 10초 타임아웃 내 파싱으로 현실적 스펙 설정 |
| **사용자 경험 보완** | ✅ 스켈레톤 UI 의무화, HWPX 전환 안내 모달 등 성능 완화에 따른 UX 대응 포함 |
| **문서 정합성** | ✅ 전체 문서 정합성 확인 완료. 잔여 이슈 없음 |

---

*End of Report*
