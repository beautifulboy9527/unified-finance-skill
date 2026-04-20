#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整Markdown报告生成器 v1.0
- 包含所有分析模块
- 详细解读
- 中文为主
"""

import sys
from typing import Dict
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def generate_markdown_report(result: Dict) -> str:
    """生成完整的Markdown报告"""
    
    symbol = result.get('symbol', '')
    name_cn = result.get('name_cn', symbol)
    score = result.get('score', 0)
    recommendation = result.get('recommendation', 'N/A')
    
    md = f'''# 📊 {name_cn} ({symbol}) 投资分析报告

**报告时间**: {result.get('timestamp', '')}  
**数据来源**: yfinance + 专业分析模块  
**综合评分**: **{score}/100**  
**投资建议**: **{recommendation}**

---

## 一、基础信息

| 项目 | 数值 |
|------|------|
| 股票名称 | {name_cn} |
| 股票代码 | {symbol} |
| 所属市场 | {result.get('market', 'N/A')} |
| 所属行业 | {result.get('industry', {}).get('name_cn', 'N/A')} |
| 所属板块 | {result.get('industry', {}).get('sector', 'N/A')} |
| 当前价格 | **{result.get('price', {}).get('current', 0):.2f}元** |
| 今日涨跌 | **{result.get('price', {}).get('change_pct', 0):+.2f}%** |
| 总市值 | {result.get('valuation', {}).get('market_cap_str', 'N/A')} |

---

## 二、行业分析

### 2.1 行业定位

| 指标 | 数值 |
|------|------|
| 所属行业 | {result.get('industry', {}).get('name_cn', 'N/A')} |
| 所属板块 | {result.get('industry', {}).get('sector', 'N/A')} |
| 行业周期 | {result.get('industry', {}).get('cycle', '未知')} |
| 行业风险 | {result.get('industry', {}).get('risk', '未知')} |

### 2.2 行业分析解读

{result.get('industry', {}).get('analysis', '暂无分析')}

---

## 三、估值分析

### 3.1 估值指标

| 指标 | 数值 | 评价 |
|------|------|------|
| 市盈率 PE | **{result.get('valuation', {}).get('pe', 0):.2f}** | {_get_pe_eval(result.get('valuation', {}).get('pe', 0))} |
| 市净率 PB | **{result.get('valuation', {}).get('pb', 0):.2f}** | {_get_pb_eval(result.get('valuation', {}).get('pb', 0))} |
| 市销率 PS | **{result.get('valuation', {}).get('ps', 0):.2f}** | - |
| 总市值 | **{result.get('valuation', {}).get('market_cap_str', 'N/A')}** | - |

### 3.2 估值分析解读

{result.get('valuation', {}).get('analysis', '暂无分析')}

---

## 四、盈利能力

### 4.1 盈利指标

| 指标 | 数值 | 评价 |
|------|------|------|
| 净资产收益率 ROE | **{result.get('profitability', {}).get('roe', 0)*100:.2f}%** | {_get_roe_eval(result.get('profitability', {}).get('roe', 0))} |
| 毛利率 | **{result.get('profitability', {}).get('gross_margin', 0)*100:.2f}%** | - |
| 净利率 | **{result.get('profitability', {}).get('net_margin', 0)*100:.2f}%** | - |
| 盈利状态 | **{'盈利' if result.get('profitability', {}).get('is_profitable') else '亏损'}** | {'✅' if result.get('profitability', {}).get('is_profitable') else '❌'} |

### 4.2 盈利能力解读

{result.get('profitability', {}).get('analysis', '暂无分析')}

---

## 五、财务健康

### 5.1 财务指标

| 指标 | 数值 | 评价 |
|------|------|------|
| 资产负债率 | **{result.get('financial', {}).get('debt_ratio', 0):.2f}%** | {_get_debt_eval(result.get('financial', {}).get('debt_ratio', 0))} |
| 流动比率 | **{result.get('financial', {}).get('current_ratio', 0):.2f}** | {_get_liquidity_eval(result.get('financial', {}).get('current_ratio', 0))} |
| 财务状态 | **{result.get('financial', {}).get('status', 'N/A')}** | - |

**数据来源**: {result.get('financial', {}).get('data_source', '财报')} (置信度: {result.get('financial', {}).get('confidence', 0)*100:.0f}%)

### 5.2 风险提示

'''

    risks = result.get('financial', {}).get('risks', [])
    if risks:
        for risk in risks:
            md += f"- ⚠️ {risk}\n"
    else:
        md += "- ✅ 暂无明显风险\n"
    
    md += f'''
### 5.3 财务健康解读

{result.get('financial', {}).get('analysis', '暂无分析')}

---

## 六、技术分析

### 6.1 核心技术指标

| 指标 | 数值 | 状态 |
|------|------|------|
| RSI 相对强弱 | **{result.get('technical', {}).get('indicators', {}).get('rsi', 50):.1f}** | {result.get('technical', {}).get('patterns', {}).get('rsi_desc', 'N/A')} |
| MACD 状态 | **{str(result.get('technical', {}).get('patterns', {}).get('macd_desc', 'N/A')).split('(')[0].strip()}** | {'看涨' if '金叉' in str(result.get('technical', {}).get('patterns', {}).get('macd_desc', '')) else '看跌'} |
| 趋势判断 | **{str(result.get('technical', {}).get('patterns', {}).get('trend_desc', 'N/A')).split('(')[0].strip()}** | - |
| 信号强度 | **{result.get('technical', {}).get('signal_strength', 0)}** | - |

### 6.2 技术形态分析

'''

    # 技术形态
    patterns = result.get('technical', {}).get('patterns', {})
    
    if patterns.get('trend_desc'):
        md += f"- **趋势**: {patterns['trend_desc']}\n"
    if patterns.get('rsi_desc'):
        md += f"- **RSI**: {patterns['rsi_desc']}\n"
    if patterns.get('macd_desc'):
        md += f"- **MACD**: {patterns['macd_desc']}\n"
    if patterns.get('bb_desc'):
        md += f"- **布林带**: {patterns['bb_desc']}\n"
    if patterns.get('double_top_desc'):
        md += f"- **形态**: {patterns['double_top_desc']}\n"
    if patterns.get('double_bottom_desc'):
        md += f"- **形态**: {patterns['double_bottom_desc']}\n"
    
    md += f'''

### 6.3 支撑阻力位

| 类型 | 价位 | 距离 |
|------|------|------|
| 近期支撑 | **{result.get('technical', {}).get('support_near', 0):.2f}元** | {result.get('technical', {}).get('support_near_pct', 0):.1f}% |
| 远期支撑 | **{result.get('technical', {}).get('support_far', 0):.2f}元** | {result.get('technical', {}).get('support_far_pct', 0):.1f}% |
| 近期阻力 | **{result.get('technical', {}).get('resistance_near', 0):.2f}元** | +{result.get('technical', {}).get('resistance_near_pct', 0):.1f}% |
| 远期阻力 | **{result.get('technical', {}).get('resistance_far', 0):.2f}元** | +{result.get('technical', {}).get('resistance_far_pct', 0):.1f}% |

**支撑解读**: {result.get('technical', {}).get('patterns', {}).get('support_desc', '暂无数据')}

**阻力解读**: {result.get('technical', {}).get('patterns', {}).get('resistance_desc', '暂无数据')}

### 6.4 成交量验证

| 指标 | 数值 | 状态 |
|------|------|------|
| 成交量比率 | **{result.get('volume_validation', {}).get('volume_ratio', 1):.2f}x** | {_get_volume_eval(result.get('volume_validation', {}).get('volume_ratio', 1))} |
| 成交量状态 | **{result.get('volume_validation', {}).get('status', 'N/A')}** | - |
| 趋势确认 | **{result.get('volume_validation', {}).get('trend_confirmation', 'N/A')}** | - |

**成交量解读**: {result.get('volume_validation', {}).get('analysis', '暂无分析')}

### 6.5 技术分析综合解读

{result.get('technical', {}).get('analysis', '暂无分析')}

---

## 七、风险管理

### 7.1 ATR止损建议

| 指标 | 数值 |
|------|------|
| 当前价格 | **{result.get('risk_management', {}).get('current_price', 0):.2f}元** |
| ATR值 | **{result.get('risk_management', {}).get('atr', 0):.2f}** |
| 标准止损 | **{result.get('risk_management', {}).get('stop_loss_price', 0):.2f}元** |
| 止损幅度 | **{result.get('risk_management', {}).get('risk_pct', 0):.1f}%** |

### 7.2 止损策略解读

{result.get('risk_management', {}).get('analysis', '暂无分析')}

---

## 八、Buff叠加分析

'''

    # Buff分析
    buffs = _calculate_buffs(result)
    
    md += "| Buff类型 | 分值 | 描述 |\n"
    md += "|----------|------|------|\n"
    
    for buff_type, score, desc, color in buffs:
        md += f"| **{buff_type}** | **{score}** | {desc} |\n"
    
    total = sum([int(b[1]) for b in buffs])
    total_text = '偏多' if total > 0 else ('偏空' if total < 0 else '中性')
    
    md += f"| **总Buff** | **{total:+d}** | **{total_text}** (综合评分 {score}/100) |\n"
    
    md += f'''

---

## 九、汇总分析

### 9.1 行业周期分析

{result.get('summary', {}).get('industry_analysis', '暂无分析')}

### 9.2 盈利能力推演

{result.get('summary', {}).get('profit_analysis', '暂无分析')}

### 9.3 估值水平分析

{result.get('summary', {}).get('valuation_analysis', '暂无分析')}

### 9.4 财务健康评估

{result.get('summary', {}).get('financial_analysis', '暂无分析')}

### 9.5 技术面判断

{result.get('summary', {}).get('tech_analysis', '暂无分析')}

### 9.6 综合投资建议

{result.get('summary', {}).get('final', '暂无分析')}

---

## 十、操作建议

{_generate_action_advice_md(result)}

---

## 十一、风险提示

⚠️ **重要提示**:
- 本报告基于公开数据分析，仅供参考，不构成投资建议
- 投资有风险，入市需谨慎
- 数据来源: yfinance
- 分析时间: {result.get('timestamp', '')}

---

**报告生成**: A股分析器 v3.0  
**数据来源**: yfinance + 专业分析模块
'''
    
    return md


def _get_pe_eval(pe: float) -> str:
    if pe < 15: return '低估 ✅'
    elif pe < 25: return '合理 ✅'
    elif pe < 40: return '偏高 ⚠️'
    return '高估 ❌'

def _get_pb_eval(pb: float) -> str:
    if pb < 2: return '低估 ✅'
    elif pb < 4: return '合理 ✅'
    elif pb < 6: return '偏高 ⚠️'
    return '高估 ❌'

def _get_roe_eval(roe: float) -> str:
    if roe > 0.20: return '优秀 ✅'
    elif roe > 0.15: return '良好 ✅'
    elif roe > 0.10: return '一般 ⚠️'
    return '较差 ❌'

def _get_debt_eval(debt: float) -> str:
    if debt < 40: return '低风险 ✅'
    elif debt < 60: return '适中 ✅'
    elif debt < 70: return '需关注 ⚠️'
    return '高风险 ❌'

def _get_liquidity_eval(ratio: float) -> str:
    if ratio > 2: return '流动性好 ✅'
    elif ratio > 1: return '流动性正常 ✅'
    elif ratio > 0.5: return '流动性不足 ⚠️'
    return '流动性风险 ❌'

def _get_volume_eval(ratio: float) -> str:
    if ratio > 2: return '放量 ✅'
    elif ratio > 1.5: return '温和放量 ✅'
    elif ratio > 0.8: return '正常 ✅'
    return '缩量 ⚠️'

def _calculate_buffs(result: Dict) -> list:
    buffs = []
    
    # 基本面buff
    roe = result.get('profitability', {}).get('roe', 0)
    if roe > 0.20:
        buffs.append(('基本面', '+3', f'ROE优秀({roe*100:.1f}%)，盈利能力强', '#22c55e'))
    elif roe > 0.15:
        buffs.append(('基本面', '+2', f'ROE良好({roe*100:.1f}%)，盈利稳健', '#22c55e'))
    elif roe > 0.10:
        buffs.append(('基本面', '+1', f'ROE一般({roe*100:.1f}%)', '#f59e0b'))
    else:
        buffs.append(('基本面', '-1', f'ROE较差({roe*100:.1f}%)', '#ef4444'))
    
    # 估值buff
    pe = result.get('valuation', {}).get('pe', 0)
    if pe and pe < 15:
        buffs.append(('估值', '+2', f'PE低估({pe:.1f})，安全边际高', '#22c55e'))
    elif pe and pe < 25:
        buffs.append(('估值', '+1', f'PE合理({pe:.1f})', '#f59e0b'))
    elif pe and pe > 40:
        buffs.append(('估值', '-2', f'PE高估({pe:.1f})，估值偏高', '#ef4444'))
    
    # 财务健康buff
    status = result.get('financial', {}).get('status', '')
    debt_ratio = result.get('financial', {}).get('debt_ratio', 0)
    if status == '健康':
        buffs.append(('财务', '+1', f'财务健康，资产负债率{debt_ratio:.1f}%', '#22c55e'))
    elif status == '需关注':
        buffs.append(('财务', '-1', f'财务需关注，资产负债率{debt_ratio:.1f}%', '#f59e0b'))
    elif status == '高风险':
        buffs.append(('财务', '-2', f'财务风险高，资产负债率{debt_ratio:.1f}%', '#ef4444'))
    
    # 技术面buff
    signal = result.get('technical', {}).get('signal_strength', 0)
    if signal > 3:
        buffs.append(('技术面', '+2', f'技术面强势，信号强度{signal}', '#22c55e'))
    elif signal > 0:
        buffs.append(('技术面', '+1', f'技术面偏多，信号强度{signal}', '#22c55e'))
    elif signal < -3:
        buffs.append(('技术面', '-2', f'技术面弱势，信号强度{signal}', '#ef4444'))
    elif signal < 0:
        buffs.append(('技术面', '-1', f'技术面偏空，信号强度{signal}', '#ef4444'))
    
    return buffs

def _generate_action_advice_md(result: Dict) -> str:
    tech = result.get('technical', {})
    volume = result.get('volume_validation', {})
    price = result.get('price', {})
    
    current = price.get('current', 0)
    support_near = tech.get('support_near', 0)
    resistance_near = tech.get('resistance_near', 0)
    rsi = tech.get('indicators', {}).get('rsi', 50)
    volume_ratio = volume.get('volume_ratio', 1)
    trend = str(tech.get('patterns', {}).get('trend_desc', '')).split('(')[0].strip()
    
    advice = []
    
    # 趋势建议
    if '多头' in trend:
        advice.append(f"✅ 当前处于{trend}，趋势向上，可考虑持股或逢低加仓")
    elif '空头' in trend:
        advice.append(f"⚠️ 当前处于{trend}，趋势向下，建议观望或减仓")
    else:
        advice.append(f"➡️ 当前趋势{trend}，建议观望等待方向明确")
    
    # RSI建议
    if rsi > 80:
        advice.append(f"⚠️ RSI={rsi:.1f}极度超买，短期回调风险大，不建议追高")
    elif rsi > 70:
        advice.append(f"⚠️ RSI={rsi:.1f}超买，注意回调风险，可考虑逢高减仓")
    elif rsi < 30:
        advice.append(f"✅ RSI={rsi:.1f}超卖，可能存在反弹机会，可关注")
    
    # 支撑阻力建议
    if current and support_near:
        support_pct = (current - support_near) / current * 100
        advice.append(f"📍 近期支撑位{support_near:.2f}元(距离{support_pct:.1f}%)，跌破支撑需警惕")
    
    if current and resistance_near:
        resistance_pct = (resistance_near - current) / current * 100
        advice.append(f"📍 近期阻力位{resistance_near:.2f}元(距离{resistance_pct:.1f}%)，突破阻力可加仓")
    
    # 成交量建议
    if volume_ratio > 1.5:
        advice.append(f"✅ 成交量放大{volume_ratio:.2f}倍，市场活跃度高，趋势可信")
    elif volume_ratio < 0.8:
        advice.append(f"⚠️ 成交量萎缩至{volume_ratio:.2f}倍，市场观望情绪浓，注意风险")
    
    return '\n\n'.join(advice)


if __name__ == '__main__':
    print("Markdown报告生成器 v1.0")
