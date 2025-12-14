import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from ocr_service import extract_text_from_image
from rag_service import RAGService

# Load environment variables
load_dotenv()

# Initialize RAG Service
rag_service = RAGService()

def load_prompt_template(path="prompt_template.txt"):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Prompt template file '{path}' not found.")
        return None

def generate_explanation(document_context, credit_score, credit_bucket, shap_negative, shap_positive, target_language="English"):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in environment variables.")
        print("Please add GROQ_API_KEY to your .env file.")
        return

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    
    # Use Llama model on Groq
    model_name = "llama-3.3-70b-versatile" 
    
    # Retrieve relevant policy context using RAG
    # We construct a query based on the available information
    query = f"Credit score {credit_score}. {document_context[:200]}"
    policy_context = rag_service.retrieve_context(query)
    
    print(f"\n[RAG] Retrieved Policy Context:\n{policy_context}\n")

    template = load_prompt_template()
    if not template:
        return
        
    # Append instructions for RAG and Language
    full_prompt = template + f"""

    [BANK POLICIES]
    {policy_context}
    
    INSTRUCTIONS:
    1. Explain the rejection based on the provided data and the [BANK POLICIES] above.
    2. If a specific policy is violated (e.g., minimum score), explicitly mention it.
    3. Generate the response in {target_language}.
    """

    # Fill the template
    prompt = full_prompt.format(
        document_context=document_context,
        credit_score=credit_score,
        credit_bucket=credit_bucket,
        shap_negative_factors=shap_negative,
        shap_positive_factors=shap_positive
    )

    print("\nGenerating explanation...")
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        print("\n" + "="*40)
        print(response.choices[0].message.content)
        print("="*40 + "\n")
    except Exception as e:
        print(f"Error calling Grok API: {e}")
        return

def main():
    print("--- Loan Rejection Explainer ---")
    
    # Language Selection
    print("Select Language:")
    print("1. English (en)")
    print("2. Spanish (es)")
    print("3. French (fr)")
    print("4. Hindi (hi)")
    lang_choice = input("Enter choice (1-4): ").strip()
    
    lang_map = {
        '1': ('English', 'en'),
        '2': ('Spanish', 'es'),
        '3': ('French', 'fr'),
        '4': ('Hindi', 'hi')
    }
    
    target_lang_name, target_lang_code = lang_map.get(lang_choice, ('English', 'en'))
    print(f"Selected Language: {target_lang_name}")

    # Check for input mode
    print("\nSelect Input Mode:")
    print("1. Use Mock Data (JSON)")
    print("2. Use Image File + Mock Data")
    choice = input("Enter choice (1/2): ").strip()
    
    # Default values
    credit_score = 620
    credit_bucket = "Fair"
    shap_negative = "- High Debt-to-Income Ratio\n- Recent Missed Payments"
    shap_positive = "- Long Credit History"
    document_context = ""

    if choice == '1':
        # Load from JSON if exists, else use defaults
        try:
            with open("mock_data.json", "r") as f:
                data = json.load(f)
                credit_score = data.get("credit_score", credit_score)
                credit_bucket = data.get("credit_bucket", credit_bucket)
                shap_negative = data.get("shap_negative_factors", shap_negative)
                shap_positive = data.get("shap_positive_factors", shap_positive)
                document_context = data.get("document_context", "Loan rejected due to insufficient income.")
                print("Loaded mock data.")
        except FileNotFoundError:
            print("mock_data.json not found, using defaults.")
            document_context = "Loan rejected due to policy 504: DTI too high."

    elif choice == '2':
        image_path = input("Enter path to loan document image: ").strip()
        print(f"Extracting text from {image_path} in {target_lang_name}...")
        # Pass language code list to OCR service
        document_context = extract_text_from_image(image_path, lang_list=[target_lang_code, 'en'])
        print(f"Extracted Context Length: {len(document_context)} chars")
        if "Error" in document_context:
            print(document_context)
            return
    
    generate_explanation(document_context, credit_score, credit_bucket, shap_negative, shap_positive, target_language=target_lang_name)

if __name__ == "__main__":
    main()
