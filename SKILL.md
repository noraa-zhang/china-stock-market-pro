---
name: china-stock-market-pro
description: Professional stock price tracking, fundamental analysis, and financial reporting tool for beginners. Supports global markets (US, KR, etc.), China A-shares (Shanghai/Shenzhen), Crypto, and Forex with real-time data. Every output follows a fixed structured template (行情→基本面→走势→小白解读). (1) Real-time quotes with multi-source fallback, (2) Valuation metrics explained in plain language (PE, EPS, ROE, PB), (3) Earnings calendar and consensus, (4) High-quality Candlestick & Line charts with technical indicators (MA5/20/60). Designed for retail investors new to financial data — every metric comes with beginner-friendly explanations. Includes documented limitations and error handling strategies.
---

# Stock Market Pro

A beginner-friendly financial analysis tool powered by Yahoo Finance (global markets) and AkShare (China A-shares). Built for people who want to *understand* the numbers, not just see them.

> ⚠️ **Disclaimer**: This tool only provides data and explanations of what the data means. It does not give personalized investment advice or buy/sell recommendations. Always do your own research or consult a licensed advisor before investing.

## Core Features

### 1. Real-time Quotes (`price`)
Get instant price updates and day ranges.
```bash
uv run --script scripts/cnstock price [TICKER]
```
**小白解释**:这个功能就是查"现在这只股票多少钱、今天最高/最低多少钱",相当于你打开股票软件看到的第一屏数字。

### 2. Professional Charts (`chart`)
Generate high-resolution PNG charts with Volume and Moving Averages. **Chart opens automatically** after generation.

```bash
# 蜡烛图（默认近6个月）
uv run --script scripts/cnstock chart 600519

# 指定时间范围
uv run --script scripts/cnstock chart 600519 30d     # 近30天
uv run --script scripts/cnstock chart 600519 90d     # 近3个月
uv run --script scripts/cnstock chart 600519 6mo     # 近半年
uv run --script scripts/cnstock chart 600519 1y      # 近1年
uv run --script scripts/cnstock chart 600519 5y      # 近5年

# 折线图
uv run --script scripts/cnstock chart 600519 90d line
```

| 周期参数 | 含义 | 适合看什么 |
|---------|------|-----------|
| `30d` | 近 30 天 | 短期趋势、突破信号 |
| `90d` | 近 3 个月 | 中期波段、支撑/压力位 |
| `6mo` | 近半年 (默认) | 中期趋势、均线形态 |
| `1y` | 近 1 年 | 长期趋势、牛熊判断 |
| `5y` | 近 5 年 | 历史大周期 |
| `max` | 全部历史 | 完整走势 |

**小白解释**:K线图(蜡烛图)上每一根"棒子"代表一天(或一周)的价格波动,红涨绿跌(或绿涨红跌,看你软件设置)。MA5/MA20/MA60 是"过去5天/20天/60天的平均价格",用来看趋势是涨是跌,不是用来预测明天会怎样的。图表生成后会自动弹窗打开。

### 3. Fundamental Analysis (`fundamentals`)
Deep dive into valuation: PE, PEG, PB, EPS, ROE, ROA, Margins, EV/EBITDA, FCF, Debt/Equity, Dividend Yield, 52-Week Range, and Analyst Consensus — all with plain-language explanations.
```bash
uv run --script scripts/cnstock fundamentals [TICKER]
```
**美股独有增强**: PEG、EV/EBITDA、毛利/运营/净利率、ROA、负债权益比、流动比率、自由现金流、股息率、52周位置可视化、分析师目标价。A股仅支持 Sina/Tencent 提供的基础字段。
**小白解释这几个指标到底是什么**:
- **PE(市盈率)**:说白了就是"这家公司现在的股价,是它一年赚的钱的多少倍"。PE 越高,说明大家越愿意为它的未来买单(但也可能是太贵了)。
- **EPS(每股收益)**:公司一年赚的钱,平均分到每一股上是多少。数字越大,说明这股票"含金量"越高。
- **ROE(净资产收益率)**:公司用股东的钱,一年能赚回多少比例。比如 ROE=15%,意思是股东每投100块,一年能帮你赚回15块的利润(注意,这不是分红,是公司账面上的盈利能力)。
- **Profit Margin(利润率)**:公司每赚100块收入,最后能留下多少利润,留得越多说明公司越"赚钱效率高"。

