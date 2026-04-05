# Install Agent Skills for Claude Code

## Preferred

```bash
npx skills add gigio1023/agent-skills --skill skill-builder --agent claude-code
```

Replace `skill-builder` with the skill you want.

## Manual install

```bash
git clone https://github.com/gigio1023/agent-skills.git ~/.claude/agent-skills
mkdir -p ~/.claude/skills
cp -R ~/.claude/agent-skills/skills/development/skill-builder ~/.claude/skills/
```

Restart Claude Code after copying.
