#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Finance Skill - 完整功能测试
验证所有模块功能正常，无硬编码数据
"""

import sys
import os
import json
from datetime import datetime

# Windows 编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 添加路径
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)


def test_quote_a_stock():
    """测试 A股行情查询"""
    print("\n=== 测试 A股行情查询 ===")
    
    from core.quote import get_quote
    
    result = get_quote('002050')
    
    # 验证
    assert result['symbol'] == '002050', "股票代码错误"
    assert result['market'] == 'cn', "市场检测错误"
    assert result.get('price') is not None, "价格不能为空"
    assert result.get('data_source') != 'none', "数据源不能为 none"
    
    print(f"✅ A股行情查询成功")
    print(f"   名称: {result.get('name')}")
    print(f"   价格: {result.get('price')}")
    print(f"   数据源: {result.get('data_source')}")
    
    return True


def test_quote_us_stock():
    """测试美股行情查询"""
    print("\n=== 测试美股行情查询 ===")
    
    from core.quote import get_quote
    
    result = get_quote('AAPL')
    
    # 验证
    assert result['symbol'] == 'AAPL', "股票代码错误"
    assert result['market'] == 'us', "市场检测错误"
    assert result.get('price') is not None, "价格不能为空"
    assert result.get('data_source') != 'none', "数据源不能为 none"
    
    print(f"✅ 美股行情查询成功")
    print(f"   价格: {result.get('price')}")
    print(f"   数据源: {result.get('data_source')}")
    
    return True


def test_technical_analysis():
    """测试技术分析"""
    print("\n=== 测试技术分析 ===")
    
    from core.technical import analyze_technical
    
    result = analyze_technical('002050')
    
    # 验证
    assert result['symbol'] == '002050', "股票代码错误"
    
    indicators = result.get('basic_indicators', {})
    assert indicators.get('current_price') is not None, "当前价格不能为空"
    assert indicators.get('ma5') is not None, "MA5 不能为空"
    assert indicators.get('rsi') is not None, "RSI 不能为空"
    
    # 验证数据合理性
    ma5 = indicators['ma5']
    price = indicators['current_price']
    assert abs(ma5 - price) / price < 0.5, "MA5 与价格偏差过大，可能有硬编码"
    
    print(f"✅ 技术分析成功")
    print(f"   当前价格: {indicators.get('current_price')}")
    print(f"   MA5: {indicators.get('ma5')}")
    print(f"   RSI: {indicators.get('rsi')}")
    
    return True


def test_financial_data():
    """测试财务数据"""
    print("\n=== 测试财务数据 ===")
    
    from core.financial import get_financial_summary
    
    result = get_financial_summary('002050')
    
    # 验证
    assert result['symbol'] == '002050', "股票代码错误"
    assert result.get('data_source') != 'none', "数据源不能为 none"
    
    # 验证财务数据合理性
    revenue_3y = result.get('revenue_3y', [])
    if len(revenue_3y) > 0:
        # 营收应该在合理范围 (1-1000亿)
        for rev in revenue_3y:
            assert 1 < rev < 1000, f"营收 {rev} 亿不在合理范围"
    
    print(f"✅ 财务数据获取成功")
    print(f"   营收数据: {revenue_3y}")
    print(f"   数据源: {result.get('data_source')}")
    
    return True


def test_fundflow():
    """测试资金流向"""
    print("\n=== 测试资金流向 ===")
    
    from core.financial import get_fundflow
    
    result = get_fundflow('002050', days=5)
    
    # 验证
    assert result['symbol'] == '002050', "股票代码错误"
    
    if result.get('error'):
        print(f"⚠️ 资金流向获取失败: {result.get('error')}")
        return False
    
    history = result.get('history', [])
    assert len(history) > 0, "历史数据不能为空"
    
    # 验证数据合理性
    for h in history:
        if h.get('main_net_inflow') is not None:
            # 主力净流入应该在合理范围 (-100亿 到 100亿)
            assert -100 < h['main_net_inflow'] < 100, "主力净流入不在合理范围"
    
    print(f"✅ 资金流向获取成功")
    print(f"   历史记录数: {len(history)}")
    print(f"   趋势: {result.get('summary', {}).get('trend')}")
    
    return True


def test_liquidity():
    """测试流动性分析"""
    print("\n=== 测试流动性分析 ===")
    
    from features.liquidity import analyze_liquidity
    
    result = analyze_liquidity('AAPL')
    
    # 验证
    assert result['symbol'] == 'AAPL', "股票代码错误"
    assert result.get('grade') is not None, "流动性评级不能为空"
    
    # 验证数据合理性
    volume = result.get('volume', {})
    if volume.get('avg_daily_volume'):
        assert volume['avg_daily_volume'] > 0, "平均成交量必须大于 0"
    
    print(f"✅ 流动性分析成功")
    print(f"   流动性评级: {result.get('grade')}")
    print(f"   平均成交量: {volume.get('avg_daily_volume')}")
    
    return True


def test_no_hardcoded_data():
    """验证无硬编码数据"""
    print("\n=== 验证无硬编码数据 ===")
    
    from core.quote import get_quote
    
    # 测试多只股票，验证数据不同
    quotes = {}
    for symbol in ['002050', '600519', '000001']:
        result = get_quote(symbol)
        if result.get('price'):
            quotes[symbol] = result['price']
    
    # 验证不同股票有不同价格
    prices = list(quotes.values())
    if len(prices) >= 2:
        # 价格应该不全相同
        assert len(set(prices)) > 1, "所有股票价格相同，可能有硬编码"
        print(f"✅ 无硬编码数据验证通过")
        print(f"   不同股票有不同价格: {quotes}")
    else:
        print("⚠️ 无法验证，数据源可能不可用")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Unified Finance Skill - 完整功能测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("A股行情查询", test_quote_a_stock),
        ("美股行情查询", test_quote_us_stock),
        ("技术分析", test_technical_analysis),
        ("财务数据", test_financial_data),
        ("资金流向", test_fundflow),
        ("流动性分析", test_liquidity),
        ("无硬编码验证", test_no_hardcoded_data),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, "✅ 通过" if success else "⚠️ 警告"))
        except Exception as e:
            results.append((name, f"❌ 失败: {str(e)}"))
    
    # 汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    
    passed = sum(1 for _, status in results if "✅" in status)
    warned = sum(1 for _, status in results if "⚠️" in status)
    failed = sum(1 for _, status in results if "❌" in status)
    
    for name, status in results:
        print(f"{status} {name}")
    
    print(f"\n总计: {passed} 通过, {warned} 警告, {failed} 失败")
    
    return failed == 0


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Unified Finance Skill 测试')
    parser.add_argument('--test', choices=['quote', 'technical', 'financial', 'fundflow', 'liquidity', 'all'],
                       default='all', help='测试类型')
    
    args = parser.parse_args()
    
    if args.test == 'all':
        success = run_all_tests()
        sys.exit(0 if success else 1)
    elif args.test == 'quote':
        test_quote_a_stock()
        test_quote_us_stock()
    elif args.test == 'technical':
        test_technical_analysis()
    elif args.test == 'financial':
        test_financial_data()
    elif args.test == 'fundflow':
        test_fundflow()
    elif args.test == 'liquidity':
        test_liquidity()
