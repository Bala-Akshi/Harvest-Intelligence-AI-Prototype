"""Phase 6 local entry point: python -m streamlit run app.py."""
import os
import sqlite3
from pathlib import Path
from harvest.locale_ui import st
from harvest.ingestion import prepare_dataset, activate_dataset
from harvest.i18n import Translator
from harvest.locale_ui import setup_locale
from harvest.storage import load_workspace, save_workspace
from harvest.views import upload_view, dashboard_view
from harvest.risk import RiskPolicy
from harvest.risk_view import risk_view
from harvest.matching_view import matching_view
from harvest.financial_view import financial_view
from harvest.assistant_view import assistant_view

ROOT = Path(__file__).resolve().parent
DB = Path(os.environ.get('HARVEST_DB_PATH', str(ROOT / 'data/harvest.sqlite3')))
PAGES = ['Home', 'Upload Data', 'Dashboard', 'Surplus and Risk', 'Buyer Matching', 'Profit Analysis', 'AI Assistant']
previous_language = st.session_state.get('language','English')
st.set_page_config(page_title=Translator(previous_language)('Harvest Intelligence AI'), layout='wide')
setup_locale()
language = st.sidebar.selectbox(Translator(previous_language)('Language'), ['English', 'தமிழ்'], key='language')
t = Translator(language)

for key, default in [('active_data', None), ('active_buyers', None), ('source', 'No active dataset'),
                     ('agriculture_metadata', None), ('buyers_metadata', None), ('risk_policy', RiskPolicy().to_dict())]:
    st.session_state.setdefault(key, default)
st.sidebar.title(t('HARVEST'))
st.sidebar.caption(t('INTELLIGENCE AI · PHASE 6'))
page = st.sidebar.radio(t('Navigation'), PAGES, format_func=t, key='navigation')

if st.sidebar.button(t('Load demo data'), key='load_demo', width='stretch'):
    # Prepare both first, then activate the complete demo together.
    prepared = [prepare_dataset((ROOT / 'data' / filename).read_bytes(), filename, kind, origin='sample')
                for kind, filename in [('agriculture', 'agriculture_demo.csv'), ('buyers', 'buyers_demo.csv')]]
    if any(result.errors for result, _ in prepared):
        st.sidebar.error(t('Demo validation failed'))
    else:
        for result, meta in prepared:
            activate_dataset(st.session_state, result, meta)
        for key in ['report_agriculture', 'report_buyers']:
            st.session_state.pop(key, None)

if st.sidebar.button(t('Restore local snapshot'), key='restore_snapshot'):
    try:
        snapshot = load_workspace(DB)
        if snapshot:
            st.session_state.update(snapshot)
            for key in ['report_agriculture', 'report_buyers', 'risk_threshold_pct', 'risk_age_days']:
                st.session_state.pop(key, None)
            st.sidebar.success(t('Restored'))
        else:
            st.sidebar.info(t('No saved snapshot'))
    except (OSError, ValueError, TypeError, sqlite3.Error) as exc:
        st.sidebar.error(f'Restore failed / மீட்டெடுப்புப் பிழை: {exc}')

t.configure(st.session_state.get('active_data'),st.session_state.get('active_buyers'))
st.sidebar.caption(t('Source: {origin}',origin=t((st.session_state.get('agriculture_metadata') or {}).get('origin','unknown'))))
if st.session_state.active_data is not None or st.session_state.active_buyers is not None:
    if st.sidebar.button(t('Save local snapshot'), key='save_snapshot'):
        try:
            save_workspace(st.session_state, DB)
            st.sidebar.success(t('Saved'))
        except (OSError, ValueError, TypeError, sqlite3.Error) as exc:
            st.sidebar.error(f'Save failed / சேமிப்புப் பிழை: {exc}')

st.title(t('Harvest Intelligence AI'))
st.caption(t('Agricultural records → practical selling decisions / வேளாண் தரவிலிருந்து விற்பனை முடிவுகள்'))
st.header(t(page))
if page == 'Home':
    st.subheader(t('Phase 6: ask the data-grounded assistant'))
    st.write(t('Understand crop availability and estimated demand before planning a sale. / விற்பனைக்கு முன் பயிர் இருப்பையும் மதிப்பிடப்பட்ட தேவையையும் அறியவும்.'))
    st.info(t('Load demo data → Dashboard, or Upload Data → map columns → validate → explore. / மாதிரித் தரவு → தரவுப் பலகை; அல்லது பதிவேற்று → பொருத்து → சரிபார்.'))
    st.write(t('Phase 2 adds agriculture and buyer uploads, record-level quality reports, source metadata, crop filters and local workspace snapshots. / வேளாண் மற்றும் வாங்குபவர் பதிவேற்றம், தர அறிக்கை, வடிகட்டிகள் மற்றும் உள்ளூர் சேமிப்பு.'))
    st.write(t('Phase 3 adds transparent surplus review flags, editable planning thresholds and a calculated crop priority. / கட்டம் 3: உபரி பரிசீலனை, மாற்றக்கூடிய வரம்புகள் மற்றும் பயிர் முன்னுரிமை.'))
    st.write(t('Phase 4 adds capped buyer previews, unmatched quantities and a source-order audit. / கட்டம் 4: வரம்புடைய வாங்குபவர் பொருத்தம் மற்றும் ஒதுக்கீட்டு விளக்கம்.'))
    st.write(t('Phase 5 compares matched buyer returns with a market-price reference and explicit transport assumptions. / கட்டம் 5: வாங்குபவர் வருவாய் மற்றும் சந்தை விலை ஒப்பீடு.'))
    st.caption(t('Demand remains an uploaded estimate. No live market feed or model forecast is generated. / தேவை பதிவேற்றிய மதிப்பீடு; நேரடிச் சந்தைத் தரவு அல்லது மாதிரி முன்னறிவிப்பு இல்லை.'))
    for filename, title in [('agriculture_demo.csv', 'Download agriculture sample'), ('buyers_demo.csv', 'Download buyers sample')]:
        st.download_button(t(title), (ROOT / 'data' / filename).read_bytes(), file_name=filename, mime='text/csv')
    st.warning(t('Sample opportunities only; not confirmed orders'))
elif page == 'Upload Data':
    upload_view(t)
elif page == 'Dashboard':
    dashboard_view(t)
elif page == 'Surplus and Risk':
    risk_view(t)
elif page == 'Buyer Matching':
    matching_view(t)
elif page == 'Profit Analysis':
    financial_view(t)
elif page == 'AI Assistant':
    assistant_view(t)
else:
    st.info(t('Planned screen / திட்டமிடப்பட்ட திரை. Detailed workflows will be added in later requested phases.'))
    st.write(t('All screens share the active validated agriculture and buyer datasets. / எல்லாத் திரைகளும் சரிபார்க்கப்பட்ட நடப்புத் தரவுகளைப் பகிர்கின்றன.'))
    if st.session_state.active_data is not None:
        st.caption(t('Active agriculture records: {n}',n=len(st.session_state.active_data)))
