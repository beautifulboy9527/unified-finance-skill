#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新版报告生成器 (v4.0)
使用完整分析器 + 叠buff逻辑
"""

import sys
import os
from datetime import datetime
from typing import Dict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def generate_crypto_report_v4(symbol: str, output_dir: str = "D:\\OpenClaw\\outputs\\reports") -> str:
    """
    生成加密货币报告 v4.0
    
    Args:
        symbol: 交易对 (BTC-USD)
        output_dir: 输出目录
        
    Returns:
        报告文件路径
    """
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from features.complete_crypto_analyzer import analyze_complete
    
    print(f"正在分析 {symbol}...")
    
    # 1. 完整分析
    result = analyze_complete(symbol)
    
    # 2. 提取数据
    market = result.get('market', {})
    technical = result.get('technical', {})
    indicators = technical.get('indicators', {})
    patterns = result.get('patterns', {})
    onchain = result.get('onchain', {})
    signals = result.get('signals', [])
    conclusion = result.get('conclusion', {})
    
    # 3. 准备模板变量
    template_vars = {
        'symbol': symbol,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'score': conclusion.get('score', 50),
        
        # 市场数据
        'price': market.get('price', 0),
        'change_24h': market.get('change_24h', 0),
        'change_desc': '📈 上涨' if market.get('change_24h', 0) > 0 else '📉 下跌',
        'high_24h': market.get('high_24h', 0),
        'low_24h': market.get('low_24h', 0),
        'volume_24h': market.get('volume_24h', 0),
        'volume_24h_b': market.get('volume_24h', 0) / 1e9,
        'market_cap': market.get('market_cap', 0),
        'market_cap_b': market.get('market_cap', 0) / 1e9,
        'market_cap_rank': market.get('market_cap_rank', 'N/A'),
        
        # 技术指标
        'trend_desc': patterns.get('trend_desc', 'N/A'),
        'trend_signal': '📈 看涨' if patterns.get('trend') in ['uptrend', 'strong_uptrend'] else '📉 看跌',
        'rsi': indicators.get('rsi', 0),
        'rsi_desc': patterns.get('rsi_desc', 'N/A'),
        'macd': indicators.get('macd', 0),
        'macd_desc': patterns.get('macd_desc', 'N/A'),
        'adx': indicators.get('adx', 0),
        'adx_desc': f"趋势强度{'充足' if indicators.get('adx', 0) > 25 else '一般'}",
        'bb_desc': patterns.get('bb_desc', 'N/A'),
        'bb_signal': patterns.get('bb_signal', 'N/A'),
        
        # 支撑阻力
        'resistance': patterns.get('resistance', indicators.get('bb_upper', 0)),
        'support': patterns.get('support', indicators.get('bb_lower', 0)),
        'ma20': indicators.get('ma20', 0),
        
        # 信号
        'bullish_count': conclusion.get('signals_count', {}).get('bullish', 0),
        'bearish_count': conclusion.get('signals_count', {}).get('bearish', 0),
        
        # 结论
        'decision': conclusion.get('decision', 'HOLD'),
        'confidence': conclusion.get('confidence', 50),
        'decision_narrative': conclusion.get('narrative', ''),
        'entry_strategy': '分3批建仓，首批30%，回调至支撑位加仓40%，突破阻力加仓30%' if conclusion.get('decision') == 'BUY' else '观望等待时机',
    }
    
    # 4. 生成形态HTML
    patterns_html = '<ul style="margin: 0; padding-left: 20px; line-height: 2;">'
    
    if patterns.get('double_bottom'):
        patterns_html += f'<li>✅ {patterns.get("double_bottom_desc", "双底形态")}</li>'
    
    if patterns.get('double_top'):
        patterns_html += f'<li>⚠️ {patterns.get("double_top_desc", "双顶形态")}</li>'
    
    if patterns.get('head_shoulders'):
        patterns_html += f'<li>⚠️ {patterns.get("head_shoulders_desc", "头肩形态")}</li>'
    
    patterns_html += f'<li>趋势: {patterns.get("trend_desc", "N/A")}</li>'
    patterns_html += '</ul>'
    
    template_vars['patterns_html'] = patterns_html
    
    # 5. 生成链上数据行
    onchain_rows = ''
    if onchain.get('hashrate'):
        onchain_rows += f'<tr><td>算力</td><td>{onchain["hashrate"]:.2f} EH/s</td><td>网络安全度</td></tr>'
    if onchain.get('difficulty'):
        onchain_rows += f'<tr><td>难度</td><td>{onchain["difficulty"]:.2f} T</td><td>挖矿难度</td></tr>'
    if onchain.get('total_btc'):
        onchain_rows += f'<tr><td>流通量</td><td>{onchain["total_btc"]:,.0f} BTC</td><td>已挖出数量</td></tr>'
    if not onchain_rows:
        onchain_rows = f'<tr><td colspan="3">{onchain.get("note", "暂无链上数据")}</td></tr>'
    
    template_vars['onchain_rows'] = onchain_rows
    template_vars['onchain_source'] = onchain.get('data_source', 'N/A')
    
    # 6. 生成信号HTML
    signals_html = ''
    for s in signals:
        signal_class = 'bullish' if s['strength'] > 0 else 'bearish'
        signals_html += f'''
            <div class="signal-card {signal_class}">
                <div class="category">{s['category']}</div>
                <div class="name">{s['name']}: {s['signal']}</div>
                <div class="desc">{s['desc']}</div>
                <div class="strength">强度: {s['strength']:+d}</div>
            </div>
        '''
    
    template_vars['signals_html'] = signals_html
    
    # 7. 读取模板并填充
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'crypto_report_v4.html')
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 填充变量
    html = template.format(**template_vars)
    
    # 8. 保存
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{symbol}_report_v4.html")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 报告已生成: {output_path}")
    
    return output_path


if __name__ == '__main__':
    symbol = 'BTC-USD'
    
    print("=" * 60)
    print(f"生成 {symbol} 报告 (v4.0)")
    print("=" * 60)
    
    report_path = generate_crypto_report_v4(symbol)
    
    print()
    print("=" * 60)
    print("🎉 报告生成完成！")
    print("=" * 60)
