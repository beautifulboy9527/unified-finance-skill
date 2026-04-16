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
        链上数据分析 - 使用 CoinGecko API
        
        Returns:
            链上指标
        """
        # CoinGecko API 获取市场数据
        try:
            import requests
            
            # 转换 symbol 格式: ETH-USD → ethereum
            coin_id = self._symbol_to_coingecko_id(symbol)
            
            # CoinGecko API (免费)
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                market_data = data.get('market_data', {})
                
                return {
                    'current_price_usd': market_data.get('current_price', {}).get('usd'),
                    'price_change_24h': market_data.get('price_change_percentage_24h'),
                    'price_change_7d': market_data.get('price_change_percentage_7d'),
                    'volume_24h': market_data.get('total_volume', {}).get('usd'),
                    'market_cap': market_data.get('market_cap', {}).get('usd'),
                    'market_cap_rank': data.get('market_cap_rank'),
                    'total_supply': market_data.get('total_supply'),
                    'circulating_supply': market_data.get('circulating_supply'),
                    'high_24h': market_data.get('high_24h', {}).get('usd'),
                    'low_24h': market_data.get('low_24h', {}).get('usd'),
                    'ath': market_data.get('ath', {}).get('usd'),
                    'ath_change_percentage': market_data.get('ath_change_percentage', {}).get('usd'),
                    'data_source': 'CoinGecko API',
                    'source_url': f'https://www.coingecko.com/en/coins/{coin_id}',
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
        except Exception as e:
            print(f"⚠️ CoinGecko 数据获取失败: {e}")
        
        return {
            'active_addresses_24h': 'N/A',
            'transaction_volume': 'N/A',
            'data_source': 'fallback',
            'note': '链上数据获取失败，请检查网络连接'
        }
    
    def _symbol_to_coingecko_id(self, symbol: str) -> str:
        """
        将交易对转换为 CoinGecko ID
        
        Args:
            symbol: 如 ETH-USD, BTC-USD
            
        Returns:
            CoinGecko coin id: 如 ethereum, bitcoin
        """
        # 常见映射
        mapping = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'BNB': 'binancecoin',
            'XRP': 'ripple',
            'ADA': 'cardano',
            'DOGE': 'dogecoin',
            'SOL': 'solana',
            'DOT': 'polkadot',
            'MATIC': 'matic-network',
            'LTC': 'litecoin',
            'SHIB': 'shiba-inu',
            'AVAX': 'avalanche-2',
            'LINK': 'chainlink',
            'ATOM': 'cosmos',
            'UNI': 'uniswap',
            'XMR': 'monero',
            'ETC': 'ethereum-classic',
            'XLM': 'stellar',
            'BCH': 'bitcoin-cash',
            'ALGO': 'algorand',
            'AAVE': 'aave',
            'COMP': 'compound-governance-token',
            'MKR': 'maker',
        }
        
        # 提取基础货币
        base = symbol.upper().split('-')[0].replace('USDT', '').replace('USDC', '')
        
        return mapping.get(base, base.lower())
    
    def _analyze_sentiment(self, symbol: str) -> Dict:
        """
        市场情绪分析 - 使用 alternative.me API
        
        Returns:
            情绪指标
        """
        try:
            # 使用 Alternative.me Fear & Greed Index API (免费)
            import requests
            
            response = requests.get(
                'https://api.alternative.me/fng/',
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()['data'][0]
                fear_greed_value = int(data['value'])
                fear_greed_class = data['value_classification']
                timestamp = int(data['timestamp'])
                
                return {
                    'fear_greed_index': fear_greed_value,
                    'fear_greed_class': fear_greed_class,
                    'sentiment_score': self._map_sentiment_to_score(fear_greed_value),
                    'data_source': 'alternative.me API',
                    'source_url': 'https://alternative.me/crypto/fear-and-greed-index/',
                    'update_time': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'),
                    'description': f"恐慌贪婪指数: {fear_greed_value} ({fear_greed_class})"
                }
        except Exception as e:
            print(f"⚠️ 情绪数据获取失败: {e}")
        
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
            
            # 新增: 生成专业文字解读
            result['narrative'] = self._generate_technical_narrative(basic, symbol)
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_technical_narrative(self, indicators: Dict, symbol: str) -> str:
        """
        生成技术面专业文字解读
        
        Args:
            indicators: 技术指标字典
            symbol: 股票代码
            
        Returns:
            专业解读文字
        """
        if not indicators or indicators.get('current_price') is None:
            return "技术数据不足，无法生成解读。"
        
        current_price = indicators.get('current_price', 0)
        trend = indicators.get('trend', 'unknown')
        rsi = indicators.get('rsi', 0)
        ma5 = indicators.get('ma5', 0)
        ma10 = indicators.get('ma10', 0)
        ma20 = indicators.get('ma20', 0)
        
        # 构建解读
        paragraphs = []
        
        # 1. 趋势分析
        if trend == 'uptrend':
            paragraphs.append(
                f"{symbol} 当前处于上升趋势，价格({current_price:.2f})站上MA5({ma5:.2f})、MA10({ma10:.2f})、MA20({ma20:.2f})三条均线，"
                f"形成多头排列，短期动能偏强。"
            )
        elif trend == 'downtrend':
            paragraphs.append(
                f"{symbol} 当前处于下降趋势，价格({current_price:.2f})低于MA5、MA10、MA20均线，"
                f"空头排列明显，短期建议观望为主。"
            )
        else:
            paragraphs.append(
                f"{symbol} 当前处于震荡整理阶段，价格({current_price:.2f})在均线间反复，"
                f"方向不明确，建议等待突破信号。"
            )
        
        # 2. RSI 分析
        if rsi:
            if rsi > 70:
                paragraphs.append(
                    f"RSI达到{rsi:.2f}，已进入超买区间(>70)，短期存在回调风险。"
                    f"若出现顶背离或成交量萎缩，需警惕高位回落。"
                )
            elif rsi > 60:
                paragraphs.append(
                    f"RSI为{rsi:.2f}，接近超买区域(60-70)，多头力量较强但仍需警惕。"
                    f"若继续上行突破70，可能进入加速上涨阶段。"
                )
            elif rsi < 30:
                paragraphs.append(
                    f"RSI仅为{rsi:.2f}，已进入超卖区间(<30)，可能是短期抄底机会。"
                    f"若出现底背离，反弹概率较大。"
                )
            elif rsi < 40:
                paragraphs.append(
                    f"RSI为{rsi:.2f}，处于弱势区域(30-40)，空头占优。"
                    f"需等待RSI回升至50以上再考虑入场。"
                )
            else:
                paragraphs.append(
                    f"RSI为{rsi:.2f}，处于中性区域(40-60)，多空力量相对平衡。"
                )
        
        # 3. 均线支撑/阻力
        if ma5 and ma10 and ma20:
            if current_price > ma20:
                paragraphs.append(
                    f"MA20({ma20:.2f})为重要支撑位，若回踩不破可考虑低吸。"
                    f"短期阻力位关注前高，突破后有望打开上行空间。"
                )
            else:
                paragraphs.append(
                    f"MA20({ma20:.2f})为上方阻力位，突破该位置才能确认趋势转强。"
                    f"下方支撑关注近期低点，若跌破可能加速下跌。"
                )
        
        # 4. 综合操作建议
        if trend == 'uptrend' and rsi and rsi < 70:
            conclusion = (
                f"综合来看，{symbol}短期偏多，技术面支撑上涨。"
                f"建议在MA20附近设置止损，目标可看前高附近。"
                f"严格执行止损纪律，仓位控制在总资金的10-20%。"
            )
        elif trend == 'uptrend' and rsi and rsi > 70:
            conclusion = (
                f"虽然趋势向上，但RSI超买提示短期风险。"
                f"建议等待回调至MA5或MA10支撑位再考虑入场，避免追高。"
            )
        elif trend == 'downtrend':
            conclusion = (
                f"当前趋势偏空，建议观望为主。"
                f"等待RSI进入超卖区或出现企稳信号后再考虑布局。"
            )
        else:
            conclusion = (
                f"技术面信号不明确，建议等待突破方向确认后再操作。"
                f"关注MA20得失，突破后顺势而为。"
            )
        
        paragraphs.append(conclusion)
        
        return "\n\n".join(paragraphs)
    
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
