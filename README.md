# Agent Skills

AI 코딩 어시스턴트용 커스텀 스킬 모음. 디바이스 이동 시 한꺼번에 설치하기 위한 용도.

## Custom Skills (이 레포에 포함)

| Skill | Category | Description |
|-------|----------|-------------|
| [unity-dev](skills/development/unity-dev/) | Dev | Unity 3D 게임 개발 -- C# 스크립팅, 아키텍처 패턴, 렌더링, NPC AI 등 |
| [skill-builder](skills/development/skill-builder/) | Dev | 에이전트 스킬 설계 및 생성 (SKILL.md + 디렉토리 구조) |
| [x-post](skills/productivity/x-post/) | Productivity | 블로그 홍보용 X (Twitter) 포스트 초안 작성 |
| [pdf-page-count](skills/productivity/pdf-page-count/) | Productivity | PDF 페이지 수 확인 및 페이지 제한 검증 |
| [web-research-audit](skills/productivity/web-research-audit/) | Productivity | 웹 리서치 품질 검증 -- 소스 다양성, 근거 최신성 등 |

```bash
# 설치: 심링크 또는 복사
ln -s "$(pwd)/skills/development/unity-dev" ~/.claude/skills/unity-dev
```

## External Skills (npx skills로 설치)

```bash
# Astro
npx skills add gigio1023/astro-dev-skill@astro-dev

# Obsidian
npx skills add kepano/obsidian-skills@obsidian-bases
npx skills add kepano/obsidian-skills@obsidian-cli
npx skills add kepano/obsidian-skills@obsidian-markdown

# Skill discovery
npx skills add vercel-labs/skills@find-skills
```

| Skill | Source | Description |
|-------|--------|-------------|
| astro-dev | [gigio1023/astro-dev-skill](https://github.com/gigio1023/astro-dev-skill) | Astro 6 개발 패턴 |
| obsidian-bases | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Obsidian Bases (.base) 편집 |
| obsidian-cli | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Obsidian vault CLI 관리 |
| obsidian-markdown | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Obsidian Flavored Markdown |
| find-skills | [vercel-labs/skills](https://github.com/vercel-labs/skills) | 스킬 검색 및 설치 |

## License

Personal use.
