import streamlit as st
from codon_table import CODON_TABLE
from amino_acids import AMINO_ACID_NAMES

# --------------------------
# Configuration and Introduction
# --------------------------
st.set_page_config(page_title="DNA to Protein Translator", layout="centered")

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

# Initialize DNA sequence variable
dna_sequence = ""

# --- Text Input ---
if input_type == "Paste DNA text":
    user_input = st.text_area("Paste your DNA sequence here (A, T, G, C only):", height=200)
    if user_input:
        dna_sequence = user_input.strip()

# --- File Upload ---
else:
    uploaded_file = st.file_uploader("Upload a .txt or .fasta file", type=["txt", "fasta"])
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")

        # Handle FASTA: remove header line starting with '>'
        if file_content.startswith(">"):
            lines = file_content.splitlines()
            lines = [line for line in lines if not line.startswith(">")]
            dna_sequence = "".join(lines)
        else:
            dna_sequence = file_content.strip()

# --------------------------
# Clean the DNA Sequence
# --------------------------
def clean_sequence(seq):
    """Remove spaces/newlines and convert to uppercase. Keep only A/T/G/C."""
    allowed = {"A", "T", "G", "C"}
    seq = seq.upper().replace(" ", "").replace("\n", "")
    return "".join([nuc for nuc in seq if nuc in allowed])

def trim_to_codons(seq):
    """Trim sequence to make it divisible by 3."""
    return seq[:len(seq) - (len(seq) % 3)]

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

        # --------------------------
        # 🧬 Translation Logic
        # --------------------------
        def translate_to_protein(seq):
            protein_sequence = []
            codon_breakdown = []

            for i in range(0, len(seq), 3):
                codon = seq[i:i + 3]
                amino_acid = CODON_TABLE.get(codon, '-')
                protein_sequence.append(amino_acid)
                codon_breakdown.append(f"{codon} → {amino_acid}")

            return "".join(protein_sequence), codon_breakdown

        protein, codon_details = translate_to_protein(trimmed_seq)

        # --------------------------
        # 📊 Display Results
        # --------------------------
        if protein:
            st.subheader("2. Translated Protein Sequence")
            st.code(protein, language="text")

            st.subheader("3. Codon Breakdown")
            for codon_info in codon_details:
                st.write(codon_info)

            # Highlight Start/Stop Codons
            if st.checkbox("Highlight Start/Stop Codons", value=True):
                highlighted = ""
                for i in range(0, len(trimmed_seq), 3):
                    codon = trimmed_seq[i:i+3]
                    if codon == 'ATG':
                        highlighted += f"<span style='color:green'>{codon}</span> "
                    elif codon in ['TAA', 'TAG', 'TGA']:
                        highlighted += f"<span style='color:red'>{codon}</span> "
                    else:
                        highlighted += codon + " "
                st.markdown("**Start and Stop Codons Highlighted:**")
                st.markdown(highlighted, unsafe_allow_html=True)

            # Full Amino Acid Names
            st.subheader("4. Amino Acid Full Names")
            cols = st.columns(2)
            for i, aa in enumerate(protein):
                full_name = AMINO_ACID_NAMES.get(aa, "Unknown")
                with cols[i % 2]:
                    st.markdown(f"**{aa}** → {full_name}")
        else:
            st.warning("⚠️ No valid protein sequence generated. Please check the DNA sequence.")

# --------------------------
# Styling
# --------------------------
st.markdown(
    """
    <style>
        .css-1d391kg {
            background-color: #f5f5f5;
            color: #333;
        }
        .stButton>button {
            background-color: #0066CC;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)
