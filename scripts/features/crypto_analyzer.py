#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密货币专用分析模块
提供链上指标、市场情绪、加密特有信号
"""

import sys
import os
from datetime import datetime
from typing import Dict, Optional

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


class CryptoAnalyzer:
    """
    加密货币分析器
    
    功能:
    - 链上数据分析 (活跃地址、交易量)
    - 市场情绪指标 (恐慌贪婪指数)
    - 加密特有信号 (Funding Rate、Long/Short)
    - 技术分析 (适配加密货币波动特征)
    """
    
    def analyze(self, symbol: str) -> Dict:
        """
        综合分析加密货币
        
        Args:
            symbol: 加密货币代码 (如 BTC-USD, ETH-USD)
            
        Returns:
            分析结果
        """
        result = {
            'symbol': symbol,
            'type': 'crypto',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'onchain': {},
            'sentiment': {},
            'technical': {},
            'signals': {},
            'score': 0,
            'recommendation': 'hold'
        }
        
        # 1. 链上分析
        result['onchain'] = self._analyze_onchain(symbol)
        
        # 2. 市场情绪
        result['sentiment'] = self._analyze_sentiment(symbol)
        
        # 3. 技术分析 (加密适配)
        result['technical'] = self._analyze_technical_crypto(symbol)
        
        # 4. 信号检测
        result['signals'] = self._detect_crypto_signals(symbol)
        
        # 5. 综合评分
        result['score'] = self._calculate_score(result)
        
        # 6. 生成建议
        result['recommendation'] = self._generate_recommendation(result)
        
        return result
    
    def _analyze_onchain(self, symbol: str) -> Dict:
        """
        链上数据分析
        
        Returns:
            链上指标
        """
        # 实际应用中可接入:
        # - Glassnode API
        # - CoinMetrics
        # - Dune Analytics
        
        return {
            'active_addresses_24h': 'N/A',
            'transaction_volume': 'N/A',
            'whale_activity': 'N/A',
            'exchange_inflow': 'N/A',
            'exchange_outflow': 'N/A',
            'data_source': 'onchain_api (需配置)',
            'note': '链上数据需要配置 Glassnode/CoinMetrics API'
        }
    
    def _analyze_sentiment(self, symbol: str) -> Dict:
        """
        市场情绪分析
        
        Returns:
            情绪指标
        """
        # 实际应用中可接入:
        # - Alternative.me Fear & Greed Index
        # - LunarCrush
        # - Santiment
        
        try:
            # 尝试获取恐慌贪婪指数
            import requests
            
            response = requests.get(
                'https://api.alternative.me/fng/',
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()['data'][0]
                fear_greed_value = int(data['value'])
                fear_greed_class = data['value_classification']
                
                return {
                    'fear_greed_index': fear_greed_value,
                    'fear_greed_class': fear_greed_class,
                    'sentiment_score': self._map_sentiment_to_score(fear_greed_value),
                    'data_source': 'alternative.me',
                    'update_time': datetime.fromtimestamp(int(data['timestamp'])).strftime('%Y-%m-%d')
                }
        except:
            pass
        
        return {
            'fear_greed_index': 'N/A',
            'fear_greed_class': 'N/A',
            'sentiment_score': 50,
            'data_source': 'fallback',
            'note': '情绪数据获取失败'
        }
    
    def _map_sentiment_to_score(self, value: int) -> int:
        """将恐慌贪婪指数映射为评分"""
        # 0-25: 极度恐惧 → 70分 (逆向买入机会)
        # 25-50: 恐惧 → 60分
        # 50-75: 贪婪 → 50分
        # 75-100: 极度贪婪 → 30分 (风险较高)
        
        if value <= 25:
            return 70
        elif value <= 50:
            return 60
        elif value <= 75:
            return 50
        else:
            return 30
    
    def _analyze_technical_crypto(self, symbol: str) -> Dict:
        """
        加密货币技术分析 (适配高波动)
        """
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        try:
            from core.technical import analyze_technical
            
            result = analyze_technical(symbol)
            
            # 加密货币特有的风险评估
            basic = result.get('basic_indicators', {})
            
            # ATR倍数调整 (加密货币波动更大)
            atr = basic.get('atr', 0)
            current_price = basic.get('current_price', 0)
            
            if atr and current_price:
                volatility_ratio = atr / current_price
                
                # 高波动警告
                if volatility_ratio > 0.05:  # ATR > 5% 价格
                    result['volatility_warning'] = f"⚠️ 高波动率: {volatility_ratio*100:.1f}% (建议ATR止损倍数3-4)"
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def _detect_crypto_signals(self, symbol: str) -> Dict:
        """
        加密货币特有信号
        """
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        try:
            from features.entry_signals import analyze_entry_signals
            
            result = analyze_entry_signals(symbol)
            
            # 加密货币信号权重调整
            # 可以添加加密特有信号如:
            # - Funding Rate 极端值
            # - Long/Short Ratio
            # - 交易所流入流出
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_score(self, result: Dict) -> int:
        """
        计算加密货币综合评分
        
        权重:
        - 技术面: 50%
        - 信号: 25%
        - 情绪: 15%
        - 链上: 10%
        """
        score = 0
        
        # 技术面 (50分)
        tech = result.get('technical', {})
        ai_decision = tech.get('ai_decision', {})
        if ai_decision.get('recommendation') == 'buy':
            score += 35
        elif ai_decision.get('recommendation') == 'hold':
            score += 20
        
        tech_score = ai_decision.get('confidence', 0)
        score += int(tech_score * 0.15)
        
        # 信号 (25分)
        signals = result.get('signals', {})
        signal_score = signals.get('score', {}).get('overall_score', 0)
        score += int(signal_score * 0.25)
        
        # 情绪 (15分)
        sentiment = result.get('sentiment', {})
        sentiment_score = sentiment.get('sentiment_score', 50)
        score += int(sentiment_score * 0.15)
        
        # 链上 (10分)
        onchain = result.get('onchain', {})
        if onchain.get('whale_activity') == 'accumulating':
            score += 10
        elif onchain.get('whale_activity') == 'distributing':
            score += 0
        else:
            score += 5  # 数据缺失给中性分
        
        return min(100, max(0, score))
    
    def _generate_recommendation(self, result: Dict) -> str:
        """生成投资建议"""
        score = result['score']
        
        if score >= 70:
            return 'buy'
        elif score >= 50:
            return 'hold'
        elif score >= 30:
            return 'reduce'
        else:
            return 'avoid'


# ============================================
# 便捷函数
# ============================================

def analyze_crypto(symbol: str) -> Dict:
    """分析加密货币"""
    analyzer = CryptoAnalyzer()
    return analyzer.analyze(symbol)


if __name__ == '__main__':
    symbol = 'ETH-USD'
    
    print("=" * 60)
    print(f"加密货币分析: {symbol}")
    print("=" * 60)
    
    result = analyze_crypto(symbol)
    
    print(f"\n综合评分: {result['score']}/100")
    print(f"建议操作: {result['recommendation']}")
    
    # 情绪
    sentiment = result['sentiment']
    print(f"\n市场情绪:")
    print(f"  恐慌贪婪指数: {sentiment.get('fear_greed_index', 'N/A')}")
    print(f"  分类: {sentiment.get('fear_greed_class', 'N/A')}")
    print(f"  数据源: {sentiment.get('data_source', 'N/A')}")
    
    # 技术面
    tech = result['technical']
    basic = tech.get('basic_indicators', {})
    print(f"\n技术面:")
    print(f"  趋势: {basic.get('trend', 'N/A')}")
    print(f"  RSI: {basic.get('rsi', 'N/A')}")
    if 'volatility_warning' in tech:
        print(f"  {tech['volatility_warning']}")
