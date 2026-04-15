#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一财务数据模块 - 整合 akshare + yfinance
A股用 akshare，美股/港股用 yfinance
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Optional, List

# Windows 编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.quote import detect_market


class FinancialDataFetcher:
    """财务数据获取器"""
    
    def __init__(self, symbol: str):
        self.symbol = str(symbol).replace('.SS', '').replace('.SZ', '')
        self.market = detect_market(symbol)
        
    def get_summary(self) -> Dict:
        """
        获取财务摘要
        """
        if self.market == 'cn':
            return self._get_summary_cn()
        else:
            return self._get_summary_global()
    
    def _get_summary_cn(self) -> Dict:
        """A股财务摘要 (akshare)"""
        result = {
            'symbol': self.symbol,
            'market': 'cn',
            'revenue_3y': [],
            'net_profit_3y': [],
            'gross_margin': None,
            'net_margin': None,
            'roe': None,
            'debt_ratio': None,
            'data_source': 'none',
            'update_time': None,
            'error': None
        }
        
        try:
            import akshare as ak
            
            df = ak.stock_financial_abstract(symbol=self.symbol)
            
            if df is not None and len(df) > 0:
                # 解析营收和利润
                for _, row in df.head(10).iterrows():
                    try:
                        # 营收
                        revenue_val = row.iloc[1] if len(row) > 1 else None
                        if revenue_val:
                            revenue = float(str(revenue_val).replace(',', '').replace('亿', ''))
                            if revenue > 0:
                                result['revenue_3y'].append(revenue)
                        
                        # 净利润
                        profit_val = row.iloc[2] if len(row) > 2 else None
                        if profit_val:
                            profit = float(str(profit_val).replace(',', '').replace('亿', ''))
                            result['net_profit_3y'].append(profit)
                    except:
                        continue
                
                # 提取指标
                latest = df.iloc[0] if len(df) > 0 else None
                if latest is not None:
                    # 从列名推断
                    for col in df.columns:
                        col_str = str(col)
                        if '毛利' in col_str:
                            try:
                                result['gross_margin'] = float(latest[col])
                            except:
                                pass
                        elif '净利' in col_str and '率' in col_str:
                            try:
                                result['net_margin'] = float(latest[col])
                            except:
                                pass
                        elif 'ROE' in col_str or '净资产收益' in col_str:
                            try:
                                result['roe'] = float(latest[col])
                            except:
                                pass
                        elif '负债' in col_str:
                            try:
                                result['debt_ratio'] = float(latest[col])
                            except:
                                pass
                
                result['data_source'] = 'akshare'
                result['update_time'] = datetime.now().strftime('%Y-%m-%d')
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _get_summary_global(self) -> Dict:
        """美股/港股财务摘要"""
        result = {
            'symbol': self.symbol,
            'market': self.market,
            'revenue_3y': [],
            'net_profit_3y': [],
            'gross_margin': None,
            'net_margin': None,
            'roe': None,
            'debt_ratio': None,
            'data_source': 'none',
            'update_time': None,
            'error': None
        }
        
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(self.symbol)
            info = ticker.info
            
            # 基本信息
            result.update({
                'gross_margin': info.get('grossMargins'),
                'net_margin': info.get('profitMargins'),
                'roe': info.get('returnOnEquity'),
                'debt_ratio': info.get('debtToEquity'),
                'data_source': 'yfinance',
                'update_time': datetime.now().strftime('%Y-%m-%d')
            })
            
            # 历史营收/利润
            income_stmt = ticker.income_stmt
            if income_stmt is not None and len(income_stmt) > 0:
                for col in income_stmt.columns[:3]:  # 最近3年
                    try:
                        revenue = income_stmt.loc['Total Revenue', col] / 1e8
                        net_income = income_stmt.loc['Net Income', col] / 1e8
                        result['revenue_3y'].append(round(revenue, 2))
                        result['net_profit_3y'].append(round(net_income, 2))
                    except:
                        continue
                        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def get_fundflow(self, days: int = 10) -> Dict:
        """
        获取资金流向 (仅A股)
        """
        result = {
            'symbol': self.symbol,
            'history': [],
            'summary': {},
            'data_source': 'none',
            'update_time': None,
            'error': None
        }
        
        if self.market != 'cn':
            result['error'] = '资金流向仅支持A股'
            return result
        
        try:
            import akshare as ak
            
            market = 'sh' if self.symbol.startswith('6') else 'sz'
            df = ak.stock_individual_fund_flow(stock=self.symbol, market=market)
            
            if df is not None and len(df) > 0:
                history = []
                
                for _, row in df.head(days).iterrows():
                    values = row.values.tolist()
                    
                    entry = {
                        'date': str(values[0]) if len(values) > 0 else '',
                        'close': float(values[1]) if len(values) > 1 and values[1] else None,
                        'change_pct': float(values[2]) if len(values) > 2 and values[2] else None,
                        'main_net_inflow': round(float(values[5]) / 1e8 + float(values[7]) / 1e8, 4) if len(values) > 7 else None,
                        'retail_net_inflow': round(float(values[9]) / 1e8 + float(values[11]) / 1e8, 4) if len(values) > 11 else None,
                    }
                    history.append(entry)
                
                # 计算汇总
                total_main = sum(h['main_net_inflow'] or 0 for h in history)
                
                result['history'] = history
                result['summary'] = {
                    'total_main_inflow': round(total_main, 2),
                    'trend': 'inflow' if total_main > 0 else 'outflow'
                }
                result['data_source'] = 'akshare_fundflow'
                result['update_time'] = datetime.now().strftime('%Y-%m-%d')
                
        except Exception as e:
            result['error'] = str(e)
        
        return result


def get_financial_summary(symbol: str) -> Dict:
    """获取财务摘要"""
    fetcher = FinancialDataFetcher(symbol)
    return fetcher.get_summary()


def get_fundflow(symbol: str, days: int = 10) -> Dict:
    """获取资金流向"""
    fetcher = FinancialDataFetcher(symbol)
    return fetcher.get_fundflow(days)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='统一财务数据')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--type', choices=['summary', 'fundflow'], default='summary')
    
    args = parser.parse_args()
    
    fetcher = FinancialDataFetcher(args.symbol)
    
    if args.type == 'summary':
        result = fetcher.get_summary()
    else:
        result = fetcher.get_fundflow()
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
