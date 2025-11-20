import streamlit as st
import pandas as pd
from io import BytesIO

# 1. Configurazione Pagina
st.set_page_config(page_title="Excel & CSV Merger", page_icon="📊", layout="centered")

# --- GESTIONE LINGUA ---
# Dizionario con tutti i testi
translations = {
    "English 🇺🇸": {
        "title": "📊 Merge your Excel/CSV files",
        "desc": """
        Do you have multiple files with the same columns? 
        Upload them below, and I'll merge them into a single file for you in seconds.
        """,
        "upload_label": "Drag and drop your files here (CSV or Excel)",
        "info_loaded": "files loaded. Ready to merge!",
        "btn_merge": "🚀 Merge Files Now",
        "error": "Error with file",
        "success": "✅ Done! Created a single file with",
        "rows": "rows.",
        "download_label": "📥 Download Merged File (.xlsx)",
        "kofi_title": "Was this helpful?",
        "kofi_desc": "Buy me a coffee to keep the server running!"
    },
    "Italiano 🇮🇹": {
        "title": "📊 Unisci i tuoi file Excel/CSV",
        "desc": """
        Hai tanti file con le stesse colonne e devi unirli in uno solo? 
        Caricali qui sotto, farò io il lavoro noioso per te in pochi secondi.
        """,
        "upload_label": "Trascina qui i file (CSV o Excel)",
        "info_loaded": "file caricati. Pronto a unire!",
        "btn_merge": "🚀 Unisci File Ora",
        "error": "Errore con il file",
        "success": "✅ Fatto! Ho creato un unico file con",
        "rows": "righe.",
        "download_label": "📥 Scarica File Unito (.xlsx)",
        "kofi_title": "Ti è stato utile?",
        "kofi_desc": "Offrimi un caffè per il server!"
    }
}

# Selettore lingua nella sidebar
language = st.sidebar.radio("Language / Lingua", ["English 🇺🇸", "Italiano 🇮🇹"])
t = translations[language] # Carica i testi della lingua scelta

# --- INIZIO APP ---

st.title(t["title"])
st.markdown(t["desc"])

# 2. Caricamento File
uploaded_files = st.file_uploader(
    t["upload_label"], 
    accept_multiple_files=True, 
    type=['csv', 'xlsx']
)

if uploaded_files:
    st.info(f"{len(uploaded_files)} {t['info_loaded']}")
    
    # Pulsante di azione
    if st.button(t["btn_merge"]):
        all_data = []
        progress_bar = st.progress(0)
        
        # 3. Ciclo di elaborazione
        for i, file in enumerate(uploaded_files):
            try:
                # Controlla se è CSV o Excel
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                
                all_data.append(df)
                
                # Aggiorna barra progresso
                progress_bar.progress((i + 1) / len(uploaded_files))
                
            except Exception as e:
                st.error(f"{t['error']} {file.name}: {e}")

        # 4. Risultato finale
        if all_data:
            final_df = pd.concat(all_data, ignore_index=True)
            
            st.success(f"{t['success']} {len(final_df)} {t['rows']}")
            
            # Anteprima dati (prime 5 righe)
            st.dataframe(final_df.head())

            # 5. Preparazione Download
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                final_df.to_excel(writer, index=False, sheet_name='Merged_Data')
            output.seek(0)

            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.download_button(
                    label=t["download_label"],
                    data=output,
                    file_name="merged_files.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            # 6. SEZIONE KO-FI
            with col2:
                st.markdown(f"### {t['kofi_title']}")
                
                # --- ⚠️ INSERISCI QUI IL TUO LINK KO-FI ---
                kofi_url = "https://ko-fi.com/screemerss" 
                # ------------------------------------------
                
                st.markdown(
                    f"""
                    <a href='{kofi_url}' target='_blank'>
                    <img style='border:0px;height:40px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee' />
                    </a>
                    <br><small>{t['kofi_desc']}</small>
                    """,
                    unsafe_allow_html=True
                )