### 4. Earnings Calendar & Countdown (`earnings`)
Check upcoming earnings dates, historical surprises, and **countdown warnings**.

**小白解释**: 不仅告诉你财报啥时候出，还会倒计时提醒。财报前14天内会自动警告"波动加大，建议等财报落地"。美股还显示分析师预期营收和 EPS。

**A 股**: 法定披露截止日倒计时（一季报 4/30、中报 8/31、三季报 10/31、年报次年 4/30），密集期临近时发出提醒。
**美股**: Yahoo Finance 精确财报日 + 倒计时天数 + 前后风险提示。

### 5. Historical Trends (`history`)
View recent 10-day trends with terminal-friendly ASCII charts.
```bash
uv run --script scripts/cnstock history [TICKER]
```

### 6. Market Temperature (`market`)
Quick health check of the broader market — no ticker needed.
```bash
uv run --script scripts/cnstock market
```
**小白解释**：一键看大盘温度。美股市场显示 VIX 恐慌指数 + SPY/QQQ 涨跌 + 黄金/美债/美元避险信号。A股显示上证指数实时行情。如果 VIX 飚了或者资金涌入避险资产（黄金+美债+美元齐涨），会高亮警告。15分钟缓存，不用担心频繁请求被限。

**避险模式检测**：当 GLD +2%、TLT +1%、UUP +1% 同时触发 → 标记"🛡️ 避险模式"，提醒股市风险偏高。

### 7. Multi-Stock Comparison (`compare`)
Overlay normalized price performance of multiple stocks on a single chart.
```bash
uv run --script scripts/cnstock compare 600519 000858 --period 6mo
uv run --script scripts/cnstock compare AAPL MSFT GOOGL --period 1y
```
**小白解释**：把几只股票的走势放在同一张图上对比，统一从"0%涨跌幅"开始算，方便看谁涨得多、谁跌得多。比单独看每只股票的图更直观。

### 8. Portfolio Management (`portfolio.py`)
Create portfolios, add/remove holdings, and track real-time P&L across stocks and crypto.
```bash
# 组合管理
uv run scripts/portfolio.py create "我的组合"
uv run scripts/portfolio.py add 600519 --name "茅台" --quantity 100 --cost 1850
uv run scripts/portfolio.py add AAPL --name "苹果" --quantity 50 --cost 290
uv run scripts/portfolio.py show

# 其他操作
uv run scripts/portfolio.py list
uv run scripts/portfolio.py remove AAPL
uv run scripts/portfolio.py delete "我的组合"
```
**小白解释**: 这个功能就是帮你记录你买了什么股票、成本多少、现在赚了还是亏了。不用自己拿计算器算了。

### 9. China A-Share Support — Powered by AkShare
For Shanghai/Shenzhen listed stocks, this tool automatically detects the market and switches to **AkShare** as the data engine — no special flags needed.

```bash
uv run --script scripts/cnstock price 600519
uv run --script scripts/cnstock fundamentals 000858
uv run --script scripts/cnstock chart 300750 6mo
```

**小白解释**:A股（像贵州茅台、比亚迪这种在上海/深圳上市的股票）用法和美股完全一样，直接写代码就行。工具会自动识别市场并切换到国内数据源，不需要你操心。

**A股代码怎么写**:
- 上海主板: 直接写 6 位数字（如 `600519` = 贵州茅台）
- 深圳主板/创业板: 直接写 6 位数字（如 `000858` = 五粮液, `300750` = 宁德时代）

