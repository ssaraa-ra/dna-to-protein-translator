import streamlit as st
from codon_table import CODON_TABLE
from amino_acids import AMINO_ACID_NAMES
from collections import Counter
import pandas as pd
import altair as alt

# --------------------------
# Streamlit Configuration
# --------------------------
st.set_page_config(
    page_title="DNA to Protein Translator",
    layout="centered",
    initial_sidebar_state="auto"
)

# --------------------------
# Styling (in-app only)
# --------------------------
st.markdown("""
<style>
    html, body, .main {
        background-color: #f9f9f9;
        color: #262730;
        font-family: "Segoe UI", sans-serif;
    }
    h1, h2, h3 {
        color: #1f3c88;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .highlight-start {
        color: green; 
        font-weight: bold;
    }
    .highlight-stop {
        color: red; 
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------
# Introduction
# --------------------------
st.title("🧬 DNA to Protein Translator")
st.markdown("Convert DNA sequences into protein using the standard genetic code.")
st.write("""
This tool allows researchers, students, and bioinformaticians to quickly translate a DNA sequence into the corresponding protein.  
Whether you're working with raw genetic data or learning about the basics of molecular biology, this tool is here to help!
""")

# --------------------------
# Input Section
# --------------------------
st.subheader("1. Input DNA Sequence")
input_type = st.radio("Choose input method:", ("Paste DNA text", "Upload .txt/.fasta file"))
dna_sequence = ""

if input_type == "Paste DNA text":
    user_input = st.text_area("Paste your DNA sequence here (A, T, G, C only):", height=200)
    if user_input:
        dna_sequence = user_input.strip()
else:
    uploaded_file = st.file_uploader("Upload a .txt or .fasta file", type=["txt", "fasta"])
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        if file_content.startswith(">"):
            lines = file_content.splitlines()
            lines = [line for line in lines if not line.startswith(">")]
            dna_sequence = "".join(lines)
        else:
            dna_sequence = file_content.strip()

# --------------------------
# Sequence Processing
# --------------------------
def clean_sequence(seq):
    allowed = {"A", "T", "G", "C"}
    seq = seq.upper().replace(" ", "").replace("\n", "")
    return "".join([nuc for nuc in seq if nuc in allowed])

def trim_to_codons(seq):
    return seq[:len(seq) - (len(seq) % 3)]

def translate_to_protein(seq):
    protein_sequence = []
    codon_breakdown = []
    for i in range(0, len(seq), 3):
        codon = seq[i:i + 3]
        amino_acid = CODON_TABLE.get(codon, '-')
        protein_sequence.append(amino_acid)
        codon_breakdown.append(f"{codon} → {amino_acid}")
    return "".join(protein_sequence), codon_breakdown

# --------------------------
# Translation Output
# --------------------------
if dna_sequence:
    cleaned_seq = clean_sequence(dna_sequence)

    if not cleaned_seq:
        st.error("❌ The sequence contains invalid characters. Only A, T, G, and C are allowed.")
    else:
        trimmed_seq = trim_to_codons(cleaned_seq)

        if len(cleaned_seq) != len(trimmed_seq):
            st.warning(f"⚠️ Sequence trimmed from {len(cleaned_seq)} bp to {len(trimmed_seq)} bp to make it divisible by 3.")

        st.success("✅ DNA sequence loaded successfully!")
        st.markdown(f"**Final sequence length:** {len(trimmed_seq)} bp")
        st.code(trimmed_seq, language="text")

        protein, codon_details = translate_to_protein(trimmed_seq)

        if protein:
            st.subheader("2. Translated Protein Sequence")
            st.code(protein, language="text")

            # Download Button
            st.download_button(
                label="📥 Download Protein Sequence",
                data=protein,
                file_name="protein_sequence.txt",
                mime="text/plain"
            )

            # Tabs for breakdown and info
            tab1, tab2, tab3 = st.tabs(["🧬 Codon Breakdown", "🔤 Full Amino Acid Names", "📊 Amino Acid Chart"])

            with tab1:
                st.markdown("### Codon → Amino Acid Mapping")
                for codon_info in codon_details:
                    st.write(codon_info)

                if st.checkbox("Highlight Start/Stop Codons", value=True):
                    highlighted = ""
                    for i in range(0, len(trimmed_seq), 3):
                        codon = trimmed_seq[i:i+3]
                        if codon == 'ATG':
                            highlighted += f"<span class='highlight-start'>{codon}</span> "
                        elif codon in ['TAA', 'TAG', 'TGA']:
                            highlighted += f"<span class='highlight-stop'>{codon}</span> "
                        else:
                            highlighted += codon + " "
                    st.markdown("**Start and Stop Codons Highlighted:**")
                    st.markdown(highlighted, unsafe_allow_html=True)

            with tab2:
                st.markdown("### Amino Acid Full Names")
                cols = st.columns(2)
                for i, aa in enumerate(protein):
                    full_name = AMINO_ACID_NAMES.get(aa, "Unknown")
                    with cols[i % 2]:
                        st.markdown(f"**{aa}** → {full_name}")

            with tab3:
                st.markdown("### Amino Acid Frequency")
                aa_count = Counter(protein)
                df = pd.DataFrame(aa_count.items(), columns=['Amino Acid', 'Count'])
                chart = alt.Chart(df).mark_bar().encode(
                    x='Amino Acid',
                    y='Count',
                    tooltip=['Amino Acid', 'Count']
                ).properties(width=500, height=300)
                st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("⚠️ No valid protein sequence generated. Please check the DNA sequence.")
