# Vibe-Coding-Methodology

更新时间: 2026-03-01

## 说明

- 你提到的 "opensec" 这里按 "OpenSpec" 处理。
- 本文档说明两件事:
  1) 你的 Pack 方案如何和 OpenSpec 结合
  2) 我已经在仓库里具体新增了什么

## 总体思路: OpenSpec 管规划, Pack 管执行

建议采用双层流程:

1. 规划层 (OpenSpec)
- 负责变更提案、规格、任务拆解
- 典型流程: `/openspec:propose -> /openspec:continue -> tasks.md`

2. 执行层 (Pack)
- 负责单次任务落地约束和质量护栏
- 核心护栏:
  - 仅改 scope 白名单文件
  - 不改 public interface (除非明确允许)
  - 必须有验证命令和回滚方案
  - 输出 diff + 回归清单 + 风险

一句话:
- OpenSpec 回答 "做什么"
- Pack 回答 "这次怎么做才稳"

## 我已经完成的改动

已新增目录:
- `.pack/`
- `scripts/pack/`

已新增文件:

1. Pack 文档与命令定义
- `.pack/README.md`
- `.pack/commands/pack-create.md`
- `.pack/commands/pack-check.md`
- `.pack/commands/pack-apply.md`
- `.pack/commands/pack-verify.md`
- `.pack/commands/pack-close.md`

2. Pack 模板与 Schema
- `.pack/templates/pack-lite.yaml`
- `.pack/templates/pack-full.yaml`
- `.pack/schemas/pack.schema.json`

3. 自动化脚本
- `scripts/pack/build_pack.py`
  - 从模板生成 pack 文件
- `scripts/pack/validate_pack.py`
  - 检查 pack 必填字段是否完整
- `scripts/pack/enforce_scope.py`
  - 基于 git diff 检查是否越界改动

## 如何和 OpenSpec 结合 (落地步骤)

Step 0: 准备
- 你的项目需要是 git 仓库 (scope 校验依赖 git diff)
- 需要 Python 3 运行脚本

Step 1: 用 OpenSpec 产出任务
- `/openspec:propose <change-name>`
- `/openspec:continue <change-name>`
- 得到: `openspec/changes/<change-name>/tasks.md`

Step 2: 基于任务创建 Pack
- 每个 task 生成一个 pack (或一组强相关 task 一个 pack)
- 示例命令:

```bash
py -3 scripts/pack/build_pack.py --change <change-name> --task-id <Txxx> --spec-ref docs/specs/<module>/<feature>.spec.md --mode full
```

Step 3: 执行前闸门
- 校验 pack:

```bash
py -3 scripts/pack/validate_pack.py <pack-file>
```

- 不通过则先补齐字段再执行

Step 4: 按 Pack 实施
- 人工/Agent 按 pack 的 `scope + constraints` 改代码
- 改完立即做越界检查:

```bash
py -3 scripts/pack/enforce_scope.py <pack-file> --repo .
```

Step 5: 验证与回写
- 按 `pack.verification_commands` 验证
- 输出 AC 结果、风险、回滚信息
- 回写到变更记录后走:
  - `/openspec:verify <change-name>`
  - `/openspec:archive <change-name>`

## 命令映射建议

可约定以下逻辑命令 (当前是文档/脚本骨架, 非 OpenSpec 内置命令):

- `/pack:create`  -> `scripts/pack/build_pack.py`
- `/pack:check`   -> `scripts/pack/validate_pack.py`
- `/pack:apply`   -> Agent 按 pack 执行改动
- `/pack:verify`  -> 执行 verification_commands + AC 对照
- `/pack:close`   -> 回写执行记录并标记完成

推荐执行顺序:

1. `/openspec:continue`
2. `/pack:create`
3. `/pack:check`
4. `/pack:apply`
5. `/pack:verify`
6. `/pack:close`
7. `/openspec:archive`

## 当前环境注意事项

我在这台机器检测到:

1. Python 3 不可用 (仅检测到 Python 2.7)
- 结果: `scripts/pack/*.py` 目前无法直接执行
- 建议: 安装 Python 3 后再运行脚本

2. 当前示例目录不是 git 仓库
- 结果: `enforce_scope.py` 无法做有效的 diff 越界检查
- 建议: 在真实项目仓库中使用这套流程

## 建议下一步

1. 先在真实业务仓库复制 `.pack + scripts/pack`
2. 安装 Python 3
3. 跑一个最小闭环:
   - OpenSpec 产出一个 change/tasks
   - 生成一个 full pack
   - 校验 + 实施 + scope 检查 + 验证 + 回写
4. 通过后再把 `/pack:*` 映射为你常用 Agent 的 prompt 命令