工具内部自动判断: 6 开头 → 沪市, 0/3 开头 → 深市。不需要手动加 `.SH` 或 `.SZ`。

## Ticker Examples
- **US Stocks**: `AAPL`, `NVDA`, `TSLA`
- **Korean Stocks**: `005930.KS` (Samsung), `000660.KS` (SK Hynix)
- **China A-Shares**: `600519`(贵州茅台), `000858`(五粮液), `300750`(宁德时代)
- **Crypto**: `BTC-USD`, `ETH-KRW`

## Output Format

When a user asks about a stock, Claude MUST present results in the following fixed template. Do NOT just dump raw command output — reformat it into this structure every time.

### Standard Report Template (单只股票查询)

```
## {emoji} {股票名称} ({代码}) — 综合报告

> 📅 数据日期：{最新交易日}｜数据源：{来源}

### 📈 实时行情

| 指标 | 数值 |
|---|---|
| 当前价 | ¥XXX.XX |
| 涨跌 | ±XX.XX (±X.XX%) |
| 今开 / 最高 / 最低 | XXX / XXX / XXX |
| 昨收 | XXX |
| 成交量 | XXX |

### 📊 基本面核心指标

| 指标 | 数值 | 一句话解读 |
|---|---|---|
| PE (市盈率) | XX.X | 偏低/适中/偏高 |
| PEG (市盈增长比) | X.X | 低估/合理 (美股独有) |
| EPS (每股收益) | XX.X | 每股盈利能力 |
| ROE | X.X% | 股东回报效率 |
| 利润率 (Gross/Op/Net) | X%/X%/X% | 赚钱效率 (美股独有) |
| 负债权益比 / 流动比率 | X.X / X.X | 财务安全度 (美股独有) |
| EV/EBITDA | X.X | 企业估值倍数 (美股独有) |
| 总市值 | X.XX万亿 | 市场体量 |
| 52周位置 | [████░░░] X% | 当前在52周区间的位 |

### 📉 近期走势 (近10日)

[ASCII 迷你走势图或表格，标注趋势方向]

**关键观察**：
- 短期趋势判断（涨/跌/震荡）
- 均线形态（金叉/死叉/粘合）
- 成交量变化（放量/缩量）
- 关键支撑/压力位

### 📌 小白解读

[3-5 句白话总结，覆盖：]
- 股价贵不贵（PE 角度）
- 公司赚不赚钱（EPS/ROE 角度）
- 近期走得怎么样
- 有什么要注意的风险

> ⚠️ **免责声明**：以上仅为数据展示和指标解读，不构成任何投资建议。股市有风险，入市需谨慎。
```

### Multi-Stock Workflow (多只股票处理流程)

When a user mentions multiple stocks (e.g., "compare AAPL and MSFT", "对比一下茅台和五粮液"), Claude MUST follow this workflow.

---

#### Step 0: Detect Industry Context

First, check if the user mentioned:
- **Specific tickers** (e.g., "茅台", "600519", "AAPL") → Go to Step 1
- **An industry keyword** without tickers (e.g., "白酒", "AI芯片", "新能源车") → Go to Step 1 with the industry-aware 3-option menu

**Industry → Ticker Reference Table** (中国市场常见行业):

