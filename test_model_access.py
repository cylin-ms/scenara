import argparse
from transformers import AutoTokenizer

def test_model_access(model_path):
    """Test if we can access the specified model"""
    try:
        print(f"Testing access to model: {model_path}")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        print(f"✓ Successfully loaded tokenizer for {model_path}")
        
        # Test basic tokenization
        test_text = "Hello, how are you?"
        tokens = tokenizer.encode(test_text)
        print(f"✓ Tokenization test passed: {len(tokens)} tokens")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to access {model_path}")
        print(f"Error: {e}")
        return False

def suggest_alternative_models():
    """Suggest publicly available models that should work"""
    models = [
        "gpt2",
        "gpt2-medium", 
        "microsoft/DialoGPT-medium",
        "microsoft/DialoGPT-large",
        "HuggingFaceH4/zephyr-7b-beta",
        "microsoft/phi-1_5",
        "microsoft/phi-2"
    ]
    
    print("\nTesting alternative models...")
    working_models = []
    
    for model in models:
        try:
            tokenizer = AutoTokenizer.from_pretrained(model)
            working_models.append(model)
            print(f"✓ {model} - accessible")
        except Exception as e:
            print(f"✗ {model} - not accessible: {str(e)[:100]}...")
    
    return working_models

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="HuggingFaceH4/zephyr-7b-beta")
    parser.add_argument("--suggest_alternatives", action="store_true", help="Test alternative models")
    
    args = parser.parse_args()
    
    if args.suggest_alternatives:
        working_models = suggest_alternative_models()
        if working_models:
            print(f"\nWorking models found: {len(working_models)}")
            print("You can use any of these models in the pipeline.")
        else:
            print("\nNo working models found. You may need to:")
            print("1. Install additional dependencies")
            print("2. Set up Hugging Face authentication")
            print("3. Check your internet connection")
    else:
        success = test_model_access(args.model_path)
        if success:
            print(f"\n✓ {args.model_path} is ready to use!")
        else:
            print(f"\n✗ Cannot use {args.model_path}")
            print("Try running with --suggest_alternatives to find working models")