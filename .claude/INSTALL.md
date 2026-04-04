# Install Agent Skills for Claude Code

## Preferred

```bash
npx skills add gigio1023/agent-skills --skill unity-dev --agent claude-code
```

Replace `unity-dev` with the skill you want.

## Manual install

```bash
git clone https://github.com/gigio1023/agent-skills.git ~/.claude/agent-skills
mkdir -p ~/.claude/skills
cp -R ~/.claude/agent-skills/skills/development/unity-dev ~/.claude/skills/
```

Restart Claude Code after copying.
