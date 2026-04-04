# Install Agent Skills for Codex

## Preferred

```bash
npx skills add gigio1023/agent-skills --skill unity-dev
```

Replace `unity-dev` with the skill you want, or repeat `--skill` for multiple skills.

## Manual install

1. Clone the repo:

```bash
git clone https://github.com/gigio1023/agent-skills.git ~/.codex/agent-skills
```

2. Copy or symlink the specific skill you want into `~/.codex/skills/`.

Example:

```bash
mkdir -p ~/.codex/skills
cp -R ~/.codex/agent-skills/skills/development/unity-dev ~/.codex/skills/
```

Or symlink it:

```bash
mkdir -p ~/.codex/skills
ln -s ~/.codex/agent-skills/skills/development/unity-dev ~/.codex/skills/unity-dev
```

3. Restart Codex.
