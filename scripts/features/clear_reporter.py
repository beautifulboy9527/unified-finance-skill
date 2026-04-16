#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成器 - 生成清晰易懂的分析报告
"""

import sys
import os
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def generate_clear_report(symbol: str, score_result: dict, risk_result: dict, 
                          signals_result: dict, technical_result: dict) -> str:
    """
    生成清晰易懂的分析报告
    
    Args:
        symbol: 股票代码
        score_result: 评分结果
        risk_result: 风险管理结果
        signals_result: 入场信号结果
        technical_result: 技术分析结果
    
    Returns:
        Markdown 格式的清晰报告
    """
    
    report = f"""# {symbol} 深度分析报告

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**综合评分**: {score_result.get('total_score', 0)}/100  
**评级**: {score_result.get('level', '未知')} ({score_result.get('rating', 'unknown')})  
**操作建议**: {score_result.get('suggestion', '观望')}

---

## 📊 一、当前状态分析 (实时)

> **说明**: 以下是基于当前市场数据的实时状态分析

### 1.1 技术面状态

"""
    
    # 技术分析
    if technical_result:
        basic = technical_result.get('basic_indicators', {})
        trend = basic.get('trend', 'unknown')
        rsi = basic.get('rsi', 0)
        ma5 = basic.get('ma5', 0)
        ma20 = basic.get('ma20', 0)
        current_price = basic.get('current_price', 0)
        
        report += f"""| 指标 | 当前值 | 状态 | 解读 |
|------|--------|------|------|
| 当前价格 | {current_price:.2f} 元 | - | 实时价格 |
| 趋势 | {trend} | {'📈 多头' if trend == 'uptrend' else '📉 空头' if trend == 'downtrend' else '➡️ 震荡'} | 当前走势方向 |
| RSI | {rsi:.1f} | {'⚠️ 超买' if rsi > 70 else '⚠️ 超卖' if rsi < 30 else '✅ 正常'} | 相对强弱 |
| MA5 | {ma5:.2f} 元 | {'高于' if current_price > ma5 else '低于'} | 短期均线 |
| MA20 | {ma20:.2f} 元 | {'高于' if current_price > ma20 else '低于'} | 中期均线 |

**技术面结论**: 当前处于{'上升' if trend == 'uptrend' else '下降' if trend == 'downtrend' else '震荡'}趋势，RSI 为 {rsi:.1f}，{'接近超买区间' if rsi > 65 else '接近超卖区间' if rsi < 35 else '处于正常区间'}。

"""
    
    # 入场信号
    report += """---

## 🎯 二、入场信号检测

> **检测原理**: 扫描当前股价走势，匹配历史验证的信号模式
> 
> **结果说明**: 
> - ✅ 已触发 = 当前股价已符合该信号特征，信号有效
> - 未列出 = 当前股价不符合该信号特征，信号未触发

"""
    
    if signals_result and signals_result.get('signals'):
        report += "### 当前已触发的信号:\n\n"
        for i, signal in enumerate(signals_result['signals'], 1):
            report += f"""**{i}. {signal.get('name', '未知信号')}** ✅ 已触发

- **信号类型**: {signal.get('action', 'hold')}
- **历史成功率**: {signal.get('success_rate', 0)*100:.0f}% (基于 {signal.get('samples', 0)} 个历史样本)
- **当前置信度**: {signal.get('confidence', 0)*100:.0f}%
- **风险等级**: {signal.get('risk_level', 'medium')}

"""
        
        score_info = signals_result.get('score', {})
        report += f"""### 信号综合评估:

- **信号评分**: {score_info.get('overall_score', 0)}/100
- **建议操作**: {score_info.get('action', 'hold')}
- **风险等级**: {score_info.get('risk_level', 'unknown')}

"""
    else:
        report += """### 当前未触发任何信号

**解读**: 当前股价走势未匹配到任何高成功率信号模式

**建议**:
- 📌 继续观望，等待信号触发
- 📌 或降低仓位，谨慎参与

"""
    
    # 风险管理
    report += """---

## ⚠️ 三、风险管理建议 (假设入场)

> **说明**: 以下是基于当前价格计算的风险管理参数
> 
> **重要**: 这是"如果现在入场"的建议，并非预测未来价格

"""
    
    if risk_result and not risk_result.get('error'):
        summary = risk_result.get('summary', {})
        report += f"""### 入场方案 (基于当前价格):

| 项目 | 数值 | 说明 |
|------|------|------|
| **假设入场价** | {summary.get('entry_price', 'N/A')} 元 | 当前价格 |
| **建议止损价** | {summary.get('stop_loss', 'N/A')} 元 | ATR动态止损 |
| **止损比例** | {summary.get('stop_loss_pct', 'N/A')}% | 单笔最大亏损 |
| **目标价** | {summary.get('target_price', 'N/A')} 元 | 2:1风险收益比 |
| **预期收益** | {summary.get('target_return_pct', 'N/A')}% | 如达目标价 |
| **建议仓位** | {summary.get('shares', 'N/A')} 股 | 基于2%风险 |
| **仓位金额** | {summary.get('position_value', 'N/A')} 元 | 约 {summary.get('position_value', 0)/10000:.1f} 万 |

### 风险收益分析:

- **风险**: 入场后如果触及止损，亏损约 {summary.get('risk_amount', 0):.0f} 元 (2%本金)
- **收益**: 入场后如果达到目标价，盈利约 {summary.get('risk_amount', 0)*2:.0f} 元
- **风险收益比**: 1:2 (每承担1元风险，可能获得2元收益)

