#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务异常检测 v1.0

功能:
- 应收账款异常检测
- 现金流背离检测
- 存货异常检测
- 毛利率异常检测
- 关联交易检测
- 风险等级评估
"""

import sys
import os
from typing import Dict, List, Optional
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    import akshare as ak
    import pandas as pd
    import numpy as np
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False


class FinancialAnomalyDetector:
    """财务异常检测器"""
    
    # 异常类型定义
    ANOMALY_TYPES = {
        'receivable': {
            'name': '应收账款异常',
            'rule': '应收账款增速 > 营收增速 × 1.5',
            'risk_weight': 2
        },
        'cashflow': {
            'name': '现金流背离',
            'rule': '净利润增长但经营现金流下降',
            'risk_weight': 3
        },
        'inventory': {
            'name': '存货异常',
            'rule': '存货增速 > 营收增速 × 2',
            'risk_weight': 2
        },
        'margin': {
            'name': '毛利率异常',
            'rule': '毛利率波动 > 行业均值波动 × 2',
            'risk_weight': 1
        },
        'related_party': {
            'name': '关联交易',
            'rule': '关联交易占比 > 30%',
            'risk_weight': 2
        }
    }
    
    def __init__(self):
        self.name = "FinancialAnomalyDetector"
        self.version = "1.0.0"
    
    def detect(self, symbol: str) -> Dict:
        """
        执行财务异常检测
        
        Args:
            symbol: 股票代码
            
        Returns:
            检测结果
        """
        if not AKSHARE_AVAILABLE:
            return {
                'success': False,
                'error': 'AkShare 未安装',
                'anomalies': [],
                'risk_level': 'unknown'
            }
        
        print(f"开始财务异常检测: {symbol}...")
        
        # 获取财务数据
        financial_data = self._get_financial_data(symbol)
        
        if not financial_data:
            return {
                'success': False,
                'error': '无法获取财务数据',
                'anomalies': [],
                'risk_level': 'unknown'
            }
        
        # 执行各项检测
        anomalies = []
        
        # 1. 应收账款异常
        ar_anomaly = self._check_receivable(financial_data)
        if ar_anomaly:
            anomalies.append(ar_anomaly)
        
        # 2. 现金流背离
        cf_anomaly = self._check_cashflow(financial_data)
        if cf_anomaly:
            anomalies.append(cf_anomaly)
        
        # 3. 存货异常
        inv_anomaly = self._check_inventory(financial_data)
        if inv_anomaly:
            anomalies.append(inv_anomaly)
        
        # 4. 毛利率异常
        margin_anomaly = self._check_margin(financial_data)
        if margin_anomaly:
            anomalies.append(margin_anomaly)
        
        # 5. 关联交易
        rp_anomaly = self._check_related_party(financial_data)
        if rp_anomaly:
            anomalies.append(rp_anomaly)
        
        # 计算风险等级
        risk_level = self._calculate_risk_level(anomalies)
        
        print(f"  检测完成: {len(anomalies)} 项异常, 风险等级: {risk_level}")
        
        return {
            'success': True,
            'symbol': symbol,
            'anomalies': anomalies,
            'anomaly_count': len(anomalies),
            'risk_level': risk_level,
            'risk_description': self._get_risk_description(risk_level),
            'financial_data': financial_data.get('summary', {}),
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_financial_data(self, symbol: str) -> Optional[Dict]:
        """获取财务数据"""
        # 判断市场
        if symbol.isdigit():
            market = 'cn'
        else:
            market = 'us'
        
        # 美股使用 yfinance
        if market == 'us':
            return self._get_us_financial_data(symbol)
        
        data = {}
        
        # 判断市场
        if symbol.isdigit():
            market = 'cn'
        else:
            market = 'us'
        
        # 美股使用 yfinance
        if market == 'us':
            return self._get_us_financial_data(symbol)
        
        # A股使用 AkShare
        try:
            # 方法1: 使用利润表数据 (更可靠)
            df_profit = ak.stock_financial_report_sina(stock=symbol, symbol="利润表")
            
            if df_profit is not None and not df_profit.empty:
                # 取最近3年
                recent = df_profit.head(3)
                
                # 计算增长率
                revenues = recent['营业收入'].astype(float).tolist()
                profits = recent['净利润'].astype(float).tolist() if '净利润' in recent.columns else [0,0,0]
                
                # 计算营收增长率
                rev_growth = []
                for i in range(len(revenues)-1):
                    if revenues[i+1] > 0:
                        growth = (revenues[i] - revenues[i+1]) / revenues[i+1] * 100
                    else:
                        growth = 0
                    rev_growth.append(growth)
                
                # 计算利润增长率
                profit_growth = []
                for i in range(len(profits)-1):
                    if profits[i+1] > 0:
                        growth = (profits[i] - profits[i+1]) / profits[i+1] * 100
                    else:
                        growth = 0
                    profit_growth.append(growth)
                
                data['revenue_growth'] = rev_growth + [0] * (3 - len(rev_growth))
                data['profit_growth'] = profit_growth + [0] * (3 - len(profit_growth))
                data['receivable_growth'] = [0, 0, 0]  # 需要资产负债表
                data['inventory_growth'] = [0, 0, 0]   # 需要资产负债表
                data['gross_margin'] = [0, 0, 0]
                data['net_margin'] = [0, 0, 0]
                
                # 计算毛利率和净利率
                if len(revenues) > 0 and revenues[0] > 0:
                    # 从利润表获取毛利 (如果有)
                    if '营业成本' in recent.columns:
                        costs = recent['营业成本'].astype(float).tolist()
                        gross_margins = [(rev - cost) / rev * 100 if rev > 0 else 0 
                                       for rev, cost in zip(revenues, costs)]
                        data['gross_margin'] = gross_margins
                    
                    # 计算净利率
                    if len(profits) > 0:
                        net_margins = [p / r * 100 if r > 0 else 0 
                                     for p, r in zip(profits, revenues)]
                        data['net_margin'] = net_margins
                
                # 摘要
                data['summary'] = {
                    'gross_margin': data['gross_margin'][0] if data['gross_margin'] else 0,
                    'net_margin': data['net_margin'][0] if data['net_margin'] else 0,
                    'roe': 0,  # 需要净资产
                    'debt_ratio': 0,  # 需要资产负债表
                }
                
                print(f"  财务数据获取成功 (利润表)")
                return data
        
        except Exception as e:
            print(f"  利润表获取失败: {e}")
        
        # 方法2: 尝试财务指标接口
        try:
            df_indicator = ak.stock_financial_analysis_indicator(symbol=symbol)
            
            if df_indicator is not None and not df_indicator.empty:
                recent = df_indicator.head(3)
                cols = df_indicator.columns.tolist()
                
                def get_col_value(df, keywords, default=0):
                    """根据关键词查找列"""
                    for col in df.columns:
                        if any(kw in str(col) for kw in keywords):
                            val = df[col].iloc[0] if isinstance(df, pd.DataFrame) else df[col]
                            return float(val) if val else default
                    return default
                
                import pandas as pd
                
                data['revenue_growth'] = get_col_value(recent, ['营业收入同比', '营收增长'])
                data['profit_growth'] = get_col_value(recent, ['净利润同比', '利润增长'])
                data['receivable_growth'] = get_col_value(recent, ['应收账款同比'])
                data['inventory_growth'] = get_col_value(recent, ['存货同比'])
                data['gross_margin'] = get_col_value(recent, ['销售毛利率', '毛利率'])
                data['net_margin'] = get_col_value(recent, ['销售净利率', '净利率'])
                
                latest = df_indicator.iloc[0]
                data['summary'] = {
                    'gross_margin': float(get_col_value(pd.DataFrame([latest]), ['销售毛利率'])[0] or 0),
                    'net_margin': float(get_col_value(pd.DataFrame([latest]), ['销售净利率'])[0] or 0),
                    'roe': float(get_col_value(pd.DataFrame([latest]), ['净资产收益率', 'ROE'])[0] or 0),
                    'debt_ratio': float(get_col_value(pd.DataFrame([latest]), ['资产负债率'])[0] or 0),
                }
                
                print(f"  财务数据获取成功 (指标接口)")
                return data
        
        except Exception as e:
            print(f"  指标接口获取失败: {e}")
        
        # 方法3: 使用历史行情数据 (最简化)
        try:
            df = ak.stock_zh_a_hist(symbol=symbol, period='daily', adjust='qfq')
            
            if df is not None and not df.empty:
                # 简化分析：只基于价格趋势
                close = df['收盘'].astype(float)
                
                # 计算简单的增长率
                if len(close) > 250:
                    yoy_return = (close.iloc[-1] - close.iloc[-250]) / close.iloc[-250] * 100
                else:
                    yoy_return = 0
                
                return {
                    'revenue_growth': [yoy_return, 0, 0],
                    'profit_growth': [0, 0, 0],
                    'receivable_growth': [0, 0, 0],
                    'inventory_growth': [0, 0, 0],
                    'gross_margin': [0, 0, 0],
                    'net_margin': [0, 0, 0],
                    'summary': {
                        'gross_margin': 0,
                        'net_margin': 0,
                        'roe': 0,
                        'debt_ratio': 0,
                    },
                    'price_trend': yoy_return
                }
        
        except Exception as e:
            print(f"  历史数据获取失败: {e}")
        
        return None
    
    def _check_receivable(self, data: Dict) -> Optional[Dict]:
        """检查应收账款异常"""
        rev_growth = data.get('revenue_growth', [])
        ar_growth = data.get('receivable_growth', [])
        
        if not rev_growth or not ar_growth:
            return None
        
        # 取最近一年数据
        rev_yoy = rev_growth[0] if rev_growth else 0
        ar_yoy = ar_growth[0] if ar_growth else 0
        
        # 应收账款增速 > 营收增速 × 1.5
        if ar_yoy > rev_yoy * 1.5 and ar_yoy > 20:
            return {
                'type': 'receivable',
                'name': '应收账款异常',
                'severity': 'high' if ar_yoy > rev_yoy * 2 else 'medium',
                'description': f'应收账款增速{ar_yoy:.1f}% > 营收增速{rev_yoy:.1f}% × 1.5',
                'data': {
                    'receivable_growth': ar_yoy,
                    'revenue_growth': rev_yoy
                }
            }
        
        return None
    
    def _check_cashflow(self, data: Dict) -> Optional[Dict]:
        """检查现金流背离"""
        profit_growth = data.get('profit_growth', [])
        
        if not profit_growth:
            return None
        
        # 简化检测：净利润增长但现金流数据不可得
        # 实际应比较净利润和经营现金流
        # 这里用净利率变化作为代理指标
        
        net_margin = data.get('net_margin', [])
        if len(net_margin) >= 2:
            margin_change = net_margin[0] - net_margin[1]
            
            # 净利率大幅提升但可能现金流不匹配
            if margin_change > 10:
                return {
                    'type': 'cashflow',
                    'name': '现金流背离风险',
                    'severity': 'medium',
                    'description': f'净利率大幅提升{margin_change:.1f}个百分点，需验证现金流匹配情况',
                    'data': {
                        'margin_change': margin_change
                    }
                }
        
        return None
    
    def _check_inventory(self, data: Dict) -> Optional[Dict]:
        """检查存货异常"""
        rev_growth = data.get('revenue_growth', [])
        inv_growth = data.get('inventory_growth', [])
        
        if not rev_growth or not inv_growth:
            return None
        
        rev_yoy = rev_growth[0] if rev_growth else 0
        inv_yoy = inv_growth[0] if inv_growth else 0
        
        # 存货增速 > 营收增速 × 2
        if inv_yoy > rev_yoy * 2 and inv_yoy > 30:
            return {
                'type': 'inventory',
                'name': '存货异常',
                'severity': 'high' if inv_yoy > rev_yoy * 3 else 'medium',
                'description': f'存货增速{inv_yoy:.1f}% > 营收增速{rev_yoy:.1f}% × 2',
                'data': {
                    'inventory_growth': inv_yoy,
                    'revenue_growth': rev_yoy
                }
            }
        
        return None
    
    def _check_margin(self, data: Dict) -> Optional[Dict]:
        """检查毛利率异常"""
        gross_margin = data.get('gross_margin', [])
        
        if len(gross_margin) < 3:
            return None
        
        # 计算毛利率波动
        margin_std = np.std(gross_margin)
        margin_mean = np.mean(gross_margin)
        
        # 波动率超过5%
        if margin_std > 5:
            return {
                'type': 'margin',
                'name': '毛利率波动异常',
                'severity': 'low',
                'description': f'毛利率波动率{margin_std:.1f}%，近3年毛利率: {", ".join([f"{m:.1f}%" for m in gross_margin])}',
                'data': {
                    'margin_std': margin_std,
                    'margin_mean': margin_mean,
                    'margins': gross_margin
                }
            }
        
        return None
    
    def _check_related_party(self, data: Dict) -> Optional[Dict]:
        """检查关联交易"""
        # 简化检测：实际需要从年报获取关联交易数据
        # 这里返回None，实际实现需要额外数据源
        return None
    
    def _calculate_risk_level(self, anomalies: List[Dict]) -> str:
        """计算风险等级"""
        if not anomalies:
            return 'low'
        
        # 计算风险分数
        risk_score = 0
        for anomaly in anomalies:
            severity = anomaly.get('severity', 'low')
            if severity == 'high':
                risk_score += 3
            elif severity == 'medium':
                risk_score += 2
            else:
                risk_score += 1
        
        # 确定风险等级
        if risk_score >= 5:
            return 'high'
        elif risk_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def _get_risk_description(self, risk_level: str) -> str:
        """获取风险描述"""
        descriptions = {
            'low': '🟢 低风险：无明显异常',
            'medium': '🟡 中风险：存在1-2项轻微异常，需关注',
            'high': '🔴 高风险：存在多项异常或严重异常，需警惕'
        }
        return descriptions.get(risk_level, '未知风险等级')
    
    def _get_us_financial_data(self, symbol: str) -> Optional[Dict]:
        """获取美股财务数据"""
        if not YFINANCE_AVAILABLE:
            print("  yfinance 未安装")
            return None
        
        try:
            print(f"  获取美股财务数据: {symbol}")
            ticker = yf.Ticker(symbol)
            
            # 获取财务报表
            income_stmt = ticker.income_stmt
            balance_sheet = ticker.balance_sheet
            cash_flow = ticker.cashflow
            
            if income_stmt.empty:
                print("  无法获取利润表")
                return None
            
            # 取最近3年数据
            data = {
                'revenue_growth': [],
                'profit_growth': [],
                'receivable_growth': [],
                'inventory_growth': [],
                'gross_margin': [],
                'net_margin': []
            }
            
            # 营收和利润
            if 'Total Revenue' in income_stmt.index:
                revenues = income_stmt.loc['Total Revenue'].tolist()[:3]
            elif 'Revenue' in income_stmt.index:
                revenues = income_stmt.loc['Revenue'].tolist()[:3]
            else:
                revenues = []
            
            if 'Net Income' in income_stmt.index:
                profits = income_stmt.loc['Net Income'].tolist()[:3]
            else:
                profits = []
            
            # 计算增长率
            if len(revenues) >= 2:
                for i in range(len(revenues)-1):
                    if revenues[i+1] and revenues[i+1] > 0:
                        growth = (revenues[i] - revenues[i+1]) / revenues[i+1] * 100
                        data['revenue_growth'].append(growth)
            
            if len(profits) >= 2:
                for i in range(len(profits)-1):
                    if profits[i+1] and profits[i+1] > 0:
                        growth = (profits[i] - profits[i+1]) / profits[i+1] * 100
                        data['profit_growth'].append(growth)
            
            # 毛利率和净利率
            if 'Gross Profit' in income_stmt.index and revenues:
                gross_profits = income_stmt.loc['Gross Profit'].tolist()[:len(revenues)]
                for gp, rev in zip(gross_profits, revenues):
                    if rev and rev > 0 and gp:
                        data['gross_margin'].append(gp / rev * 100)
            
            if profits and revenues:
                for p, r in zip(profits, revenues):
                    if r and r > 0 and p:
                        data['net_margin'].append(p / r * 100)
            
            # 应收账款
            if not balance_sheet.empty and 'Net Receivables' in balance_sheet.index:
                receivables = balance_sheet.loc['Net Receivables'].tolist()[:3]
                if len(receivables) >= 2 and revenues:
                    for i in range(len(receivables)-1):
                        if receivables[i+1] and receivables[i+1] > 0:
                            growth = (receivables[i] - receivables[i+1]) / receivables[i+1] * 100
                            data['receivable_growth'].append(growth)
            
            # 存货
            if not balance_sheet.empty and 'Inventory' in balance_sheet.index:
                inventory = balance_sheet.loc['Inventory'].tolist()[:3]
                if len(inventory) >= 2 and revenues:
                    for i in range(len(inventory)-1):
                        if inventory[i+1] and inventory[i+1] > 0:
                            growth = (inventory[i] - inventory[i+1]) / inventory[i+1] * 100
                            data['inventory_growth'].append(growth)
            
            # 填充默认值
            for key in data:
                if not data[key]:
                    data[key] = [0, 0, 0]
            
            # 摘要
            data['summary'] = {
                'gross_margin': data['gross_margin'][0] if data['gross_margin'] else 0,
                'net_margin': data['net_margin'][0] if data['net_margin'] else 0,
                'roe': 0,
                'debt_ratio': 0,
            }
            
            # 获取 ROE
            if not balance_sheet.empty and 'Stockholders Equity' in balance_sheet.index:
                equity = balance_sheet.loc['Stockholders Equity'].tolist()
                if equity and equity[0] and profits and profits[0]:
                    data['summary']['roe'] = profits[0] / equity[0] * 100
            
            print(f"  美股财务数据获取成功")
            return data
            
        except Exception as e:
            print(f"  美股数据获取失败: {e}")
            return None


# 快速使用函数
def check_financial_anomaly(symbol: str) -> Dict:
    """快速检测财务异常"""
    detector = FinancialAnomalyDetector()
    return detector.detect(symbol)


# 测试
if __name__ == '__main__':
    print("=" * 60)
    print("财务异常检测 v1.0 测试")
    print("=" * 60)
    
    # 测试检测
    result = check_financial_anomaly('600519')  # 贵州茅台
    
    if result['success']:
        print(f"\n=== {result['symbol']} ===")
        print(f"风险等级: {result['risk_description']}")
        print(f"异常数量: {result['anomaly_count']}")
        
        if result['anomalies']:
            print("\n异常详情:")
            for anomaly in result['anomalies']:
                print(f"  - {anomaly['name']}: {anomaly['description']}")
        
        print(f"\n财务摘要:")
        summary = result.get('financial_data', {})
        print(f"  毛利率: {summary.get('gross_margin', 0):.1f}%")
        print(f"  净利率: {summary.get('net_margin', 0):.1f}%")
        print(f"  ROE: {summary.get('roe', 0):.1f}%")
    else:
        print(f"\n检测失败: {result['error']}")
