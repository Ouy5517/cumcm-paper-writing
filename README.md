# CUMCM 国赛建模与论文工作流

面向全国大学生数学建模竞赛（CUMCM）的 Codex skill：从读题、数据或参数审计、模型建立与求解，到结果验证、中文论文写作、排版和提交检查，按实际任务调用相应流程。

**当前版本：3.1.0** · **14 类任务** · **8 类模型族** · **6 组来源案例、47 条条件规则**

[快速开始](#快速开始) · [使用示例](#使用示例) · [完整工作流](#完整工作流) · [案例蒸馏](#案例蒸馏) · [开发与验证](#开发与验证) · [版本记录](CHANGELOG.md)

本项目是一套指令、参考资料和辅助脚本。模型计算由运行 skill 的代理结合题目和可用工具完成；仓库没有预装所有题型的求解器。既可以从原题开始，也可以接着已有代码、结果或论文继续工作。

## 快速开始

### 1. 安装

在支持 skill 的 Codex 环境中，可向内置安装器发送：

```text
使用 $skill-installer 安装 https://github.com/Ouy5517/cumcm-paper-writing。
SKILL.md 位于仓库根目录，技能名称为 cumcm-paper-writing。
```

安装器应选择仓库根路径 `.` 并保留该名称。若同名技能已存在，先保留自己的修改，再更新原安装位置，避免重复安装。

也可以手动克隆到个人技能目录。以下两组命令任选与你的系统对应的一组，只用于首次安装。

**Windows PowerShell：**

```powershell
$skillRoot = Join-Path $HOME '.agents/skills'
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
git clone https://github.com/Ouy5517/cumcm-paper-writing.git (Join-Path $skillRoot 'cumcm-paper-writing')
```

**macOS / Linux：**

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/Ouy5517/cumcm-paper-writing.git "$HOME/.agents/skills/cumcm-paper-writing"
```

项目内共享时可改用 `.agents/skills/cumcm-paper-writing/`。上述手动路径依据 [OpenAI 技能文档](https://learn.chatgpt.com/docs/build-skills)；由安装器管理的路径可能不同，应以其实际输出为准。已有 `.codex/skills/cumcm-paper-writing/` 安装可继续在原位置维护，无需为了此示例再克隆一份。

安装后发送下一条任务并选择该技能；若没有出现，重启 Codex 后检查。Git 克隆安装可在对应技能目录执行 `git status`，确认自己的改动已妥善保存后执行 `git pull --ff-only`。非 Git 安装则使用安装器更新，不直接套用 Git 命令。

### 2. 提供材料与目标

| 材料 | 建议提供的内容 |
|---|---|
| 题目 | 完整题面、竞赛年份、题号及需要回答的小问 |
| 输入 | 原始附件；无附件题提供给定参数、图像、几何条件或解析条件 |
| 已有进展 | 代码、运行结果、图表或论文草稿，说明希望从哪一步继续 |
| 交付目标 | 只分析、只计算、局部写作、完整论文，或需要 PDF / DOCX / 提交包 |
| 实际约束 | 截止时间、可用软件、算力限制，以及已有官方通知和模板 |

有多少材料就先提供多少。局部润色通常只需原文与相关事实；缺少某问的数据时，其他可独立推进的小问仍可继续。

### 3. 发出第一条任务

```text
使用 $cumcm-paper-writing，读取项目内的原题和附件，完成国赛建模、
求解、验证及论文初稿。先逐问梳理输出要求，建立可计算的基线，
再根据验证结果改进。记录真实执行结果，不补造缺失数值。
```

这些提示词在 Codex 中使用，不是在终端执行的命令。普通中文描述也可用于匹配任务；显式写出技能名称更便于明确调用。

## 使用示例

**只读题与选模型：**

```text
使用 $cumcm-paper-writing，只分析附件中的赛题。
逐问列出输入、所求量、约束和依赖，比较可行模型路线，
说明每条路线需要的数据与验证方法，暂不写论文正文。
```

**接着已有代码求解和验证：**

```text
使用 $cumcm-paper-writing，检查 src 中已有实现与原题是否一致，
运行可执行部分，核对导出方案的约束和单位。
保留已验证结果，修复受影响的小问，并给出可复算入口。
```

**只写结果章节：**

```text
使用 $cumcm-paper-writing，依据 results 中的真实输出写“模型求解与结果”。
每问将方法、结果和检验接起来，图表注明口径；
尚未验证的结论保持条件性，不补写不存在的实验成绩。
```

**局部润色：**

```text
使用 $cumcm-paper-writing，只润色下面这一段，保留数字、符号和结论强度。
不要扩写全文，也不要重做建模流程：
[粘贴原文]
```

**排版与提交前检查：**

```text
使用 $cumcm-paper-writing，依据提供的当年官方通知与模板检查论文和附件。
核对题目覆盖、结果一致性、引用、匿名、排版及支持文件。
分别报告科学验证、渲染检查、规则核验和队员人工复核状态。
```

## 完整工作流

每问分别记录进度，按当前已验证的状态继续。阶段之间按需要推进；若发现错误，只返回受影响的部分。

| 阶段 | 主要工作 | 进入下一步所需的依据 |
|---|---|---|
| 读题 | 拆解小问、所求量、约束和相互依赖 | 每个要求都有对应输出 |
| 输入审计 | 核对数据粒度、主键、单位、参数、缺失及时间口径 | 输入可用，或明确缺口和条件 |
| 建模 | 定义变量、假设、目标、约束及模型接口 | 模型能回答题目，所需信息有来源 |
| 求解 | 先做手算、枚举或简单基线，再按需要改进 | 实际运行记录或可检查的推导 |
| 验证 | 选择适用的约束、误差、回测、收敛或敏感性检查 | 结论强度与证据相符 |
| 写作 | 组织各问论证、公式、结果和图表，最后稳定摘要 | 正文数字与结果来源一致 |
| 渲染 | 使用合适的文档工具或 LaTeX，检查实际输出 | 公式、引用、字体及版式已检查 |
| 交付 | 按所选年份已核验规则整理论文和支持材料 | 科学、格式、规则与人工复核分别报告 |

无附件题可以使用参数、边界条件和解析推导。确定性计算不机械要求随机种子或重复抽样；时间序列、动态曲线和事件调度分别使用相应的时间检查。仅要求计算时，到求解与验证结束；仅要求局部编辑时，不强制执行全流程。

### 可单独调用的任务

| 用途 | 任务名称 |
|---|---|
| 端到端推进 | `full-workflow` |
| 读题、输入、建模、计算、验证 | `understand`、`prepare-inputs`、`formulate`、`solve`、`validate` |
| 写作规划、章节或全文初稿 | `plan`、`draft-section`、`draft-paper` |
| 润色、结构调整、审查 | `polish`、`restructure`、`audit` |
| 提交前检查、打包 | `preflight`、`submission-package` |

这些名称是内部路由标识，日常使用可以直接描述任务。`plan` 对应写作规划，数学问题的初步拆解使用 `understand`。

### 模型、章节与交付范围

| 维度 | 已实现的范围 |
|---|---|
| 模型族（8 类） | 评价、预测、优化、机理、仿真、统计推断、几何、混合模型 |
| 章节（10 类） | 摘要、问题分析、假设与符号、模型建立、求解结果、检验与敏感性、模型评价、结论、参考文献、附录 |
| 交付（5 类） | 可编辑源文件、渲染文档、电子提交包、纸质提交包、两类提交包 |

混合模型需要存在实际的输入输出耦合；多个互不依赖的模型不会仅因数量多就被归入混合模型。新题即使没有匹配的历史案例，也可以使用通用流程。

### 会交付什么

按请求返回计算或推导、真实结果、相应检验、论文内容和必要文件，并说明哪些步骤实际运行、哪些仅做了检查、哪些仍待验证。局部编辑只返回修改内容及必要说明。

提交检查使用 `ready`、`ready_with_author_checks` 或 `blocked` 状态，同时分开记录题目覆盖、科学验证、渲染、提交规则和队员人工复核。成功编译 PDF 不等于模型正确或已满足全部参赛要求。详细约定见 [输出契约](static/core/output-format.md)。

## 案例蒸馏

这里的“蒸馏”是从题面、作品及可核对材料中提炼操作规则，再写入 skill；不涉及模型参数训练，也不把历史论文当作新题的标准答案。

| 来源题目 | 条数 | 重点提炼内容 |
|---|---:|---|
| [2023A 定日镜](references/cases/solar-2023a.md) | 7 | 坐标与单位链、布局约束、随机评价、导出方案复检 |
| [2022C 玻璃成分](references/cases/glass-2022c.md) | 8 | 实体与测点、成分数据、零值、分类验证和结果口径 |
| [2024B 生产决策](references/cases/production-2024b.md) | 8 | 抽样与决策、物料和现金守恒、拆解返工、结果一致性 |
| [2020A 炉温曲线](references/cases/thermal-2020a.md) | 8 | PDE/ODE 假设、观测起点、阈值事件、标定与验证 |
| [2018B RGV 调度](references/cases/rgv-2018b.md) | 8 | 状态与事件、资源互斥、多工序、班次首尾和指标解释 |
| [2023C 蔬菜定价补货](references/cases/vegetables-2023c.md) | 8 | 信息可获得时间、回测、销量与需求、价格和补货接口 |

第二波来自 [CUMCM-Archive 固定版本](https://github.com/yushugulao/CUMCM-Archive/tree/ef5fa17360e7ea37547320849eac1469403cda97)，在炉温、RGV、蔬菜三个题组中各选择两篇作品，新增 **24 条规则**。两波共 **47 条案例规则**，共同的检查合并到主流程，具体来源留在案例卡中。

写作经验包括：解释模型选择及其适用域，用流程图或状态图说明过程，让结果表承接约束验证，将代表结果放正文、完整清单放附录，以及把新增数据建议对应到当前模型的缺口。具体操作见 [专项规则入口](references/distilled-playbooks.md)；动态与时序任务另见 [时间与事件检查](references/temporal-validation.md)。

构建参考了 [nature-skills](https://github.com/Yuan1z0825/nature-skills) 的入口、片段和按需资料分层，没有把 Nature 期刊的投稿规范当作国赛要求。固定版本、作品定位及证据等级见 [来源和蒸馏方法](references/distillation-method.md)。

### 证据与使用边界

- 案例卡记录触发条件、操作、验收、失败处理和来源；归档奖项标签未独立认证，不用于证明方法正确。
- 已做的独立数值核验仅支持卡中列出的局部结论；没有完整复现所有历史求解器，也没有证明 skill 能正确解决所有国赛题型或保证获奖。
- 原题、论文、数据、图片、第三方源码及 `distillation/wave*/notes/` 等本地研究记录不随此仓库或安装包分发；公开来源通过案例卡定位。
- 比赛年份由任务确定，不能直接使用当前日历年份。页数、匿名、披露和支持文件要求以所选年份已核验的官方材料为准；模板和优秀论文版式不能代替官方规则。
- 不补造数据、引文、运行记录或队员复核。正式参赛时需核验当年的 AI 使用规定，并由队员实际确认相关工作。

## 环境与文档生成

| 场景 | 所需环境 |
|---|---|
| 读取流程、分析与写作 | 能读取 skill 文件的代理环境 |
| 执行模型和数据分析 | 根据题目选择 Python、MATLAB、R 或其他可用工具及依赖；仓库不统一安装这些求解依赖 |
| 校验本仓库 | Python；开发依赖见 `requirements-dev.txt`，CI 使用 Python 3.12 |
| 生成 LaTeX PDF | Python、XeLaTeX，以及稿件使用的字体、宏包、模板；文献按需使用 BibTeX 或 Biber |
| 生成或检查 DOCX | 宿主环境中可用的文档生成、读取和渲染工具；本仓库未提供独立的 DOCX 构建脚本 |

已有完整 TeX 源文件后，在本仓库根目录运行下例，并把路径替换为自己的稿件路径：

```bash
python scripts/build_pdf.py ./paper/paper.tex --output ./paper/paper.pdf
```

模板位于单独目录时增加 `--template-dir ./template`。脚本默认使用 XeLaTeX，按辅助文件识别 BibTeX / Biber；发现未解决的引用或排版错误时报告失败，成功后才替换目标 PDF。编译后仍需检查实际页面及正文证据。完整操作见 [LaTeX 工作流](references/latex-production-workflow.md)。

## 开发与验证

在仓库根目录运行：

```bash
python -m pip install -r requirements-dev.txt
python -X utf8 scripts/validate_skill.py
python -X utf8 -m unittest discover -s tests -v
```

元数据和路由检查覆盖片段路径、默认值和引用关系；回归检查覆盖工作流约定及 PDF 构建行为。每次推送和拉取请求会触发 [GitHub Actions](https://github.com/Ouy5517/cumcm-paper-writing/actions)。这些工程检查不等于对陌生赛题的求解能力评测。

真实 TeX 集成检查默认跳过。已具备 XeLaTeX、BibTeX 和 Biber 时，可显式开启：

**PowerShell：**

```powershell
$env:CUMCM_RUN_TEX_INTEGRATION = '1'
python -X utf8 -m unittest discover -s tests -p test_build_pdf_integration.py -v
Remove-Item Env:CUMCM_RUN_TEX_INTEGRATION
```

**macOS / Linux：**

```bash
CUMCM_RUN_TEX_INTEGRATION=1 python -X utf8 -m unittest discover -s tests -p test_build_pdf_integration.py -v
```

## 仓库结构与扩充

```text
cumcm-paper-writing/
├── SKILL.md                 # 技能入口、路由与证据要求
├── manifest.yaml            # 任务、交付、章节、模型族映射
├── agents/openai.yaml       # 技能显示信息
├── static/core/             # 共用工作流、输出和术语约定
├── static/fragments/        # 按任务、交付、章节、模型族加载的片段
├── references/              # 按需检查与写作资料
│   └── cases/               # 带来源和边界的案例卡
├── scripts/                 # 元数据校验和 PDF 构建
├── tests/                   # 回归与可选 TeX 集成检查
├── docs/superpowers/        # 历史设计与实施记录
└── CHANGELOG.md             # 版本与迁移记录
```

入口读取共用约定后，只加载当前任务需要的片段与资料。`manifest.yaml` 是本项目的路由映射；各目录的实际职责以 `SKILL.md` 为准。

新增案例时，先检查题面与原始材料，锁定来源版本和页码，区分论文主张、文件事实、独立核验和推广建议，再把可迁移操作归入已有流程。不要仅按算法名称增加空片段。新增路由同步更新 `manifest.yaml` 并执行上述校验；完整方法见 [蒸馏与扩充说明](references/distillation-method.md)。

后续优先补充图像反演、一般网络与路径、无附件解析题，并保留未参与蒸馏的题目做迁移验证。涉及第三方原文、代码或素材时按其各自授权处理；引用上游项目不意味着本仓库继承其许可证。
