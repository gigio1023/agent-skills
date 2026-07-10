# Install Agent Skills for Codex

Install only the published `main` version at global scope:

```bash
npx --yes skills add 'gigio1023/agent-skills#main' --skill skill-builder --agent codex --global --yes
```

Replace `skill-builder` with the skill you want, or repeat `--skill` for multiple skills.
Do not install from a checkout, PR branch, or commit SHA.
