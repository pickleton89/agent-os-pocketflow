# For End-Users: You Probably Want Generated Documentation

## 🚨 Are You Looking for Template Documentation?

**If you received a generated PocketFlow template, you're in the wrong place.**

This repository contains the **framework that generates templates** - not documentation for using those templates.

---

## 📍 Where to Find What You Need

### ✅ If You Have a Generated Template

**Look in YOUR generated project for documentation:**

```
your-generated-project/
├── README.md              # 👈 Start here - implementation guide
├── docs/
│   ├── design.md          # 👈 Your project's architecture  
│   ├── api.md             # 👈 API documentation
│   └── deployment.md      # 👈 How to deploy your app
├── flow.py                # 👈 Your workflow implementation
├── nodes.py               # 👈 Your nodes with TODO guidance
└── pyproject.toml         # 👈 Your dependencies
```

**The documentation you need is WITH your generated template, not here.**

### ❌ What This Repository Contains

This repository has:
- Framework development guides
- Template generation documentation  
- Contributor instructions
- System architecture for the framework

This repository does NOT have:
- How to use PocketFlow (that's in your generated project)
- How to implement TODO stubs (that's in your generated README)
- API documentation for your application (that's generated with your template)
- Deployment guides for your app (that's in your generated docs/)

---

## 🎯 Quick Decision Tree

**Ask yourself:**

1. **Do you have a folder with generated PocketFlow files?**
   → YES: Look at the README.md IN that folder
   → NO: You might want to generate a template first

2. **Are you trying to complete TODO stubs in generated code?**
   → YES: Check the implementation guidance in your generated docs/
   → NO: You might be looking for framework documentation

3. **Are you trying to understand PocketFlow patterns?**
   → Generated project: See your generated docs/design.md
   → Framework development: [See our pattern docs](../template-generation/patterns/)

4. **Are you getting import errors for PocketFlow modules?**
   → That's normal in a framework repository (templates have placeholders)
   → In your generated project, run `pip install pocketflow`

---

## 🚀 Getting Started (If You Don't Have a Template Yet)

If you don't have a generated template yet:

1. **Use Claude Code or another AI agent** with this framework
2. **Ask it to generate a PocketFlow template** for your use case
3. **Follow the generated project's documentation** (not this repository's docs)

Example request:
```
"Create a PocketFlow template for a document Q&A system using RAG patterns"
```

The AI agent will use this framework to generate a complete starter project with its own documentation.

---

## 🤔 Still Confused?

### Framework vs Generated Project

| Framework Repository (This One) | Your Generated Project |
|--------------------------------|------------------------|
| 🏗️ Builds the generator | 🚀 Contains your application |
| 📝 Has placeholder TODOs | ✅ You complete the TODOs |  
| 🧪 Tests the framework | ✅ You test your application |
| 📦 Framework dependencies | 📦 Runtime dependencies |
| 🎯 For contributors | 🎯 For end-users |

### What Each README Contains

**This Repository's README:**
- How to contribute to the framework
- Framework architecture
- Template generation system
- Meta-documentation about documentation

**Your Generated Project's README:**
- How to implement YOUR specific application
- What each TODO means in YOUR context  
- How to deploy YOUR application
- YOUR project's dependencies and setup

---

## 📞 Need Help?

**For Generated Template Issues:**
- Check the implementation guidance in your generated docs/
- Review the TODO comments in your generated code
- Ask your AI agent for help with implementation

**For Framework Issues:**
- See [Framework Development](../framework-development/QUICKSTART.md)
- Check [Architecture Documentation](../architecture/README.md)
- Review [Contributor Guidelines](../framework-development/QUICKSTART.md)

Remember: The framework generates starting points. Your generated project contains the documentation for completing those starting points.