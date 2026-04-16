#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地区化新闻分析器 - 整合自 stock-recommend 思路
按地区分析新闻影响，生成地区化投资建议

功能:
- 地区分类 (美国/欧洲/亚洲/中国)
- 地区影响评估
- 新闻驱动推荐
- 地区联动分析
"""

import sys
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


class RegionalNewsAnalyzer:
    """
    地区化新闻分析器
    
    地区分类:
    - 美国 (US): 美联储、华尔街、纳斯达克、美股
    - 欧洲 (EU): 欧盟、欧元区、欧央行
    - 亚洲 (Asia): 日本、韩国、东南亚
    - 中国 (China): A股、港股、人民币
    """
    
    # 地区关键词映射
    REGION_KEYWORDS = {
        'us': {
            'name': '美国',
            'keywords': [
                '美国', '美联储', 'Fed', '华尔街', 'Wall Street',
                '纳斯达克', 'Nasdaq', '道琼斯', 'Dow Jones',
                '标普', 'S&P', '美股', '美元', 'USD',
                '拜登', 'Biden', '特朗普', 'Trump',
                '美国经济', 'US economy'
            ],
            'markets': ['美股', '纳斯达克', '道琼斯'],
            'impact_stocks': {
                'positive': ['AAPL', 'MSFT', 'GOOGL', 'AMZN'],
                'negative': []
            }
        },
        'eu': {
            'name': '欧洲',
            'keywords': [
                '欧洲', '欧盟', 'EU', '欧元区', 'Eurozone',
                '欧央行', 'ECB', '欧元', 'Euro',
                '德国', 'Germany', '法国', 'France',
                '英国', 'UK', '英镑', 'GBP'
            ],
            'markets': ['欧洲股市', '德国DAX', '法国CAC'],
            'impact_stocks': {
                'positive': [],
                'negative': []
            }
        },
        'asia': {
            'name': '亚洲',
            'keywords': [
                '亚洲', 'Asia', '日本', 'Japan', '日经',
                '韩国', 'Korea', '韩元', 'KRW',
                '东南亚', 'Southeast Asia',
                '新加坡', 'Singapore', '印度', 'India'
            ],
            'markets': ['日经225', '韩国KOSPI', '印度SENSEX'],
            'impact_stocks': {
                'positive': [],
                'negative': []
            }
        },
        'china': {
            'name': '中国',
            'keywords': [
                '中国', 'China', 'A股', '港股', '人民币', 'CNY',
                '央行', 'PBOC', '证监会', 'CSRC',
                '上证', '深证', '创业板', '科创板',
                '北向资金', '南向资金', '沪深港通',
                '中国经济增长', 'GDP'
            ],
            'markets': ['A股', '港股', '人民币'],
            'impact_stocks': {
                'positive': ['600519', '000858', '601318'],
                'negative': []
            }
        }
    }
    
    # 行业关键词映射
    SECTOR_KEYWORDS = {
        '科技': ['科技', '半导体', '芯片', 'AI', '人工智能', '互联网'],
        '金融': ['银行', '保险', '证券', '金融', '券商'],
        '消费': ['消费', '零售', '电商', '白酒', '食品'],
        '医药': ['医药', '医疗', '生物', '疫苗', '创新药'],
        '新能源': ['新能源', '光伏', '风电', '储能', '电动车'],
        '地产': ['地产', '房地产', '物业', '租赁']
    }
    
    # 情绪关键词
    SENTIMENT_KEYWORDS = {
        'positive': [
            '上涨', '增长', '利好', '突破', '创新高',
            '盈利', '收益', '反弹', '复苏', '扩张',
            '降息', '宽松', '刺激', '支持', '鼓励'
        ],
        'negative': [
            '下跌', '下降', '利空', '跌破', '新低',
            '亏损', '风险', '暴跌', '衰退', '收缩',
            '加息', '收紧', '限制', '打压', '处罚'
        ]
    }
    
    def analyze_news(self, news_list: List[Dict]) -> Dict:
        """
        分析新闻的地区影响
        
        Args:
            news_list: 新闻列表
            
        Returns:
            {
                'regions': {
                    'us': {'impact': 'positive', 'news_count': 5, ...},
                    'china': {'impact': 'negative', 'news_count': 3, ...}
                },
                'overall_sentiment': 'neutral',
                'recommendations': [...]
            }
        """
        result = {
            'regions': {},
            'overall_sentiment': 'neutral',
            'recommendations': [],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 按地区分析
        for region_code, region_info in self.REGION_KEYWORDS.items():
            region_analysis = self._analyze_region(news_list, region_code, region_info)
            result['regions'][region_code] = region_analysis
        
        # 计算整体情绪
        result['overall_sentiment'] = self._calculate_overall_sentiment(result['regions'])
        
        # 生成推荐
        result['recommendations'] = self._generate_recommendations(result['regions'])
        
        return result
    
    def _analyze_region(
        self,
        news_list: List[Dict],
        region_code: str,
        region_info: Dict
    ) -> Dict:
        """分析单个地区的新闻影响"""
        # 筛选相关新闻
        related_news = []
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '') or news.get('summary', '')
            text = title + ' ' + content
            
            # 检查是否包含地区关键词
            if any(kw in text for kw in region_info['keywords']):
                related_news.append(news)
        
        # 分析情绪
        sentiment_score = 0
        for news in related_news:
            title = news.get('title', '')
            content = news.get('content', '') or news.get('summary', '')
            text = title + ' ' + content
            
            # 正面关键词
            positive_count = sum(1 for kw in self.SENTIMENT_KEYWORDS['positive'] if kw in text)
            # 负面关键词
            negative_count = sum(1 for kw in self.SENTIMENT_KEYWORDS['negative'] if kw in text)
            
            sentiment_score += (positive_count - negative_count)
        
        # 确定影响
        if sentiment_score > 2:
            impact = 'positive'
            impact_desc = '利好'
        elif sentiment_score < -2:
            impact = 'negative'
            impact_desc = '利空'
        else:
            impact = 'neutral'
            impact_desc = '中性'
        
        # 识别受影响的行业
        affected_sectors = self._identify_sectors(related_news)
        
        return {
            'name': region_info['name'],
            'news_count': len(related_news),
            'sentiment_score': sentiment_score,
            'impact': impact,
            'impact_desc': impact_desc,
            'affected_sectors': affected_sectors,
            'top_news': related_news[:3],
            'markets': region_info['markets']
        }
    
    def _identify_sectors(self, news_list: List[Dict]) -> List[str]:
        """识别受影响的行业"""
        affected = set()
        
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '') or news.get('summary', '')
            text = title + ' ' + content
            
            for sector, keywords in self.SECTOR_KEYWORDS.items():
                if any(kw in text for kw in keywords):
                    affected.add(sector)
        
        return list(affected)
    
    def _calculate_overall_sentiment(self, regions: Dict) -> str:
        """计算整体市场情绪"""
        total_score = sum(r['sentiment_score'] for r in regions.values())
        
        if total_score > 5:
            return 'very_bullish'
        elif total_score > 2:
            return 'bullish'
        elif total_score < -5:
            return 'very_bearish'
        elif total_score < -2:
            return 'bearish'
        else:
            return 'neutral'
    
    def _generate_recommendations(self, regions: Dict) -> List[Dict]:
        """生成投资建议"""
        recommendations = []
        
        for region_code, region_data in regions.items():
            if region_data['impact'] == 'positive' and region_data['news_count'] >= 2:
                # 利好消息较多，建议关注
                region_info = self.REGION_KEYWORDS[region_code]
                
                for sector in region_data['affected_sectors']:
                    recommendations.append({
                        'region': region_data['name'],
                        'sector': sector,
                        'action': '关注',
                        'confidence': min(0.5 + region_data['sentiment_score'] * 0.05, 0.9),
                        'reason': f"{region_data['name']}{sector}板块受{region_data['news_count']}条利好消息影响",
                        'markets': region_data['markets']
                    })
            
            elif region_data['impact'] == 'negative' and region_data['news_count'] >= 2:
                # 利空消息较多，建议谨慎
                for sector in region_data['affected_sectors']:
                    recommendations.append({
                        'region': region_data['name'],
                        'sector': sector,
                        'action': '谨慎',
                        'confidence': min(0.5 + abs(region_data['sentiment_score']) * 0.05, 0.9),
                        'reason': f"{region_data['name']}{sector}板块受{region_data['news_count']}条利空消息影响",
                        'markets': region_data['markets']
                    })
        
        # 按置信度排序
        recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        
        return recommendations[:10]


class NewsDrivenRecommender:
    """
    新闻驱动推荐器
    
    从新闻直接生成股票推荐
    """
    
    # 关键词到股票的映射
    KEYWORD_STOCK_MAP = {
        # 科技
        '半导体': ['688981', '002371', '600584'],
        '芯片': ['688981', '002371', '300666'],
        'AI': ['300750', '002230', '688099'],
        '人工智能': ['300750', '002230', '688099'],
        
        # 消费
        '白酒': ['600519', '000858', '000568'],
        '消费': ['600519', '000858', '002304'],
        '电商': ['300750', '002142', '600803'],
        
        # 新能源
        '新能源': ['300750', '002594', '601012'],
        '光伏': ['601012', '300274', '002129'],
        '电动车': ['002594', '300750', '688567'],
        
        # 金融
        '银行': ['601398', '601288', '600036'],
        '保险': ['601318', '601601', '601628'],
        '券商': ['600030', '601211', '600837'],
        
        # 医药
        '医药': ['600276', '000661', '300760'],
        '疫苗': ['300760', '688180', '002007'],
        
        # 地产
        '地产': ['000002', '600048', '001979']
    }
    
    def recommend_from_news(self, news_list: List[Dict]) -> List[Dict]:
        """
        从新闻生成股票推荐
        
        Args:
            news_list: 新闻列表
            
        Returns:
            [
                {
                    'symbol': '600519',
                    'name': '贵州茅台',
                    'reason': '受益于消费升级政策',
                    'confidence': 0.7,
                    'related_news': [...]
                }
            ]
        """
        recommendations = []
        
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '') or news.get('summary', '')
            text = title + ' ' + content
            
            # 匹配关键词
            for keyword, stocks in self.KEYWORD_STOCK_MAP.items():
                if keyword in text:
                    # 判断情绪
                    sentiment = self._analyze_sentiment(text)
                    
                    for stock in stocks:
                        # 检查是否已存在
                        existing = next(
                            (r for r in recommendations if r['symbol'] == stock),
                            None
                        )
                        
                        if existing:
                            # 更新置信度
                            existing['confidence'] = min(existing['confidence'] + 0.1, 0.9)
                            existing['related_news'].append(title)
                        else:
                            recommendations.append({
                                'symbol': stock,
                                'reason': f'受益于{keyword}相关新闻',
                                'confidence': 0.6 if sentiment == 'positive' else 0.4,
                                'sentiment': sentiment,
                                'related_news': [title],
                                'keyword': keyword
                            })
        
        # 按置信度排序
        recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        
        return recommendations[:15]
    
    def _analyze_sentiment(self, text: str) -> str:
        """分析新闻情绪"""
        positive_words = ['利好', '增长', '上涨', '突破', '创新高']
        negative_words = ['利空', '下降', '下跌', '跌破', '新低']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'


def analyze_regional_news(news_list: List[Dict]) -> Dict:
    """地区化新闻分析入口"""
    analyzer = RegionalNewsAnalyzer()
    return analyzer.analyze_news(news_list)


def recommend_from_news(news_list: List[Dict]) -> List[Dict]:
    """新闻驱动推荐入口"""
    recommender = NewsDrivenRecommender()
    return recommender.recommend_from_news(news_list)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='地区化新闻分析')
    parser.add_argument('--type', choices=['regional', 'recommend'], 
                       default='regional', help='分析类型')
    
    args = parser.parse_args()
    
    # 示例新闻
    sample_news = [
        {
            'title': '美联储暗示可能降息，美股大涨',
            'content': '美联储主席表示可能在未来几个月降息...'
        },
        {
            'title': '中国发布新能源产业支持政策',
            'content': '国务院发布新能源产业发展规划...'
        }
    ]
    
    if args.type == 'regional':
        result = analyze_regional_news(sample_news)
    else:
        result = recommend_from_news(sample_news)
    
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
