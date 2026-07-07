# Direction B Stage-2 HYBRID panel screener spec

Status: quote-request package only. These are vendor quote scenarios, not
fielding commitments. The pre-registration in
`docs/thesis/directionB_preregistration.md` governs analysis and exclusions;
the fielding playbook in
`docs/thesis/directionB_stage2_fielding_playbook.md` governs operations.

## Open human decisions

| Decision | Default for vendor quotes | Human action |
|---|---|---|
| Recency window | Planned travel in next 12 months or recent travel in past 12 months | Confirm or revise before sending |
| EN panel composition | Domestic-international mix acceptable if screened to the same travel criteria | Decide whether EN must be Japan-resident, international, or mixed |
| Budget ceiling | Not stated | Provide ceiling before launch ADR; quotes must price all scenarios below |

## Target population

Online panelists eligible for an anonymous browser instrument in English or
Japanese, screened for planned or recent Hokuriku rail travel without
telegraphing the quota condition. Target geography: Fukui, Ishikawa, or
Toyama. Target travel mode: shinkansen or other rail as the main arrival mode
or intended main arrival mode.

Working eligibility definition for quotes:

- Planned: considering or planning leisure travel to Fukui, Ishikawa, or
  Toyama in the next 12 months, with shinkansen or other rail as the main
  arrival mode.
- Recent: completed leisure travel to Fukui, Ishikawa, or Toyama in the past
  12 months, with shinkansen or other rail as the main arrival mode.
- Exclude: professional travel-industry respondents; minors if vendor panel
  includes them; respondents who fail the attention/consistency check.

The 12-month window is a proposed human decision, not frozen design language.

## Screener items

Use neutral study framing: "travel planning and destination information."
Do not mention Fukui tourism sponsorship, rail-traveler quotas, or the
condition structure. Randomize option order where feasible, except "None" and
"Prefer not to say."

| # | Purpose | English item | Japanese item | Routing |
|---:|---|---|---|---|
| S1 | Planned travel | In the next 12 months, which of these areas are you seriously considering for a leisure trip? Select all that apply. Options: Fukui Prefecture; Ishikawa Prefecture; Toyama Prefecture; Nagano Prefecture; Gifu Prefecture; Niigata Prefecture; Kyoto/Osaka area; somewhere else in Japan; not considering leisure travel in Japan. | 今後12か月以内に、観光・レジャー目的の旅行先として具体的に検討している地域をすべて選んでください。選択肢：福井県；石川県；富山県；長野県；岐阜県；新潟県；京都・大阪方面；日本国内のその他の地域；日本国内の観光・レジャー旅行は検討していない。 | Eligible path if any of Fukui/Ishikawa/Toyama selected and S3 rail/shinkansen selected. |
| S2 | Recent travel | In the past 12 months, which of these areas have you visited for leisure? Select all that apply. Options: Fukui Prefecture; Ishikawa Prefecture; Toyama Prefecture; Nagano Prefecture; Gifu Prefecture; Niigata Prefecture; Kyoto/Osaka area; somewhere else in Japan; none of these. | 過去12か月以内に、観光・レジャー目的で訪れた地域をすべて選んでください。選択肢：福井県；石川県；富山県；長野県；岐阜県；新潟県；京都・大阪方面；日本国内のその他の地域；この中にはない。 | Eligible path if any of Fukui/Ishikawa/Toyama selected and S4 rail/shinkansen selected. |
| S3 | Planned main mode | For the trip you are most likely to take from the places selected above, what would probably be your main way of arriving in the area? Options: shinkansen; other train/rail; highway bus or coach; rental car; private car; domestic flight; tour bus; not decided yet; other. | 上で選んだ地域のうち、最も行く可能性が高い旅行について、現地エリアまでの主な到着手段は何になりそうですか。選択肢：新幹線；その他の鉄道；高速バス・貸切バス；レンタカー；自家用車；国内線航空機；ツアーバス；まだ決めていない；その他。 | Planned eligible if shinkansen or other train/rail. Retain nonrail responses for incidence denominator. |
| S4 | Recent main mode | For your most recent leisure trip to the places selected above, what was your main way of arriving in the area? Options: shinkansen; other train/rail; highway bus or coach; rental car; private car; domestic flight; tour bus; other; I have not taken this trip. | 上で選んだ地域への直近の観光・レジャー旅行について、現地エリアまでの主な到着手段は何でしたか。選択肢：新幹線；その他の鉄道；高速バス・貸切バス；レンタカー；自家用車；国内線航空機；ツアーバス；その他；そのような旅行はしていない。 | Recent eligible if shinkansen or other train/rail. Retain car/bus/flight responses for incidence denominator. |
| S5 | Travel party and purpose mask | Which statement best describes that trip or likely trip? Options: mostly sightseeing/leisure; visiting friends or relatives; event/festival/sports; food/hot spring trip; business or conference; school/research; transit through the area; other. | その旅行、または予定している旅行に最も近いものを選んでください。選択肢：主に観光・レジャー；友人・親族訪問；イベント・祭り・スポーツ観戦；食・温泉目的；出張・会議；学校・研究；通過・乗り継ぎ；その他。 | Exclude if business/conference only and no leisure selection in S1/S2 context. |
| S6 | Professional exclusion | Do you currently work in any of the following roles? Select all that apply. Options: travel agency or tour operator; railway, bus, airline, taxi, or car-rental company; hotel/ryokan or tourism attraction management; destination marketing/tourism bureau; market research or advertising; none of these; prefer not to say. | 現在、次のいずれかの業務に従事していますか。あてはまるものをすべて選んでください。選択肢：旅行会社・ツアー事業者；鉄道・バス・航空・タクシー・レンタカー会社；ホテル・旅館・観光施設の運営；観光協会・DMO・自治体観光部門；市場調査・広告；この中にはない；回答しない。 | Exclude travel-industry roles: travel agency/tour operator; transport operator; hotel/ryokan/attraction management; destination marketing/tourism bureau. Market research/advertising may be retained unless vendor policy excludes. |
| S7 | Attention/consistency | To check survey quality, please select "highway bus or coach" for this question. Options: shinkansen; other train/rail; highway bus or coach; private car; domestic flight. | 回答品質確認のため、この設問では「高速バス・貸切バス」を選んでください。選択肢：新幹線；その他の鉄道；高速バス・貸切バス；自家用車；国内線航空機。 | Exclude if not selected. Place after mode items. Do not use outcome/accuracy checks for exclusion after main instrument entry. |

