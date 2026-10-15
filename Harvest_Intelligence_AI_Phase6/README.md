# Harvest Intelligence AI — Phase 6

Complete local source through Phase 6: seven working screens, a rule-based assistant grounded in active calculations, and English-only or Tamil-only application text. Phase 7 final judging-demo verification remains pending.

Python, Streamlit, Pandas, Plotly and SQLite. No API key, external AI model or live data service is required. Internet is needed only for initial dependency installation.

## Windows VS Code — exact commands

Install Python 3.11 or 3.12 and the VS Code Python extension. Extract the ZIP into `C:\Harvest_Intelligence_AI_Phase6`; it contains the project folder `Harvest_Intelligence_AI_Phase6`.

Open VS Code in that project folder. Choose **Terminal → New Terminal → Command Prompt**:

```bat
cd /d C:\Harvest_Intelligence_AI_Phase6\Harvest_Intelligence_AI_Phase6
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

For Python 3.12, replace `py -3.11` with `py -3.12`. Open http://localhost:8501. Stop with Ctrl+C. In VS Code, use **Python: Select Interpreter** and choose `.venv\Scripts\python.exe`.

PowerShell without activation:

```powershell
Set-Location C:\Harvest_Intelligence_AI_Phase6\Harvest_Intelligence_AI_Phase6
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app.py
```

SQLite ships with Python. No Node.js installation or frontend build is required; the Tamil upload component is included as a local HTML asset. `requirements-tested.txt` records the exact tested direct dependency versions.

## Seven screens

| Screen | Delivered behavior |
|---|---|
| Home | Introduction, demo downloads and shared navigation |
| Upload Data | Separate agriculture/buyer uploads, automatic suggestions, editable mapping, strict validation and record-level quality reports |
| Dashboard | Five calculated KPIs, crop filters, charts, active data and provenance |
| Surplus and Risk | Explicit planning rules, adjustable thresholds, calculated crop priority, explanations and exports |
| Buyer Matching | Capped source-order allocations, unmatched quantities, full buyer audit and opportunity labels |
| Profit Analysis | Buyer gross/transport/return breakdown, equal-quantity market reference, explicit optional transport scenario |
| AI Assistant | Deterministic English/Tamil questions, evidence tables, calculation sources and current-data answers |

All screens use the same validated agriculture and buyer data in Session State. Invalid uploads never replace prior validated data. New browser sessions start empty. Save/restore persists both datasets, provenance and applied risk settings in `data/harvest.sqlite3`. Set `HARVEST_DB_PATH` to override the database path. Older Phase 1–5 snapshots are supported. Optional financial scenarios and assistant conversation contexts are session-only.

## Phase 6 walkthrough

1. Start the app and click **Load demo data**. Both supplied CSVs load as sample datasets.
2. Select English: app headings, captions, controls, table/report text, chart labels and assistant replies are English only.
3. Open AI Assistant. Use **Which crop should I prioritise?** or type it into the question box.
4. Expected reasoning: Tomatoes has 500 − 300 = **200 kg potential surplus**, larger than the 50 kg Onion surplus. The source-order preview potentially matches **180 kg**, leaving **20 kg**. Combined return after buyer transport is **₹4,430**. These remain potential opportunities and estimated returns, not confirmed orders or profit.
5. Ask about surplus/shortages, buyer matches, transport returns or risk rules. The scope selector applies to these topics; priority always ranks all active crops. A crop named in the question takes precedence over the scope selector.
6. Select Tamil. All generated application text switches to Tamil only, including existing answers and evidence. A question may be entered in either supported language; the answer language follows the selected option.
7. Change active quantities through Upload Data. Return to the assistant: existing question contexts are recalculated from the new inputs. For example, raising Onion availability to 1,000 kg gives a 650 kg surplus and changes the global first priority to Onions.
8. Requests for live prices, weather, model forecasts or confirmed orders receive a supported-scope response instead of fabricated facts.

## Assistant contract

`harvest/assistant.py` contains pure question routing and structured responses. It calls the same `calculate_kpis`, `crop_balances`, `analyse_risk`, `prioritise_crop`, `matching_preview`, `analyse_financials` and `financial_totals` functions as the other screens. No result is hardcoded to the demo crop names or numbers.

Supported topics are limited and explicit. This is a rule-based assistant, not an unrestricted language model. Unsupported/ambiguous questions receive a scope explanation. Unknown named crops are not replaced with invented stock. Missing buyer data is reported rather than replaced with sample buyers.

The interface keeps at most 20 question contexts in the browser session. Replies are recalculated on every rerun and rendered in the selected language; they are not stale stored answer strings. The visible question heading uses the recognized topic in the selected language. Original typed questions remain in internal session state. Clear conversation removes these contexts. Conversation downloads contain current localized answers. No messages are sent to buyers and no external model is contacted.

## Language contract — preserved for Phase 7

- English mode renders English application text only. Tamil mode renders Tamil application text only. No bilingual concatenation or English fallback is used for generated Tamil labels.
- The central catalog and rendering boundary cover navigation, messages, mappings, quality reports, crop/buyer labels, status values, calculations, charts, evidence, provenance summaries, report downloads and assistant replies.
- Tamil mode uses the included Tamil file-upload component, a labelled Tamil question form, and static localized tables to avoid the default English upload instructions and table-toolbar text. Chart toolbars are disabled. English mode retains the standard English uploader and interactive tables.
- Known demo crop and buyer names have explicit translations. For an unknown identifier written in a different script, the interface uses a stable numbered label such as “Crop 1” or its Tamil counterpart. It does not guess a translation or change the original identity used by calculations/storage. Source record numbers help locate the original row.
- Canonical uploaded records, source filenames, validation metadata and SQLite values remain unchanged internally. Original source files included in this ZIP retain their original schemas. Downloaded user-facing reports follow the selected language; they are display/report exports, not lossless backups of foreign-script source identifiers. Use the SQLite snapshot or original source files for lossless backup.
- Localized agriculture/buyer column headers are also recognized when re-uploaded. To preserve crop identity when importing localized files, use consistently localized agriculture and buyer datasets; matching remains exact, ignoring case and outer whitespace.
- Metadata reports represent source hashes as equivalent decimal identifiers in order to avoid Latin hex letters in Tamil reports. Original hexadecimal hashes remain in internal metadata.
- User-typed input, the operating system's own file picker and the browser's own controls belong to the user/host environment. Their language is not changed by this app. Application-generated labels and replies follow the selected language.

See `AGENTS.md` and `docs/LANGUAGE_POLICY.md` for the same requirement applied to subsequent work.

## Demo data and required results

`data/agriculture_demo.csv` and `data/buyers_demo.csv` contain the exact original records requested for the demo.

| Check | Calculated result |
|---|---:|
| Uploaded agriculture records | 3 |
| Available | 1,050 kg |
| Uploaded estimated demand | 850 kg |
| Sum of positive crop surpluses | 250 kg |
| Sum of crop shortages | 50 kg |
| Tomato positive surplus | 200 kg |
| Tomato potentially matched / still unmatched | 180 / 20 kg |
| Green Leaf after transport | ₹2,600 |
| City Hostel after transport | ₹1,830 |
| Combined Tomato after transport | ₹4,430 |

## Validation and calculation rules

CSV limits: 10 MB, 50,000 records, UTF-8/UTF-8-BOM, comma-delimited. Duplicate/blank headers, ragged/blank records, blank required text, negative/non-finite/malformed numbers and duplicate crop/buyer-crop identities are rejected. Zero values and fractional quantities are allowed. One record per crop is accepted. No silent imputation, duplicate dropping or partial invalid-row activation occurs. Ambiguous aliases require manual mapping. Extra unmapped columns are excluded with a warning. Quality reports distinguish invalid and unassessed rows.

- Crop surplus = `max(available − uploaded estimated demand, 0)`.
- Crop shortage = `max(uploaded estimated demand − available, 0)`.
- Sum positive surpluses and shortages separately. The 200 kg net gap is not the 250 kg positive-surplus KPI.
- Uploaded demand is an estimate, never a model forecast. Harvest age is the uploaded value in days; it does not advance automatically with the clock.
- Risk defaults are adjustable **planning choices**, not crop shelf-life science: positive surplus share ≥25% and stock age ≥3 days. Score for surplus crops = large-surplus flag + age-review flag: 0 Low, 1 Moderate, 2 High. Other crops show No surplus, with age review independently visible. Selling rank is surplus kg descending, then age descending, then case-insensitive crop name ascending.
- Matching processes every validated buyer/crop row once in original CSV order. Each match is `min(remaining surplus, requested kg)`. Repeated runs recompute rather than append allocations. Filters affect views after complete calculations. Unknown buyer crops, zero requests, no surplus and exhausted surplus remain visible in the audit.
- Each positive buyer/crop allocation incurs its full quoted transport once, including partial matches. Different crops for one buyer represent separate quoted trips. Zero allocations incur no trip or cost.
- Currency: round gross line amounts and charged costs to paise using decimal half-up, then subtract; totals sum those rounded lines. Negative returns stay visible. Unsupported oversized derived amounts produce a clear error.
- Buyer return after transport = matched kg × offered price − charged transport. This is **not actual profit**; production, labour, packaging, storage, taxes and other costs are unknown.
- The market gross reference uses the **same matched quantity** × uploaded market price. Market transport is unknown unless the optional financial scenario is explicitly enabled. For Tomatoes, 180 × ₹25 = ₹4,500 before those costs. Entering a ₹100 market-transport assumption gives ₹4,400 for that scenario; it does not establish actual profit.
- Unmatched Tomato surplus has a separate 20 × ₹25 = ₹500 reference. It is never added to matched buyer revenue.
- No live market feed, model forecast, real-world order, guaranteed buyer or transaction is invented.

## Modules and verification

`app.py` is the entry point. `harvest/data.py` and `ingestion.py` handle validation/activation; `analytics.py`, `risk.py`, `matching.py`, `money.py` and `financials.py` contain business logic. Screen modules render those functions. `assistant.py` is the pure assistant engine; `assistant_view.py` is its UI. `i18n.py`, `locale_ui.py` and `tamil_upload/index.html` handle presentation language. `storage.py` handles SQLite.

Run `python -m pytest -q`. Tests cover the original numeric contract, previous phase behavior, both input languages, supported/unsupported assistant topics, recomputation, missing data, language switching, every screen's text/table/chart labels, localized reports, Tamil upload handoff and preservation of original data. See `docs/VERIFICATION.md` for actual results and limits. Full browser/mobile visual verification remains part of Phase 7; do not infer it from simulated app tests.

## Upgrade

This is the complete standalone Phase 6 source. Keep the old project as a backup, install dependencies in the new folder and run it there. To retain a saved snapshot, close both apps and copy the old `data/harvest.sqlite3` into the new project's `data` folder. Do not merge old Python files into the new project. Language and assistant changes do not modify existing canonical snapshot records.

Phase 7 is not started. It will verify the final five-minute judging workflow and preserve this strict language contract.
