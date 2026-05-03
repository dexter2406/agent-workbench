# Third-party Skills

| Skill | 来源平台 | 安装命令 | 状态 |
|-------|----------|----------|------|
| frontend-design | `anthropics` | `npx skills add anthropics/skills@frontend-design -g -y` | ✅ 已装 |
| skill-creator | `anthropics` | — | ✅ 已装 |
| grill-me | `mattpocock` | `npx skills add mattpocock/skills@grill-me -g -y` | ✅ 已装 |
| to-prd | `mattpocock` | `npx skills add mattpocock/skills@to-prd -g -y` | ✅ 已装 |
| vercel-react-best-practices | `vercel-labs` | `npx skills add vercel-labs/agent-skills@vercel-react-best-practices -g -y` | ✅ 已装 |
| find-skills | `vercel-labs` | `npx skills add vercel-labs/skills@find-skills -g -y` | ✅ 已装 |
| powershell-windows | `davila7` | `npx skills add davila7/claude-code-templates@powershell-windows -g -y` | ✅ 已装 |
| continuous-learning | `affaan-m` | — | ✅ 已装 |
| api-integration-builder | `daffy0208` | `npx skills add daffy0208/ai-dev-standards@api-integration-builder -g -y` | ✅ 已装 |
| code-review | `supercent-io` | `npx skills add supercent-io/skills-template@code-review -g -y` | ✅ 已装 |
| git-workflow | `supercent-io` | `npx skills add supercent-io/skills-template@git-workflow -g -y` | ✅ 已装 |
| documentation-generator | `jorgealves` | `npx skills add jorgealves/agent_skills@documentation-generator -g -y` | ✅ 已装 |
| prompt-optimizer | `daymade` | `npx skills add daymade/claude-code-skills@prompt-optimizer -g -y` | ✅ 已装 |
| test-generator | `oimiragieo` | `npx skills add oimiragieo/agent-studio@test-generator -g -y` | ✅ 已装 |

## 说明
- 所有第三方 skills 均 vendor 到 `skills/` 目录，通过整目录 junction 对所有宿主可见
- 安装命令详见 `registry/skills.lock.json`；根目录 `skills-lock.json` 由 npx 自动维护，为安装来源的权威记录
- ✅ 已装：当前机器上已可用；⬜ 未装：已登记但未检测到
- 自建 skills 不登记在此


