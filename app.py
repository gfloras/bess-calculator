import streamlit as st
import pandas as pd
import numpy_financial as npf
import plotly.graph_objects as go
import io
import os
import csv
from datetime import datetime

# --- URLs ΠΡΟΪΟΝΤΩΝ & ΕΙΚΟΝΩΝ ---
# ΕΝΗΜΕΡΩΜΕΝΟ URL ΕΔΩ:
URL_IMG_BIG = "https://bessenergy.gr/wp-content/uploads/2026/01/gotion-5015-1-new.jpg"
URL_PAGE_BIG = "https://bessenergy.gr/bess/"

URL_IMG_SMALL = "https://bessenergy.gr/wp-content/uploads/2025/09/ESC-R1125-261-CE.png"
URL_PAGE_SMALL = "https://bessenergy.gr/industrial-and-commercial/"

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
        'analytic_tip': "💡 Μπορείτε να συμπληρώσετε τον πίνακα χειροκίνητα ή να ανεβάσετε ένα αρχείο Excel.",
        'download_template': "📥 Κατεβάστε Πρότυπο Excel (Template)",
        'upload_label': "📂 Ανεβάστε το συμπληρωμένο Excel",
        'upload_error': "⚠️ Το αρχείο Excel πρέπει να έχει τις σωστές στήλες. Κατεβάστε το πρότυπο για οδηγίες.",

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

        # Print Instruction (New)
        'print_instruction': "🖨️ **Αποθήκευση & Εκτύπωση:** Αν θέλετε να τυπώσετε τα αποτελέσματα, χρησιμοποιήστε τις επιλογές στο κάτω μέρος της σελίδας.",

        # PROMO SECTION
        'promo_title': "⚡ Οι Λύσεις Αποθήκευσης GOTION της BESS ENERGY",
        'promo_desc': "Επιλέξτε την ιδανική λύση μπαταρίας **Gotion** για την επένδυσή σας.",
        'prod1_title': "Gotion Utility Scale (5.015 MWh)",
        'prod1_btn': "Δείτε το Προϊόν",
        'prod2_title': "Gotion C&I (261 kWh)",
        'prod2_btn': "Δείτε το Προϊόν",
        
        # Disclaimer
        'disclaimer_title': "⚠️ Αποποίηση Ευθύνης (Disclaimer)",
        'disclaimer_text': """
            Η παρούσα εφαρμογή αναπτύχθηκε από την BESS ENERGY, εξουσιοδοτημένο διανομέα των Μπαταριών GOTION, αποκλειστικά για ενημερωτικούς και εκπαιδευτικούς σκοπούς. 
            Οι υπολογισμοί και τα αποτελέσματα που παρουσιάζονται αποτελούν εκτιμήσεις που βασίζονται στα δεδομένα που εισάγει ο χρήστης.
            Η BESS ENERGY δεν εγγυάται την ακρίβεια των αποτελεσμάτων και δεν φέρει ουδεμία ευθύνη για τυχόν λάθη ή επενδυτικές αποφάσεις. 
            Συνιστάται αυστηρά στους χρήστες να συμβουλεύονται τους εξειδικευμένους συμβούλους τους.
        """,

        # Leads Form
        'leads_title': "📬 Μείνετε Ενημερωμένοι (Προαιρετικό)",
        'leads_desc': "Συμπληρώστε τα στοιχεία σας για να λαμβάνετε ενημερώσεις σχετικά με τις μπαταρίες Gotion.",
        'lbl_name': "Ονοματεπώνυμο",
        'lbl_email': "Email",
        'lbl_consent': "Επιθυμώ να λαμβάνω ενημερωτικά email από την BESS ENERGY.",
        'btn_subscribe': "Εγγραφή στην Ενημέρωση",
        'msg_success': "✅ Ευχαριστούμε! Τα στοιχεία σας καταχωρήθηκαν επιτυχώς.",
        'msg_fail': "⚠️ Παρακαλούμε επιλέξτε το κουτάκι συγκατάθεσης για να προχωρήσετε.",

        # Export Buttons
        'btn_download': "📥 Λήψη σε Excel",
        'print_tip': "💡 Για εκτύπωση / αποθήκευση PDF πατήστε **Ctrl + P**.",
        'sheet_res': "Αποτελέσματα",
        'sheet_param': "Παράμετροι",
        'param_col': "Παράμετρος",
        'val_col': "Τιμή",
        
        'feedback_text': "📧 Αν έχετε κάποια παρατήρηση για την εφαρμογή ή αν θέλετε κάποια βελτίωση, παρακαλούμε στείλτε μας μήνυμα στο: bess@bessenergy.gr",
        
        # MANUAL
        'manual_title': "📘 Αναλυτικός Οδηγός Χρήσης & Επεξηγήσεις (Πατήστε εδώ)",
        'manual_text': """
        ### 👋 Καλώς ήρθατε στο BESS ROI Calculator
        Αυτή η εφαρμογή σας βοηθά να αξιολογήσετε τη βιωσιμότητα μιας επένδυσης σε συστήματα αποθήκευσης ενέργειας (μπαταρίες) BESS. 
        Η παρούσα εφαρμογή αναπτύχθηκε από την BESS ENERGY, εξουσιοδοτημένο διανομέα των Μπαταριών GOTION, αποκλειστικά για ενημερωτικούς και εκπαιδευτικούς σκοπούς. 
        Υπολογίζει τα μελλοντικά έσοδα και λαμβάνει υπόψη το κόστος δανεισμού.

        ---

        ### ⚙️ 1. Επεξήγηση Παραμέτρων (Sidebar)
        
        #### Α. Βασικά Στοιχεία Έργου
        * **Χωρητικότητα (Capacity):** Το μέγεθος της μπαταρίας σε kWh.
        * **Κόστος Επένδυσης (CAPEX):** Το συνολικό ποσό που κοστίζει η αγορά και η εγκατάσταση (πριν το δάνειο).
        * **Απόδοση (Efficiency):** Συνήθως 85%-90%. Δείχνει πόση ενέργεια χάνεται κατά τη φόρτιση/εκφόρτιση.
        
        #### Β. Χρηματοδότηση (Δάνειο)
        * **Ποσοστό Δανειοδότησης:** Τι ποσοστό της επένδυσης θα καλύψει η τράπεζα. Το υπόλοιπο είναι τα δικά σας χρήματα (**Ίδια Κεφάλαια**).
        * **Spread & Euribor:** Το επιτόκιο του δανείου είναι το άθροισμα αυτών των δύο. (π.χ. 2.5% Spread + 3.0% Euribor = 5.5% Τελικό Επιτόκιο).

        #### Γ. Οικονομικά & Λειτουργικά Στοιχεία
        * **Τιμή Φόρτισης/Εκφόρτισης:** Η μέση τιμή που αγοράζετε και πουλάτε το ρεύμα.
        * **Ετήσια Φθορά (Degradation):** Οι μπαταρίες χάνουν χωρητικότητα κάθε χρόνο. Μια τυπική τιμή είναι 1.5% - 2.5%.
        * **OPEX:** Τα ετήσια έξοδα συντήρησης, ασφάλισης και διαχείρισης.

        ---

        ### 📊 2. Επεξήγηση Δεικτών (Αποτελέσματα)
        
        * **NPV (Καθαρή Παρούσα Αξία):** Δείχνει το συνολικό κέρδος σε σημερινή αξία χρημάτων. Αν είναι θετικό (>0), η επένδυση είναι κερδοφόρα.
        * **IRR (Εσωτερικός Βαθμός Απόδοσης):** Το πραγματικό ετήσιο επιτόκιο που κερδίζουν τα χρήματά σας. Αν το IRR είναι μεγαλύτερο από το επιτόκιο της τράπεζας, τότε συμφέρει η επένδυση.
        * **Απόσβεση (Payback Period):** Ο χρόνος που απαιτείται για να πάρετε πίσω τα χρήματα που βάλατε από την τσέπη σας (Ίδια Κεφάλαια).
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
        
        'analytic_tip': "💡 You can fill the table manually or upload an Excel file.",
        'download_template': "📥 Download Excel Template",
        'upload_label': "📂 Upload Excel File",
        'upload_error': "⚠️ The Excel file must have the correct columns. Download the template for guidance.",

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

        'print_instruction': "🖨️ **Storage & Printing:** If you want to print the results, please use the options at the bottom of the page.",

        'promo_title': "⚡ BESS ENERGY Storage Solutions",
        'promo_desc': "Choose the ideal **Gotion** battery solution for your investment.",
        'prod1_title': "Gotion Utility Scale (5.015 MWh)",
        'prod1_btn': "View Product",
        'prod2_title': "Gotion C&I (261 kWh)",
        'prod2_btn': "View Product",

        'disclaimer_title': "⚠️ Disclaimer",
        'disclaimer_text': """
            This application was developed by BESS ENERGY, an authorized distributor of GOTION Batteries, exclusively for informational and educational purposes. 
            The calculations and results presented are estimates based on user inputs and theoretical models.
            BESS ENERGY does not guarantee the accuracy of the results and assumes no liability for any errors or investment decisions made based on this tool. 
            Users are strictly advised to consult with qualified financial and legal advisors before making any investment commitments.
        """,

        'leads_title': "📬 Stay Informed (Optional)",
        'leads_desc': "Fill in your details to receive updates about Gotion batteries and investment opportunities.",
        'lbl_name': "Full Name",
        'lbl_email': "Email",
        'lbl_consent': "I agree to receive newsletters from BESS ENERGY.",
        'btn_subscribe': "Subscribe to Updates",
        'msg_success': "✅ Thank you! Your details have been registered.",
        'msg_fail': "⚠️ Please check the consent box to proceed.",

        'btn_download': "📥 Download to Excel",
        'print_tip': "💡 To print or save as PDF press **Ctrl + P**.",
        'sheet_res': "Results",
        'sheet_param': "Parameters",
        'param_col': "Parameter",
        'val_col': "Value",
        
        'feedback_text': "📧 If you have any feedback regarding the application or suggestions for improvement, please send us a message at: bess@bessenergy.gr",
        
        'manual_title': "📘 Comprehensive User Guide (Click to expand)",
        'manual_text': """
        ### 👋 Welcome to BESS ROI Calculator
        This application was developed by BESS ENERGY, an authorized distributor of GOTION Batteries, exclusively for informational and educational purposes.
        This tool helps you evaluate the profitability of a Battery Energy Storage System (BESS) investment, factoring in revenue and financing costs.

        ---

        ### ⚙️ 1. Parameters Guide (Sidebar)
        
        #### A. Technical Specs
        * **Capacity:** The size of the battery in kWh.
        * **CAPEX (Cost):** Total investment cost before any loans.
        * **Efficiency:** Usually 85%-90%. Energy lost during charging/discharging cycles.
        
        #### B. Financing
        * **LTV (Loan to Value):** Percentage of investment covered by the bank. The rest is your **Equity**.
        * **Interest Rate:** Calculated as Euribor + Bank Margin (Spread).

        #### C. Financial & Operational
        * **Charge/Discharge Price:** Average prices for buying/selling electricity.
        * **Degradation:** Annual loss of battery capacity (typically 1.5% - 2.5%).
        * **OPEX:** Annual operational expenses (maintenance, insurance).

        ---

        ### 📊 2. Metrics Explained
        
        * **NPV (Net Present Value):** Total profit in today's money value. Positive (>0) means the project is profitable.
        * **IRR (Internal Rate of Return):** The annual return rate on your specific Equity. Compare this with alternative investments.
        * **Payback Period:** Years required to recover your initial Equity.
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
        .leads-box { display: none; }
    }
    
    /* Custom Styling for Boxes */
    .disclaimer-box {
        background-color: #f0f2f6; 
        padding: 15px; 
        border-radius: 8px; 
        font-size: 13px; 
        color: #444;
        border-left: 5px solid #6c757d;
        margin-bottom: 20px;
    }
    
    .leads-box {
        background-color: #e8f4f8; 
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #d1e7dd;
        margin-bottom: 20px;
    }

    .promo-box {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #eeeeee;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 10px;
    }
    
    .info-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #ffeeba;
        margin-bottom: 20px;
        font-weight: 500;
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

