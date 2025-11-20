import streamlit as st
import pandas as pd
from io import BytesIO

# 1. Configurazione della pagina
st.set_page_config(page_title="Excel & CSV Merger", page_icon="📊", layout="centered")

# 2. Titolo e Intro
st.title("📊 Unisci i tuoi file Excel/CSV")
st.markdown("""
Hai tanti file con le stesse colonne e devi unirli in uno solo? 
Caricali qui sotto, farò io il lavoro noioso per te in pochi secondi.
""")

# 3. Caricamento File
uploaded_files = st.file_uploader(
    "Trascina qui i file (CSV o Excel)", 
    accept_multiple_files=True, 
    type=['csv', 'xlsx']
)

if uploaded_files:
    st.info(f"Hai caricato {len(uploaded_files)} file. Pronto a unire!")
    
    # Pulsante di azione
    if st.button("🚀 Unisci File Ora"):
        all_data = []
        progress_bar = st.progress(0)
        
        # 4. Ciclo di elaborazione
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
                st.error(f"Errore con il file {file.name}: {e}")

        # 5. Risultato finale
        if all_data:
            final_df = pd.concat(all_data, ignore_index=True)
            
            st.success(f"✅ Fatto! Ho creato un unico file con {len(final_df)} righe.")
            
            # Anteprima dati (prime 5 righe)
            st.dataframe(final_df.head())

            # 6. Preparazione Download
            output = BytesIO()
            # Salviamo sempre in Excel che è più professionale per l'utente business
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                final_df.to_excel(writer, index=False, sheet_name='Dati_Uniti')
            output.seek(0)

            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.download_button(
                    label="📥 Scarica File Unito (.xlsx)",
                    data=output,
                    file_name="file_uniti.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            # 7. SEZIONE KO-FI (La parte importante per te)
            with col2:
                st.markdown("### Ti è stato utile?")
                # Sostituisci il link qui sotto con il tuo reale di Ko-fi
                kofi_url = "https://ko-fi.com/screemerss"
                
                st.markdown(
                    f"""
                    <a href='{kofi_url}' target='_blank'>
                    <img style='border:0px;height:40px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee' />
                    </a>
                    <br><small>Offrimi un caffè per il server!</small>
                    """,
                    unsafe_allow_html=True
                )