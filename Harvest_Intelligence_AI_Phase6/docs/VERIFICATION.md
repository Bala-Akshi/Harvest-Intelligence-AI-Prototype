# Phase 6 verification

- `python -m pytest -q`: **143 passed**.
- All 110 Phase 1–5 regression checks remain passing, including every mandatory supplied numeric result.
- Added 33 Phase 6 cases covering calculated crop priority, changed-data recommendations, English/Tamil question routing, every supported answer topic, unsupported/live-information requests, unknown crops, no surplus, missing datasets, custom policies, unchanged inputs, bounded history, evidence and calculation sources, conversation recalculation, language switching, localized CSV/JSON reports, localized-header re-upload, stable display aliases, Tamil validation feedback and the Tamil question form.
- Both-language screen audit: all seven screens, visible headings/messages/captions, widget labels/options, table headings/cells and chart labels. No Tamil text in generated English UI; no Latin-letter English text in generated Tamil UI. User-entered input and host browser/OS controls are outside generated application text.
- Demo assistant answer: Tomatoes has 500 − 300 = 200 kg potential surplus; 180 kg potentially matched; 20 kg still unmatched; ₹4,430 estimated return after buyer transport. Changing Onion availability to 1,000 kg changes the first priority to Onions with 650 kg surplus.
- Tamil upload component: local client protocol test verified component initialization, exact CSV byte handoff, localized feedback and file-size rejection. Server-side handoff/validation is also covered through AppTest.
- Live local checks: health HTTP 200 (`ok`); a real Streamlit WebSocket app session completed its script; the bundled Tamil upload HTML asset returned HTTP 200 and contained the expected local Tamil control; entry page HTTP 200.
- No external model or real-time service is called by the assistant.
- Runtime: Python 3.12; direct dependency versions recorded in requirements-tested.txt.
- Full browser rendering/mobile visual review was not completed. Browser provisioning was unavailable in this environment. The upload protocol, served asset and simulated app interactions were tested; these are not claimed as full browser tests. Actual Windows execution was not performed.
- Phase 7 remains pending: final five-minute judging walkthrough, accessibility/responsive review and final regression verification. AGENTS.md and docs/LANGUAGE_POLICY.md require preserving selected-language-only text.