Eligible respondent:

1. S1 or S2 includes Fukui, Ishikawa, or Toyama.
2. Matching S3 or S4 main mode is shinkansen or other rail.
3. S5 is not business/conference-only.
4. S6 does not indicate travel-industry professional role.
5. S7 passes.

## Quota and volume quote scenarios

Formula for quoting only:
`n(d)=ceil(2*(1.959964+0.841621)^2/d^2)` per arm.

Playbook §1 states mixed-model credit for two tasks per participant enters as
approximately `n(d_plan) * (1 + r_hat) / 2`. The table shows quote scenarios
at `r = 0.3` and `r = 0.5`; actual Stage-2 size is determined only after the
Stage-1 readout using the frozen pre-registration §5 rule
`d_plan = max(0.10, d_hat - SE(d_hat))`.

| d_plan quote scenario | n/arm before credit | 3-arm total before credit | 5-arm total before credit | n/arm with r=0.3 | 3-arm total r=0.3 | 5-arm total r=0.3 | n/arm with r=0.5 | 3-arm total r=0.5 | 5-arm total r=0.5 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.10 | 1,570 | 4,710 | 7,850 | 1,021 | 3,063 | 5,105 | 1,178 | 3,534 | 5,890 |
| 0.125 | 1,005 | 3,015 | 5,025 | 654 | 1,962 | 3,270 | 754 | 2,262 | 3,770 |
| 0.15 | 698 | 2,094 | 3,490 | 454 | 1,362 | 2,270 | 524 | 1,572 | 2,620 |
| 0.20 | 393 | 1,179 | 1,965 | 256 | 768 | 1,280 | 295 | 885 | 1,475 |

Arm-count quote branches from playbook §3:

| Branch | Arms to quote | Operational meaning |
|---|---|---|
| 3-arm | `control`, `transport_access`, `combined` | Used if `d_plan < 0.15`, or if cost/availability requires arm reduction under the frozen ladder. |
| 5-arm | `control`, `transport_access`, `opening_hours_availability`, `itinerary_fit_time_cost`, `combined` | Used if `d_plan >= 0.15` and budget/vendor feasibility preserve secondary contrasts. |

These are pricing scenarios only. They do not authorize interim looks,
outcome-based stopping, or changing the pre-registration.

## Incidence and pricing requirements

Expected screener incidence is low in general JP/EN panels because the
eligibility stack is narrow: planned or recent leisure travel to Fukui,
Ishikawa, or Toyama; shinkansen/rail as main arrival mode; no travel-industry
professional role; pass quality check.

Vendors must quote incidence assumptions explicitly:

