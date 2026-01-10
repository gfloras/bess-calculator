import streamlit as st
import pandas as pd
import numpy_financial as npf
import plotly.graph_objects as go
import io
import os

# --- ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ (TRANSLATION DICTIONARY) ---
TRANS = {
    'el': {
        'title': "🔋 Υπολογισμός Απόδοσης Επένδυσης (BESS ROI Calculator)",
        'sidebar_header': "⚙️ Παράμετροι Επένδυσης",
        'lang_select': "Γλώσσα / Language",
        'mode_label': "Επιλογή Μεθόδου Εισαγωγής:",
        'mode_simple': "Απλή (Σταθερές Τιμές)",
        'mode_analytic': "Αναλυτική (Ανά Έτος)",
        
        # Sections
        'subheader_tech': "1. Βασικά Στοιχεία Έργου",
        'subheader_loan': "2. 🏦 Χρηματοδότηση & Δάνειο",
        'subheader_simple': "3. Οικονομικά & Φθορά (Μέσοι Όροι)",
        'subheader_analytic': "3. Αναλυτική Εισαγωγή (15 Έτη)",

        # Tech Inputs
        'cap_label': "Χωρητικότητα (kWh)",
        'cost_label': "Συνολικό Κόστος Επένδυσης (€)",
        'days_label': "Ημέρες Λειτουργίας/Έτος",
        'cycles_label': "Κύκλοι ανά ημέρα",
        'eff_label': "Απόδοση (Round-trip Efficiency)",

        # Loan Inputs
        'loan_enable': "Ενεργοποίηση Δανεισμού",
        'loan_percent': "Ποσοστό Δανειοδότησης (%)",
        'loan_amount_display': "Ποσό Δανείου: ",
        'loan_equity_display': "Ίδια Κεφάλαια (Εμείς): ",
        'loan_duration': "Διάρκεια Δανείου (Έτη)",
        'loan_margin': "Περιθώριο Τράπεζας (Spread %)",
        'loan_euribor': "Επιτόκιο Euribor (%)",

        # Financial Inputs
        'deg_input': "Ετήσια Φθορά (%)",
        'p_charge_input': "Τιμή Φόρτισης (€/kWh)",
        'p_discharge_input': "Τιμή Εκφόρτισης (€/kWh)",
        'opex_input': "Ετήσια Λειτουργικά Έξοδα (€)",
        
        # EXCEL UPLOAD FEATURES
        'analytic_tip': "💡 Μπορείτε να επεξεργαστείτε τον πίνακα ή να ανεβάσετε δικό σας αρχείο Excel.",
        'download_tmpl_btn': "📥 Κατεβάστε Πρότυπο Excel (Template)",
        'upload_label': "📤 Ανεβάστε το συμπληρωμένο Excel",
        'upload_success': "✅ Το αρχείο φορτώθηκε επιτυχώς!",
        'upload_error': "⚠️ Το αρχείο δεν έχει τη σωστή μορφή. Παρακαλώ χρησιμοποιήστε το Πρότυπο.",

        # Table Columns
        'col_year': "Έτος",
        'col_deg': "Φθορά (%)",
        'col_p_charge': "Τιμή Φόρτισης (€)",
        'col_p_discharge': "Τιμή Εκφόρτισης (€)",
        'col_opex': "Έξοδα OPEX (€)",
        'col_euribor': "Euribor (%)",

        # Metrics
        'selected_mode': "**Επιλεγμένη Λειτουργία:**",
        'metric_npv': "💰 NPV (Ίδια Κεφ.)",
        'metric_irr': "📈 IRR (Ίδια Κεφ.)",
        'metric_payback': "⏱️ Απόσβεση",
        'metric_roi': "🔋 ROI (15ετίας)",
        'years_suffix': " Έτη",

        # Plots
        'plot_cum_title': "Καμπύλη Απόσβεσης (Ίδια Κεφάλαια)",
        'plot_cum_series': "Σωρευτικά Κέρδη",
        'plot_bar_title': "Ετήσιες Ταμειακές Ροές (Μετά Δόσεων)",
        'plot_bar_series': "Ετήσιο Κέρδος (FCFE)",

        # Report Table
        'table_header': "📋 Αναλυτική Αναφορά (Free Cash Flow to Equity)",
        'tbl_soh': "Υγεία (SoH)",
        'tbl_dis': "Εκφόρτιση (kWh)",
        'tbl_rev': "Έσοδα",
        'tbl_cost': "Κόστος Ρεύματος",
        'tbl_opex': "Λειτ. Έξοδα",
        'tbl_interest': "Τόκοι",
        'tbl_principal': "Αποπλ. Κεφαλαίου",
        'tbl_net': "Τελικό Ταμείο",
        'tbl_cum': "Σωρευτικό",

        # Export & Footer
        'btn_download': "📥 Λήψη σε Excel",
        'print_tip': "💡 Για εκτύπωση / αποθήκευση PDF πατήστε **Ctrl + P**.",
        'sheet_res': "Αποτελέσματα",
        'sheet_param': "Παράμετροι",
        'param_col': "Παράμετρος",
        'val_col': "Τιμή",
        
        'feedback_text': "📧 Αν έχετε κάποια παρατήρηση για την εφαρμογή ή αν θέλετε κάποια βελτίωση, παρακαλούμε στείλτε μας μήνυμα στο: **bess@bessenergy.gr**",
        'disclaimer_title': "⚠️ Αποποίηση Ευθύνης (Disclaimer):",
        'disclaimer_text': """
            Η παρούσα εφαρμογή αναπτύχθηκε από την BESS ENERGY αποκλειστικά για ενημερωτικούς και εκπαιδευτικούς σκοπούς. 
            Οι υπολογισμοί και τα αποτελέσματα που παρουσιάζονται αποτελούν εκτιμήσεις που βασίζονται στα δεδομένα που εισάγει ο χρήστης.
            <br><br>
            Η BESS ENERGY δεν εγγυάται την ακρίβεια των αποτελεσμάτων και δεν φέρει ουδεμία ευθύνη για τυχόν λάθη ή επενδυτικές αποφάσεις. 
            Συνιστάται αυστηρά στους χρήστες να συμβουλεύονται τους εξειδικευμένους συμβούλους τους.
        """,

        'manual_title': "📘 Οδηγίες Χρήσης & Επεξηγήσεις (Πατήστε εδώ)",
        'manual_text': """
        ### 1. Πώς λειτουργεί;
        Η εφαρμογή υπολογίζει την κερδοφορία μιας επένδυσης σε μπαταρίες (BESS).

        ### 2. Βήματα
        1.  **Αριστερή Μπάρα:** Εισάγετε τα τεχνικά χαρακτηριστικά.
        2.  **Χρηματοδότηση:** Επιλέξτε αν θα πάρετε δάνειο.
        3.  **Μέθοδος:** * *Απλή:* Βάζετε μέσες τιμές για όλη τη 15ετία.
            * *Αναλυτική:* Μπορείτε να επεξεργαστείτε τον πίνακα έτος-έτος ή **να ανεβάσετε δικό σας Excel**.

        ### 3. Πώς να ανεβάσω δικό μου Excel;
        * Στην "Αναλυτική" μέθοδο, πατήστε **"📥 Κατεβάστε Πρότυπο"**.
        * Ανοίξτε το αρχείο, συμπληρώστε τα δεδομένα σας (χωρίς να αλλάξετε τις στήλες) και αποθηκεύστε το.
        * Πατήστε **"📤 Ανεβάστε το Excel"** και επιλέξτε το αρχείο σας. Ο πίνακας θα ενημερωθεί αυτόματα!
        """
    },
    'en': {
        'title': "🔋 BESS ROI Calculator",
        'sidebar_header': "⚙️ Investment Parameters",
        'lang_select': "Language / Γλώσσα",
        'mode_label': "Input Method:",
        'mode_simple': "Simple (Fixed Values)",
        'mode_analytic': "Advanced (Year-by-Year)",
        
        'subheader_tech': "1. Technical Specifications",
        'subheader_loan': "2. 🏦 Financing & Loan",
        'subheader_simple': "3. Financials & Degradation (Averages)",
        'subheader_analytic': "3. Advanced Input (15 Years)",

        'cap_label': "Capacity (kWh)",
        'cost_label': "Total Investment Cost (€)",
        'days_label': "Operating Days/Year",
        'cycles_label': "Cycles per Day",
        'eff_label': "Round-trip Efficiency",

        'loan_enable': "Enable Financing",
        'loan_percent': "Loan to Value (LTV %)",
        'loan_amount_display': "Loan Amount: ",
        'loan_equity_display': "Equity Amount: ",
        'loan_duration': "Loan Duration (Years)",
        'loan_margin': "Bank Margin (Spread %)",
        'loan_euribor': "Euribor Rate (%)",

        'deg_input': "Annual Degradation (%)",
        'p_charge_input': "Charge Price (€/kWh)",
        'p_discharge_input': "Discharge Price (€/kWh)",
        'opex_input': "Annual OPEX (€)",
        
        # EXCEL UPLOAD FEATURES
        'analytic_tip': "💡 You can edit the table below or upload your own Excel file.",
        'download_tmpl_btn': "📥 Download Excel Template",
        'upload_label': "📤 Upload Filled Excel",
        'upload_success': "✅ File loaded successfully!",
        'upload_error': "⚠️ File format incorrect. Please use the Template.",

        'col_year': "Year",
        'col_deg': "Degradation (%)",
        'col_p_charge': "Charge Price (€)",
        'col_p_discharge': "Discharge Price (€)",
        'col_opex': "OPEX (€)",
        'col_euribor': "Euribor (%)",

        'selected_mode': "**Selected Mode:**",
        'metric_npv': "💰 NPV (Equity)",
        'metric_irr': "📈 IRR (Equity)",
        'metric_payback': "⏱️ Payback",
        'metric_roi': "🔋 ROI (15 Years)",
        'years_suffix': " Years",

        'plot_cum_title': "Payback Curve (Equity)",
        'plot_cum_series': "Cumulative Cash Flow",
        'plot_bar_title': "Annual Cash Flows (Post-Debt)",
        'plot_bar_series': "Free Cash Flow (FCFE)",

        'table_header': "📋 Detailed Report (Free Cash Flow to Equity)",
        'tbl_soh': "Battery Health (SoH)",
        'tbl_dis': "Discharge (kWh)",
        'tbl_rev': "Revenue",
        'tbl_cost': "Charging Cost",
        'tbl_opex': "OPEX",
        'tbl_interest': "Interest",
        'tbl_principal': "Principal Rep.",
        'tbl_net': "Net Cash Flow",
        'tbl_cum': "Cumulative",

        'btn_download': "📥 Download to Excel",
        'print_tip': "💡 To print or save as PDF press **Ctrl + P**.",
        'sheet_res': "Results",
        'sheet_param': "Parameters",
        'param_col': "Parameter",
        'val_col': "Value",
        
        'feedback_text': "📧 If you have any feedback regarding the application or suggestions for improvement, please send us a message at: **bess@bessenergy.gr**",
        'disclaimer_title': "⚠️ Disclaimer:",
        'disclaimer_text': """
            This application was developed by BESS ENERGY solely for informational and educational purposes. 
            The calculations and results presented are estimates based on user inputs and theoretical models.
            <br><br>
            BESS ENERGY does not guarantee the accuracy of the results and assumes no liability for any errors or investment decisions made based on this tool. 
            Users are strictly advised to consult with qualified financial and legal advisors before making any investment commitments.
        """,

        'manual_title': "📘 User Manual & Guide (Click to expand)",
        'manual_text': """
        ### 1. How it works
        This app calculates the profitability of a Battery Energy Storage System (BESS).

        ### 2. Steps
        1.  **Sidebar (Left):** Enter technical specs.
        2.  **Financing:** Enable "Financing" if you use a loan.
        3.  **Mode:** * *Simple:* Use average values.
            * *Advanced:* Edit the table year-by-year or **Upload your own Excel**.

        ### 3. How to upload my Excel?
        * In "Advanced" mode, click **"📥 Download Template"**.
        * Open the file, fill in your data (keep columns as is), and save.
        * Click **"📤 Upload Excel"** and select your file. The table will update automatically!
        """
    }
}

