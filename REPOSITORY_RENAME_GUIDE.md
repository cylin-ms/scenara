# Repository Rename Guide: PromptCoT → Scenara

## 🎯 **Objective**
Rename the GitHub repository from "PromptCoT" to "Scenara" to align with the project branding.

## 🔧 **Manual Steps Required**

### 1. **GitHub Repository Rename** (Repository Owner Only)
1. **Navigate to**: `https://github.com/inclusionAI/PromptCoT`
2. **Click**: Settings tab
3. **Scroll to**: "Repository name" section
4. **Change**: `PromptCoT` → `Scenara`
5. **Click**: "Rename" button
6. **Confirm**: The rename operation

**Result**: Repository URL becomes `https://github.com/inclusionAI/Scenara`

### 2. **Update Local Git Remote**
After GitHub rename, run this command locally:
```bash
cd /Users/cyl/projects/PromptCoT
git remote set-url origin https://github.com/inclusionAI/Scenara.git
```

### 3. **Optional: Rename Local Directory**
```bash
cd /Users/cyl/projects/
mv PromptCoT Scenara
cd Scenara
```

## ✅ **Already Updated** (By AI Assistant)

### **Internal Project References**
- ✅ `tools/platform_detection.py` - Updated to "Scenara 2.0"
- ✅ `startup.py` - Updated to "Scenara 2.0"
- ✅ `.github/copilot-instructions.md` - Updated to "Scenara 2.0"
- ✅ Platform detection output messages
- ✅ Documentation summaries
- ✅ Git clone URL in technical documentation
- ✅ Training data collection messages

### **Files with Mixed References** (Require Careful Review)
The following files contain both:
- **PromptCoT 2.0** = Original research framework (should keep)
- **Project references** = Should change to "Scenara"

📁 **`docs/Meeting_PromptCoT_2.0_Executive_Summary.md`**
📁 **`docs/Meeting_PromptCoT_2.0_Comprehensive_Report.md`**
📁 **`Meeting_PromptCoT_Report.md`**

These files reference:
1. **PromptCoT 2.0 methodology** (research framework - keep as is)
2. **"Meeting PromptCoT"** (your implementation - could rename to "Scenara")
3. **Project/repository references** (should update to "Scenara")

## 🤔 **Decision Needed**

### **Research Framework vs Project Name**
- **PromptCoT 2.0** = The underlying research methodology you're building on
- **Scenara 2.0** = Your enterprise meeting intelligence system

**Question**: Should documentation refer to:
1. **"Scenara 2.0 (based on PromptCoT 2.0 framework)"** 
2. Keep technical references to "Meeting PromptCoT" as implementation name
3. Or fully rebrand everything to "Scenara"?

## 📋 **Post-Rename Checklist**

After GitHub rename:
- [ ] Update local git remote URL
- [ ] Test git push/pull operations
- [ ] Update any CI/CD configurations that reference old repo name
- [ ] Update documentation links that point to GitHub
- [ ] Consider updating file names in `docs/` folder to use "Scenara"
- [ ] Update README.md title and descriptions
- [ ] Update any hardcoded URLs in code or documentation

## ⚠️ **Important Notes**

1. **GitHub will automatically redirect** old URLs to new ones
2. **Existing clones** will need remote URL updates
3. **CI/CD systems** may need configuration updates
4. **External links** will continue to work due to GitHub redirects
5. **Keep research attribution** to original PromptCoT 2.0 framework

---

**Status**: Ready for repository owner to rename via GitHub Settings
**Next**: Manual GitHub repository rename → Update local git remote → Continue development as "Scenara"