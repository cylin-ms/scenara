# Scenara 2.0 Project Structure Template

## 📁 **Recommended Directory Structure**

```
Scenara/
├── .cursorrules                    # AI assistant configuration
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot instructions
├── README.md                      # Project overview
├── requirements.txt               # Python dependencies
├── startup.py                     # Platform detection startup
├── tools/                         # Core utilities
│   ├── __init__.py
│   ├── platform_detection.py     # Environment detection
│   ├── llm_api.py                # Multi-provider LLM client
│   ├── meeting_extractor.py      # Meeting data collection
│   ├── web_scraper.py            # Research capabilities
│   ├── screenshot_utils.py       # UI verification
│   └── search_engine.py          # Search integration
├── src/                          # Core application
│   ├── __init__.py
│   ├── meeting_intelligence/     # Meeting analysis
│   ├── gutt_framework/          # GUTT v4.0 evaluation
│   ├── data_architecture/       # Separated data handling
│   └── scenara_core/            # Main system
├── data/                        # Data storage
│   ├── real_meetings/           # Real meeting data
│   ├── synthetic_scenarios/     # Generated scenarios
│   └── evaluation_results/      # GUTT scores
├── Priority_Calendar/           # Meeting prioritization system
│   ├── Meeting_Importance_Overview.md
│   ├── Meeting_Priority_Overview.md
│   ├── Priority_Calendar_Analysis_Summary.md
│   └── Me_Notes_Integration_*.md
├── config/                      # Configuration
│   ├── llm_models.yaml         # LLM configurations
│   ├── meeting_types.yaml      # Meeting taxonomy
│   └── scenara_config.yaml     # System settings
├── tests/                       # Test suite
│   ├── unit/
│   ├── integration/
│   └── evaluation/
├── docs/                        # Documentation
│   ├── user_guide.md
│   ├── api_reference.md
│   ├── deployment_guide.md
│   └── architecture.md
└── scripts/                     # Utility scripts
    ├── setup_environment.py
    ├── data_collection.py
    └── evaluation_runner.py
```

## 🎯 **Core Components to Port from PromptCoT**

### **From Tools Directory**
- [X] Platform detection system
- [X] LLM API integration (multi-provider)
- [X] Meeting extraction tools
- [X] Web scraping capabilities
- [X] Screenshot verification workflow

### **From Meeting Intelligence**
- [X] Meeting taxonomy (31+ types)
- [X] Real meeting data processing
- [X] Synthetic scenario generation
- [X] GUTT v4.0 evaluation framework
- [X] Timezone handling (UTC → PDT)
- [ ] Priority Calendar system integration

### **From Priority Calendar System**
- [ ] Intelligent meeting prioritization framework
- [ ] 1-10 importance scoring system
- [ ] 4-category classification (Important/Participant/Flex/Follow)
- [ ] Meeting ranking algorithms and signal detection
- [ ] Integration with Meeting Extraction Tool
- [ ] Me Notes integration and enhancement

### **From Me Notes Intelligence System**
- [ ] Personal meeting preparation enhancement system
- [ ] Real-time Microsoft 365 integration
- [ ] Multi-user access control and analytics
- [ ] Enhanced ranking and prioritization features
- [ ] Automated meeting intelligence reports
- [ ] Integration with Priority Calendar framework

### **From AI Integration**
- [X] .cursorrules configuration
- [X] GitHub Copilot instructions
- [X] Cross-platform AI synchronization
- [X] Task management system
- [X] Lesson learning framework

## 🔧 **Setup Process**

1. **Create directory structure**
2. **Port core tools and configurations**
3. **Update all references to use "Scenara 2.0"**
4. **Implement clean meeting intelligence architecture**
5. **Set up Python virtual environment**
6. **Configure AI assistant integration**
7. **Test platform detection and tools**

## 📋 **Benefits of Fresh Start**

- ✅ Clean project structure
- ✅ Consistent "Scenara 2.0" branding throughout
- ✅ No legacy PromptCoT references to clean up
- ✅ Optimized for meeting intelligence focus
- ✅ Modern Python project layout
- ✅ Clear separation of concerns
- ✅ Proper documentation structure

## 🚀 **Next Steps**

1. Create empty `~/projects/Scenara` directory
2. Open in VS Code/Cursor
3. Let AI assistant populate the structure
4. Port and adapt the best components from PromptCoT
5. Launch as Scenara 2.0!

---

**Status**: Ready to create clean Scenara 2.0 project  
**Advantage**: No migration complexity, fresh start with proper structure