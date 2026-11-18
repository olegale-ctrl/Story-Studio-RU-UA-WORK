**Status: PROPOSAL — OWNER REVIEW REQUIRED.** Проверено 2026-11-18 (Europe/Kyiv).

Scope: DOCS_ONLY; экспериментальный MVP. Нет production permissions, реализации, покупок, регистрации, платных запросов, CI, merge или release.

# MVP-08.0 — Daily production model

## Units and separation

This is an **analytic PROPOSAL**, not measured throughput or purchase authorization. External price evidence checked2026-11-18: inventoryS13 PixVerse V6 silent720p9credits/s÷225=$0.04/s (H). This gives a concrete low-cost model; **it does not recommend spending or clear PixVerse commercial rights**. Rights conflictS17 blocks actual final use until resolved. Sensitivity costs below are scenarios, not equivalent model quality.

Let d=clip seconds, k=outputs/request, Qd=dailycredits, Qm=monthlycredits, Q0=one-timecredits, c=credits/request for that exact setting, p=USD/generatedsecond, r=unusable fraction including artistic/technical/rights rejection, h=usable-source fraction after trims/overlap, a=AI-video share of final timeline, L=filmseconds. t=average remote+download minutes, w=authorized concurrency, H=allowed hours/day, u=availability factor. **ASSUMPTION** inputs must be replaced with observed account/model values.

For credit plan n_day=floor(Qd/c)+floor((Qm_remaining/monthdays)/c) only if pools are actually fungible/valid; calculate each independentpool separately to avoid rounding/expiry errors. Q0 contributes once on eligible days, never daily refill. If one request yields k outputs charged individually, use requestcost reflecting k; do not multiply capacity for free. Budget mode n_month=floor(B/(p*d*k)), outputcount=n_month*k. Capacity cap n_day≤floor(60*H*w*u/t); choose min(spendquota,rate/concurrencyqueuecapacity). Generatedseconds G=n*d*k. Acceptedseconds A=G*(1-r). Usable AI timeline coverage C=A*h. Totalfilmcapacity C/a is possible **only if** the remaining (1-a)L has separately available, cleared stills/maps/local assets/narration. Coverage is union of **distinct** accepted intervals, not sum of duplicates/LOOP/HOLD repetitions.

Days=ceil(a*L/C_day) for steady-state expected-average planning with C_day>0; C_day=0 => not attainable. Initialtrial can reduce numerator once by C0, never reduce everymonth budget. Stochastic rejection and discrete clip requirements mean this simple ceil is not an SLA.

## Main monthly-budget scenario

**ASSUMPTION** B=$0/$10/$20/$50,30-daymonth;d=5s,k=1,p=$0.04/s silent720p; r=30% (no quality benchmark),h=80%,a=25%. No freevideoAPI daily pool assumed. Each clip$0.20. Budgets net of tax/FX/minimumdeposit/input upload/storage/egress; all extra costs would reduce capacity or require separate approved allowance. Inputs in this scenario not video references and no charged nativeaudio/upscale. Rateprice only H; every operational/quality input here **ASSUMPTION**.

Queue**ASSUMPTION** H=8h/day,w=1,t=5min,u=0.8 =>76requests/day ceiling; paidbudget below never hits it. Exceeding five minutes observed or account gating can reduce capacity. Remote SLA/rate not measured. B=0 excludes unqualified and exhaustedtrials.

| Monthlybudget |5soutputs/month|Generateds/month|Generateds/day (average)|Accepteds/day|Distinct AI coverages/day|Expected days:8min|10min|12min|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|$0|0|0|0.000|0.000|0.000|not attainable|not attainable|not attainable|
|$10|50|250|8.333|5.833|4.667|26|33|39|
|$20|100|500|16.667|11.667|9.333|13|17|20|
|$50|250|1250|41.667|29.167|23.333|6|7|8|

All paid rows are **conditional arithmetic, not guaranteed daily generation**. Day averages may be fractional clips; paced discrete scheduling can have zero-output days. For $10 exact example:50outputs→250s generated/month→175s expectedaccepted→140s usablecoverage. An8min25%AI film needs120scoverage,10min150s,12min180s. At monthly pacing some schedules take longer than ceil average; no claim of fullfilm in26days without the other360s of cleared content.