| 行业关键词 | 代表股票 | 补充股票（可自定义添加） |
|-----------|---------|----------------------|
| 白酒 | 600519(茅台), 000858(五粮液), 000568(老窖) | 002304(洋河), 000596(古井贡), 600809(汾酒), 603369(今世缘) |
| 新能源车 | 300750(宁德时代), 002594(比亚迪) | 601012(隆基), 300014(亿纬锂能), 300274(阳光电源) |
| AI/芯片 | 688981(中芯国际), 002049(紫光国微) | 603986(兆易创新), 300782(卓胜微), 688256(寒武纪) |
| 银行 | 601398(工商银行), 600036(招商银行) | 601939(建设银行), 000001(平安银行), 601166(兴业银行) |
| 医药 | 600276(恒瑞医药), 300760(迈瑞医疗) | 000538(云南白药), 300015(爱尔眼科), 600196(复星医药) |
| 互联网 | 00700.HK(腾讯), 09988.HK(阿里巴巴) | 03690.HK(美团), 09888.HK(百度), 09999.HK(网易) |
| 电力/能源 | 600900(长江电力), 601088(中国神华) | 600905(三峡能源), 601857(中国石油) |
| 消费 | 000333(美的集团), 002415(海康威视) | 600887(伊利股份), 002714(牧原股份) |
| 证券 | 600030(中信证券), 300059(东方财富) | 601688(华泰证券), 000776(广发证券) |

> 💡 上表是市场常见代表，不是投资推荐。用户提到的行业如果不在表中，Claude 应搜索或询问用户想关注哪些股票。

---

#### Step 1: Clarify Intent

If the user mentioned an **行业关键词** (no specific tickers), present the **3-option menu**:

> "这个行业有几只代表性的股票。你想：
> 1. 📈 **对比走势** — 把它们的价格走势放在一张图上对比
> 2. 📁 **创建投资组合** — 追踪它们的实时盈亏
> 3. ✏️ **自定义选择** — 从行业里挑特定几只，或者加上别的股票"

- **选 1 (对比)** → 直接用行业代表股票（3-4只）跑 `compare` → Go to Step 2
- **选 2 (组合)** → Go to Step 3，组合名自动建议为行业名（如"白酒组合"）
- **选 3 (自定义)** → 列出行业所有候选股票供用户勾选，或将用户指定的股票加入对比/组合。

If the user mentioned **specific tickers** but intent is ambiguous, ask the simpler question:

> "你想**对比这几只股票的走势**，还是**创建一个投资组合**来追踪它们？"

- **对比走势** → Go to Step 2
- **创建投资组合** → Go to Step 3

If the user has already stated their intent clearly (e.g., "对比一下茅台和五粮液"), skip to the appropriate step.

#### Step 2: Comparison Mode (走势对比)

Run these commands in parallel where possible:

1. **Comparison chart** (the key new command):
   ```bash
   uv run --script scripts/cnstock compare TICKER1 TICKER2 [TICKER3...] --period 6mo
   ```

2. **Individual quotes and fundamentals** for each ticker (run concurrently):
   ```bash
   uv run --script scripts/cnstock price TICKER
   uv run --script scripts/cnstock fundamentals TICKER
   ```

3. Present results using the **Multi-Stock Comparison Table**:

| | 股票A | 股票B | 股票C |
|---|---|---|---|
| **当前价** | ... | ... | ... |
| **涨跌幅** | ... | ... | ... |
| **PE** | ... | ... | ... |
| **EPS** | ... | ... | ... |
| **市值** | ... | ... | ... |

4. Add a **comparison summary** (3-5 lines) covering:
   - Which stock gained/lost the most over the period
   - Relative valuation (PE comparison)
   - Notable divergence points visible in the chart

5. Mention the comparison chart path: `/tmp/compare_{tickers}_{period}.png`

#### Step 3: Portfolio Mode (投资组合)

Guide the user through `portfolio.py`:

1. Create a portfolio:
   ```bash
   uv run scripts/portfolio.py create "白酒组合"
   ```

2. Add each holding:
   ```bash
   uv run scripts/portfolio.py add 600519 --name "茅台" --quantity 100 --cost 1850
   uv run scripts/portfolio.py add 000858 --name "五粮液" --quantity 200 --cost 150
   ```

3. Show P&L:
   ```bash
   uv run scripts/portfolio.py show
   ```

For existing portfolios, use `list` to find them and `show` to display.

### Chart Output

