# Install Agent Skills for Codex

## Preferred

```bash
npx skills add gigio1023/agent-skills --skill skill-builder --agent codex
```

Replace `skill-builder` with the skill you want, or repeat `--skill` for multiple skills.

## Manual install

1. Clone the repo:

```bash
mkdir -p ~/.local/share
git clone https://github.com/gigio1023/agent-skills.git ~/.local/share/agent-skills
```

2. Copy or symlink the specific skill you want into `~/.agents/skills/`.

Example:

```bash
mkdir -p ~/.agents/skills
cp -R ~/.local/share/agent-skills/skills/development/skill-builder ~/.agents/skills/
```

Or symlink it:

```bash
mkdir -p ~/.agents/skills
ln -s ~/.local/share/agent-skills/skills/development/skill-builder ~/.agents/skills/skill-builder
```

3. Restart Codex.
