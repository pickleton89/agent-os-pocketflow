# Agent OS - Complete Documentation

*Source: https://buildermethods.com/agent-os*

## Stop prompting AI coding agents like it's 2024

Your coding agents are capable of so much more—they just need an operating system. Introducing, Agent OS.

## A system to make AI coding agents build your way, not their way.

Agent OS transforms AI coding agents from confused interns into productive developers. With structured workflows that capture your standards, your stack, and the unique details of your codebase, Agent OS gives your agents the specs they need to ship quality code on the first try—not the fifth.

### Use it with:
- Claude Code, Cursor, or any other AI coding tool
- New products or established codebases
- Big features, small fixes, or anything in between
- Any language or framework

### Free & Open Source
- [Docs & Setup](#installation)
- [View on GitHub](https://github.com/buildermethods/agent-os)

---

## Why use Agent OS?

Stop wrestling with AI that writes the wrong code. Agent OS transforms coding agents from confused assistants into trusted developers who truly understand your codebase.

3 reasons why product teams use Agent OS:

### 1. Complete context, not just prompts

Unlike basic AI setups, Agent OS provides three layers of context that work together:

- **Standards** - Your coding style, tech stack, and best practices
- **Product** - Your mission, architecture, roadmap, and decisions
- **Specs** - Detailed plans & tasks for each feature implementation

**The result:** Agents write code that looks like you wrote it—first time, every time.

### 2. Structured development, not chaos

Agent OS replaces random prompting and circular rewrites with a proven workflow. It automatically:

- Writes comprehensive specs before coding begins
- Breaks features into trackable, TDD-focused tasks
- Documents key decisions as they happen
- Updates your roadmap as features ship

**The difference:** Ship features faster with clear specs and completed tasks—not endless cycles of (re)explaining requirements and redoing work.

### 3. Your standards, your way

Agent OS is completely yours to shape. Define your own coding standards, write custom instructions, and adapt every workflow to match how your team operates. No rigid interfaces or prescribed processes—just markdown files you control. Works seamlessly with any AI tool or IDE you choose.

**The relief:** Your coding agent finally feels like a senior developer on your team—thinking your way, following your patterns, and shipping at your standards.

---

## The Three Layers of Context

Agent OS works by layering context—just like you'd onboard a human developer. Each layer builds on the previous one, creating a complete picture of how you build software.

### Layer 1: Your standards

Your standards define how you build software. Your stack. Your opinions. Your style. Your priorities. The standards you expect everyone on your team to follow when building anything. These should include:

- **Tech Stack** — Your default frameworks, libraries, and tools
- **Code Style** — Your formatting rules, naming conventions, and preferences
- **Best Practices** — Your development philosophy (e.g., TDD, commit patterns, etc.)

Your standards documentation lives on your system in `~/.agent-os/standards/...` and are referenced from every project, every codebase. Set once, use everywhere, override as needed.

### Layer 2: Your product

At the product (codebase) layer, we document what it is we're building, why we're building it, who it's for, and the big-picture product roadmap. This includes:

- **Mission** — What you're building, for whom, and why it matters
- **Roadmap** — Features shipped, in progress, and planned
- **Decisions** — Key architectural and technical choices (with rationale)
- **Product-specific stack** — The exact versions and configurations for this codebase

Product documentation lives in your codebase (`.agent-os/product/`) and give agents the full picture of your product.

### Layer 3: Your specs

Throughout your product's development, you'll create many specs. Each spec is a single feature or enhancement or fix, which typically represents a few hours or days of work (accelerated with the help of AI). Each spec will have its own requirements, technical specs, and tasks breakdown.

Individual feature specifications include:

- **SRD (Spec Requirements Document)** — Goals for the feature, user stories, success criteria
- **Technical Specs** — API design, database changes, UI requirements
- **Tasks Breakdown** — Trackable step-by-step implementation plan with dependencies

Specs live in dated folders inside your codebase (`.agent-os/specs/2025-12-19-user-auth/`) and guide agents through each spec's implementations.

With all three layers in place, your agent has everything it needs: how you build (Standards), what you're building (Product), and what to build next (Specs). No more confusion, no more rewrites—just clean, consistent code that looks like you wrote it.

---

## Install Agent OS

Getting started with Agent OS is a two-step process:

1. **Base Installation** - Install Agent OS on your system
2. **Tool-Specific Setup** - Set up Claude Code, Cursor, or whichever IDE you're using

Installing Agent OS in an existing codebase that's been around a while? Then see [Working with Existing Codebases](#working-with-existing-codebases).

### 1. Base Installation

Everyone starts here. The fastest way to get started is by running the install script with this one-liner in your terminal:

```bash
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup.sh | bash
```

#### What the install script does:
- Creates the `~/.agent-os/` folder in your home directory
- Downloads and installs instructions files (plan-product, create-spec, execute-tasks, execute-task, analyze-product) from the GitHub repo
- Downloads and installs standards file templates (tech-stack, code-style, best-practices) from the GitHub repo
- Downloads and installs language-specific code style guides (html-style, css-style, javascript-style) from the GitHub repo
- Preserves any existing files (won't overwrite your customizations)

#### Manual Installation (if preferred):

**1. Create the Agent OS directories**
```bash
mkdir -p ~/.agent-os/standards/code-style
mkdir -p ~/.agent-os/instructions
```

**2. Copy the standards files**
Copy these files to `~/.agent-os/standards/`:
- `tech-stack.md`
- `code-style.md`
- `best-practices.md`

Also copy the Python-specific style guides to `~/.agent-os/standards/code-style/`:
- `python-style.md`
- `fastapi-style.md`
- `pocketflow-style.md`
- `testing-style.md`

**3. Copy the instructions files**
Copy these files to `~/.agent-os/instructions/`:
- `core/plan-product.md`
- `core/create-spec.md`
- `core/execute-tasks.md`
- `core/execute-task.md`
- `core/analyze-product.md`
- `meta/pre-flight.md`

#### Update Instructions

As Agent OS evolves, you may want to update your instruction files while preserving your custom standards. Use these flags with the install script:

**Update Instruction Files Only:**
```bash
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup.sh | bash -s -- --overwrite-instructions
```

**Update Standards Files Only:** (Warning: This will overwrite your customizations!)
```bash
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup.sh | bash -s -- --overwrite-standards
```

**Update Both Instructions and Standards:** (Warning: This will overwrite all your customizations!)
```bash
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup.sh | bash -s -- --overwrite-instructions --overwrite-standards
```

### Important: Customize your standards files

Once you've installed the base files, you'll need to customize the standards files in `~/.agent-os/standards/` to match your preferences. This is where you define your way of building software.

The files that were installed (`tech-stack.md`, `code-style.md`, and `best-practices.md`) are just examples or starting points. You're encouraged to replace or add to them, or delete them and start fresh. Then edit them to match your preferences.

### 2. Tool-Specific Setup

With the base installation complete, now set up Agent OS for your AI tool:

#### Claude Code Setup

Use the following one-liner to run the Claude Code setup script:

```bash
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup-claude-code.sh | bash
```

**What the Claude Code setup script does:**
- Copies the commands from the GitHub Repo to use as custom slash commands in your `~/.claude/commands/` folder
- Optionally installs specialized subagent files from the GitHub Repo to your `~/.claude/agents/` folder for enhanced performance

**Manual Installation (if preferred):**

1. Copy the command files to `~/.claude/commands/`:
   - `plan-product.md`
   - `create-spec.md`
   - `execute-tasks.md`
   - `analyze-product.md`

2. Copy the subagent files to `~/.claude/agents/`:
   - `context-fetcher.md`
   - `date-checker.md`
   - `file-creator.md`
   - `git-workflow.md`
   - `test-runner.md`

That's it! You can now use these commands in Claude Code:
- `/plan-product`
- `/create-spec`
- `/execute-tasks`
- `/analyze-product`

#### Cursor Setup

For each project where you want to use Agent OS, use the following one-liner to run the Cursor setup script:

**Important:** First be sure that you're inside your project's root folder so that Cursor rules are installed inside of it.

```bash
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup-cursor.sh | bash
```

**What the Cursor setup script does:**
- Creates the `.cursor/rules/` directory in your project
- Copies the commands from the GitHub repo to your `.cursor/rules/` folder with `.mdc` extensions

**Manual Installation (if preferred):**

1. Create the Cursor rules directory:
```bash
mkdir -p .cursor/rules
```

2. Copy the command files to `.cursor/rules/` and rename them with `.mdc` extension:
   - `plan-product.md` → `plan-product.mdc`
   - `create-spec.md` → `create-spec.mdc`
   - `execute-tasks.md` → `execute-tasks.mdc`
   - `analyze-product.md` → `analyze-product.mdc`

That's it! You can now use these commands in Cursor:
- `@plan-product`
- `@create-spec`
- `@execute-tasks`
- `@analyze-product`

#### Hybrid Setup (Claude Code + Cursor)

Using both Claude Code and Cursor? Follow both setups above to enable Agent OS in both tools.

1. Follow the Claude Code setup to enable global commands
2. For each project, follow the Cursor setup to add project rules

Both tools will now work with the same Agent OS installation.

#### Other AI coding tools

Agent OS is just markdown files. To adapt it for any AI tool, find where your tool looks for commands or context, then copy our command files there.

1. Find where your tool looks for commands or context
2. Copy our command files there, adjusting the format as needed

The command files simply point to the instructions and standards located in your `~/.agent-os/` installation.

### Working with Existing Codebases

Already have a product in development? Agent OS works great with existing code:

1. Complete steps 1 and 2 above for your tool
2. Run the `@analyze-product` command:

```
@analyze-product

I want to install Agent OS in my existing codebase
```

This will analyze your codebase, understand what's already built, and create Agent OS documentation that reflects your actual implementation.

### What Gets Installed Where?

After installation, you'll have:

**Base Installation:**
```
~/.agent-os/
├── standards/
│   ├── tech-stack.md         # Your default tech choices
│   ├── code-style.md         # Your formatting preferences
│   ├── best-practices.md     # Your development philosophy
│   └── code-style/           # Python-specific style guides
│       ├── python-style.md
│       ├── fastapi-style.md
│       ├── pocketflow-style.md
│       └── testing-style.md
└── instructions/
    ├── plan-product.md       # Agent's instructions to initialize a product
    ├── create-spec.md        # Agent's instructions to plan features
    ├── execute-tasks.md      # Agent's instructions to coordinate task execution
    ├── execute-task.md       # Agent's instructions to execute individual tasks
    └── analyze-product.md    # Agent's instructions to add to existing code
```

**Claude Code Addition:**
```
~/.claude/
├── CLAUDE.md                # Points to your default preferences
├── commands/
│   ├── plan-product.md      # → points to ~/.agent-os/instructions/
│   ├── create-spec.md       # → points to ~/.agent-os/instructions/
│   ├── execute-tasks.md     # → points to ~/.agent-os/instructions/
│   └── analyze-product.md   # → points to ~/.agent-os/instructions/
└── agents/                  # (Optional) Specialized agents for enhanced performance
    ├── context-fetcher.md
    ├── date-checker.md
    ├── file-creator.md
    ├── git-workflow.md
    └── test-runner.md

your-product/
├── .claude/
│   └── CLAUDE.md          # Points to project details and instructions
└── .agent-os/
    ├── product/           # Created by plan-product
    └── specs/             # Created by create-spec
```

**Cursor Addition (Per Project):**
```
your-product/
├── .cursor/
│   └── rules/
│       ├── plan-product.mdc       # → points to ~/.agent-os/instructions/
│       ├── create-spec.mdc        # → points to ~/.agent-os/instructions/
│       ├── execute-tasks.mdc      # → points to ~/.agent-os/instructions/
│       └── analyze-product.mdc    # → points to ~/.agent-os/instructions/
├── .agent-os/
│   ├── product/                   # Created by plan-product
│   └── specs/                     # Created by create-spec
└──CLAUDE.md                       # If also using Claude Code
```

---

## Using Agent OS

With Agent OS installed, you're ready to supercharge your AI coding workflow. Here's how to use each part:

### Setting Your Standards

Before starting any project, customize your global standards to match how you like to build. Your agent will reference these standards constantly when planning projects and writing code, so make them reflect your actual preferences:

**Edit your tech stack** (`~/.agent-os/standards/tech-stack.md`):
- Set your preferred frameworks and versions
- Define default database choices
- Specify hosting preferences

**Edit your code style** (`~/.agent-os/standards/code-style.md`):
- Indentation preferences (spaces vs tabs, how many)
- Naming conventions (camelCase vs snake_case)
- File organization patterns

**Edit your best practices** (`~/.agent-os/standards/best-practices.md`):
- Testing philosophy (TDD? Integration first?)
- Performance vs readability trade-offs
- Security considerations

💡 **Pro tip:** Be opinionated! The more specific your standards, the more consistent your agent's output.

### Starting a New Product

When beginning a fresh codebase, you can provide as much or as little detail as you want—though more detail leads to better results by using the `@plan-product` command.

```
@plan-product

I want to build a SaaS tool for tracking customer feedback
Key features: feedback collection, sentiment analysis, reporting dashboard
Target users: Product managers at B2B SaaS companies
Tech stack: Use my defaults
```

**Note:** When starting a new product, feel free to provide as much or as little detail in your initial prompt. You can even invoke the `@plan-product` command with no other details and your agent will then prompt you for the specific details it needs to get started on your product's plan and roadmap.

Once your agent has collected the basic details it needs, it will:
- ✅ Create `.agent-os/product/` structure
- ✅ Generate mission.md with product vision
- ✅ Create a 5-phase roadmap
- ✅ Document all technical decisions
- ✅ Set up your preferred tech stack

**Behind the scenes:** Agent OS uses 5 specialized instruction files to guide this process: plan-product, create-spec, execute-tasks, execute-task, and analyze-product.

**Important:** Review and edit the generated documentation to ensure it accurately reflects your vision and goals.

### Adding Agent OS to Existing Products

Have an existing codebase? No problem. Use the `@analyze-product` command to install Agent OS into your existing codebase.

```
@analyze-product

I want to install Agent OS in my existing codebase
```

Your agent will:
- 🔍 Analyze your current code structure
- 📊 Detect your tech stack and patterns
- 📝 Create documentation reflecting what's already built
- ✅ Add completed features to "Phase 0" in the roadmap

**Important:** Review the generated documentation carefully—your agent's analysis might miss nuances or business context that only you know.

### Planning a Feature

Ready to build something new? You have two options:

**Option 1: Ask "what's next?"**
Your agent should automatically trigger the `@create-spec` command, check your product's roadmap.md file, and suggest the next uncompleted feature. You can confirm or adjust the feature before proceeding.

**Option 2: Request a specific feature**
Use the `@create-spec` command along with your instructions or request for a new feature or task.

```
@create-spec

Let's add user authentication with email/password and OAuth
```

Either way, your agent will:
- 📋 Create a Spec Requirements Document (SRD)
- 🔧 Write technical specifications
- 💾 Design database schemas (if needed)
- 🔌 Document API endpoints (if needed)
- ✅ Break down work into ordered tasks

**Important:** This is the most critical review point! Carefully examine the SRD, specs, and especially the task breakdown. Adjust anything that doesn't match your expectations before proceeding.

Specs live in: `.agent-os/specs/2025-07-16-user-authentication/`

### Executing Tasks

Time to code! Start building:

```
@execute-task

Work on the next task in the user authentication project
```

By default, your agent will complete one parent task and all its sub-tasks. You can adjust this:
- **More work:** "Complete tasks 1 and 2 with all sub-tasks"
- **Less work:** "Just do task 1.1 and 1.2"
- **Specific task:** "Work on task 3: API endpoints"

Your agent will:
- 📝 Follow your coding standards exactly
- 🧪 Write tests first (if that's your style)
- 💾 Commit with clear messages
- ✅ Update task progress as it goes
- 🔊 Play a sound when done

**Important:** While agents are great at following patterns, always review the code for business logic accuracy and edge cases before merging.

**Performance tip:** Agent OS uses smart context loading—your agent only reads what's needed for the current task, resulting in faster responses and better focus.

### Workflow Examples

**Example 1: Monday Morning**
```
What's next on the roadmap?
```
Your agent checks `.agent-os/product/roadmap.md` and suggests the next uncompleted feature.

**Example 2: Quick Bug Fix**
```
@create-spec

Users report the dashboard is slow when filtering by date
```
Even for bug fixes, your agent creates a mini-spec with clear tasks.

**Example 3: Continuing Work**
```
@execute-task

Continue where we left off yesterday
```
Your agent reads the task list and picks up exactly where it stopped.

---

## Refining Your Agent OS

Agent OS gets better with use. Each spec teaches you something about your process, your preferences, and how to better guide your AI agents. Here's how to continuously improve your setup.

### The Refinement Loop

After each feature or spec, ask yourself:

1. **What worked well?** - Patterns to document and repeat
2. **What needed correction?** - Gaps in your standards or instructions
3. **What surprised you?** - Unexpected approaches that might be worth adopting

### Common Refinements

**After Your First Project:**
- Add specific examples to code-style.md based on actual code
- Update best-practices.md with patterns you had to correct
- Clarify any tech stack choices that caused confusion

**After Code Reviews:**
- Notice yourself making the same corrections? Add them to standards
- Find a pattern you love? Document it so agents use it consistently
- Spot anti-patterns? Add them to best-practices.md with clear "don't do this" examples

**After Team Feedback:**
- Incorporate team preferences into your standards
- Add team-specific workflows to best-practices.md
- Document naming conventions everyone agrees on

### Where to Make Updates

**Standards Files** *(Global - affects all specs)*
- `tech-stack.md` - New tool preferences, version updates
- `code-style.md` - Formatting patterns, naming conventions
- `best-practices.md` - Development philosophy, patterns to follow/avoid

**Code Style Organization** *(For Python-specific rules)*
- Create separate files in `~/.agent-os/standards/code-style/` for each technology
- Examples: `python-style.md`, `fastapi-style.md`, `pocketflow-style.md`, `testing-style.md`
- Reference them conditionally in your main `code-style.md` file
- This keeps context lean—agents only load styles relevant to current work

**Product Files** *(Product-specific)*
- `roadmap.md` - Adjust phases based on learnings
- `decisions.md` - Document why certain approaches work (or don't)
- `tech-stack.md` - Override global standards when needed

### Making Refinements Stick

**Be Specific:**
- ❌ "Write better tests"
- ✅ "Write integration tests first, then unit tests. Mock external services using [specific pattern]"

**Show, Don't Just Tell:**
- Include code examples in your standards
- Show both good and bad patterns
- Explain why one approach is preferred

**Version Your Changes:**
- Update version numbers when making significant changes
- Keep a brief changelog at the bottom of modified files
- This helps track what changed and when

### Team Refinement

If working with a team:

1. **Schedule Regular Reviews** - Monthly or after major features
2. **Collect Patterns** - What is everyone correcting in code reviews?
3. **Reach Consensus** - Agree on patterns before adding to standards
4. **Share Updates** - Ensure everyone updates their local Agent OS files

### Signs You Need Refinement

- You're making the same corrections repeatedly
- Agents consistently miss certain patterns
- Code reviews reveal style inconsistencies
- New team members point out unclear conventions
- You discover better patterns worth standardizing

### The Long Game

Remember: Agent OS is a living system. The goal isn't perfection on day one—it's continuous improvement. Each refinement makes your agents more effective and your codebase more consistent.

Your Agent OS a year from now will be dramatically better than today's, shaped by real experience and tailored to exactly how you and your team work best.

---

## Best Practices

While Agent OS's task execution process automatically updates your roadmap and prompts for decision updates, it's good practice to regularly:

1. **Review and refine your standards** - As you see patterns in code reviews, update your standards files
2. **Regularly review roadmap.md** - Ensure it reflects actual progress and priorities
3. **Update decisions.md** - Document important choices that affect future development
4. **Refine best-practices.md** - Add patterns that help your agent think like you think

Regular maintenance keeps your Agent OS aligned with your evolving project and team needs.

### Tips for Success

**Review Plans Carefully:**
- The planning phase is crucial—invest time here to save time later
- Review the PRD and task breakdown before execution
- Ask your agent to adjust plans if something doesn't look right
- Ensure you're aligned on the approach before coding begins

**Start Small:**
- Don't try to document everything at once
- Begin with basic standards, refine as you go

**Be Specific:**
- "Use PostgreSQL" → "Use PostgreSQL 15+ with schemas for multi-tenancy"
- "Write tests" → "Write unit tests first, aim for 80% coverage"

**Trust the Process:**
- Let your agent own entire features, not just snippets
- Review and refine rather than micromanage

**Know When to Start Fresh:**
- Not happy with the implementation? It's often better to revert and redo with better planning
- Don't ask your agent to fix incorrectly implemented code—start clean with refined specs
- A clear redo usually beats incremental fixes

### Troubleshooting

**Agent not following your style?**
- Check your standards files are specific enough
- Add examples to code-style.md
- Update best-practices.md with clear dos and don'ts

**Tasks too big or too small?**
- This is a planning issue—catch it early!
- During create-spec, review the task breakdown carefully
- Ask your agent to adjust: "Can you break task 3 into smaller sub-tasks?"
- Or: "Tasks 2 and 3 should be combined"

**Wrong technical approach?**
- Review technical specs during the planning phase
- Don't wait until code is written to course-correct
- Say: "I'd prefer we use [different approach] for this"
- Update tech-stack.md, decisions.md, or best-practices.md to prevent future issues
- Best-practices.md is especially important—it teaches your agent to think like you

**Remember:** The best time to fix issues is during planning, not after code is written!

---

## FAQ

### What is Agent OS?

Agent OS is a system for better planning and executing software development tasks with your AI agents. It consists of a set of finely tuned instructions, commands, and specs that you and your team can dial in to ensure your agents build the right things, the right way— your way.

Agent OS is free and open source, created by Brian Casel, the creator of Builder Methods.

### What makes Agent OS different?

Agent OS goes a few steps further than surface-level commands and project notes. There are 3 specific ways Agent OS is different:

- Enhanced Context
- Task & Roadmap Management
- Customizability

### What is 'spec-driven development'?

Spec-driven development is a software development methodology that emphasizes the use of specifications to guide the development process—particularly in the age of building with AI coding agents.

It is a way to ensure that the software is built the right way— your way.

### Is Agent OS free?

Agent OS is free and open source and released under the MIT license.

### Who created Agent OS?

Agent OS is free and open source, created by Brian Casel.

I'm the creator of Builder Methods, where I teach fellow software designers and developers how to leverage AI to build better products, faster. Get my free Builder Briefing newsletter to get my latest insights and updates to help you grow as a professional in the age of building with AI.

You can subscribe to my YouTube channel, and connect with me on X, Bluesky.

### What's Builder Methods?

Builder Methods, is where I (Brian Casel) teach fellow software designers and developers how to leverage AI to build better products, faster. Get my free Builder Briefing newsletter to get my latest insights and updates to help you grow as a professional in the age of building with AI.

### How does Agent OS manage context efficiently?

Agent OS uses smart context management to optimize your agent's performance:

- **Conditional Loading:** Files are only loaded when needed for the current task
- **Lite Files:** Condensed versions of mission and spec documents for efficient AI context usage
- **Context-Aware Instructions:** Standards only load relevant sections based on what you're building
- **60-80% Context Reduction:** Compared to loading everything upfront

This means faster responses, better focus on the task at hand, and the ability to work with larger codebases without hitting context limits.

### Does Agent OS support Claude Code's specialized agents?

Yes! If you're using Claude Code, Agent OS automatically detects and uses specialized subagents for better performance:

- **test-runner:** Runs and analyzes test failures
- **context-fetcher:** Efficiently retrieves relevant documentation
- **git-workflow:** Handles branches, commits, and pull requests
- **file-creator:** Creates multiple files and directories in batch

These agents work seamlessly with Agent OS instructions, providing faster and more reliable execution while maintaining full compatibility for users of other AI tools.

### I don't use Claude Code or Cursor. Can I still use Agent OS?

Absolutely!

Agent OS can be installed and adapted no matter which AI coding tool(s) you use. See the section on installing Agent OS in your tools for more details.

### Is support or coaching available for me or my team?

Yes — Coaching and courses for teams and individuals looking to get the most out of Agent OS, taught by me, Brian Casel (the creator of Agent OS).

Click here to learn more and inquire.

### How can I learn more about building with AI?

My best free training and resources are available through my Builder Briefing newsletter. You can also subscribe to my YouTube channel where I regularly release build-with-AI tutorials.

You'll also find just-in-time courses and coaching packages available from Builder Methods.

---

*© 2025 CasJam Media, LLC / Builder Methods*

*Training for pro software developers building with AI.*

*Created by Brian Casel (that's me). I'm a career software developer, founder, and creator of Builder Methods and the Agent OS system for building with AI.*