#!/usr/bin/env python3
"""
Wrapper script to run meeting identification
Can be executed directly from VS Code or any Python environment
"""

import sys
from pathlib import Path

# Add tools directory to path
tools_dir = Path(__file__).parent / "tools"
sys.path.insert(0, str(tools_dir))

# Import and run the main function directly
try:
    from identify_top7_meetings import main
    
    print("="*60)
    print("Top 7 Meeting Type Identification")
    print("="*60)
    print("Using Ollama LLM (gpt-oss:20b)")
    print()
    
    main()
    
except ImportError as e:
    print(f"Error importing identification script: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error running identification: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
