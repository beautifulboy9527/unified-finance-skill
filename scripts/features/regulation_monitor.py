#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监管监控器 - 监控中国金融监管机构网站
整合自 regulation-monitor skill

监控目标:
- NFRA: 国家金融监督管理总局
- CSRC: 中国证券监督管理委员会
- PBOC: 中国人民银行
"""

import sys
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


class RegulationMonitor:
    """
    监管监控器
    
    监控目标:
    - NFRA: 国家金融监督管理总局
    - CSRC: 中国证券监督管理委员会
    - PBOC: 中国人民银行
    """
    
    SOURCES = {
        'nfra': {
            'name': '国家金融监督管理总局',
            'url': 'http://www.nfra.gov.cn',
            'type': 'banking_insurance',
            'keywords': ['银行', '保险', '信托', '金融']
        },
        'csrc': {
            'name': '中国证监会',
            'url': 'http://www.csrc.gov.cn',
            'type': 'securities',
            'keywords': ['证券', '上市公司', '股票', '基金']
        },
        'pboc': {
            'name': '中国人民银行',
            'url': 'http://www.pbc.gov.cn',
            'type': 'monetary_policy',
            'keywords': ['货币政策', '利率', '存款准备金', '信贷']
        }
    }
    
    # 影响级别关键词
    IMPACT_KEYWORDS = {
        'high': ['处罚', '立案调查', '停牌', '退市', '违法', '违规', '禁入'],
        'medium': ['监管', '规范', '整顿', '检查', '整改', '约谈'],
        'low': ['指导意见', '征求意见稿', '通知', '办法', '规定']
    }
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), '.cache')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_announcements(
        self,
        source: str = 'all',
        days: int = 7,
        use_cache: bool = True
    ) -> List[Dict]:
        """
        获取监管公告
        
        Args:
            source: 监管机构 (nfra/csrc/pboc/all)
            days: 回溯天数
            use_cache: 是否使用缓存
            
        Returns:
            [
                {
                    'source': 'CSRC',
                    'title': '关于加强投资者保护的指导意见',
                    'date': '2026-04-16',
                    'url': 'http://...',
                    'summary': '...',
                    'impact': 'high/medium/low'
                }
            ]
        """
        announcements = []
        
        # 检查缓存
        cache_file = os.path.join(self.cache_dir, f'regulation_{source}_{days}d.json')
        if use_cache and os.path.exists(cache_file):
            cache_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if datetime.now() - cache_time < timedelta(hours=6):  # 6小时缓存
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        # 抓取公告
        if source == 'all':
            for src in self.SOURCES.keys():
                try:
                    announcements.extend(self._fetch_source(src, days))
                except Exception as e:
                    print(f"抓取 {src} 失败: {str(e)}")
        else:
            try:
                announcements = self._fetch_source(source, days)
            except Exception as e:
                print(f"抓取失败: {str(e)}")
        
        # 按日期排序
        announcements.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        # 保存缓存
        if use_cache and announcements:
            os.makedirs(self.cache_dir, exist_ok=True)
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(announcements, f, ensure_ascii=False, indent=2)
        
        return announcements
    
    def _fetch_source(self, source: str, days: int) -> List[Dict]:
        """抓取单个监管机构"""
        source_info = self.SOURCES.get(source)
        if not source_info:
            return []
        
        # 由于实际网站结构复杂，这里提供备用数据
        # 实际使用时需要根据各网站结构定制解析逻辑
        
        announcements = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        try:
            response = self.session.get(
                source_info['url'],
                timeout=10
            )
            
            if response.status_code == 200:
                # 简化实现：返回示例数据
                # 实际需要解析具体网站结构
                announcements = self._generate_sample_announcements(source_info, days)
        
        except Exception as e:
            # 网络错误时返回示例数据
            announcements = self._generate_sample_announcements(source_info, days)
        
        return announcements
    
    def _generate_sample_announcements(
        self,
        source_info: Dict,
        days: int
    ) -> List[Dict]:
        """生成示例公告（实际使用时需替换为真实抓取）"""
        # 示例数据，展示功能结构
        sample = [
            {
                'source': source_info['name'],
                'title': f'关于规范{source_info["keywords"][0]}业务的通知',
                'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'url': source_info['url'],
                'summary': f'为进一步规范{source_info["keywords"][0]}业务...',
                'impact': 'medium'
            }
        ]
        return sample
    
    def analyze_impact(
        self,
        announcement: Dict,
        portfolio: List[str] = None
    ) -> Dict:
        """
        分析公告对投资组合的影响
        
        Args:
            announcement: 公告内容
            portfolio: 投资组合股票列表
            
        Returns:
            {
                'impact_level': 'high/medium/low',
                'affected_sectors': ['银行', '保险'],
                'affected_stocks': ['600036', '601318'],
                'recommendation': '...',
                'reasoning': '...'
            }
        """
        title = announcement.get('title', '')
        summary = announcement.get('summary', '')
        content = title + ' ' + summary
        
        # 判断影响等级
        impact_level = 'low'
        for level, keywords in self.IMPACT_KEYWORDS.items():
            if any(kw in content for kw in keywords):
                impact_level = level
                break
        
        # 识别受影响的行业
        affected_sectors = self._identify_sectors(content)
        
        # 识别受影响的股票
        affected_stocks = self._identify_stocks(content, portfolio)
        
        # 生成建议
        recommendation = self._generate_recommendation(impact_level)
        reasoning = f'公告包含"{impact_level}"级别关键词'
        
        return {
            'impact_level': impact_level,
            'affected_sectors': affected_sectors,
            'affected_stocks': affected_stocks,
            'recommendation': recommendation,
            'reasoning': reasoning
        }
    
    def _identify_sectors(self, content: str) -> List[str]:
        """识别受影响的行业"""
        sector_keywords = {
            '银行': ['银行', '信贷', '存款', '贷款'],
            '保险': ['保险', '寿险', '财险', '保费'],
            '证券': ['证券', '券商', '投行', '经纪'],
            '基金': ['基金', '公募', '私募', 'ETF'],
            '信托': ['信托', '资管']
        }
        
        affected = []
        for sector, keywords in sector_keywords.items():
            if any(kw in content for kw in keywords):
                affected.append(sector)
        
        return affected
    
    def _identify_stocks(
        self,
        content: str,
        portfolio: List[str]
    ) -> List[str]:
        """识别受影响的股票"""
        if not portfolio:
            return []
        
        # 简化实现：实际需要根据股票所属行业匹配
        return []
    
    def _generate_recommendation(self, impact_level: str) -> str:
        """生成操作建议"""
        recommendations = {
            'high': '⚠️ 高影响公告，建议立即评估持仓风险',
            'medium': '📋 中等影响，建议密切关注后续发展',
            'low': 'ℹ️ 低影响，可正常关注'
        }
        return recommendations.get(impact_level, '继续关注')
    
    def get_regulatory_risk_score(
        self,
        symbol: str,
        days: int = 30
    ) -> Dict:
        """
        获取股票的监管风险评分
        
        Args:
            symbol: 股票代码
            days: 回溯天数
            
        Returns:
            {
                'symbol': '600036',
                'risk_score': 35,
                'risk_level': 'low',
                'recent_events': [...],
                'warnings': [...]
            }
        """
        # 获取相关公告
        announcements = self.fetch_announcements(days=days)
        
        # 筛选相关公告
        related = self._filter_related(announcements, symbol)
        
        # 计算风险评分
        risk_score = 0
        warnings = []
        
        for ann in related:
            impact = self.analyze_impact(ann)
            if impact['impact_level'] == 'high':
                risk_score += 30
                warnings.append(ann['title'])
            elif impact['impact_level'] == 'medium':
                risk_score += 15
            else:
                risk_score += 5
        
        # 确定风险等级
        if risk_score >= 60:
            risk_level = 'high'
        elif risk_score >= 30:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'symbol': symbol,
            'risk_score': min(risk_score, 100),
            'risk_level': risk_level,
            'recent_events': related[:5],
            'warnings': warnings,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _filter_related(
        self,
        announcements: List[Dict],
        symbol: str
    ) -> List[Dict]:
        """筛选与股票相关的公告"""
        # 简化实现：返回所有公告
        # 实际需要根据股票所属行业和公司信息过滤
        return announcements
    
    def summarize_recent(self, days: int = 7) -> Dict:
        """
        生成监管动态摘要
        
        Args:
            days: 回溯天数
            
        Returns:
            {
                'period': '最近7天',
                'total_announcements': 15,
                'by_source': {...},
                'by_impact': {...},
                'highlights': [...]
            }
        """
        announcements = self.fetch_announcements(days=days)
        
        # 按来源统计
        by_source = {}
        for ann in announcements:
            source = ann.get('source', 'Unknown')
            by_source[source] = by_source.get(source, 0) + 1
        
        # 按影响等级统计
        by_impact = {'high': 0, 'medium': 0, 'low': 0}
        for ann in announcements:
            impact = ann.get('impact', 'low')
            by_impact[impact] = by_impact.get(impact, 0) + 1
        
        # 提取高影响公告
        highlights = [
            ann for ann in announcements
            if ann.get('impact') == 'high'
        ][:5]
        
        return {
            'period': f'最近{days}天',
            'total_announcements': len(announcements),
            'by_source': by_source,
            'by_impact': by_impact,
            'highlights': highlights,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


def monitor_regulations(days: int = 7) -> List[Dict]:
    """监管监控入口"""
    monitor = RegulationMonitor()
    return monitor.fetch_announcements(days=days)


def check_regulatory_risk(symbol: str, days: int = 30) -> Dict:
    """监管风险检查入口"""
    monitor = RegulationMonitor()
    return monitor.get_regulatory_risk_score(symbol, days)


def summarize_regulations(days: int = 7) -> Dict:
    """监管动态摘要入口"""
    monitor = RegulationMonitor()
    return monitor.summarize_recent(days)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='监管监控')
    parser.add_argument('--days', type=int, default=7, help='回溯天数')
    parser.add_argument('--symbol', help='股票代码')
    parser.add_argument('--summary', action='store_true', help='生成摘要')
    
    args = parser.parse_args()
    
    if args.summary:
        result = summarize_regulations(args.days)
    elif args.symbol:
        result = check_regulatory_risk(args.symbol, args.days)
    else:
        result = monitor_regulations(args.days)
    
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