"""
    else:
        report += "*无法计算风险管理参数 (数据不足)*\n\n"
    
    # 综合评分
    report += f"""---

## 📈 四、综合评分

| 维度 | 得分 | 满分 | 权重说明 |
|------|------|------|---------|
| 宏观环境 | {score_result['breakdown']['macro']} | 20 | 市场周期 + 北向资金 |
| 行业分析 | {score_result['breakdown']['sector']} | 20 | 板块强度 + 资金流向 |
| 技术分析 | {score_result['breakdown']['technical']} | 60 | 趋势 + 动能 + 量价 |
| 信号加成 | {score_result['breakdown']['signal_bonus']} | ±10 | 入场信号加成 |
| **总分** | **{score_result['total_score']}** | **100** | - |

"""
    
    # 操作建议
    action = score_result.get('action', 'hold')
    level = score_result.get('level', '未知')
    suggestion = score_result.get('suggestion', '观望')
    
    # 统一结论模块
    report += f"""---

## 🎯 五、统一结论

### 各模块分析汇总:

| 模块 | 结果 | 方向 |
|------|------|------|
| 技术分析 | {'上升趋势' if technical_result and technical_result.get('basic_indicators', {}).get('trend') == 'uptrend' else '下降趋势' if technical_result and technical_result.get('basic_indicators', {}).get('trend') == 'downtrend' else '震荡'} | {'🟢 偏多' if technical_result and technical_result.get('ai_decision', {}).get('recommendation') == 'buy' else '🔴 偏空' if technical_result and technical_result.get('ai_decision', {}).get('recommendation') == 'sell' else '🟡 中性'} |
| 入场信号 | {'已触发 ' + str(len(signals_result.get('signals', []))) + ' 个信号' if signals_result and signals_result.get('signals') else '未触发信号'} | {'🟢 看多' if signals_result and signals_result.get('score', {}).get('action') == 'buy' else '🔴 看空' if signals_result and signals_result.get('score', {}).get('action') == 'sell' else '🟡 中性'} |
| 风险管理 | 可入场 | {'🟢 支持' if not risk_result.get('error') else '🔴 不支持'} |
| 综合评分 | {score_result['total_score']}/100 ({level}) | {'🟢 偏多' if score_result['total_score'] >= 65 else '🟡 中性' if score_result['total_score'] >= 50 else '🔴 偏空'} |

### 最终结论:

"""
    
    # 多数投票
    bullish_count = 0
    bearish_count = 0
    
    if technical_result and technical_result.get('ai_decision', {}).get('recommendation') == 'buy':
        bullish_count += 1
    elif technical_result and technical_result.get('ai_decision', {}).get('recommendation') == 'sell':
        bearish_count += 1
    
    if signals_result and signals_result.get('score', {}).get('action') == 'buy':
        bullish_count += 1
    elif signals_result and signals_result.get('score', {}).get('action') == 'sell':
        bearish_count += 1
    
    if score_result['total_score'] >= 65:
        bullish_count += 1
    elif score_result['total_score'] < 50:
        bearish_count += 1
    
    if bullish_count > bearish_count:
        final_direction = '偏多 🟢'
        final_action = '可考虑买入或加仓'
    elif bearish_count > bullish_count:
        final_direction = '偏空 🔴'
        final_action = '建议观望或减仓'
    else:
        final_direction = '中性 🟡'
        final_action = '建议观望'
    
    report += f"""**方向判断**: {final_direction} ({bullish_count} 票看多, {bearish_count} 票看空)

**建议操作**: {final_action}

**详细建议**: {suggestion}

"""
    
    # 操作流程建议
    report += f"""---

## 💡 六、操作流程建议

"""
    
    if action == 'buy':
        report += """1. **确认信号**: 检查入场信号是否已出现 ✅
2. **设置止损**: 挂单买入同时设置止损价 (重要!)
3. **控制仓位**: 按建议仓位买入，不要满仓
4. **设定目标**: 到达目标价后考虑止盈
5. **严格执行**: 触及止损价必须卖出，不要犹豫

"""
    elif action == 'hold':
        report += """1. **继续观望**: 当前信号不明确
2. **等待机会**: 关注是否出现入场信号
3. **控制仓位**: 如需参与，建议小仓位试探
4. **设置止损**: 必须设置止损保护

"""
    elif action == 'reduce':
        report += """1. **减仓或观望**: 当前有风险信号
2. **检查持仓**: 如有持仓，考虑减仓
3. **谨慎操作**: 不建议新开仓位
4. **等待转机**: 等待信号好转再参与

"""
    else:  # avoid
        report += """1. **回避**: 当前风险较大
2. **不要入场**: 等待评分改善
3. **如有持仓**: 建议止损离场

"""
    
    # 风险提示
    report += """---

## ⚠️ 重要提示

1. **本报告仅供参考**，不构成投资建议
2. **股市有风险**，入市需谨慎
3. **历史信号成功率不代表未来**，仅供参考
4. **严格执行止损**是风险控制的关键
5. **建议结合其他数据源**验证分析结果

---

*数据来源: agent-stock, akshare, yfinance*  
*分析工具: Unified Finance Skill*  
*报告生成: 小灰灰 🐕*
"""
    
    return report


if __name__ == '__main__':
    # 测试
    print("Report generator loaded successfully")