After generating a chart, always mention the file path (`/tmp/{ticker}_{period}_{style}.png`) so the user knows where to find it. If the chart shows CJK font tofu (□□□), warn the user that Chinese labels may not render correctly and suggest installing a CJK font.

---

## Technical Notes
- **Engine**: Python 3.11+, `yfinance` (global), `akshare` (China A-shares), `mplfinance`, `rich`
- **Auto-routing**: The tool detects the ticker format and automatically picks the right data engine — you don't need to specify which one to use.
- **No API key required** for either data source.
- **Cache TTL**: 报价 5min | 基本面 1h | K线 15min-1h | 市场环境 15min

---

## Limitations

### Data Freshness (数据时效性)
- **A股实时行情 (Sina/Tencent)**: 盘中 ~3秒延迟，盘后显示当日收盘价。周末/节假日显示上一交易日收盘价。
- **美股行情 (Yahoo Finance)**: 可能有 15-20 分钟延迟（非实时用户），盘后/盘前数据可能不完整。**YF 容易限流 (429)**，限流时自动指数退避重试，极端情况下可能降级到 HTTP 直连或返回空数据。
- **市场温度计 (market)**: VIX/SPY/QQQ 15分钟缓存 TTL；上证指数实时。YF 限流时美股部分可能为空。
- **Crypto (Yahoo Finance)**: 接近实时，但极端行情下可能延迟。

### A股特有局限
- **基本面数据不全**: Sina/Tencent 接口提供的财务指标有限。ROE、利润率等字段经常缺失（显示"暂无数据"），因为这些数据源侧重实时行情而非财务分析。
- **财报日历无精确日期**: A股没有 Yahoo Finance 那种 EPS 预期和分析师共识。`earnings` 命令只显示A股法定披露截止日（一季报4/30、中报8/31、三季报10/31、年报4/30），不显示公司具体公告日期。
- **无分析师评级**: A股数据源不支持分析师目标价、评级共识等美股常见的指标。

### 图表已知问题
- **CJK 字体缺失**: 图表中的中文标签（价格、成交量等）可能显示为方块(□□□)，这是因为系统缺少中文字体。macOS 默认的图表中文字体支持有限。价格数字、均线等技术指标不受影响。
- **大周期图表加载慢**: `5y` 和 `max` 周期需要拉取大量历史数据，生成时间明显更长（5-15秒）。

### 数据源稳定性
- **Sina 新浪财经**: 最稳定的A股实时行情源，20年+历史。但工作日 9:00-15:30 外可能无数据或返回过期数据。
- **Tencent 腾讯财经**: 备用源，提供更丰富的基本面字段。偶尔字段格式变动。
- **AKShare**: 最后后备源。可能被代理/VPN 拦截。首次使用需要下载数据包（慢）。依赖东方财富/新浪等上游，遇到反爬可能短时间内不可用。
- **baostock**: 纯 Python 证券数据包，免费无需 token，但需要登录/登出流程，速度较慢。

### 缓存说明
- 同一股票 5 分钟内重复查询，直接返回缓存数据（不重新请求），避免触发反爬。
- 缓存存储在 `~/.clawdbot/skills/cn-stock-pro/cache/`，过期自动删除。
- 如果你发现数据和交易软件不一致，可能是缓存还没过期 → 等 5 分钟后再试。

### 市场休市
- **A股交易日**: 周一至周五（法定节假日休市）。周末和节假日查询，实时行情显示的是最近一个交易日的收盘数据。
- **美股交易日**: 周一至周五（美国节假日休市）。
- **港股交易日**: 周一至周五（香港节假日休市）。港股还有台风/暴雨休市机制。

