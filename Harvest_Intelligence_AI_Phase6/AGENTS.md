# Harvest Intelligence AI project requirements

## User language requirement — applies to Phase 6, Phase 7 and later edits

When English is selected, application-owned visible text must be English only. When Tamil is selected, application-owned visible text must be Tamil only. Never append the other language in brackets, captions, headings, widget options, explanations or assistant messages.

Use `Translator`, the strict catalog and the `locale_ui` rendering boundary. Do not import Streamlit directly in screen modules or render backend English reasons directly. Data calculations and storage retain canonical values; display/report localization must not mutate active datasets. Unknown foreign-script identifiers use stable numbered labels instead of invented translations. Known demo crop and buyer identities have explicit translations. Tamil uploads use the bundled local component, not an English default upload prompt.

Assistant responses must call the existing calculation functions, be rendered from structured facts, and be recalculated against active inputs. No live prices, weather, confirmed orders, model forecasts or actual profit may be invented.

Before delivering Phase 7, rerun all regression and language tests. Preserve the 143 Phase 6 checks and add final workflow checks. Full browser/mobile rendering still requires review; do not claim checks that were not performed.

Only advance phases when requested. Phase 6 is delivered; Phase 7 remains pending.
