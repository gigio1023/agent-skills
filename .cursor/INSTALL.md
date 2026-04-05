# Install Agent Skills for Cursor

## Preferred

```bash
npx skills add gigio1023/agent-skills --skill skill-builder --agent cursor
```

## Manual install

```bash
git clone https://github.com/gigio1023/agent-skills.git ~/.cursor/agent-skills
mkdir -p ~/.cursor/skills
cp -R ~/.cursor/agent-skills/skills/development/skill-builder ~/.cursor/skills/
```

Restart Cursor after copying.
