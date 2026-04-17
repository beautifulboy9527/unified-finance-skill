---
name: shared-modules
description: >
  共享模块 - 跨资产类型复用的通用能力
  
  包含模块:
  - citation-validator: 引用验证体系
  - risk-monitor: 风险监控清单
  
  使用方法:
  from skills.shared import CitationValidator, RiskMonitor
  
version: 1.0.0
author: Neo9527
---

# 共享模块 (Shared Modules)

> 可跨资产类型复用的通用能力模块

## 模块列表

| 模块 | 说明 | 文档 |
|------|------|------|
| citation-validator | A-E级数据来源评级 | [SKILL.md](citation-validator/SKILL.md) |
| risk-monitor | 三级风险监控清单 | [SKILL.md](risk-monitor/SKILL.md) |

---

## 快速使用

### Python 导入

```python
# 引用验证
from skills.shared.citation_validator.validator import CitationValidator

validator = CitationValidator()
rating = validator.get_rating("DeFiLlama")  # 'B'
citation = validator.cite("DeFiLlama", "https://defillama.com", "2026-04-17")

# 风险监控
from skills.shared.risk_monitor.monitor import RiskMonitor

monitor = RiskMonitor(asset_type='crypto')
status = monitor.check({
    'tvl_change_24h': -12,
    'whale_holding_change_7d': 3.5
})
```

### 整合到现有 Skill

```python
# 在报告生成器中添加引用验证
def generate_report_with_citations(symbol):
    from skills.shared.citation_validator.validator import CitationValidator
    validator = CitationValidator()
    
    # 获取数据时标注来源
    data = fetch_data(symbol)
    for item in data:
        item['citation'] = validator.cite(
            source=item['source'],
            url=item['url'],
            date=item['date']
        )
    
    return generate_html(data)

# 在报告中添加监控清单
def add_monitoring_to_report(report, symbol, asset_type='crypto'):
    from skills.shared.risk_monitor.monitor import RiskMonitor
    monitor = RiskMonitor(asset_type=asset_type)
    
    checklist = monitor.generate_checklist_html(symbol)
    report.add_section('监控清单', checklist)
    
    return report
```

---

## 设计原则

1. **独立可复用**: 每个模块可独立使用
2. **资产类型适配**: 支持加密货币/股票等不同资产
3. **轻量级**: 避免复杂依赖
4. **标准化接口**: 统一的使用方式

---

*by Neo9527 Finance Skill v4.8 | 2026-04-17*