| Required quote element | Vendor response needed |
|---|---|
| Estimated raw incidence | Percent of invited panelists expected to pass S1/S2 geography and 12-month window. |
| Estimated rail incidence | Percent expected to pass Hokuriku geography plus shinkansen/rail mode. |
| Final eligible incidence | Percent expected after professional exclusion and attention check. |
| Feasible delivery | Completes per week by language and by 3-arm/5-arm branch. |
| Pricing | Per-complete pricing at stated incidence bands, not a flat CPI detached from incidence. |

Request pricing at minimum for these incidence bands: `<1%`, `1-3%`, `3-5%`,
and `>5%`, separately for EN and JP if vendor pricing differs.

## Vendor quote-request template: English

Subject: Quote request: screened EN/JP online panel for Hokuriku travel study

Dear [Vendor],

We are requesting a quote for an anonymous browser-based academic travel
planning study. The sample will be screened from EN and JP online panels for
adults with planned or recent leisure travel to the Hokuriku area
(Fukui/Ishikawa/Toyama), including shinkansen or other rail as the main
arrival mode.

Please quote the volume scenarios in the attached table for both a 3-arm and
5-arm design. These are quote scenarios only; final launch size will be fixed
after an internal Stage-1 readout. Candidate fielding windows are autumn 2026
and spring 2027. The online panel main sample may launch once study gates are
met; the station QR subsample, if active, is seasonal.

Instrument requirements:

- Device-agnostic browser instrument hosted by the research team.
- Vendor sends respondents to the study URL with only an anonymous panel ID or
  redirect token needed for completion reconciliation.
- No personally identifying information is passed to the research team.
- EN and JP instruments are required.
- Stratification variables `fukui_familiarity` and
  `japan_travel_experience` are collected inside the instrument; the vendor
  does not need to quota on them.

Complete definition:

A complete is a respondent who passes the screener, enters the hosted
instrument, completes both assigned travel-planning tasks, and completes the
pre-task strata items. Partial completions are not completes. The study does
not exclude completes based on outcome values or in-instrument accuracy-item
performance.

Please provide:

1. Expected incidence assumptions for each screener stage.
2. Per-complete pricing at incidence bands `<1%`, `1-3%`, `3-5%`, and `>5%`.
3. Feasible completes per week by language.
4. Any constraints on EN panel composition: Japan-resident, international, or
   mixed.
5. Redirect, reconciliation, and fraud-control requirements.

Regards,

[Name]

## Vendor quote-request template: Japanese

件名：見積依頼：北陸旅行調査向け EN/JP オンラインパネル

[Vendor] ご担当者様

匿名のブラウザ型学術調査について、オンラインパネルの見積をお願い
いたします。対象は、福井県・石川県・富山県を含む北陸エリアへの観光・
レジャー旅行を予定している、または過去12か月以内に経験した成人で、
主な到着手段が新幹線またはその他の鉄道である方をスクリーニングする
想定です。

添付の数量シナリオについて、3群設計と5群設計の両方でお見積ください。
これらは見積用シナリオであり、最終的な実施数は内部のStage-1結果確認後
に固定します。候補となる実査時期は、2026年秋および2027年春です。
オンラインパネルの本サンプルは研究上の開始条件が満たされ次第開始する
可能性があり、駅QRサブサンプルを実施する場合は季節窓に従います。

調査仕様：

- 研究チームがホストする、端末を問わないブラウザ調査。
- ベンダー様からは、完了照合に必要な匿名パネルIDまたはリダイレクト
  トークンのみを付与して調査URLへ送客。
- 個人を特定できる情報は研究チームへ提供しない。
- 英語版および日本語版の調査票が必要。
- 層化変数 `fukui_familiarity` と `japan_travel_experience` は
  調査内で取得するため、ベンダー様側での割付・割当は不要。

完了の定義：

完了とは、スクリーナーを通過し、研究チームがホストする調査に入り、
割り当てられた2つの旅行計画タスクと事前の層化項目を完了した回答者を
指します。途中離脱は完了に含めません。主要な分析では、回答結果の値や
調査内の正答確認項目の成績を理由とした完了者の除外は行いません。

以下をご提示ください。

1. スクリーナー各段階の想定出現率。
2. 出現率 `<1%`、`1-3%`、`3-5%`、`>5%` の各帯における完了単価。
3. 言語別の週あたり実現可能完了数。
4. 英語パネル構成上の制約（日本在住、海外在住、混合など）。
5. リダイレクト、完了照合、不正回答対策に関する要件。

よろしくお願いいたします。

[Name]
