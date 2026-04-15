#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Financial Data Fetcher - 实时财报数据获取
从多个数据源获取真实数据，拒绝硬编码
"""

import sys
import os
import json
import re
from datetime import datetime
from typing import Dict, Optional, List

# Windows 编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

class FinancialDataFetcher:
    """财报数据获取器 - 多数据源"""
    
    def __init__(self, symbol: str):
        self.symbol = str(symbol).replace('.SS', '').replace('.SZ', '')
        
    def get_financial_summary(self) -> Dict:
        """
        获取财务摘要（多数据源尝试）
        """
        result = {
            'symbol': self.symbol,
            'revenue_3y': [],
            'net_profit_3y': [],
            'revenue_growth': None,
            'profit_growth': None,
            'gross_margin': None,
            'net_margin': None,
            'roe': None,
            'debt_ratio': None,
            'current_ratio': None,
            'data_source': 'none',
            'update_time': None,
            'error': None
        }
        
        # 尝试数据源1: akshare 主要财务指标
        try:
            import akshare as ak
            
            # 获取主要财务指标
            df = ak.stock_financial_abstract(symbol=self.symbol)
            
            if df is not None and len(df) > 0:
                # 解析数据
                for _, row in df.head(10).iterrows():
                    date = str(row.iloc[0]) if len(row) > 0 else ''
                    if date and '20' in date:
                        # 提取营收
                        try:
                            revenue = float(str(row.get('营业收入', 0)).replace(',', '').replace('亿', ''))
                            if revenue > 0:
                                result['revenue_3y'].append(revenue)
                        except:
                            pass
                        
                        # 提取净利润
                        try:
                            profit = float(str(row.get('净利润', 0)).replace(',', '').replace('亿', ''))
                            if profit != 0:
                                result['net_profit_3y'].append(profit)
                        except:
                            pass
                
                # 提取最新指标
                latest = df.iloc[0] if len(df) > 0 else None
                if latest is not None:
                    result['gross_margin'] = self._safe_float(latest.get('销售毛利率'))
                    result['net_margin'] = self._safe_float(latest.get('销售净利率'))
                    result['roe'] = self._safe_float(latest.get('净资产收益率'))
                    result['debt_ratio'] = self._safe_float(latest.get('资产负债比率'))
                
                result['data_source'] = 'akshare_financial_abstract'
                result['update_time'] = datetime.now().strftime('%Y-%m-%d')
                
                # 如果获取到数据就返回
                if result['revenue_3y'] or result['gross_margin']:
                    return result
                    
        except Exception as e:
            result['error'] = f'数据源1失败: {str(e)}'
        
        # 尝试数据源2: 东方财富实时数据
        try:
            import akshare as ak
            
            # 获取实时行情中的财务指标
            df_realtime = ak.stock_zh_a_spot_em()
            stock = df_realtime[df_realtime['代码'] == self.symbol]
            
            if len(stock) > 0:
                row = stock.iloc[0]
                
                # 从实时数据提取
                result['pe_ratio'] = self._safe_float(row.get('市盈率-动态'))
                result['pb_ratio'] = self._safe_float(row.get('市净率'))
                result['market_cap'] = self._safe_float(row.get('总市值'))
                
                if result['data_source'] == 'none':
                    result['data_source'] = 'akshare_realtime'
                    result['update_time'] = datetime.now().strftime('%Y-%m-%d')
                    
        except Exception as e:
            if result.get('error'):
                result['error'] += f'; 数据源2失败: {str(e)}'
            else:
                result['error'] = f'数据源2失败: {str(e)}'
        
        # 尝试数据源3: 新浪财经
        try:
            import akshare as ak
            
            # 利润表
            df_profit = ak.stock_financial_report_sina(stock=self.symbol, symbol='利润表')
            
            if df_profit is not None and len(df_profit) > 0:
                # 提取营收和利润
                for i in range(min(3, len(df_profit))):
                    row = df_profit.iloc[i]
                    try:
                        # 营业收入
                        revenue_col = [c for c in df_profit.columns if '营业收入' in str(c)]
                        if revenue_col:
                            revenue = float(df_profit.iloc[i][revenue_col[0]]) / 1e8  # 转换为亿
                            if revenue > 0:
                                result['revenue_3y'].append(revenue)
                        
                        # 净利润
                        profit_col = [c for c in df_profit.columns if '净利润' in str(c) and '归属' in str(c)]
                        if profit_col:
                            profit = float(df_profit.iloc[i][profit_col[0]]) / 1e8
                            if profit != 0:
                                result['net_profit_3y'].append(profit)
                    except:
                        continue
                
                if result['data_source'] == 'none':
                    result['data_source'] = 'akshare_sina'
                    result['update_time'] = datetime.now().strftime('%Y-%m-%d')
                    
        except Exception as e:
            if result.get('error'):
                result['error'] += f'; 数据源3失败: {str(e)}'
            else:
                result['error'] = f'数据源3失败: {str(e)}'
        
        # 最终检查：如果所有数据源都失败，明确告知用户
        if result['data_source'] == 'none':
            result['error'] = result.get('error', '所有数据源均无法获取数据')
        
        return result
    
    def _safe_float(self, value) -> Optional[float]:
        """安全转换为浮点数"""
        try:
            if value is None or value == '' or value == '-':
                return None
            return float(str(value).replace(',', '').replace('%', '').replace('亿', ''))
        except:
            return None
    
    def get_business_segment(self) -> Dict:
        """
        获取业务分部数据
        """
        result = {
            'symbol': self.symbol,
            'segments': [],
            'data_source': 'none',
            'update_time': None,
            'error': None
        }
        
        try:
            import akshare as ak
            
            # 获取主营业务构成（尝试不同接口）
            try:
                # 方法1: 主营业务构成
                df = ak.stock_zygc_em(symbol=self.symbol)
            except:
                try:
                    # 方法2: 主营产品
                    df = ak.stock_zygc_ths(symbol=self.symbol, indicator='主营产品')
                except:
                    df = None
            
            if df is not None and len(df) > 0:
                segments = []
                total_revenue = 0
                
                for _, row in df.head(10).iterrows():
                    # 尝试解析不同格式的列名
                    name = str(row.get('分类') or row.get('业务类型') or row.get('产品') or row.get('行业') or row.get('主营产品') or '未知')
                    
                    # 尝试多个可能的列名
                    revenue = self._safe_float(row.get('营业收入') or row.get('主营收入') or row.get('收入'))
                    ratio = self._safe_float(row.get('收入占比') or row.get('占比') or row.get('比重'))
                    growth = self._safe_float(row.get('同比增长') or row.get('增速'))
                    
                    if revenue:
                        segment = {
                            'name': name,
                            'revenue': revenue / 1e8 if revenue > 1e8 else revenue,
                            'ratio': ratio if ratio else 0,
                            'growth': growth
                        }
                        segments.append(segment)
                        total_revenue += segment['revenue']
                
                # 计算占比（如果数据中没有）
                for seg in segments:
                    if seg['ratio'] == 0 and total_revenue > 0:
                        seg['ratio'] = round((seg['revenue'] / total_revenue) * 100, 2)
                
                result['segments'] = segments
                result['data_source'] = 'akshare_zygc'
                result['update_time'] = datetime.now().strftime('%Y-%m-%d')
            else:
                result['error'] = '业务分部数据为空或接口不可用'
                
        except Exception as e:
            result['error'] = f'业务分部数据获取失败: {str(e)}'
        
        return result
    
    def get_peer_comparison(self, peer_codes: List[str] = None) -> Dict:
        """
        获取可比公司对比
        """
        result = {
            'symbol': self.symbol,
            'peers': [],
            'industry_avg': {},
            'data_source': 'none',
            'update_time': None,
            'error': None
        }
        
        # 使用 agent-stock 获取数据（更稳定）
        try:
            import subprocess
            
            # 获取当前股票数据
            current_result = subprocess.run(
                ['python', '-m', 'stock', 'quote', self.symbol],
                capture_output=True,
                text=True,
                cwd=r'C:\Users\Administrator\.openclaw\workspace\.agents\skills\agent-stock',
                timeout=30
            )
            
            if current_result.returncode == 0:
                # 解析输出
                output = current_result.stdout
                peer_data = self._parse_quote_output(self.symbol, output)
                if peer_data:
                    peer_data['category'] = '当前股票'
                    result['peers'].append(peer_data)
            
            # 获取可比公司数据
            if peer_codes:
                for code in peer_codes[:5]:
                    try:
                        peer_result = subprocess.run(
                            ['python', '-m', 'stock', 'quote', code],
                            capture_output=True,
                            text=True,
                            cwd=r'C:\Users\Administrator\.openclaw\workspace\.agents\skills\agent-stock',
                            timeout=30
                        )
                        
                        if peer_result.returncode == 0:
                            peer_data = self._parse_quote_output(code, peer_result.stdout)
                            if peer_data:
                                peer_data['category'] = '可比公司'
                                result['peers'].append(peer_data)
                    except:
                        continue
            
            # 计算行业平均
            pe_values = [p['pe'] for p in result['peers'] if p.get('pe') and p['pe'] > 0]
            if pe_values:
                result['industry_avg'] = {
                    'pe_min': round(min(pe_values), 2),
                    'pe_max': round(max(pe_values), 2),
                    'pe_avg': round(sum(pe_values) / len(pe_values), 2)
                }
            
            result['data_source'] = 'agent-stock'
            result['update_time'] = datetime.now().strftime('%Y-%m-%d')
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _parse_quote_output(self, symbol: str, output: str) -> Optional[Dict]:
        """解析 agent-stock quote 输出"""
        import re
        
        try:
            # 解析名称
            name_match = re.search(r'名称:\s*(\S+)', output)
            name = name_match.group(1) if name_match else symbol
            
            # 解析价格
            price_match = re.search(r'价格:\s*([\d.]+)', output)
            price = float(price_match.group(1)) if price_match else None
            
            # 解析市盈率
            pe_match = re.search(r'市盈率:\s*([\d.]+)', output)
            pe = float(pe_match.group(1)) if pe_match else None
            
            # 解析市净率
            pb_match = re.search(r'市净率:\s*([\d.]+)', output)
            pb = float(pb_match.group(1)) if pb_match else None
            
            # 解析涨跌幅
            change_match = re.search(r'涨跌幅:\s*([\d.-]+)%', output)
            change_pct = float(change_match.group(1)) if change_match else None
            
            # 解析市值
            cap_match = re.search(r'总市值:\s*([\d.]+)亿', output)
            market_cap = float(cap_match.group(1)) if cap_match else None
            
            return {
                'symbol': symbol,
                'name': name,
                'pe': pe,
                'pb': pb,
                'price': price,
                'change_pct': change_pct,
                'market_cap': market_cap
            }
        except:
            return None
    
    def get_fundflow(self, days: int = 10) -> Dict:
        """
        获取资金流向数据
        """
        result = {
            'symbol': self.symbol,
            'history': [],
            'summary': {},
            'data_source': 'none',
            'update_time': None,
            'error': None
        }
        
        try:
            import akshare as ak
            
            # 确定市场代码
            market = 'sh' if self.symbol.startswith('6') else 'sz'
            
            # 获取个股资金流向
            df = ak.stock_individual_fund_flow(stock=self.symbol, market=market)
            
            if df is not None and len(df) > 0:
                history = []
                
                for _, row in df.head(days).iterrows():
                    try:
                        # 获取所有列值（避免编码问题）
                        values = row.values.tolist()
                        
                        entry = {
                            'date': str(values[0]) if len(values) > 0 else '',
                            'close': float(values[1]) if len(values) > 1 and values[1] else None,
                            'change_pct': float(values[2]) if len(values) > 2 and values[2] else None,
                            'total_net_inflow': float(values[3]) / 1e8 if len(values) > 3 and values[3] else None,
                            'total_net_inflow_pct': float(values[4]) if len(values) > 4 and values[4] else None,
                            'super_large_net_inflow': float(values[5]) / 1e8 if len(values) > 5 and values[5] else None,
                            'super_large_net_inflow_pct': float(values[6]) if len(values) > 6 and values[6] else None,
                            'large_net_inflow': float(values[7]) / 1e8 if len(values) > 7 and values[7] else None,
                            'large_net_inflow_pct': float(values[8]) if len(values) > 8 and values[8] else None,
                            'medium_net_inflow': float(values[9]) / 1e8 if len(values) > 9 and values[9] else None,
                            'medium_net_inflow_pct': float(values[10]) if len(values) > 10 and values[10] else None,
                            'small_net_inflow': float(values[11]) / 1e8 if len(values) > 11 and values[11] else None,
                            'small_net_inflow_pct': float(values[12]) if len(values) > 12 and values[12] else None,
                        }
                        
                        # 主力资金 = 超大单 + 大单
                        entry['main_net_inflow'] = None
                        if entry.get('super_large_net_inflow') is not None and entry.get('large_net_inflow') is not None:
                            entry['main_net_inflow'] = round(entry['super_large_net_inflow'] + entry['large_net_inflow'], 4)
                        
                        # 散户资金 = 中单 + 小单
                        entry['retail_net_inflow'] = None
                        if entry.get('medium_net_inflow') is not None and entry.get('small_net_inflow') is not None:
                            entry['retail_net_inflow'] = round(entry['medium_net_inflow'] + entry['small_net_inflow'], 4)
                        
                        history.append(entry)
                    except Exception as e:
                        continue
                
                # 计算汇总
                if history:
                    total_main = sum(h['main_net_inflow'] or 0 for h in history)
                    total_retail = sum(h['retail_net_inflow'] or 0 for h in history)
                    
                    result['history'] = history
                    result['summary'] = {
                        'total_main_inflow': round(total_main, 2),
                        'total_retail_inflow': round(total_retail, 2),
                        'avg_main_inflow': round(total_main / len(history), 4) if history else 0,
                        'main_inflow_days': sum(1 for h in history if h.get('main_net_inflow', 0) > 0),
                        'trend': 'inflow' if total_main > 0 else 'outflow'
                    }
                
                result['data_source'] = 'akshare_fundflow'
                result['update_time'] = datetime.now().strftime('%Y-%m-%d')
            else:
                result['error'] = '资金流向数据为空'
                
        except Exception as e:
            result['error'] = f'资金流向获取失败: {str(e)}'
        
        return result
    
    def get_risk_metrics(self) -> Dict:
        """
        获取风险指标
        """
        result = {
            'symbol': self.symbol,
            'customer_concentration': {},
            'raw_material_exposure': {},
            'valuation_percentile': {},
            'data_source': 'none',
            'update_time': None,
            'error': None
        }
        
        # 从财务摘要获取基础数据
        summary = self.get_financial_summary()
        
        if summary.get('data_source') != 'none':
            result['valuation_percentile'] = {
                'current_pe': summary.get('pe_ratio'),
                'current_pb': summary.get('pb_ratio'),
                'note': '估值分位需要历史数据，当前仅提供静态估值'
            }
            result['data_source'] = summary['data_source']
            result['update_time'] = summary.get('update_time')
        else:
            result['error'] = summary.get('error', '无法获取财务数据')
        
        return result


def get_financial_data(symbol: str, peer_codes: List[str] = None) -> Dict:
    """获取完整财务数据"""
    fetcher = FinancialDataFetcher(symbol)
    
    return {
        'symbol': symbol,
        'summary': fetcher.get_financial_summary(),
        'business': fetcher.get_business_segment(),
        'peers': fetcher.get_peer_comparison(peer_codes),
        'fundflow': fetcher.get_fundflow(10),
        'risk': fetcher.get_risk_metrics(),
        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='财报数据获取')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--type', choices=['summary', 'business', 'peers', 'fundflow', 'risk', 'all'], 
                       default='all', help='数据类型')
    parser.add_argument('--peers', nargs='+', help='可比公司代码')
    
    args = parser.parse_args()
    
    fetcher = FinancialDataFetcher(args.symbol)
    
    if args.type == 'summary':
        data = fetcher.get_financial_summary()
    elif args.type == 'business':
        data = fetcher.get_business_segment()
    elif args.type == 'peers':
        data = fetcher.get_peer_comparison(args.peers)
    elif args.type == 'fundflow':
        data = fetcher.get_fundflow(10)
    elif args.type == 'risk':
        data = fetcher.get_risk_metrics()
    else:
        data = get_financial_data(args.symbol, args.peers)
    
    print(json.dumps(data, indent=2, ensure_ascii=False))