# --- LEADS STORAGE FUNCTION ---
LEADS_FILE = 'leads.csv'

def save_lead(name, email, consent):
    if name and email and consent:
        file_exists = os.path.isfile(LEADS_FILE)
        try:
            with open(LEADS_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['Date', 'Name', 'Email', 'Consent'])
                
                # Timestamp
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([now, name, email, "Yes" if consent else "No"])
        except Exception as e:
            pass 

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

        default_data = {
            c_year: range(1, 16),
            c_deg: [1.9] * 15,
            c_pch: [0.4468] * 15,
            c_pdis: [1.1501] * 15,
            c_opex: [5000.0] * 15,
            c_eur: [3.0] * 15 
        }
        df_input = pd.DataFrame(default_data)
        
        # EXCEL UPLOAD LOGIC
        buffer_temp = io.BytesIO()
        with pd.ExcelWriter(buffer_temp, engine='xlsxwriter') as writer:
            df_input.to_excel(writer, index=False)
        
        st.download_button(
            label=T['download_template'],
            data=buffer_temp.getvalue(),
            file_name="BESS_Input_Template.xlsx",
            mime="application/vnd.ms-excel",
            key="dl_template"
        )
        
        uploaded_file = st.file_uploader(T['upload_label'], type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                df_uploaded = pd.read_excel(uploaded_file)
                if len(df_uploaded.columns) >= 5:
                    df_input = df_uploaded
                else:
                    st.error(T['upload_error'])
            except Exception as e:
                st.error(f"Error reading file: {e}")

        col_config = {
            c_year: st.column_config.NumberColumn(disabled=True),
            c_deg: st.column_config.NumberColumn(format="%.2f%%"),
            c_pch: st.column_config.NumberColumn(format="%.4f€"),
            c_pdis: st.column_config.NumberColumn(format="%.4f€"),
            c_opex: st.column_config.NumberColumn(format="%.0f€"),
            c_eur: st.column_config.NumberColumn(format="%.2f%%")
        }
        
        edited_df = st.data_editor(
            df_input, 
            hide_index=True, 
            column_config=col_config
        )
        
        try:
            list_degradation = edited_df[c_deg].tolist()
            list_price_charge = edited_df[c_pch].tolist()
            list_price_discharge = edited_df[c_pdis].tolist()
            list_opex = edited_df[c_opex].tolist()
            list_euribor = edited_df[c_eur].tolist()
        except KeyError:
            st.error(T['upload_error'])
            list_degradation = [1.9] * 15
            list_price_charge = [0.4468] * 15
            list_price_discharge = [1.1501] * 15
            list_opex = [5000.0] * 15
            list_euribor = [3.0] * 15

# --- ENGINE ---
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
cash_flows = [-equity_amount] 
annual_data = [] 
running_balance = -equity_amount
cumulative_cash_flow = [-equity_amount]
current_loan_balance = loan_amount

for i in range(15):
    year = years[i]
    deg_factor = soh_curve[i]
    
    p_charge = list_price_charge[i]
    p_discharge = list_price_discharge[i]
    opex = list_opex[i]
    euribor = list_euribor[i]
    
    daily_discharge_kwh = capacity_kwh * cycles_per_day * deg_factor
    daily_charge_kwh = daily_discharge_kwh / efficiency 
    
    annual_discharge = daily_discharge_kwh * days_operation
    annual_charge = daily_charge_kwh * days_operation
    
    revenue = annual_discharge * p_discharge
    charging_cost = annual_charge * p_charge
    gross_profit = revenue - charging_cost
    ebitda = gross_profit - opex
    
    interest_payment = 0.0
    principal_payment = 0.0
    
    if use_loan and current_loan_balance > 0.1:
        total_rate = (euribor + loan_margin) / 100.0
        years_remaining = loan_duration - i
        
        if years_remaining > 0:
            pmt = npf.pmt(total_rate, years_remaining, -current_loan_balance)
            interest_payment = current_loan_balance * total_rate
            principal_payment = pmt - interest_payment
            
            if principal_payment > current_loan_balance:
                principal_payment = current_loan_balance
                pmt = interest_payment + principal_payment
            
            current_loan_balance -= principal_payment
        else:
            interest_payment = 0
            principal_payment = 0
            
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

# --- PRINT INSTRUCTION (NEW POSITION) ---
st.markdown(f"""
<div class="info-box">
    {T['print_instruction']}
</div>
""", unsafe_allow_html=True)


# --- PROMO SECTION ---
st.divider()
st.subheader(T['promo_title'])
st.markdown(T['promo_desc'])

col_p1, col_p2 = st.columns(2)

with col_p1:
    with st.container(border=True):
        st.image(URL_IMG_BIG, use_container_width=True)
        st.subheader(T['prod1_title'])
        st.link_button(T['prod1_btn'], URL_PAGE_BIG, use_container_width=True)

with col_p2:
    with st.container(border=True):
        st.image(URL_IMG_SMALL, use_container_width=True)
        st.subheader(T['prod2_title'])
        st.link_button(T['prod2_btn'], URL_PAGE_SMALL, use_container_width=True)


# --- DISCLAIMER BOX ---
st.divider()
st.markdown(f"""
<div class="disclaimer-box">
    <strong>{T['disclaimer_title']}</strong><br>
    {T['disclaimer_text']}
</div>
""", unsafe_allow_html=True)

# --- LEADS BOX (INDEPENDENT) ---
st.markdown(f'<div class="leads-box"><h3>{T["leads_title"]}</h3><p>{T["leads_desc"]}</p></div>', unsafe_allow_html=True)

with st.container():
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        lead_name = st.text_input(T['lbl_name'], key="lead_name")
    with col_l2:
        lead_email = st.text_input(T['lbl_email'], key="lead_email")
    lead_consent = st.checkbox(T['lbl_consent'], key="lead_consent")
    
    # NEW SUBSCRIBE BUTTON Logic
    if st.button(T['btn_subscribe'], type="primary"):
        if lead_consent:
            save_lead(lead_name, lead_email, lead_consent)
            st.success(T['msg_success'])
        else:
            st.warning(T['msg_fail'])

# --- DOWNLOAD BUTTONS ---
st.markdown("---") 
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


# --- FEEDBACK & ADMIN ---
st.markdown(f"""
<div class="feedback-box" style='text-align: center; color: #555; font-weight: 500; margin-top: 30px; margin-bottom: 20px;'>
    {T['feedback_text']}
</div>
""", unsafe_allow_html=True)


with st.expander("Admin Login (Restricted)"):
    admin_pass = st.text_input("Password", type="password")
    if admin_pass == "bessadmin2024":
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "rb") as f:
                st.download_button(
                    label="📥 Download Leads (CSV)",
                    data=f,
                    file_name="leads_backup.csv",
                    mime="text/csv"
                )
            st.success(f"Found leads file! Size: {os.path.getsize(LEADS_FILE)} bytes")
        else:
            st.warning("No leads collected yet.")
