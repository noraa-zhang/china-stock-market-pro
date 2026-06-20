#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "yfinance>=0.2.40",
#     "pandas>=2.0.0",
#     "rich>=13.0.0",
# ]
# ///
"""
组合管理 — 创建组合、增删持仓、实时盈亏追踪

Usage:
    uv run scripts/portfolio.py create "组合名称"
    uv run scripts/portfolio.py list
    uv run scripts/portfolio.py show [--portfolio NAME]
    uv run scripts/portfolio.py delete "组合名称"
    uv run scripts/portfolio.py rename "旧名称" "新名称"

    持仓操作:
    uv run scripts/portfolio.py add TICKER --name "股票名" --quantity 100 --cost 150.00 [--portfolio NAME]
    uv run scripts/portfolio.py update TICKER --quantity 150 [--portfolio NAME]
    uv run scripts/portfolio.py remove TICKER [--portfolio NAME]
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Literal

import yfinance as yf


# ──────────────────────────────────────────────────────────────────
# 数据模型
# ──────────────────────────────────────────────────────────────────

@dataclass
class Asset:
    ticker: str
    name: str
    asset_type: str  # "stock" | "crypto"
    quantity: float
    cost_per_share: float
    added_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Portfolio:
    name: str
    assets: list[Asset] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ──────────────────────────────────────────────────────────────────
# 存储层
# ──────────────────────────────────────────────────────────────────

def get_storage_path() -> Path:
    """获取组合数据存储路径"""
    state_dir = os.environ.get(
        "CLAWDBOT_STATE_DIR",
        os.path.expanduser("~/.clawdbot"),
    )
    portfolio_dir = Path(state_dir) / "skills" / "cn-stock-pro"
    portfolio_dir.mkdir(parents=True, exist_ok=True)
    return portfolio_dir / "portfolios.json"


def load_portfolios() -> dict[str, Portfolio]:
    """加载所有组合"""
    path = get_storage_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r") as f:
            data = json.load(f)
        portfolios = {}
        for name, pdata in data.items():
            assets = [Asset(**a) for a in pdata.get("assets", [])]
            pdata["assets"] = assets
            portfolios[name] = Portfolio(**pdata)
        return portfolios
    except (json.JSONDecodeError, TypeError):
        return {}


def save_portfolios(portfolios: dict[str, Portfolio]):
    """保存所有组合"""
    path = get_storage_path()
    data = {}
    for name, p in portfolios.items():
        pdata = asdict(p)
        pdata["assets"] = [asdict(a) for a in p.assets]
        data[name] = pdata
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────────────────────────

def detect_asset_type(ticker: str) -> str:
    """自动识别资产类型"""
    ticker_upper = ticker.upper()
    if "-" in ticker_upper:
        return "crypto"
    return "stock"


def get_current_price(ticker: str) -> float | None:
    """获取当前价格"""
    import pandas as pd

    try:
        # 尝试 yfinance
        stock = yf.Ticker(ticker)
        info = stock.info
        price = (
            info.get("regularMarketPrice")
            or info.get("currentPrice")
            or info.get("regularMarketPreviousClose")
        )
        if price:
            return float(price)

        # fallback: 获取最近收盘价
        hist = stock.history(period="5d")
        if not hist.empty:
            return float(hist["Close"].iloc[-1])
    except Exception:
        pass

    try:
        # 尝试 AKShare (A股)
        import akshare as ak
        df = ak.stock_zh_a_spot_em()
        row = df[df["代码"] == ticker]
        if not row.empty:
            return float(row.iloc[0]["最新价"])
    except Exception:
        pass

    return None


def format_price(price: float | None) -> str:
    if price is None:
        return "N/A"
    return f"¥{price:.2f}" if price < 10000 else f"¥{price:,.2f}"


def format_pnl(pnl: float | None) -> str:
    if pnl is None:
        return "N/A"
    color = "🟢" if pnl > 0 else "🔴" if pnl < 0 else "⚪"
    return f"{color} ¥{pnl:+,.2f}"


# ──────────────────────────────────────────────────────────────────
# 子命令
# ──────────────────────────────────────────────────────────────────

def cmd_create(name: str):
    """创建组合"""
    portfolios = load_portfolios()
    if name in portfolios:
        print(f"❌ 组合 '{name}' 已存在")
        sys.exit(1)

    portfolios[name] = Portfolio(name=name)
    save_portfolios(portfolios)
    print(f"✅ 组合 '{name}' 创建成功")
    print(f"   存储路径: {get_storage_path()}")


def cmd_list():
    """列出所有组合"""
    portfolios = load_portfolios()
    if not portfolios:
        print("📭 暂无组合，使用 'create' 命令创建一个吧")
        return

    print(f"\n📋 共 {len(portfolios)} 个组合:\n")
    for name, p in portfolios.items():
        total_cost = sum(a.quantity * a.cost_per_share for a in p.assets)
        print(f"   📁 {name}")
        print(f"      持仓: {len(p.assets)} 只")
        print(f"      总成本: ¥{total_cost:,.2f}")
        print(f"      创建时间: {p.created_at[:10]}")
        print()


def cmd_show(portfolio_name: str | None):
    """查看组合详情（含实时盈亏）"""
    portfolios = load_portfolios()
    active = _resolve_portfolio(portfolios, portfolio_name)

    if not active:
        print("❌ 没有找到组合")
        return

    from rich.console import Console
    from rich.table import Table

    console = Console()

    if not active.assets:
        console.print(f"\n📁 [bold]{active.name}[/bold] — 暂无持仓\n")
        return

    console.print(f"\n📁 [bold]{active.name}[/bold] 持仓明细\n")

    table = Table()
    table.add_column("代码", style="cyan")
    table.add_column("名称")
    table.add_column("类型")
    table.add_column("数量", justify="right")
    table.add_column("成本价", justify="right")
    table.add_column("现价", justify="right")
    table.add_column("成本", justify="right")
    table.add_column("市值", justify="right")
    table.add_column("盈亏", justify="right")
    table.add_column("收益率", justify="right")

    total_cost = 0.0
    total_value = 0.0
    unknown_count = 0

    for asset in active.assets:
        current_price = get_current_price(asset.ticker)
        cost = asset.quantity * asset.cost_per_share
        total_cost += cost

        if current_price:
            value = asset.quantity * current_price
            total_value += value
            pnl = value - cost
            pnl_pct = (pnl / cost * 100) if cost > 0 else 0
            pnl_str = format_pnl(pnl)
            pct_str = f"{'+' if pnl_pct > 0 else ''}{pnl_pct:.2f}%"
            price_str = format_price(current_price)
            value_str = f"¥{value:,.2f}"
        else:
            unknown_count += 1
            price_str = "N/A"
            value_str = "N/A"
            pnl_str = "N/A"
            pct_str = "N/A"

        table.add_row(
            asset.ticker,
            asset.name or "-",
            asset.asset_type,
            f"{asset.quantity:,.0f}",
            f"¥{asset.cost_per_share:.2f}",
            price_str,
            f"¥{cost:,.2f}",
            value_str,
            pnl_str,
            pct_str,
        )

    console.print(table)

    print(f"\n   📊 汇总:")
    print(f"      持仓数量: {len(active.assets)} 只")
    print(f"      总成本:   ¥{total_cost:,.2f}")
    if total_value > 0:
        total_pnl = total_value - total_cost
        total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
        print(f"      总市值:   ¥{total_value:,.2f}")
        print(f"      总盈亏:   {format_pnl(total_pnl)} ({total_pnl_pct:+.2f}%)")
    if unknown_count > 0:
        print(f"      ⚠️ {unknown_count} 只资产无法获取实时价格")
    print()


def cmd_delete(name: str):
    """删除组合"""
    portfolios = load_portfolios()
    if name not in portfolios:
        print(f"❌ 组合 '{name}' 不存在")
        sys.exit(1)

    del portfolios[name]
    save_portfolios(portfolios)
    print(f"🗑️ 组合 '{name}' 已删除")


def cmd_rename(old_name: str, new_name: str):
    """重命名组合"""
    portfolios = load_portfolios()
    if old_name not in portfolios:
        print(f"❌ 组合 '{old_name}' 不存在")
        sys.exit(1)
    if new_name in portfolios:
        print(f"❌ 组合 '{new_name}' 已存在")
        sys.exit(1)

    portfolios[new_name] = portfolios.pop(old_name)
    portfolios[new_name].name = new_name
    portfolios[new_name].updated_at = datetime.now().isoformat()
    save_portfolios(portfolios)
    print(f"✅ 组合 '{old_name}' → '{new_name}' 重命名成功")


def cmd_add(ticker: str, name: str, quantity: float, cost: float, portfolio_name: str | None):
    """添加资产到组合"""
    portfolios = load_portfolios()
    active_name, active = _get_or_create_active(portfolios, portfolio_name)

    # 检查是否已存在
    for a in active.assets:
        if a.ticker.upper() == ticker.upper():
            print(f"⚠️ {ticker} 已存在于组合中，使用 'update' 命令修改数量")
            return

    asset = Asset(
        ticker=ticker.upper(),
        name=name or ticker,
        asset_type=detect_asset_type(ticker),
        quantity=quantity,
        cost_per_share=cost,
    )
    active.assets.append(asset)
    active.updated_at = datetime.now().isoformat()
    save_portfolios(portfolios)

    total = quantity * cost
    print(f"✅ 已添加 {ticker.upper()} 到组合 '{active_name}'")
    print(f"   {name or ticker} × {quantity:,.0f} 股, 成本 ¥{cost:.2f}/股, 总计 ¥{total:,.2f}")


def cmd_update(ticker: str, quantity: float | None, portfolio_name: str | None):
    """更新持仓数量"""
    portfolios = load_portfolios()
    active_name, active = _get_or_create_active(portfolios, portfolio_name)

    for a in active.assets:
        if a.ticker.upper() == ticker.upper():
            if quantity is not None:
                old_qty = a.quantity
                a.quantity = quantity
                a.updated_at = datetime.now().isoformat()
                print(f"✅ {ticker} 数量已更新: {old_qty:,.0f} → {quantity:,.0f}")
            active.updated_at = datetime.now().isoformat()
            save_portfolios(portfolios)
            return

    print(f"❌ {ticker} 不在组合 '{active_name}' 中")
    sys.exit(1)


def cmd_remove(ticker: str, portfolio_name: str | None):
    """移除资产"""
    portfolios = load_portfolios()
    active_name, active = _get_or_create_active(portfolios, portfolio_name)

    for i, a in enumerate(active.assets):
        if a.ticker.upper() == ticker.upper():
            removed = active.assets.pop(i)
            active.updated_at = datetime.now().isoformat()
            save_portfolios(portfolios)
            print(f"🗑️ {removed.ticker} ({removed.name}) 已从组合 '{active_name}' 移除")
            return

    print(f"❌ {ticker} 不在组合 '{active_name}' 中")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────
# 辅助
# ──────────────────────────────────────────────────────────────────

def _resolve_portfolio(portfolios: dict, name: str | None) -> Portfolio | None:
    """解析要操作的组合"""
    if not portfolios:
        return None
    if name:
        return portfolios.get(name)
    if len(portfolios) == 1:
        return list(portfolios.values())[0]
    # 默认选第一个
    return list(portfolios.values())[0] if portfolios else None


def _get_or_create_active(portfolios: dict, name: str | None) -> tuple[str, Portfolio]:
    """获取或创建当前操作组合"""
    if name:
        if name not in portfolios:
            print(f"❌ 组合 '{name}' 不存在，先用 'create' 命令创建")
            sys.exit(1)
        return name, portfolios[name]

    if not portfolios:
        print("📭 还没有组合，先用 'create' 命令创建一个吧")
        print("   例如: uv run scripts/portfolio.py create \"我的组合\"")
        sys.exit(1)

    # 取第一个（或唯一的一个）
    active_name = list(portfolios.keys())[0]
    if len(portfolios) > 1:
        print(f"💡 使用默认组合: '{active_name}' (可用 --portfolio 指定其他)")

    return active_name, portfolios[active_name]


# ──────────────────────────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="组合管理 — 创建组合、增删持仓、实时盈亏追踪"
    )
    subparsers = parser.add_subparsers(dest="action", help="操作")

    # create
    c = subparsers.add_parser("create", help="创建新组合")
    c.add_argument("name", help="组合名称")

    # list
    subparsers.add_parser("list", help="列出所有组合")

    # show
    s = subparsers.add_parser("show", help="查看组合持仓与盈亏")
    s.add_argument("--portfolio", "-p", help="组合名称（不指定则使用默认）")

    # delete
    d = subparsers.add_parser("delete", help="删除组合")
    d.add_argument("name", help="组合名称")

    # rename
    r = subparsers.add_parser("rename", help="重命名组合")
    r.add_argument("old_name", help="旧名称")
    r.add_argument("new_name", help="新名称")

    # add
    a = subparsers.add_parser("add", help="添加资产到组合")
    a.add_argument("ticker", help="股票/加密货币代码")
    a.add_argument("--name", default="", help="资产显示名称")
    a.add_argument("--quantity", "-q", type=float, required=True, help="数量（股）")
    a.add_argument("--cost", "-c", type=float, required=True, help="成本价（每股）")
    a.add_argument("--portfolio", "-p", help="组合名称（不指定则使用默认）")

    # update
    u = subparsers.add_parser("update", help="更新持仓数量")
    u.add_argument("ticker", help="股票代码")
    u.add_argument("--quantity", "-q", type=float, required=True, help="新数量")
    u.add_argument("--portfolio", "-p", help="组合名称")

    # remove
    rm = subparsers.add_parser("remove", help="从组合移除资产")
    rm.add_argument("ticker", help="股票代码")
    rm.add_argument("--portfolio", "-p", help="组合名称")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    if args.action == "create":
        cmd_create(args.name)
    elif args.action == "list":
        cmd_list()
    elif args.action == "show":
        cmd_show(getattr(args, "portfolio", None))
    elif args.action == "delete":
        cmd_delete(args.name)
    elif args.action == "rename":
        cmd_rename(args.old_name, args.new_name)
    elif args.action == "add":
        cmd_add(args.ticker, args.name, args.quantity, args.cost, getattr(args, "portfolio", None))
    elif args.action == "update":
        cmd_update(args.ticker, args.quantity, getattr(args, "portfolio", None))
    elif args.action == "remove":
        cmd_remove(args.ticker, getattr(args, "portfolio", None))


if __name__ == "__main__":
    main()