## Discrete single-film budget check

Conservative usable coverage per5s output in the model=5×0.7×0.8=2.8s.8/10/12min films at25%AI need ceil(120/2.8)=43, ceil(150/2.8)=54, ceil(180/2.8)=65 purchasedoutputs; expectedcost$8.60/$10.80/$13.00. This uses expectation, not binomial confidence. At100%AI required outputcounts172/215/258 and costs$34.40/$43.00/$51.60; corresponding main-table days roughly4× (recompute ceil, not exact4×rounded cells). Static/looped imagery does not turn purchasedseconds into unique AI coverage.

## Free mode and one-time exception

Sustained account-qualified recurring freeAPI capacity: not established; planning lowerbound**0s/day**,8/10/12min completion not attainable from such supply. Manualfreeweb capacity is not autonomouscapacity.

Alibaba S03/S48 documented50s once for eligibleWan2.1turbo,90dayvalidity. **ASSUMPTION** fresheligibleaccount+unusedquota+providerFreeQuotaOnly+legalapproval+alljobswork:10×5s=50generateds once,35accepteds,28susableAIcoverage at r/h above. This can cover112s of a25%AI film when remaining84s othercontent exists; it does not complete8/10/12min. Account not created/verified, so actualtrialcapacity**UNKNOWN**, not promised. No multiplying expiredmodelaliases/trials/accounts. Reset cannot manufacture additionaltrial.

Flow S40 manual theoretical50credits/day÷10×8s=40s/day if all5generations available/eligible; at assumedr/h22.4usableAIseconds. Excluded from automatic rows: no permitted unattendedroute proven; peaklimits, rights and downloads unresolved. Arena pair count is not a download/rights quota.

## Price and reject sensitivity

**ASSUMPTION** all p are output-only USD/s, same5s/k1/h0.8/a0.25 and B=$20. Base price sourced above; p=$0.08 approximates MiniMaxH3 768P output-onlyS20, p=$0.10 RunwayWan3 720pS23. These are not quality-equivalent. Values show acceptedseconds/day then usablecoverage/day then expected10minfilm days.

|p|r=10%|r=30%|r=50%|
|---|---|---|---|
|$0.04|15.000 / 12.000 / 13days|11.667 / 9.333 / 17days|8.333 / 6.667 / 23days|
|$0.08|7.500 / 6.000 / 25days|5.833 / 4.667 / 33days|4.167 / 3.333 / 45days|
|$0.10|6.000 / 4.800 / 32days|4.667 / 3.733 / 41days|3.333 / 2.667 / 57days|

## Retries, queues, limits and cost per accepted second

r already counts charged unusable attempts; don't silently apply a second “retry penalty” to the same reject. If billednetworkattempts fail without output, add separate f. Effective cost/usable second =p/((1-f)*(1-r)*h), assumingall failurescharged. For p.04,r.30,h.80,f0 =>$.071429; f.10 =>$.079365. If refunds verified, settle actual ledger, not assumedrefunds. Maxretry count/budget belongs to original job cap; “retry until good” is unbounded spending.

Queue downtime, rate limits, consent pauses, manualreviews, expiry, regionaccess and rights-holds can make actualacceptedcapacity**zero at any budget**. Duration-dependent billing minima, model-drivenclip lengths, multipleoutputs and selectedreferencecharges require recomputinginteger n. Taxes/minimumtopups vary; $10scenario is not proof anyprovider sells exact$10 bundle. No monthlysubscription converted toAPIcredits withoutsource.

To calibrate afterownerapproval: log ≥30authorizedrequests perselectedmode/model with charge/refund/latency and separate technical/artistic/rights passrates; report confidenceintervals, not justaverage.30 is an **ASSUMPTION** proposal, not expenditure authorization. OwnerD06 chooses planningrejectrange. Until then alldays conditional, Windows/runtimeperformanceNOT_RUN.
