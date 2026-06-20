# China Stock Market Pro

中国市场一站式股票分析工具 — 覆盖 A 股（沪深）、港股、美股中概，适合新手入门。

## 功能一览

| 功能 | 命令 | 说明 |
|------|------|------|
| 实时报价 | `cnstock price 600519` | 当前价、涨跌幅、日内最高最低 |
| 专业图表 | `cnstock chart 600519 3mo` | 蜡烛图/折线图 + 均线 + 成交量 |
| 多股对比 🆕 | `cnstock compare 600519 000858` | 归一化百分比走势，一张图对比多只股票 |
| 基本面分析 | `cnstock fundamentals 600519` | PE/PB/EPS/ROE/利润率，附带新手解释 |
| 财报日历 | `cnstock earnings 600519` | 下次财报日期 + 分析师一致预期 |
| 历史趋势 | `cnstock history 600519` | 近 10 个交易日 ASCII 趋势图 |
| 组合管理 | `portfolio.py create/add/show/remove` | 创建组合、增删持仓、实时盈亏 |

## 快速开始

```bash
# A股报价（贵州茅台）
uv run scripts/cnstock price 600519

# 港股报价（腾讯）
uv run scripts/cnstock price 00700.HK

# 美股报价（苹果）
uv run scripts/cnstock price AAPL

# 6个月K线图
uv run scripts/cnstock chart 600519 6mo

# 基本面分析
uv run scripts/cnstock fundamentals 600519

# 折线图
uv run scripts/cnstock chart 600519 1y line

# 多股走势对比 🆕
uv run scripts/cnstock compare 600519 000858 000568 --period 6mo
```

## 组合管理

```bash
uv run scripts/portfolio.py create "我的组合"
uv run scripts/portfolio.py add 600519 --name "贵州茅台" --quantity 100 --cost 1850
uv run scripts/portfolio.py add 00700.HK --name "腾讯" --quantity 200 --cost 380
uv run scripts/portfolio.py show
```

## 数据源

| 市场 | 数据源 | 需要 API Key |
|------|--------|-------------|
| A股（沪/深） | AKShare | ❌ 不需要 |
| 港股 | Yahoo Finance / AKShare | ❌ 不需要 |
| 美股 | Yahoo Finance | ❌ 不需要 |
| 加密货币 | Yahoo Finance | ❌ 不需要 |

## 系统要求

- Python 3.11+
- `uv` 包管理器（自动处理依赖）

## 免责声明

本工具仅提供数据展示和指标解释，**不构成任何投资建议**。所有投资决策请自行判断，或咨询持牌投资顾问。
