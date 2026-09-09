# CUMCM 国赛建模与论文工作流

A source-grounded workflow from problem interpretation, input audit and model
formulation through computation, validation, Chinese writing and delivery.

Current release: `3.1.0`. See [CHANGELOG.md](CHANGELOG.md) for the upgrade and
migration notes.

## Inputs

Invoke `$cumcm-paper-writing` with the problem, competition year, data, code,
results, requested task and delivery format, plus any official notice or supplied
template. Chinese is the manuscript default; canonical English method names,
mathematics, variables, units, and citations remain intact.

## Supported tasks

`full-workflow`, `understand`, `prepare-inputs`, `formulate`, `solve`, `validate`,
`plan`, `draft-section`, `draft-paper`, `polish`, `restructure`, `audit`,
`preflight`, and `submission-package` are available. Delivery routes cover
source, rendered output, electronic or physical packages, and both packages.

## Authority

Only inspected selected-year official sources establish CUMCM rules. Templates
implement typography; dated summaries, case papers and editorial practices are
guidance. The current calendar year never selects rules;
inspect a year-specific authority before enforcing exact requirements.

## Validation

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_skill.py
```

实际文献编译集成检查需本机具备 XeLaTeX、BibTeX、Biber：

```powershell
$env:CUMCM_RUN_TEX_INTEGRATION = '1'
python -m unittest discover -s tests -p test_build_pdf_integration.py -v
```

## Repository layout

`SKILL.md` defines routing behavior; `manifest.yaml` maps task, delivery,
section, and model-family fragments; `static/` contains shared and routed
instructions; `references/` contains focused CUMCM guidance; `scripts/` and
`tests/` provide validation.

## 案例蒸馏

已整理 2023A 定日镜、2022C 玻璃成分、2024B 生产决策三组案例，形成
带来源、触发条件、检查方法和边界的案例卡，并落实到工作流阶段。
第二波从本地 CUMCM-Archive 选择 2020A 炉温、2018B RGV、2023C 蔬菜
定价补货，每题对照两篇作品，加入动态曲线、事件调度和时序决策的
具体检查，以及模型比较、过程图、结果表和附录组织经验。
第二波新增24条案例规则，两波共6组案例、47条规则；共性检查在主流程
合并，来源和适用范围保留在案例卡中。
阅读 [专项规则入口](references/distilled-playbooks.md) 与
[来源和蒸馏方法](references/distillation-method.md)。
时间相关任务按需读取 [时间与事件检查](references/temporal-validation.md)。

保留 `cumcm-paper-writing` 名称，兼容原触发方式；模型族增加统计推断、
几何两类。按问推进，支持无数据的参数题、解析推导和确定性仿真。
这是一套可扩展工作流，现有案例和局部核验不能证明覆盖所有国赛题型或保证获奖。
原题、论文、第三方源码和本地核验记录保留在研究工作区，不随此仓库或
安装包分发；案例卡提供公开来源、具体页码、核验结果与适用边界。

示例：`使用 $cumcm-paper-writing，从附件原题开始完成国赛建模、求解、
验证和论文初稿；逐问记录结果及适用边界。` 单独给出“只润色这一句”
会走局部编辑，不强制重做全流程。
