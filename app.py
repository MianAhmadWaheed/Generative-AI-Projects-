
import streamlit as st
import torch

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Instantiate the model (assuming train_dataset is already defined)
model = Transformer(
    src_vocab_size=len(train_dataset.src_vocab),
    tgt_vocab_size=len(train_dataset.tgt_vocab)
).to(device)

# Load model checkpoint and set to evaluation mode
model.load_state_dict(torch.load("transformer_code.pth", map_location=device))
model.eval()

# Streamlit UI
st.title("🚀 Code to Pseudocode Generator")
st.write("Enter C++ code, and the model will generate pseudocode.")

# Input area
code_input = st.text_area("Enter C++ code here...", height=150)

# Generate button
if st.button("Generate Pseudocode"):
    if code_input.strip():
        generated_pseudo = generate_output(model, code_input, train_dataset.src_vocab, train_dataset.tgt_vocab, device)
        st.subheader("Generated Pseudocode:")
        st.code(generated_pseudo, language="python")
    else:
        st.warning("⚠️ Please enter C++ code before generating!")
