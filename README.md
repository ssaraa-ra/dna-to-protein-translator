# 🧬 DNA to Protein Translator

**DNA to Protein Translator** is a web-based tool that converts DNA sequences into protein sequences using the standard genetic code. This tool is designed to help researchers, students, and bioinformaticians easily translate DNA sequences to proteins, aiding in molecular biology studies.

## Features

- **Input Methods:**  
  Users can either paste a DNA sequence directly into the tool or upload a `.txt` or `.fasta` file containing the sequence.

- **Sequence Cleaning:**  
  The app automatically cleans the input DNA sequence by:
  - Removing spaces and newline characters.
  - Converting the sequence to uppercase.
  - Validating and keeping only the nucleotide bases A, T, G, C.

- **DNA to Protein Translation:**  
  The DNA sequence is translated into the corresponding protein sequence using the standard genetic code.

- **Codon Breakdown:**  
  Displays the codon breakdown (3-letter DNA code) and the corresponding amino acids for each codon.

- **Start and Stop Codons Highlighted:**  
  Highlights the **start codon** (`ATG`) and **stop codons** (`TAA`, `TAG`, `TGA`), allowing easy identification of translation points.

- **Full Amino Acid Names:**  
  For each translated amino acid, the tool displays its full name (e.g., `C → Cysteine`).

---

## Installation

To run this project locally, follow these instructions:

### 1. Clone the Repository

```bash
git clone https://github.com/sararamadanii/dna-to-protein.git
cd dna-to-protein
```

 ### 2. Install Dependencies
 Install streamlit 
 ```bash
pip install streamlit
```

### 3. Run the App
You can start the application by running:

```bash
streamlit run app.py
```

After the app starts, open the URL in your browser (typically http://localhost:8501/).



### Technologies Used
Streamlit: For building the web interface.

Python: Programming language for the backend and logic.

Codon Table: Standard genetic code used for DNA to protein translation.

Amino Acid Table: Mapping of amino acid abbreviations to their full names.
