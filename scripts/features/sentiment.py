#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情绪分析模块 - 完整集成自 finance-sentiment skill
Reddit、X.com、新闻、Polymarket 情绪分析
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Optional, List

# Windows 编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


class SentimentAnalyzer:
    """
    情绪分析器 - 集成自 finance-sentiment skill
    
    数据源:
    - Reddit (Reddit 情绪)
    - X.com (Twitter 情绪)
    - News (新闻情绪)
    - Polymarket (预测市场)
    
    API: Adanos Finance API
    依赖: ADANOS_API_KEY 环境变量
    """
    
    API_BASE = "https://api.adanos.org"
    
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.api_key = os.getenv('ADANOS_API_KEY')
        
    def _make_request(self, endpoint: str, tickers: str, days: int = 7) -> Optional[List]:
        """
        发送 API 请求
        
        Args:
            endpoint: 端点路径
            tickers: 股票代码 (逗号分隔)
            days: 天数
        """
        if not self.api_key:
            return None
        
        try:
            import requests
            
            url = f"{self.API_BASE}{endpoint}?tickers={tickers}&days={days}"
            headers = {'X-API-Key': self.api_key}
            
            resp = requests.get(url, headers=headers, timeout=30)
            
            if resp.status_code == 200:
                data = resp.json()
                return data
            else:
                return None
                
        except Exception:
            return None
    
    def analyze_reddit(self, days: int = 7) -> Dict:
        """
        Reddit 情绪分析
        
        Returns:
            {
                'source': 'reddit',
                'buzz': 热度分数 (0-100),
                'bullish_pct': 看涨百分比,
                'bearish_pct': 看跌百分比,
                'mentions': 提及次数,
                'trend': 趋势 (rising/falling/stable),
                'sentiment_score': 情绪分数,
                'unique_posts': 独立帖子数,
                'subreddit_count': 涉及的子版块数,
                'total_upvotes': 总点赞数
            }
        """
        result = {
            'source': 'reddit',
            'symbol': self.symbol,
            'buzz': None,
            'bullish_pct': None,
            'bearish_pct': None,
            'mentions': None,
            'trend': None,
            'sentiment_score': None,
            'unique_posts': None,
            'subreddit_count': None,
            'total_upvotes': None,
            'data_source': 'none',
            'error': None
        }
        
        if not self.api_key:
            result['error'] = '需要设置 ADANOS_API_KEY 环境变量'
            return result
        
        data = self._make_request('/reddit/stocks/v1/compare', self.symbol, days)
        
        if data and len(data) > 0:
            item = data[0]
            result.update({
                'buzz': item.get('buzz_score'),
                'bullish_pct': item.get('bullish_pct'),
                'bearish_pct': item.get('bearish_pct'),
                'mentions': item.get('mentions'),
                'trend': item.get('trend'),
                'sentiment_score': item.get('sentiment_score'),
                'unique_posts': item.get('unique_posts'),
                'subreddit_count': item.get('subreddit_count'),
                'total_upvotes': item.get('total_upvotes'),
                'data_source': 'adanos_reddit'
            })
        else:
            result['error'] = '无法获取 Reddit 数据'
        
        return result
    
    def analyze_x(self, days: int = 7) -> Dict:
        """
        X.com (Twitter) 情绪分析
        
        Returns:
            {
                'source': 'x',
                'buzz': 热度分数,
                'bullish_pct': 看涨百分比,
                'mentions': 推文数,
                'trend': 趋势,
                'unique_tweets': 独立推文数,
                'total_upvotes': 总点赞数
            }
        """
        result = {
            'source': 'x',
            'symbol': self.symbol,
            'buzz': None,
            'bullish_pct': None,
            'bearish_pct': None,
            'mentions': None,
            'trend': None,
            'sentiment_score': None,
            'unique_tweets': None,
            'total_upvotes': None,
            'data_source': 'none',
            'error': None
        }
        
        if not self.api_key:
            result['error'] = '需要设置 ADANOS_API_KEY 环境变量'
            return result
        
        data = self._make_request('/x/stocks/v1/compare', self.symbol, days)
        
        if data and len(data) > 0:
            item = data[0]
            result.update({
                'buzz': item.get('buzz_score'),
                'bullish_pct': item.get('bullish_pct'),
                'bearish_pct': item.get('bearish_pct'),
                'mentions': item.get('mentions'),
                'trend': item.get('trend'),
                'sentiment_score': item.get('sentiment_score'),
                'unique_tweets': item.get('unique_tweets'),
                'total_upvotes': item.get('total_upvotes'),
                'data_source': 'adanos_x'
            })
        else:
            result['error'] = '无法获取 X.com 数据'
        
        return result
    
    def analyze_news(self, days: int = 7) -> Dict:
        """
        新闻情绪分析
        
        Returns:
            {
                'source': 'news',
                'buzz': 热度分数,
                'bullish_pct': 看涨百分比,
                'mentions': 新闻数,
                'trend': 趋势,
                'source_count': 新闻来源数
            }
        """
        result = {
            'source': 'news',
            'symbol': self.symbol,
            'buzz': None,
            'bullish_pct': None,
            'bearish_pct': None,
            'mentions': None,
            'trend': None,
            'sentiment_score': None,
            'source_count': None,
            'data_source': 'none',
            'error': None
        }
        
        if not self.api_key:
            result['error'] = '需要设置 ADANOS_API_KEY 环境变量'
            return result
        
        data = self._make_request('/news/stocks/v1/compare', self.symbol, days)
        
        if data and len(data) > 0:
            item = data[0]
            result.update({
                'buzz': item.get('buzz_score'),
                'bullish_pct': item.get('bullish_pct'),
                'bearish_pct': item.get('bearish_pct'),
                'mentions': item.get('mentions'),
                'trend': item.get('trend'),
                'sentiment_score': item.get('sentiment_score'),
                'source_count': item.get('source_count'),
                'data_source': 'adanos_news'
            })
        else:
            result['error'] = '无法获取新闻数据'
        
        return result
    
    def analyze_polymarket(self, days: int = 7) -> Dict:
        """
        Polymarket 预测市场分析
        
        Returns:
            {
                'source': 'polymarket',
                'buzz': 热度分数,
                'bullish_pct': 看涨百分比,
                'trade_count': 交易数,
                'trend': 趋势,
                'market_count': 市场数,
                'unique_traders': 独立交易者数,
                'total_liquidity': 总流动性
            }
        """
        result = {
            'source': 'polymarket',
            'symbol': self.symbol,
            'buzz': None,
            'bullish_pct': None,
            'bearish_pct': None,
            'trade_count': None,
            'trend': None,
            'sentiment_score': None,
            'market_count': None,
            'unique_traders': None,
            'total_liquidity': None,
            'data_source': 'none',
            'error': None
        }
        
        if not self.api_key:
            result['error'] = '需要设置 ADANOS_API_KEY 环境变量'
            return result
        
        data = self._make_request('/polymarket/stocks/v1/compare', self.symbol, days)
        
        if data and len(data) > 0:
            item = data[0]
            result.update({
                'buzz': item.get('buzz_score'),
                'bullish_pct': item.get('bullish_pct'),
                'bearish_pct': item.get('bearish_pct'),
                'trade_count': item.get('trade_count'),
                'trend': item.get('trend'),
                'sentiment_score': item.get('sentiment_score'),
                'market_count': item.get('market_count'),
                'unique_traders': item.get('unique_traders'),
                'total_liquidity': item.get('total_liquidity'),
                'data_source': 'adanos_polymarket'
            })
        else:
            result['error'] = '无法获取 Polymarket 数据'
        
        return result
    
    def analyze_all(self, days: int = 7) -> Dict:
        """
        全源情绪分析
        
        Returns:
            所有数据源的情绪分析结果
        """
        return {
            'symbol': self.symbol,
            'reddit': self.analyze_reddit(days),
            'x': self.analyze_x(days),
            'news': self.analyze_news(days),
            'polymarket': self.analyze_polymarket(days),
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_summary(self, days: int = 7) -> Dict:
        """
        获取情绪摘要 - 综合所有数据源
        
        Returns:
            {
                'symbol': 股票代码,
                'avg_bullish_pct': 平均看涨百分比,
                'avg_buzz': 平均热度,
                'sentiment': 综合情绪,
                'alignment': 数据源一致性,
                'sources': 各数据源详情
            }
        """
        all_sources = self.analyze_all(days)
        
        # 综合计算
        bullish_scores = []
        buzz_scores = []
        sources_available = []
        
        for source_name in ['reddit', 'x', 'news', 'polymarket']:
            data = all_sources.get(source_name, {})
            if data.get('bullish_pct') is not None:
                bullish_scores.append(data['bullish_pct'])
                sources_available.append(source_name)
            if data.get('buzz') is not None:
                buzz_scores.append(data['buzz'])
        
        avg_bullish = sum(bullish_scores) / len(bullish_scores) if bullish_scores else None
        avg_buzz = sum(buzz_scores) / len(buzz_scores) if buzz_scores else None
        
        # 情绪判断
        if avg_bullish:
            if avg_bullish > 60:
                sentiment = 'bullish'
                sentiment_desc = '看涨'
            elif avg_bullish > 40:
                sentiment = 'neutral'
                sentiment_desc = '中性'
            else:
                sentiment = 'bearish'
                sentiment_desc = '看跌'
        else:
            sentiment = 'unknown'
            sentiment_desc = '未知'
        
        # 数据源一致性
        if len(bullish_scores) >= 2:
            max_diff = max(bullish_scores) - min(bullish_scores)
            if max_diff < 10:
                alignment = 'aligned'
                alignment_desc = '数据源一致'
            elif max_diff < 25:
                alignment = 'somewhat_aligned'
                alignment_desc = '数据源大致一致'
            else:
                alignment = 'diverging'
                alignment_desc = '数据源分歧较大'
        else:
            alignment = 'insufficient_data'
            alignment_desc = '数据不足'
        
        return {
            'symbol': self.symbol,
            'avg_bullish_pct': round(avg_bullish, 2) if avg_bullish else None,
            'avg_buzz': round(avg_buzz, 2) if avg_buzz else None,
            'sentiment': sentiment,
            'sentiment_description': sentiment_desc,
            'alignment': alignment,
            'alignment_description': alignment_desc,
            'sources_available': sources_available,
            'sources': all_sources,
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def compare_tickers(self, symbols: List[str], days: int = 7, source: str = 'reddit') -> Dict:
        """
        对比多只股票的情绪
        
        Args:
            symbols: 股票代码列表
            days: 天数
            source: 数据源
        """
        result = {
            'symbols': symbols,
            'source': source,
            'comparison': [],
            'ranking': [],
            'data_source': 'none',
            'error': None
        }
        
        if not self.api_key:
            result['error'] = '需要设置 ADANOS_API_KEY 环境变量'
            return result
        
        endpoints = {
            'reddit': '/reddit/stocks/v1/compare',
            'x': '/x/stocks/v1/compare',
            'news': '/news/stocks/v1/compare',
            'polymarket': '/polymarket/stocks/v1/compare'
        }
        
        endpoint = endpoints.get(source, '/reddit/stocks/v1/compare')
        tickers = ','.join([s.upper() for s in symbols])
        
        data = self._make_request(endpoint, tickers, days)
        
        if data:
            result['comparison'] = data
            result['ranking'] = sorted(data, key=lambda x: x.get('buzz_score', 0), reverse=True)
            result['data_source'] = f'adanos_{source}'
        else:
            result['error'] = '无法获取对比数据'
        
        return result


def analyze_sentiment(symbol: str, days: int = 7) -> Dict:
    """情绪分析入口"""
    analyzer = SentimentAnalyzer(symbol)
    return analyzer.get_summary(days)


def analyze_reddit(symbol: str, days: int = 7) -> Dict:
    """Reddit 情绪分析"""
    analyzer = SentimentAnalyzer(symbol)
    return analyzer.analyze_reddit(days)


def analyze_x(symbol: str, days: int = 7) -> Dict:
    """X.com 情绪分析"""
    analyzer = SentimentAnalyzer(symbol)
    return analyzer.analyze_x(days)


def analyze_news(symbol: str, days: int = 7) -> Dict:
    """新闻情绪分析"""
    analyzer = SentimentAnalyzer(symbol)
    return analyzer.analyze_news(days)


def compare_sentiment(symbols: List[str], days: int = 7, source: str = 'reddit') -> Dict:
    """多股票情绪对比"""
    analyzer = SentimentAnalyzer(symbols[0])
    return analyzer.compare_tickers(symbols, days, source)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='情绪分析 - 集成自 finance-sentiment skill')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--days', type=int, default=7, help='分析天数')
    parser.add_argument('--type', choices=['summary', 'reddit', 'x', 'news', 'polymarket'], default='summary')
    parser.add_argument('--compare', nargs='+', help='对比多只股票')
    parser.add_argument('--source', choices=['reddit', 'x', 'news', 'polymarket'], default='reddit')
    
    args = parser.parse_args()
    
    if args.compare:
        result = compare_sentiment(args.compare, args.days, args.source)
    else:
        analyzer = SentimentAnalyzer(args.symbol)
        
        if args.type == 'summary':
            result = analyzer.get_summary(args.days)
        elif args.type == 'reddit':
            result = analyzer.analyze_reddit(args.days)
        elif args.type == 'x':
            result = analyzer.analyze_x(args.days)
        elif args.type == 'news':
            result = analyzer.analyze_news(args.days)
        elif args.type == 'polymarket':
            result = analyzer.analyze_polymarket(args.days)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
