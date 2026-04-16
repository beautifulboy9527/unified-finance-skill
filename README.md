# Neo9527 Unified Finance Skill

> 📊 多维度金融分析系统 | v4.2 | by Neo9527

[![GitHub](https://img.shields.io/badge/GitHub-Neo9527--unified--finance--skill-blue)](https://github.com/beautifulboy9527/Neo9527-unified-finance-skill)
[![Version](https://img.shields.io/badge/version-v4.2-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-orange)]()
[![PyPI](https://img.shields.io/badge/pypi-neo9527--finance--skill-green)]()

---

## 🎯 项目简介

**Neo9527 Unified Finance Skill v4.2** 是一个生产级金融分析系统，整合了交互式K线图、链上数据、鲸鱼行为、信号叠加等专业能力，提供从市场数据到投资决策的完整解决方案。

### v4.2 核心特性

- 📈 **交互式K线图**: 可缩放/拖拽 + 均线叠加 + 成交量
- 🐋 **鲸鱼数据**: 大单流入/流出 + 链上行为分析
- 💎 **DeFi数据**: TVL + 协议排名 + 资金流
- 🎨 **现代报告**: 卡片式布局 + 响应式设计
- 📊 **叠buff逻辑**: 多因子信号叠加 + 综合评分
- 🔧 **CLI工具**: 统一命令行接口 + PyPI打包

### v4.0 → v4.2 升级亮点

| 功能 | v4.0 | v4.2 |
|------|------|------|
| K线图 | ❌ | ✅ 交互式 + 缩放 |
| 鲸鱼数据 | ❌ | ✅ 大单追踪 |
| DeFi数据 | ❌ | ✅ TVL + 协议 |
| CLI | 基础 | ✅ 5个命令 |
| PyPI | ❌ | ✅ 可安装 |

---

## 🚀 快速开始

### 方式1: PyPI安装 (推荐)

```bash
pip install neo9527-finance-skill

# 使用
neo-finance report BTC-USD --format html
```

### 方式2: 源码安装

```bash
# 克隆仓库
git clone https://github.com/beautifulboy9527/Neo9527-unified-finance-skill.git
cd Neo9527-unified-finance-skill

# 安装依赖
pip install -r requirements.txt

# 使用
python scripts/finance.py report BTC-USD --format html
```

---

## 💻 CLI命令

### 1. 生成报告

```bash
# HTML报告 (默认)
python scripts/finance.py report BTC-USD --format html

# 指定周期
python scripts/finance.py report ETH-USD --period long

# PDF格式
python scripts/finance.py report AAPL --format pdf
```

### 2. 快速分析

```bash
python scripts/finance.py analyze BTC-USD

# 输出:
# Price: $75,369
# Score: 75/100
# Decision: BUY
# Confidence: 75%
```

### 3. 信号检测

```bash
python scripts/finance.py signals BTC-USD

# 输出:
# 📈 Bullish Signals (3):
#   [技术形态] 趋势: 强烈看涨 (+5)
#   [趋势指标] MACD: 金叉看涨 (+3)
#   [经典形态] 双底: 看涨 (+4)
# 
# 📉 Bearish Signals (1):
#   [动量指标] RSI: 超买回调 (-2)
# 
# Total Strength: +10 (Bullish)
```

### 4. K线数据

```bash
# 获取K线数据
python scripts/finance.py kline BTC-USD --period 3mo

# 保存到JSON
python scripts/finance.py kline ETH-USD --save
```

### 5. 链上数据

```bash
python scripts/finance.py onchain BTC

# 输出:
# Network Metrics:
#   Hashrate: 0.00 EH/s
#   Difficulty: 138.97 T
#   Total Supply: 20,016,806
# 
# Whale Activity:
#   Net Flow: +350 BTC
#   Status: accumulating
#   Signal: 看涨 (低吸信号)
```

---

## 📊 报告结构

```
一、综合评分 (75/100)
    └─ 视觉卡片展示

二、市场数据 (实时)
    └─ 价格/涨跌/成交量/市值

三、技术分析
    📈 K线图 (交互式) ✨
       - 3个月历史数据
       - MA5/MA10/MA20 均线
       - 成交量柱状图
       - 可缩放/拖拽
    
    3.1 核心指标 (RSI/MACD/ADX/布林带)
    3.2 支撑阻力 (阻力位/支撑位)
    3.3 形态识别 (趋势/双顶双底/头肩)
    3.4 技术面专业解读

四、链上数据 ✨
    🐋 鲸鱼行为分析
       - 24h 净流入: +350 BTC
       - 状态: accumulating
       - 信号: 看涨
    
    ⛏️ 网络指标 (BTC)
       - 算力/难度/流通量
    
    💎 DeFi 数据 (ETH)
       - TVL: $485.2B
       - Top 5 协议排名

五、信号汇总 (多因子共振)
    ├─ 看涨信号卡片 (绿色)
    └─ 看跌信号卡片 (红色)

六、最终结论与操作建议
    ├─ 综合分析
    ├─ 核心支撑因素
    ├─ 风险提示
    ├─ 入场策略
    └─ 止损位/目标位

七、风险提示
```

---

## 🔧 核心模块

```
scripts/
├── finance.py                      # CLI入口 ✨
├── features/
│   ├── complete_crypto_analyzer.py # 完整分析器
│   ├── report_generator_v4.py      # 报告生成器 v4
│   ├── kline_chart.py              # K线数据生成 ✨
│   ├── onchain_data.py             # 链上数据获取 ✨
│   ├── investment_framework.py     # 投资框架
│   ├── finance_toolkit.py          # 金融工具包
│   ├── backtest_engine.py          # 回测引擎
│   └── templates/
│       ├── crypto_report_v4.html   # HTML模板
│       └── kline_component.html    # K线组件 ✨
├── core/
│   ├── technical.py                # 技术分析
│   └── quote.py                    # 行情数据
└── agent/
    └── smart_orchestrator.py       # 智能调度
```

---

## 📈 数据来源

| 数据类型 | 来源 | API | 状态 |
|---------|------|-----|------|
| 市场数据 | CoinGecko | 免费 | ✅ |
| 技术指标 | yfinance | 免费 | ✅ |
| K线数据 | yfinance | 免费 | ✅ |
| 链上数据 | Blockchain.com | 免费 | ✅ |
| DeFi数据 | DeFiLlama | 免费 | ✅ |
| 情绪指数 | alternative.me | 免费 | ✅ |
| 鲸鱼数据 | 模拟/需API | - | ⚠️ |

---

## 🎨 特色功能

### 1. 交互式K线图

- ✅ 轻量级 (40KB)
- ✅ 缩放/拖拽交互
- ✅ 均线叠加 (MA5/MA10/MA20)
- ✅ 成交量柱状图
- ✅ 响应式布局

### 2. 鲸鱼行为分析

- ✅ 24h 大单流入/流出
- ✅ 净流入量计算
- ✅ 鲸鱼状态判断
- ✅ 信号自动生成

### 3. 叠buff信号系统

| 形态 | 识别方法 | 信号强度 |
|------|---------|---------|
| 趋势判断 | MA排列 | ±5分 |
| 头肩顶 | 三峰检测 | -5分 |
| 双顶双底 | 两峰/谷相近 | ±4分 |
| RSI超买超卖 | >70/<30 | -2/+3分 |
| MACD金叉死叉 | 柱状图 | +3/-3分 |
| 布林带突破 | 价格位置 | ±2分 |
| 鲸鱼流入流出 | 链上数据 | ±4分 |

### 4. 专业文字解读

每个分析环节都有详细文字说明：

- ✅ 趋势分析 (多头/空头/震荡)
- ✅ RSI区间解读 (超买/超卖/中性)
- ✅ MACD动能判断
- ✅ 支撑阻力建议
- ✅ 综合操作建议

---

## 📝 更新日志

### v4.2 (2026-04-16)

- ✨ 交互式K线图 (lightweight-charts)
- ✨ 鲸鱼行为数据集成
- ✨ DeFi TVL 数据
- ✨ CLI工具 (5个命令)
- ✨ PyPI打包准备
- 🔧 链上数据模块重构
- 🗑️ 清理冗余文件

### v4.0 (2026-04-16)

- ✨ HTML报告重构 (卡片式 + 响应式)
- ✨ 叠buff信号系统
- ✨ 形态识别 (头肩/双顶双底)
- ✨ 技术面专业解读
- ✨ 结论详细分析

### v3.2 (2026-04-15)

- 🔌 插件系统重构
- 📊 FinanceToolkit集成
- ✅ 回测验证引擎
- 💼 组合优化器

---

## 📦 PyPI发布

### 安装

```bash
pip install neo9527-finance-skill
```

### 使用

```bash
# 方式1: 命令行
neo-finance report BTC-USD --format html

# 方式2: Python API
from neo9527_finance_skill import analyze_complete

result = analyze_complete('BTC-USD')
print(f"Score: {result['conclusion']['score']}/100")
print(f"Decision: {result['conclusion']['decision']}")
```

---

## 🛠️ 开发指南

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/beautifulboy9527/Neo9527-unified-finance-skill.git
cd Neo9527-unified-finance-skill

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements.txt -e ".[dev]"
```

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 生成覆盖率报告
pytest --cov=scripts tests/
```

---

## 📄 License

MIT License

---

## 👤 Author

**Neo9527**

- GitHub: [@beautifulboy9527](https://github.com/beautifulboy9527)
- Email: beautifulboy9527@gmail.com

---

## 🙏 Acknowledgments

感谢以下开源项目:

- [yfinance](https://github.com/ranaroussi/yfinance)
- [pandas](https://pandas.pydata.org/)
- [lightweight-charts](https://www.tradingview.com/lightweight-charts/)
- [DeFiLlama](https://defillama.com/)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [Blockchain.com API](https://www.blockchain.com/api)

---

## 🗺️ 路线图

- [ ] Phase 12.4: 测试覆盖 (80%+)
- [ ] Phase 13: 多语言支持
- [ ] Phase 14: ML增强
- [ ] Phase 15: 移动端适配

---

**Star ⭐ 本项目以获取最新更新！**