### 功能覆盖范围
| 功能 | A股 | 美股 | 港股 | Crypto |
|---|---|---|---|---|
| 实时报价 | ✅ 优秀 | ✅ 良好 | ⚠️ 基础 | ✅ 良好 |
| 基本面(PE/EPS/ROE) | ⚠️ 部分 | ✅ 完整 | ⚠️ 部分 | ❌ 不适用 |
| K线图 | ✅ 优秀 | ✅ 优秀 | ⚠️ 基础 | ✅ 优秀 |
| 财报日历 | ⚠️ 仅法定截止日 | ✅ 完整 | ⚠️ 基础 | ❌ 不适用 |
| 近10日趋势 | ✅ 优秀 | ✅ 优秀 | ⚠️ 基础 | ✅ 优秀 |

> ⚠️ **免责声明**: 本工具仅提供数据展示和指标解读，不对数据准确性做任何保证。所有信息仅供参考，不构成投资建议。投资决策请以交易所官方数据和持牌投资顾问意见为准。

---

## Error Handling

The tool and Claude handle errors at two levels:

### Script-Level Error Handling (脚本层)

| 错误场景 | 处理方式 |
|---|---|
| **无效代码** (如 `999999`) | 所有数据源返回空 → 输出 `❌ 无法获取 XXX 的数据` |
| **网络超时/不通** | 多源自动降级: Sina → Tencent → baostock → AKShare，每个源 8-10s 超时 |
| **Yahoo 限流 (429)** | 自动等待（指数退避: 2s → 4s → 8s → 16s，最多4次重试），超限后跳过 Yahoo 用直接 HTTP |
| **AKShare 被代理拦截** | 静默跳过，转下一个源，不影响其他数据源 |
| **baostock 登录失败** | 静默跳过，转下一个源 |
| **Sina/Tencent 返回空** | 静默跳过，转下一个源 |
| **K线数据格式异常** | 输出 `❌ 数据格式不正确`，不生成图表 |
| **mplfinance 中文渲染失败** | 输出 warning 到 stderr，图表仍正常生成（用英文标题） |
| **matplotlib 缺字体** | 自动 fallback 到 DejaVu Sans，不阻断图表生成 |

### Claude-Level Error Handling (AI 层 — 你需要做的)

When a command fails or returns partial data, DO NOT retry the same command. Instead:

1. **全部命令失败** → 告知用户当前无法获取数据，建议：
   - 检查网络连接
   - 确认股票代码是否正确
   - 等待几分钟后重试（可能是数据源临时故障）

2. **部分数据缺失** (如 PE 有但 ROE 无) → 在输出模板中标注"暂无数据"，继续展示已有的指标。不要因为一个字段缺失就放弃整个报告。

3. **周末/节假日查询** → 在报告顶部明确标注"📅 今日休市，以下为最近交易日 (X月X日) 数据"。不要假装这是实时数据。

4. **图表生成成功但 CJK 字体缺失** → 正常展示报告，额外提醒用户"图表中的中文标签可能显示为方块，但价格数字和均线不受影响"。

5. **缓存数据** → 如果输出中包含 `⚡缓存` 标记，告知用户这是缓存数据（5分钟内查询过），如需刷新等几分钟后再试。

6. **市场温度计无数据** → 美股或 A 股某一边可能因限流/网络问题无数据。正常展示可用的一边，缺失的标注"暂不可用"。不要因为美股没数据就放弃展示 A 股部分。

7. **非A股/美股股票** → 如果用户查询港股或加密货币但仍可用，标注数据源和质量。如果完全不支持，如实告知。

---

## Beginner Glossary(新手术语速查)
| 术语 | 大白话解释 |
|---|---|
| PE 市盈率 | 股价是年利润的几倍,越低相对越"便宜" |
| EPS 每股收益 | 每一股能分到公司多少利润 |
| ROE 净资产收益率 | 公司用股东的钱赚钱的效率 |
| MA5/20/60 | 过去5/20/60天的平均价,看趋势用 |
| K线/蜡烛图 | 一天内开盘、收盘、最高、最低价格的图形化表示 |
| 成交量 | 当天有多少股票被买卖了,量越大说明关注度越高 |
