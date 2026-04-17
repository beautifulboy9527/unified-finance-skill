#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票投资尽调分析器
8阶段基本面分析框架
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Optional
import yfinance as yf

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入共享模块
try:
    from skills.shared.citation_validator.validator import CitationValidator
    from skills.shared.risk_monitor.monitor import RiskMonitor
    SHARED_MODULES_AVAILABLE = True
except ImportError:
    SHARED_MODULES_AVAILABLE = False


class InvestmentStyle:
    """投资风格"""
    VALUE = 'value'        # 价值投资
    GROWTH = 'growth'      # 成长投资
    TURNAROUND = 'turnaround'  # 困境反转
    DIVIDEND = 'dividend'  # 红利投资


class SignalRating:
    """信号评级"""
    STRONG_BUY = '🟢🟢🟢'
    HOLD = '🟡🟡🟡'
    SELL = '🔴🔴'


class StockAnalyzer:
    """股票投资尽调分析器"""
    
    def __init__(self, style: str = InvestmentStyle.VALUE):
        """
        初始化分析器
        
        Args:
            style: 投资风格 (value/growth/turnaround/dividend)
        """
        self.style = style
        self.validator = CitationValidator() if SHARED_MODULES_AVAILABLE else None
        self.monitor = RiskMonitor(asset_type='stock') if SHARED_MODULES_AVAILABLE else None
        
        # 根据投资风格设置阶段优先级
        self.phase_priority = self._get_phase_priority(style)
    
    def _get_phase_priority(self, style: str) -> Dict:
        """根据投资风格获取阶段优先级"""
        priorities = {
            InvestmentStyle.VALUE: {
                'core': [4, 5, 7],      # 财务、治理、估值
                'secondary': [1, 2, 3],  # 业务、行业、拆解
                'optional': [6]          # 市场分歧
            },
            InvestmentStyle.GROWTH: {
                'core': [1, 2, 3],       # 业务、行业、拆解
                'secondary': [4, 7],     # 财务、估值
                'optional': [5, 6]       # 治理、分歧
            },
            InvestmentStyle.TURNAROUND: {
                'core': [4, 5],          # 财务、治理
                'secondary': [1, 6],     # 业务、分歧
                'optional': [2, 3, 7]    # 行业、拆解、估值
            },
            InvestmentStyle.DIVIDEND: {
                'core': [4, 5, 7],       # 财务、治理、估值
                'secondary': [1, 3],     # 业务、拆解
                'optional': [2, 6]       # 行业、分歧
            }
        }
        return priorities.get(style, priorities[InvestmentStyle.VALUE])
    
    def analyze(self, symbol: str, depth: str = 'standard') -> Dict:
        """
        执行完整分析
        
        Args:
            symbol: 股票代码
            depth: 分析深度 (quick/standard/deep)
            
        Returns:
            分析结果字典
        """
        print(f"开始分析 {symbol} (风格: {self.style}, 深度: {depth})")
        
        results = {
            'symbol': symbol,
            'style': self.style,
            'timestamp': datetime.now().isoformat(),
            'phases': {}
        }
        
        # 根据深度决定执行哪些阶段
        if depth == 'quick':
            phases_to_run = self.phase_priority['core']
        elif depth == 'standard':
            phases_to_run = self.phase_priority['core'] + self.phase_priority['secondary']
        else:  # deep
            phases_to_run = list(range(1, 9))
        
        # 执行各阶段分析
        for phase_num in phases_to_run:
            phase_method = getattr(self, f'_phase{phase_num}', None)
            if phase_method:
                print(f"  Phase {phase_num}...")
                results['phases'][phase_num] = phase_method(symbol)
        
        # 综合评分
        results['rating'] = self._calculate_rating(results)
        
        # 生成监控清单
        if self.monitor:
            results['monitoring_checklist'] = self.monitor.generate_checklist(symbol)
        
        return results
    
    def _phase1(self, symbol: str) -> Dict:
        """Phase 1: 公司事实底座"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'name': '公司事实底座',
                'data': {
                    'company_name': info.get('longName', ''),
                    'sector': info.get('sector', ''),
                    'industry': info.get('industry', ''),
                    'business_summary': info.get('longBusinessSummary', '')[:500],
                    'employees': info.get('fullTimeEmployees', 0),
                    'website': info.get('website', ''),
                },
                'citation': self._cite('yfinance') if self.validator else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _phase2(self, symbol: str) -> Dict:
        """Phase 2: 行业周期分析"""
        # TODO: 实现行业分析
        return {
            'name': '行业周期分析',
            'data': {
                'industry': '待分析',
                'cycle_stage': '待判断',
                'competition': '待分析'
            }
        }
    
    def _phase3(self, symbol: str) -> Dict:
        """Phase 3: 业务拆解"""
        # TODO: 实现业务拆解
        return {
            'name': '业务拆解',
            'data': {
                'segments': '待分析',
                'profit_drivers': '待分析',
                'pricing_power': '待分析'
            }
        }
    
    def _phase4(self, symbol: str) -> Dict:
        """Phase 4: 财务质量分析"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # 获取财务数据
            financials = ticker.financials
            cashflow = ticker.cashflow
            balance_sheet = ticker.balance_sheet
            
            # 计算关键指标
            revenue = info.get('totalRevenue', 0)
            net_income = info.get('netIncomeToCommon', 0)
            operating_cf = info.get('operatingCashflow', 0)
            total_assets = info.get('totalAssets', 0)
            total_debt = info.get('totalDebt', 0)
            shareholders_equity = info.get('totalStockholderEquity', 0)
            
            # 核心指标
            roe = (net_income / shareholders_equity * 100) if shareholders_equity else 0
            ocf_to_ni = (operating_cf / net_income) if net_income else 0
            debt_to_equity = (total_debt / shareholders_equity) if shareholders_equity else 0
            
            # 现金流验证
            cashflow_check = '✅' if ocf_to_ni > 0.8 else '⚠️' if ocf_to_ni > 0.5 else '❌'
            
            return {
                'name': '财务质量分析',
                'data': {
                    'key_metrics': {
                        'ROE': f'{roe:.1f}%',
                        '毛利率': f'{info.get("grossMargins", 0)*100:.1f}%',
                        '净利率': f'{info.get("profitMargins", 0)*100:.1f}%',
                        '负债率': f'{debt_to_equity:.2f}'
                    },
                    'cashflow_validation': {
                        'OCF/净利润': f'{ocf_to_ni:.2f}',
                        '判断': cashflow_check,
                        '说明': '利润质量高' if ocf_to_ni > 0.8 else '现金流偏弱'
                    },
                    'warnings': self._check_financial_warnings(info)
                },
                'citation': self._cite('yfinance') if self.validator else None
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _phase5(self, symbol: str) -> Dict:
        """Phase 5: 股权治理分析"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'name': '股权治理分析',
                'data': {
                    'institutional_ownership': f'{info.get("heldPercentInstitutions", 0)*100:.1f}%',
                    'insider_ownership': f'{info.get("heldPercentInsiders", 0)*100:.1f}%',
                    'shares_outstanding': info.get('sharesOutstanding', 0),
                    'float_shares': info.get('floatShares', 0),
                },
                'citation': self._cite('yfinance') if self.validator else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _phase6(self, symbol: str) -> Dict:
        """Phase 6: 市场分歧分析"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'name': '市场分歧分析',
                'data': {
                    'target_price': info.get('targetMeanPrice', 0),
                    'current_price': info.get('currentPrice', 0),
                    'analyst_recommendation': info.get('recommendationKey', 'N/A'),
                    'earnings_estimate': info.get('earningsEstimate', {})
                },
                'citation': self._cite('yfinance') if self.validator else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _phase7(self, symbol: str) -> Dict:
        """Phase 7: 估值与护城河分析"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # 估值指标
            pe_ratio = info.get('trailingPE', 0)
            pb_ratio = info.get('priceToBook', 0)
            ps_ratio = info.get('priceToSalesTrailing12Months', 0)
            ev_ebitda = info.get('enterpriseToEbitda', 0)
            
            # 护城河评分 (简化版)
            moat_score = self._estimate_moat(info)
            
            return {
                'name': '估值与护城河',
                'data': {
                    'valuation': {
                        'P/E': f'{pe_ratio:.1f}' if pe_ratio else 'N/A',
                        'P/B': f'{pb_ratio:.1f}' if pb_ratio else 'N/A',
                        'P/S': f'{ps_ratio:.1f}' if ps_ratio else 'N/A',
                        'EV/EBITDA': f'{ev_ebitda:.1f}' if ev_ebitda else 'N/A'
                    },
                    'moat_score': moat_score,
                    'moat_desc': self._get_moat_desc(moat_score)
                },
                'citation': self._cite('yfinance') if self.validator else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _phase8(self, symbol: str) -> Dict:
        """Phase 8: 综合报告"""
        # 此方法在 analyze() 中调用 _calculate_rating 后生成
        return {
            'name': '综合报告',
            'signal_rating': '待计算',
            'investment_thesis': '待生成'
        }
    
    def _check_financial_warnings(self, info: Dict) -> List[str]:
        """检查财务异常"""
        warnings = []
        
        # 检查现金流
        ocf = info.get('operatingCashflow', 0)
        ni = info.get('netIncomeToCommon', 0)
        if ni > 0 and ocf / ni < 0.5:
            warnings.append('⚠️ OCF/净利润 < 0.5，利润质量存疑')
        
        # 检查负债率
        debt = info.get('totalDebt', 0)
        equity = info.get('totalStockholderEquity', 0)
        if equity > 0 and debt / equity > 2:
            warnings.append('⚠️ 负债率 > 2，财务风险较高')
        
        # 检查盈利能力
        if info.get('profitMargins', 0) < 0:
            warnings.append('⚠️ 净利率为负，处于亏损状态')
        
        return warnings if warnings else ['✅ 无明显财务异常']
    
    def _estimate_moat(self, info: Dict) -> int:
        """估算护城河评分 (简化版)"""
        score = 0
        
        # 毛利率 (定价权)
        gross_margin = info.get('grossMargins', 0)
        if gross_margin > 0.5:
            score += 1
        if gross_margin > 0.7:
            score += 1
        
        # 市值 (规模效应)
        market_cap = info.get('marketCap', 0)
        if market_cap > 1e11:  # 1000亿
            score += 1
        
        # 品牌 (简化判断)
        if info.get('sector') in ['Technology', 'Healthcare']:
            score += 1
        
        # ROE (盈利能力)
        roe = info.get('returnOnEquity', 0)
        if roe > 0.15:
            score += 1
        
        return min(score, 5)
    
    def _get_moat_desc(self, score: int) -> str:
        """获取护城河描述"""
        if score >= 5:
            return '强护城河'
        elif score >= 3:
            return '弱护城河'
        else:
            return '无明显护城河'
    
    def _calculate_rating(self, results: Dict) -> Dict:
        """计算综合评级"""
        # 简化版评级逻辑
        score = 0
        
        # 财务质量评分
        if 4 in results['phases']:
            phase4 = results['phases'][4]
            if 'data' in phase4:
                cf_check = phase4['data'].get('cashflow_validation', {}).get('判断', '')
                if '✅' in cf_check:
                    score += 2
                elif '⚠️' in cf_check:
                    score += 1
                
                warnings = phase4['data'].get('warnings', [])
                if '✅' in str(warnings):
                    score += 1
        
        # 估值评分
        if 7 in results['phases']:
            phase7 = results['phases'][7]
            if 'data' in phase7:
                moat = phase7['data'].get('moat_score', 0)
                if moat >= 4:
                    score += 2
                elif moat >= 3:
                    score += 1
        
        # 确定评级
        if score >= 4:
            rating = SignalRating.STRONG_BUY
            recommendation = '基本面强劲，值得深入研究'
        elif score >= 2:
            rating = SignalRating.HOLD
            recommendation = '基本面尚可，需进一步分析'
        else:
            rating = SignalRating.SELL
            recommendation = '基本面存疑，建议谨慎'
        
        return {
            'rating': rating,
            'score': score,
            'recommendation': recommendation
        }
    
    def _cite(self, source: str) -> str:
        """生成引用"""
        if self.validator:
            return self.validator.cite(source, '', datetime.now().strftime('%Y-%m-%d'))
        return f"来源: {source}"
    
    def generate_report(self, symbol: str, output_dir: str = './reports') -> str:
        """
        生成分析报告
        
        Args:
            symbol: 股票代码
            output_dir: 输出目录
            
        Returns:
            报告文件路径
        """
        results = self.analyze(symbol)
        
        # 生成 Markdown 报告
        report_md = self._format_report_markdown(results)
        
        # 保存报告
        os.makedirs(output_dir, exist_ok=True)
        report_file = os.path.join(
            output_dir,
            f"STOCK_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_md)
        
        print(f"\n✅ 报告已生成: {report_file}")
        return report_file
    
    def _format_report_markdown(self, results: Dict) -> str:
        """格式化 Markdown 报告"""
        md = f"""# 股票投资尽调报告

**股票代码**: {results['symbol']}  
**投资风格**: {results['style']}  
**分析时间**: {results['timestamp']}  

---

## 综合评级

**信号评级**: {results['rating']['rating']}  
**评分**: {results['rating']['score']}/5  
**建议**: {results['rating']['recommendation']}  

---

"""
        
        # 添加各阶段分析
        for phase_num in sorted(results['phases'].keys()):
            phase = results['phases'][phase_num]
            md += f"## Phase {phase_num}: {phase['name']}\n\n"
            
            if 'error' in phase:
                md += f"❌ 分析失败: {phase['error']}\n\n"
            else:
                for key, value in phase.get('data', {}).items():
                    if isinstance(value, dict):
                        md += f"### {key}\n\n"
                        for k, v in value.items():
                            md += f"- **{k}**: {v}\n"
                        md += "\n"
                    elif isinstance(value, list):
                        md += f"### {key}\n\n"
                        for v in value:
                            md += f"- {v}\n"
                        md += "\n"
                    else:
                        md += f"- **{key}**: {value}\n"
                md += "\n"
            
            if phase.get('citation'):
                md += f"> {phase['citation']}\n\n"
        
        # 添加监控清单
        if 'monitoring_checklist' in results:
            md += "---\n\n"
            md += results['monitoring_checklist']
        
        # 免责声明
        md += """
---

## ⚠️ 免责声明

本报告仅供参考，不构成投资建议。所有分析基于公开信息，可能存在滞后或不完整。投资有风险，决策需谨慎。

---

*by Neo9527 Finance Skill v4.9*
"""
        
        return md


# 快速使用函数
def analyze_stock(symbol: str, style: str = 'value') -> Dict:
    """快速分析股票"""
    analyzer = StockAnalyzer(style=style)
    return analyzer.analyze(symbol)


# 测试
if __name__ == '__main__':
    print("=" * 60)
    print("股票投资尽调分析器测试")
    print("=" * 60)
    
    # 测试美股
    analyzer = StockAnalyzer(style=InvestmentStyle.VALUE)
    results = analyzer.analyze('AAPL', depth='quick')
    
    print(f"\n综合评级: {results['rating']['rating']}")
    print(f"建议: {results['rating']['recommendation']}")
    
    # 测试生成报告
    report_file = analyzer.generate_report('AAPL', output_dir='D:/OpenClaw/outputs/reports')
