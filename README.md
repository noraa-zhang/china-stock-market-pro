# China Stock Market Pro

> 🤖 **Claude Code Skill** — 中国市场一站式股票分析工具。覆盖 A 股（沪深）、港股、美股、加密货币，专为新手设计，每个指标都附带白话解释。

---

## 💡 核心亮点

> **🆓 零 API Key，开箱即用。** 所有数据源（新浪财经、腾讯财经、Yahoo Finance、AKShare）完全免费，不需要注册任何 API 密钥，无需付费订阅，安装即可获取实时报价。

---

## 📦 安装方式

### 方式一：作为 Claude Code Skill 安装（推荐）

这是本工具的**原生形态**。安装后，在 Claude Code 里直接说话就能查股票，Claude 会自动调用后台脚本并整理成结构化报告。

**Step 1: Clone 到 Claude Code skills 目录**

```bash
git clone https://github.com/noraa-zhang/china-stock-market-pro.git ~/.claude/skills/china-stock-market-pro
```

**Step 2: 安装依赖 (只需 `uv`)**

```bash
# macOS
brew install uv

# 或通过 pip
pip install uv
```

**Step 3: 在 Claude Code 中使用**

```
> 查一下茅台股票
> 对比茅台、五粮液、泸州老窖的走势
> 帮我分析一下 000858 的基本面
```

Claude 会自动识别你的意图：单只查询 → 出综合报告；多只查询 → 问你"对比走势"还是"创建投资组合"。

### 方式二：命令行独立使用

不用 Claude Code 也可以直接跑脚本：

```bash
cd ~/.claude/skills/china-stock-market-pro

# 实时报价
uv run --script scripts/cnstock price 600519

# K线图
uv run --script scripts/cnstock chart AAPL 6mo

# 多股对比图
uv run --script scripts/cnstock compare 600519 000858 000568 --period 6mo

# 基本面分析
uv run --script scripts/cnstock fundamentals 000858

# 投资组合
uv run scripts/portfolio.py create "我的组合"
uv run scripts/portfolio.py add 600519 --name "茅台" --quantity 100 --cost 1850
uv run scripts/portfolio.py show
```

---

## 🔧 兼容性

| 运行环境 | 支持 | 说明 |
|----------|------|------|
| **Claude Code** (CLI) | ✅ | 原生 skill，自动固定模板输出 |
| **Claude Code** (VS Code 扩展) | ✅ | 图表自动弹窗打开 |
| **Claude Code** (JetBrains 扩展) | ✅ | 同上 |
| **Claude Desktop** | ✅ | 作为 MCP 工具或 skill 加载 |
| **Claude Agent SDK** | ✅ | 可作为自定义 skill 集成 |
| **独立命令行** | ✅ | 不依赖 Claude，直接 `uv run` |
| **其他 LLM 工具** (Cursor/Copilot) | ⚠️ | 脚本可直接调用，但无结构化报告模板 |

---

## 🎯 功能一览

| 功能 | 命令 | 说明 |
|------|------|------|
| 实时报价 | `cnstock price 600519` | 当前价、涨跌幅、日内最高最低 |
| 专业图表 | `cnstock chart 600519 3mo` | 蜡烛图/折线图 + MA5/20/60 + 成交量 |
| 多股对比 🆕 | `cnstock compare 600519 000858` | 归一化百分比走势，所有股票叠加在一张图上 |
| 基本面分析 | `cnstock fundamentals 600519` | PE/PB/EPS/ROE/利润率，附带新手白话解释 |
| 财报日历 | `cnstock earnings 600519` | 下次财报日期 + 分析师一致预期 |
| 历史趋势 | `cnstock history 600519` | 近 10 个交易日走势表格 |
| 组合管理 | `portfolio.py create/add/show/remove` | 创建组合、增删持仓、实时盈亏追踪 |

---

## 🌍 市场覆盖

| 市场 | 示例代码 | 数据源 | API Key |
|------|----------|--------|---------|
| A股上海 | `600519` (茅台) | 新浪财经 → 腾讯财经 → baostock → AKShare | **❌ 免费** |
| A股深圳 | `000858` (五粮液) | 同上 | **❌ 免费** |
| 港股 | `00700.HK` (腾讯) | Yahoo Finance / AKShare | **❌ 免费** |
| 美股 | `AAPL`, `TSLA` | Yahoo Finance → Stooq | **❌ 免费** |
| 加密货币 | `BTC-USD`, `ETH-USD` | Yahoo Finance | **❌ 免费** |

> 工具自动识别市场（6位数字=6开头→沪市，0/3开头→深市，.HK→港股），不需要手动加后缀。

---

## 🧠 Skill 智能工作流

| 用户输入 | Claude 行为 |
|----------|-------------|
| "查一下茅台" | 自动拉取 `price` + `fundamentals` + `chart` + `history`，输出固定模板的**综合报告** |
| "对比茅台和五粮液" | 反问"**对比走势**还是**创建投资组合**？" → 对比模式出一张归一化叠加图 + 横向对比表 |
| "创建投资组合" | 引导 `portfolio.py create → add → show` 流程 |

所有输出遵循 [SKILL.md](SKILL.md) 定义的固定模板，包含实时行情表、基本面指标表、走势分析和白话解读。

---

## 🐍 系统要求

- **Python** 3.11+
- **[uv](https://docs.astral.sh/uv/)** 包管理器（一键安装依赖，无需手动 pip install）
- 首次运行自动下载依赖，后续秒启动

---

## ⚠️ 免责声明

本工具仅提供数据展示和指标解释，**不构成任何投资建议**。所有数据来源于公开接口（新浪/腾讯/Yahoo/AKShare），不对准确性做保证。投资决策请以交易所官方数据为准，或咨询持牌投资顾问。
