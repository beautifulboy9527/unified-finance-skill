# Neo9527 Unified Finance Skill

> 📊 多市场金融分析技能库 | v3.1 | by Neo9527

[![GitHub](https://img.shields.io/badge/GitHub-Neo9527--unified--finance--skill-blue)](https://github.com/beautifulboy9527/Neo9527-unified-finance-skill)
[![Version](https://img.shields.io/badge/version-v3.1-green)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-orange)]()

---

## 🎯 项目简介

**Neo9527 Unified Finance Skill** 是一个功能完整的多市场金融分析技能库，整合了传统股票市场、加密货币、贵金属等多个领域的分析能力，提供从数据获取到交易决策的完整解决方案。

### 核心特点

- 🌍 **多市场支持**: A股、港股、美股、加密货币、贵金属
- 📊 **三层分析框架**: 宏观 → 行业 → 个股 系统化分析
- 🎯 **信号验证**: 30个历史验证信号，最高88%成功率
- ⚙️ **风险管理**: ATR止损 + 仓位计算 + 目标价
- 🤖 **Agent协调**: 智能路由 + 多Agent协作
- 🔍 **选股器**: 11种筛选策略 + 多策略组合

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/beautifulboy9527/Neo9527-unified-finance-skill.git

# 安装依赖
pip install -r requirements.txt
```

### 基础使用

```bash
# 综合评分 (推荐)
python finance.py score AAPL
# → 88分 | 强势 | 建议买入

# 完整分析报告
python finance.py report-full 600519
# → Markdown格式完整报告

# 风险管理
python finance.py risk AAPL --capital 100000
# → 止损价 | 目标价 | 建议仓位

# 入场信号
python finance.py signals AAPL
# → 检测到的信号 + 成功率
```

### 高级功能

```bash
# 股票筛选
python finance.py screen --strategy ma_bull --market a

# 多策略组合
python finance.py screen --strategies ma_bull macd_golden --mode and

# 打板机会
python finance.py board --opportunities

# 监管监控
python finance.py regulation --days 7

# 地区化新闻分析
python finance.py regional-news --type regional
```

---

## 📊 能力矩阵

### 市场覆盖

| 市场 | 行情 | 分析 | 信号 | 评分 | 风险 | 监管 | 打板 | 筛选 |
|------|------|------|------|------|------|------|------|------|
| **A股** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **港股** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **美股** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ |
| **加密货币** | ✅ | ✅ | ✅ | ✅ | ✅ | - | - | - |
| **贵金属** | ✅ | ✅ | ✅ | ✅ | ✅ | - | - | - |

### 核心模块

| 模块 | 功能 | 文件 |
|------|------|------|
| **三层框架** | 宏观-行业-个股分析 | `analysis_framework.py` |
| **信号库** | 30个验证信号 | `entry_signals.py` |
| **风险管理** | ATR止损 + 仓位 | `risk_management.py` |
| **评分引擎** | 0-100分评分 | `scoring_engine.py` |
| **监管监控** | 公告监控 | `regulation_monitor.py` |
| **打板筛选** | 涨停板扫描 | `board_scanner.py` |
| **地区分析** | 新闻地区化 | `regional_news.py` |
| **选股器** | 11种策略 | `stock_screener.py` |

---

## 📁 目录结构

```
Neo9527-unified-finance-skill/
├── SKILL.md              # Skill 定义
├── README.md             # 项目说明
├── requirements.txt      # 依赖列表
│
├── scripts/              # 源代码
│   ├── finance.py       # 主入口 (60+ 命令)
│   ├── core/            # 核心模块
│   │   ├── quote.py    # 行情获取
│   │   ├── news.py     # 新闻数据
│   │   └── technical.py # 技术分析
│   ├── features/        # 功能模块 (15+)
│   │   ├── analysis_framework.py
│   │   ├── entry_signals.py
│   │   ├── stock_screener.py
│   │   └── ...
│   └── agent/           # Agent 模块
│       └── orchestrator.py
│
├── docs/                 # 文档
│   ├── ARCHITECTURE.md  # 架构文档
│   ├── CLI-Reference.md # CLI 参考
│   └── guides/          # 使用指南
│
├── planning/             # 规划文档
│   ├── evaluations/     # Skills 评估
│   └── integration-plans/ # 整合计划
│
├── tests/                # 测试
├── config/               # 配置
└── references/           # 参考资料
```

---

## 🔧 整合来源

本项目整合了多个高价值 Skills 的核心能力：

| 来源 | 整合内容 | 整合方式 |
|------|---------|---------|
| [sm-analyze](https://skills.yangsir.net/skill/sm-analyze) | 三层分析框架 | 代码重写 |
| [entry-signals](https://skills.yangsir.net/skill/sm-entry-signals) | 信号库 | 理念吸收 |
| [technical-analysis](https://skills.yangsir.net/skill/ssh2-technical-analysis) | 成交量验证 | 理念吸收 |
| [regulation-monitor](https://clawhub.ai/gentleming/regulation-monitor) | 监管监控 | 代码重写 |
| [stock-board](https://clawhub.ai/mrblarkerx/stock-board) | 打板筛选 | Python重写 |
| [stock-recommend](https://clawhub.ai/violin/stock-recommend) | 地区化分析 | 思路借鉴 |
| [stock-screener-cn](https://clawhub.ai/otouman/stock-screener-cn) | 股票筛选器 | 代码重写 |

---

## 📈 版本历史

| 版本 | 日期 | 主要更新 |
|------|------|---------|
| **v3.1** | 2026-04-16 | Phase 5-8: 监管监控 + 打板筛选 + 地区化分析 + 选股器 |
| **v3.0** | 2026-04-16 | Phase 3-4: 三层框架 + 信号库 + 风险管理 |
| **v2.0** | 2026-04-15 | 多市场扩展: 加密货币 + 贵金属 |
| **v1.0** | 2026-04-14 | 基础版本: A股/港股/美股核心功能 |

详见 [CHANGELOG.md](CHANGELOG.md)

---

## 📊 统计数据

| 指标 | 数量 |
|------|------|
| **代码行数** | 20,000+ |
| **功能模块** | 15+ |
| **CLI命令** | 60+ |
| **筛选策略** | 11种 |
| **验证信号** | 30个 |
| **支持市场** | 5个 |

---

## 📖 文档

- [架构文档](docs/ARCHITECTURE.md)
- [CLI 参考](docs/Unified-Finance-Skill-快速参考.md)
- [开发历程](docs/Unified-Finance-Skill-开发历程.md)
- [Agent 架构](docs/AGENT-ARCHITECTURE.md)

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

[MIT License](LICENSE)

---

## 👤 作者

**Neo9527** (一辉)

- GitHub: [@beautifulboy9527](https://github.com/beautifulboy9527)
- 项目: [Neo9527-unified-finance-skill](https://github.com/beautifulboy9527/Neo9527-unified-finance-skill)

---

## 🙏 致谢

感谢以下项目和社区的支持：

- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架
- [AkShare](https://github.com/akfamily/akshare) - 金融数据接口
- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance API
- [ClawHub](https://clawhub.ai) - Skills 市场

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！⭐**