# --- Ρυθμίσεις Σελίδας ---
st.set_page_config(page_title="BESS ROI Calculator", layout="wide")

st.markdown("""
<style>
    @media print {
        [data-testid="stSidebar"] { display: none; }
        footer { display: none; }
        .block-container { padding-top: 1rem; }
        .stButton { display: none; }
        .stDownloadButton { display: none; }
        .disclaimer-box { display: block !important; border: 1px solid #ccc; }
        .feedback-box { display: block !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- ΔΙΑΧΕΙΡΙΣΗ ΓΛΩΣΣΑΣ ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'el'

# --- FORMATTING FUNCTIONS ---
def fmt_currency(x, lang):
    if not isinstance(x, (int, float)): return x
    if lang == 'el':
        s = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{s}€"
    else:
        return f"€{x:,.2f}"

def fmt_num(x, lang):
    if not isinstance(x, (int, float)): return x
    if lang == 'el':
        return f"{x:,.0f}".replace(",", ".")
    else:
        return f"{x:,.0f}"

# -------------------------------------------------------

# --- SIDEBAR ---
with st.sidebar:
    # 1. LOGO
    logo_file = "cropped-bessenergy-logo.bmp"
    if os.path.exists(logo_file):
        st.image(logo_file, use_container_width=True)
    
    st.divider()

    # 2. LANGUAGE
    lang_choice = st.selectbox(
        "🌐 Language / Γλώσσα", 
        ["Ελληνικά", "English"], 
        index=0 if st.session_state.lang == 'el' else 1
    )
    st.session_state.lang = 'el' if lang_choice == "Ελληνικά" else 'en'
    T = TRANS[st.session_state.lang]

# Main Title
st.title(T['title'])

# --- MANUAL EXPANDER ---
with st.expander(T['manual_title']):
    st.markdown(T['manual_text'])

# --- SIDEBAR: INPUTS ---
with st.sidebar:
    st.header(T['sidebar_header'])
    
    calc_mode = st.radio(
        T['mode_label'],
        [T['mode_simple'], T['mode_analytic']],
        horizontal=True
    )
    st.divider()

    # SECTION 1: TECH
    st.subheader(T['subheader_tech'])
    capacity_kwh = st.number_input(T['cap_label'], value=784.0, step=10.0)
    battery_cost = st.number_input(T['cost_label'], value=666400.0, step=1000.0)
    days_operation = st.slider(T['days_label'], 300, 365, 330)
    cycles_per_day = st.slider(T['cycles_label'], 1, 3, 2)
    efficiency = st.slider(T['eff_label'], 0.80, 0.99, 0.865)

    st.divider()

    # SECTION 2: LOAN
    st.subheader(T['subheader_loan'])
    use_loan = st.checkbox(T['loan_enable'], value=True)
    
    loan_amount = 0.0
    equity_amount = battery_cost
    loan_duration = 0
    loan_margin = 0.0
    
    if use_loan:
        loan_pct = st.slider(T['loan_percent'], 0, 90, 70)
        loan_amount = battery_cost * (loan_pct / 100.0)
        equity_amount = battery_cost - loan_amount
        
        st.caption(f"{T['loan_amount_display']} **{fmt_currency(loan_amount, st.session_state.lang)}**")
        st.caption(f"{T['loan_equity_display']} **{fmt_currency(equity_amount, st.session_state.lang)}**")
        
        loan_duration = st.number_input(T['loan_duration'], value=7, min_value=1, max_value=15)
        loan_margin = st.number_input(T['loan_margin'], value=2.5, step=0.1)

    st.divider()

    # SECTION 3: FINANCIALS & VARIABLES
    list_degradation = []
    list_price_charge = []
    list_price_discharge = []
    list_opex = []
    list_euribor = []

    if calc_mode == T['mode_simple']:
        st.subheader(T['subheader_simple'])
        deg_input = st.number_input(T['deg_input'], value=1.9, step=0.1)
        p_charge_input = st.number_input(T['p_charge_input'], value=0.4468, format="%.4f")
        p_discharge_input = st.number_input(T['p_discharge_input'], value=1.1501, format="%.4f")
        opex_input = st.number_input(T['opex_input'], value=5000.0, step=500.0)
        
        euribor_input = 0.0
        if use_loan:
            euribor_input = st.number_input(T['loan_euribor'], value=3.0, step=0.1)
        
        list_degradation = [deg_input] * 15
        list_price_charge = [p_charge_input] * 15
        list_price_discharge = [p_discharge_input] * 15
        list_opex = [opex_input] * 15
        list_euribor = [euribor_input] * 15

    else:
        st.subheader(T['subheader_analytic'])
        st.info(T['analytic_tip'])
        
        c_year = T['col_year']
        c_deg = T['col_deg']
        c_pch = T['col_p_charge']
        c_pdis = T['col_p_discharge']
        c_opex = T['col_opex']
        c_eur = T['col_euribor']

        # --- UPLOAD/DOWNLOAD LOGIC ---
        # 1. Create Default Data
        default_data = {
            c_year: range(1, 16),
            c_deg: [1.9] * 15,
            c_pch: [0.4468] * 15,
            c_pdis: [1.1501] * 15,
            c_opex: [5000.0] * 15,
            c_eur: [3.0] * 15
        }
        
        # 2. Template Button
        df_template = pd.DataFrame(default_data)
        buffer_tmpl = io.BytesIO()
        with pd.ExcelWriter(buffer_tmpl, engine='xlsxwriter') as writer:
            df_template.to_excel(writer, index=False)
        
        st.download_button(
            label=T['download_tmpl_btn'],
            data=buffer_tmpl.getvalue(),
            file_name="BESS_Input_Template.xlsx",
            mime="application/vnd.ms-excel",
            key="dl_template"
        )
        
        # 3. Upload Button
        uploaded_file = st.file_uploader(T['upload_label'], type=['xlsx'])
        
        if uploaded_file:
            try:
                uploaded_df = pd.read_excel(uploaded_file)
                # Basic validation: Check if columns match roughly (by length)
                # We assume user uses the template
                if len(uploaded_df.columns) >= 5:
                    st.success(T['upload_success'])
                    # Map uploaded columns to our expected list lists
                    # We assume column order: Year, Deg, Charge, Discharge, Opex, Euribor
                    # Safety check on length
                    rows = min(len(uploaded_df), 15)
                    
                    # Extract data using iloc to be safe against column name changes
                    list_degradation = uploaded_df.iloc[:rows, 1].tolist()
                    list_price_charge = uploaded_df.iloc[:rows, 2].tolist()
                    list_price_discharge = uploaded_df.iloc[:rows, 3].tolist()
                    list_opex = uploaded_df.iloc[:rows, 4].tolist()
                    if len(uploaded_df.columns) > 5:
                        list_euribor = uploaded_df.iloc[:rows, 5].tolist()
                    else:
                        list_euribor = [3.0]*15
                    
                    # Pad if less than 15 rows
                    if rows < 15:
                        missing = 15 - rows
                        list_degradation += [1.9] * missing
                        list_price_charge += [0.4468] * missing
                        list_price_discharge += [1.1501] * missing
                        list_opex += [5000.0] * missing
                        list_euribor += [3.0] * missing
                        
                    # Prepare DF for editor (visual confirmation)
                    df_display = pd.DataFrame({
                        c_year: range(1, 16),
                        c_deg: list_degradation,
                        c_pch: list_price_charge,
                        c_pdis: list_price_discharge,
                        c_opex: list_opex,
                        c_eur: list_euribor
                    })
                else:
                    st.error(T['upload_error'])
                    df_display = pd.DataFrame(default_data)
                    list_degradation = df_display[c_deg].tolist()
                    list_price_charge = df_display[c_pch].tolist()
                    list_price_discharge = df_display[c_pdis].tolist()
                    list_opex = df_display[c_opex].tolist()
                    list_euribor = df_display[c_eur].tolist()

            except Exception as e:
                st.error(f"Error: {e}")
                df_display = pd.DataFrame(default_data)
        else:
            df_display = pd.DataFrame(default_data)
            list_degradation = df_display[c_deg].tolist()
            list_price_charge = df_display[c_pch].tolist()
            list_price_discharge = df_display[c_pdis].tolist()
            list_opex = df_display[c_opex].tolist()
            list_euribor = df_display[c_eur].tolist()
        
        # Hide Euribor column if loan is not used (Visualization only)
        col_config = {
            c_year: st.column_config.NumberColumn(disabled=True),
            c_deg: st.column_config.NumberColumn(format="%.2f%%"),
            c_pch: st.column_config.NumberColumn(format="%.4f€"),
            c_pdis: st.column_config.NumberColumn(format="%.4f€"),
            c_opex: st.column_config.NumberColumn(format="%.0f€"),
            c_eur: st.column_config.NumberColumn(format="%.2f%%")
        }
        
        # Show the editor (so they can see what was uploaded or edit further)
        edited_df = st.data_editor(
            df_display, 
            hide_index=True, 
            column_config=col_config
        )
        
        # Final extraction from editor (in case they edit after upload)
        list_degradation = edited_df[c_deg].tolist()
        list_price_charge = edited_df[c_pch].tolist()
        list_price_discharge = edited_df[c_pdis].tolist()
        list_opex = edited_df[c_opex].tolist()
        list_euribor = edited_df[c_eur].tolist()

# --- ENGINE ---
# 1. SoH Curve
current_soh = 1.0
soh_curve = [] 
temp_soh = 1.0
soh_curve.append(1.0)
for i in range(14):
    drop = list_degradation[i] / 100.0
    temp_soh -= drop
    if temp_soh < 0: temp_soh = 0
    soh_curve.append(temp_soh)

years = list(range(1, 16))
# CASH FLOW 0 = EQUITY (Negative)
cash_flows = [-equity_amount] 
annual_data = [] 
running_balance = -equity_amount
cumulative_cash_flow = [-equity_amount]

# LOAN TRACKING
current_loan_balance = loan_amount

for i in range(15):
    year = years[i]
    deg_factor = soh_curve[i]
    
    # Financial Inputs for Year i
    p_charge = list_price_charge[i]
    p_discharge = list_price_discharge[i]
    opex = list_opex[i]
    euribor = list_euribor[i]
    
    # Energy Calculation
    daily_discharge_kwh = capacity_kwh * cycles_per_day * deg_factor
    daily_charge_kwh = daily_discharge_kwh / efficiency 
    
    annual_discharge = daily_discharge_kwh * days_operation
    annual_charge = daily_charge_kwh * days_operation
    
    # Operating Cash Flow
    revenue = annual_discharge * p_discharge
    charging_cost = annual_charge * p_charge
    gross_profit = revenue - charging_cost
    ebitda = gross_profit - opex
    
    # Loan Calculation (Annuity Method with Variable Rate logic)
    interest_payment = 0.0
    principal_payment = 0.0
    
    if use_loan and current_loan_balance > 0.1: # Threshold for float precision
        # Rate for this year
        total_rate = (euribor + loan_margin) / 100.0
        
        # Years remaining including this one
        years_remaining = loan_duration - i
        
        if years_remaining > 0:
            # Calculate PMT (Total Payment) for this year based on current balance
            pmt = npf.pmt(total_rate, years_remaining, -current_loan_balance)
            
            interest_payment = current_loan_balance * total_rate
            principal_payment = pmt - interest_payment
            
            # Handle last year precision or if principal > balance
            if principal_payment > current_loan_balance:
                principal_payment = current_loan_balance
                pmt = interest_payment + principal_payment
            
            current_loan_balance -= principal_payment
        else:
            interest_payment = 0
            principal_payment = 0
            
    # Free Cash Flow to Equity (FCFE)
    net_cash_flow = ebitda - interest_payment - principal_payment
    
    cash_flows.append(net_cash_flow)
    running_balance += net_cash_flow
    cumulative_cash_flow.append(running_balance)
    
    annual_data.append([
        year, 
        deg_factor, 
        annual_discharge, 
        revenue, 
        charging_cost, 
        opex,
        interest_payment,
        principal_payment,
        net_cash_flow, 
        running_balance
    ])

# IRR Calculation
try:
    irr = npf.irr(cash_flows)
    if pd.isna(irr): irr = 0.0
except:
    irr = 0.0

payback_year = "N/A"
for i, val in enumerate(cumulative_cash_flow):
    if val >= 0:
        payback_year = i 
        break

# --- FRONTEND ---
st.markdown(f"{T['selected_mode']} {calc_mode}")

# Metrics
st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric(T['metric_npv'], fmt_currency(cumulative_cash_flow[-1], st.session_state.lang)) 
col2.metric(T['metric_irr'], f"{irr:.2%}")
val_payback = f"{payback_year}{T['years_suffix']}" if isinstance(payback_year, int) else payback_year
col3.metric(T['metric_payback'], val_payback)
col4.metric(T['metric_roi'], f"{(cumulative_cash_flow[-1]/equity_amount):.1%}" if equity_amount > 0 else "Inf")

st.divider()

# Plots
c1, c2 = st.columns(2)
with c1:
    st.subheader(T['plot_cum_title'])
    fig_cum = go.Figure()
    fig_cum.add_trace(go.Scatter(x=[0]+years, y=cumulative_cash_flow, fill='tozeroy', name=T['plot_cum_series'], line=dict(color='#00CC96')))
    fig_cum.add_hline(y=0, line_dash="dash", line_color="red")
    fig_cum.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_cum, use_container_width=True)

with c2:
    st.subheader(T['plot_bar_title'])
    yearly_profits = cash_flows[1:]
    colors = ['#EF553B' if x < 0 else '#636EFA' for x in yearly_profits]
    fig_bar = go.Bar(x=years, y=yearly_profits, name=T['plot_bar_series'], marker_color=colors)
    st.plotly_chart(go.Figure(data=[fig_bar], layout=dict(height=350, margin=dict(l=20, r=20, t=30, b=20))), use_container_width=True)

# Table
st.subheader(T['table_header'])

cols_table = [
    T['col_year'], T['tbl_soh'], T['tbl_dis'], T['tbl_rev'], T['tbl_cost'], T['tbl_opex'], 
    T['tbl_interest'], T['tbl_principal'], T['tbl_net'], T['tbl_cum']
]
df_results = pd.DataFrame(annual_data, columns=cols_table)

def fmt_curr_wrapper(x): return fmt_currency(x, st.session_state.lang)
def fmt_num_wrapper(x): return fmt_num(x, st.session_state.lang)

styler = df_results.style.format({
    T['tbl_soh']: "{:.1%}",
    T['tbl_dis']: fmt_num_wrapper,
    T['tbl_rev']: fmt_curr_wrapper,
    T['tbl_cost']: fmt_curr_wrapper,
    T['tbl_opex']: fmt_curr_wrapper,
    T['tbl_interest']: fmt_curr_wrapper,
    T['tbl_principal']: fmt_curr_wrapper,
    T['tbl_net']: fmt_curr_wrapper,
    T['tbl_cum']: fmt_curr_wrapper
})

st.dataframe(styler, use_container_width=True)

# --- EXPORT ---
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df_export = df_results.copy()
    df_export.to_excel(writer, sheet_name=T['sheet_res'], index=False)
    
    workbook = writer.book
    worksheet = writer.sheets[T['sheet_res']]
    
    if st.session_state.lang == 'el':
        money_fmt = workbook.add_format({'num_format': '#,##0.00 "€"'}) 
    else:
        money_fmt = workbook.add_format({'num_format': '"€"#,##0.00'}) 
        
    kwh_fmt = workbook.add_format({'num_format': '#,##0'})
    percent_fmt = workbook.add_format({'num_format': '0.0%'})
    
    worksheet.set_column('B:B', 15, percent_fmt)
    worksheet.set_column('C:C', 18, kwh_fmt)
    worksheet.set_column('D:J', 18, money_fmt)
    
    param_data = [
        ["Mode", calc_mode],
        ["Capacity", capacity_kwh],
        ["Total Cost", battery_cost],
        ["Loan Active", "Yes" if use_loan else "No"]
    ]
    if use_loan:
        param_data.extend([
            ["Loan Amount", loan_amount],
            ["Equity Amount", equity_amount],
            ["Duration (Years)", loan_duration],
            ["Margin (%)", loan_margin],
            ["Avg Euribor", sum(list_euribor)/15]
        ])
    
    df_params = pd.DataFrame(param_data, columns=[T['param_col'], T['val_col']])
    df_params.to_excel(writer, sheet_name=T['sheet_param'], index=False)

download_data = buffer.getvalue()

col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    st.download_button(
        label=T['btn_download'],
        data=download_data,
        file_name="BESS_ROI_Report.xlsx",
        mime="application/vnd.ms-excel"
    )

with col_btn2:
    st.info(T['print_tip'])

# --- FEEDBACK & DISCLAIMER ---
st.divider()

st.markdown(f"""
<div class="feedback-box" style='text-align: center; color: #555; font-weight: 500; margin-bottom: 20px;'>
    {T['feedback_text']}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="disclaimer-box" style='background-color: #f0f2f6; padding: 15px; border-radius: 8px; font-size: 13px; color: #444;'>
    <strong>{T['disclaimer_title']}</strong>
    {T['disclaimer_text']}
</div>
""", unsafe_allow_html=True)
