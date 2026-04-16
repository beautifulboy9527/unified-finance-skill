# Phase 12 开发计划

**版本目标**: v4.5 - 可视化增强 + 数据冗余 + 生产化

---

## 📊 Phase 12.1: 可视化增强 (最高优先)

### 目标
嵌入交互式 K 线图，让 HTML 报告"活"起来

### 技术方案

#### 方案 A: lightweight-charts (推荐)
```html
<!-- CDN 引入 -->
<script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>

<!-- 嵌入图表 -->
<div id="kline-chart"></div>
<script>
const chart = LightweightCharts.createChart(document.getElementById('kline-chart'), {
    width: 800,
    height: 400
});

const candlestickSeries = chart.addCandlestickSeries();
candlestickSeries.setData(klineData);

// 添加均线
const ma5Line = chart.addLineSeries({ color: 'blue' });
ma5Line.setData(ma5Data);
</script>
```

**优点**:
- ✅ 纯 JS，无需构建
- ✅ 轻量 (40KB)
- ✅ 支持缩放/拖拽
- ✅ 专业金融图表库

#### 方案 B: Plotly (已有基础)
```python
import plotly.graph_objects as go

fig = go.Figure(data=[
    go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )
])

# 转为 HTML
plotly_html = fig.to_html(include_plotlyjs='cdn', full_html=False)
```

### 实施步骤
1. 在 `complete_crypto_analyzer.py` 添加 K 线数据获取
2. 在 `report_generator_v4.py` 添加图表生成逻辑
3. 在 HTML 模板嵌入图表区域
4. 测试交互功能

### 预期效果
```
三、技术分析
    3.1 K线图 (交互式) ✨
        - 缩放/拖拽
        - MA5/MA10/MA20 叠加
        - 成交量柱状图
    3.2 核心指标
    3.3 支撑阻力
    ...
```

---

## 🔗 Phase 12.2: 数据冗余 + 鲸鱼数据

### 目标
补充链上大单/鲸鱼行为数据

### 免费数据源

#### 1. DeFiLlama API
```python
def get_defillama_data(chain="ethereum"):
    """获取 DeFi TVL 数据"""
    url = f"https://api.llama.fi/protocols"
    resp = requests.get(url)
    
    # 筛选目标链
    protocols = [p for p in resp.json() if p['chain'] == chain]
    
    return {
        'total_tvl': sum(p['tvl'] for p in protocols),
        'top_protocols': sorted(protocols, key=lambda x: x['tvl'], reverse=True)[:5],
        'data_source': 'DeFiLlama'
    }
```

#### 2. Dune Analytics 公开查询
```python
def get_whale_transactions(dune_query_id):
    """获取鲸鱼转账数据"""
    url = f"https://api.dune.com/api/v1/query/{dune_query_id}/results"
    # 需要免费注册获取 API key
    headers = {"X-Dune-API-Key": "YOUR_FREE_KEY"}
    resp = requests.get(url, headers=headers)
    
    return {
        'large_transfers': resp.json()['result']['rows'],
        'data_source': 'Dune Analytics'
    }
```

#### 3. CoinMarketCap API (备用)
```python
def get_cmc_data(symbol):
    """CoinGecko 备用数据源"""
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": "YOUR_FREE_KEY"}
    params = {"symbol": symbol}
    
    # 免费额度: 333 calls/day
    resp = requests.get(url, headers=headers, params=params)
    return resp.json()
```

### 报告新增内容
```
四、链上数据
    4.1 网络状态
        - 算力/难度/流通量
    4.2 DeFi 数据 ✨
        - TVL 变化: +12%
        - Top 5 协议
    4.3 鲸鱼行为 ✨
        - 24h 大单流入: +1,240 BTC
        - 鲸鱼地址活跃度
```

---

## 📦 Phase 12.3: 生产化 & CLI

### 1. CLI 命令标准化
```bash
# 完整报告
python finance.py report BTC-USD --format html --with-chart

# 快速分析
python finance.py analyze ETH-USD --period medium

# 信号检测
python finance.py signals BTC-USD --timeframe 4h

# 组合优化
python finance.py optimize portfolio.json --output excel
```

### 2. PyPI 打包
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="neo9527-finance-skill",
    version="4.5.0",
    packages=find_packages(),
    install_requires=[
        'yfinance>=0.2.0',
        'pandas>=1.5.0',
        'requests>=2.28.0',
        'matplotlib>=3.6.0',
        'plotly>=5.0.0',
    ],
    entry_points={
        'console_scripts': [
            'neo-finance=finance:main',
        ],
    },
)
```

### 3. 文档完善
- API 文档 (Sphinx)
- 使用示例 (Jupyter Notebook)
- 部署指南

---

## 🧪 Phase 12.4: 测试 & 质量保证

### pytest 覆盖
```python
# tests/test_buff_logic.py
def test_buff_calculation():
    signals = [
        {'strength': 5},
        {'strength': -2},
        {'strength': 3}
    ]
    total = sum(s['strength'] for s in signals)
    assert total == 6

def test_pattern_detection():
    result = analyze_complete('BTC-USD')
    patterns = result['patterns']
    assert 'trend' in patterns
    assert patterns['trend'] in ['uptrend', 'downtrend', 'sideways']
```

### 质量检查
- ✅ 代码覆盖率 > 80%
- ✅ 类型提示 (mypy)
- ✅ 代码风格 (black/isort)
- ✅ 安全检查 (bandit)

---

## 📅 实施时间表

### Week 1 (2026-04-17 ~ 04-23)
- [ ] Day 1-2: K 线图嵌入 (lightweight-charts)
- [ ] Day 3-4: DeFiLlama + Dune 集成
- [ ] Day 5: CLI 标准化

### Week 2 (2026-04-24 ~ 04-30)
- [ ] Day 1-2: pytest 覆盖
- [ ] Day 3: PyPI 打包
- [ ] Day 4-5: 文档完善

### Week 3 (2026-05-01 ~ 05-07)
- [ ] 测试 & 优化
- [ ] 社区发布准备

---

## 🎯 成功指标

| 指标 | 当前 | 目标 |
|------|------|------|
| 代码行数 | 5,200+ | 6,500+ |
| 测试覆盖率 | 0% | 80%+ |
| 文档完整度 | 60% | 95% |
| PyPI 下载量 | 0 | 100+ |
| GitHub Stars | - | 50+ |

---

## 📚 参考资源

### 开源项目
- [Crypto-Panda](https://github.com/sjmoran/crypto-panda) - 报告模板参考
- [Freqtrade](https://github.com/freqtrade/freqtrade) - 回测框架参考
- [FinRobot](https://github.com/ai4finance-foundation/finrobot) - Agent 编排参考

### 数据源
- [DeFiLlama API](https://defillama.com/docs/api) - 免费 DeFi 数据
- [Dune Analytics](https://dune.com) - 链上 SQL 查询
- [CoinMarketCap API](https://coinmarketcap.com/api) - 备用市场数据

### 可视化
- [lightweight-charts](https://www.tradingview.com/lightweight-charts/) - 金融图表库
- [Plotly](https://plotly.com/python/) - 交互式图表

---

**创建时间**: 2026-04-16
**最后更新**: 2026-04-16
**状态**: 📝 规划中
