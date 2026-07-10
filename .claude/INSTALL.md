# Install Agent Skills for Claude Code

Install only the published `main` version at global scope:

```bash
npx --yes skills add 'gigio1023/agent-skills#main' --skill skill-builder --agent claude-code --global --yes
```

Replace `skill-builder` with the skill you want.
Do not install from a checkout, PR branch, or commit SHA.
