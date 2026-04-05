# Install Agent Skills for Gemini CLI

## Preferred

```bash
npx skills add gigio1023/agent-skills --skill skill-builder --agent gemini-cli
```

## Manual install

```bash
git clone https://github.com/gigio1023/agent-skills.git ~/.gemini/agent-skills
mkdir -p ~/.gemini/skills
cp -R ~/.gemini/agent-skills/skills/development/skill-builder ~/.gemini/skills/
```

Restart Gemini CLI after copying.
