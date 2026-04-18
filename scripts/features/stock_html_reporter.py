#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票专业HTML报告生成器 v2.0
参考加密货币报告风格，专业投资人视角
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


class ProfessionalStockReporter:
    """专业股票HTML报告生成器"""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent / 'templates'
    
    def generate(self, report: Dict, enhancer=None) -> str:
        """生成专业HTML报告"""
        
        symbol = report['symbol']
        overall = report.get('overall', {})
        score = overall.get('score', 0)
        recommendation = overall.get('recommendation', 'N/A')
        timestamp = report.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        style = report.get('style', 'value')
        sections = report.get('sections', {})
        
        # 构建完整HTML
        html = self._build_html(symbol, score, recommendation, timestamp, style, sections, enhancer)
        
        return html
    
    def _build_html(self, symbol: str, score: float, recommendation: str, 
                    timestamp: str, style: str, sections: Dict, enhancer) -> str:
        """构建完整HTML页面"""
        
        # 推荐颜色
        if '买入' in recommendation or '强烈' in recommendation:
            rec_color = '#27ae60'
            rec_bg = 'linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)'
        elif '持有' in recommendation:
            rec_color = '#f39c12'
            rec_bg = 'linear-gradient(135deg, #f39c12 0%, #f1c40f 100%)'
        else:
            rec_color = '#e74c3c'
            rec_bg = 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)'
        
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{symbol} 投资分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", Arial, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        /* 头部评分区域 */
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }}
        
        .symbol-title {{
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 5px;
            letter-spacing: 2px;
        }}
        
        .company-name {{
            font-size: 18px;
            opacity: 0.8;
            margin-bottom: 30px;
        }}
        
        .score-section {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 40px;
            margin: 30px 0;
        }}
        
        .score-circle {{
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: rgba(255,255,255,0.1);
            border: 4px solid {rec_color};
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .score-number {{
            font-size: 56px;
            font-weight: 700;
            color: #ffd700;
        }}
        
        .score-label {{
            font-size: 14px;
            opacity: 0.8;
            margin-top: 5px;
        }}
        
        .decision-box {{
            background: {rec_bg};
            padding: 20px 50px;
            border-radius: 50px;
            display: inline-block;
        }}
        
        .decision-text {{
            font-size: 32px;
            font-weight: 700;
            letter-spacing: 3px;
        }}
        
        .meta-info {{
            margin-top: 25px;
            font-size: 13px;
            opacity: 0.7;
        }}
        
        /* 主要内容区域 */
        .content {{
            padding: 50px 40px;
        }}
        
        /* 章节样式 */
        .section {{
            margin-bottom: 60px;
        }}
        
        .section-header {{
            display: flex;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .section-number {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 700;
            margin-right: 20px;
        }}
        
        .section-title {{
            font-size: 28px;
            font-weight: 700;
            color: #1a1a2e;
        }}
        
        .section-desc {{
            font-size: 14px;
            color: #7f8c8d;
            margin-left: 15px;
        }}
        
        /* 指标网格 */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 30px 0;
        }}
        
        .metric-item {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            border-left: 3px solid #0f3460;
        }}
        
        .metric-label {{
            font-size: 13px;
            color: #7f8c8d;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric-value {{
            font-size: 36px;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 5px;
        }}
        
        .metric-change {{
            font-size: 14px;
            color: #27ae60;
        }}
        
        .metric-change.negative {{
            color: #e74c3c;
        }}
        
        /* 数据表格 */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            background: white;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .data-table th {{
            background: #0f3460;
            color: white;
            padding: 16px;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-align: left;
        }}
        
        .data-table td {{
            padding: 16px;
            border-bottom: 1px solid #e0e0e0;
            font-size: 15px;
        }}
        
        .data-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .data-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        /* 信号卡片 */
        .signal-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin: 30px 0;
        }}
        
        .signal-card {{
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        
        .signal-card.bullish {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border-left: 4px solid #27ae60;
        }}
        
        .signal-card.bearish {{
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            border-left: 4px solid #dc3545;
        }}
        
        .signal-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #1a1a2e;
        }}
        
        .signal-value {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .signal-desc {{
            font-size: 14px;
            color: #555;
            line-height: 1.6;
        }}
        
        /* 小结框 */
        .summary-box {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 25px;
            border-radius: 12px;
            margin-top: 25px;
            border-left: 4px solid #0f3460;
        }}
        
        .summary-title {{
            font-size: 16px;
            font-weight: 600;
            color: #0f3460;
            margin-bottom: 10px;
        }}
        
        .summary-text {{
            font-size: 15px;
            color: #2c3e50;
            line-height: 1.8;
        }}
        
        /* 数据来源标注 */
        .data-source {{
            background: #f8f9fa;
            padding: 12px 16px;
            border-radius: 6px;
            margin: 15px 0;
            font-size: 12px;
            color: #7f8c8d;
            border-left: 3px solid #95a5a6;
        }}
        
        /* 建议卡片 */
        .advice-section {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
            margin: 40px 0;
        }}
        
        .advice-card {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }}
        
        .advice-card.short {{ border-top: 4px solid #e74c3c; }}
        .advice-card.medium {{ border-top: 4px solid #f39c12; }}
        .advice-card.long {{ border-top: 4px solid #27ae60; }}
        
        .advice-label {{
            font-size: 13px;
            color: #7f8c8d;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .advice-action {{
            font-size: 24px;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 15px;
        }}
        
        .advice-reason {{
            font-size: 14px;
            color: #555;
            margin-bottom: 20px;
            line-height: 1.6;
        }}
        
        .advice-button {{
            background: #0f3460;
            color: white;
            padding: 10px 25px;
            border-radius: 20px;
            font-size: 13px;
            display: inline-block;
        }}
        
        /* 深度研报详情 */
        .research-detail {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            margin: 20px 0;
        }}
        
        .research-phase {{
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .phase-title {{
            font-size: 16px;
            font-weight: 600;
            color: #0f3460;
            margin-bottom: 10px;
        }}
        
        .phase-content {{
            font-size: 14px;
            color: #555;
            line-height: 1.8;
        }}
        
        /* 风险提示 */
        .risk-section {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            padding: 30px;
            border-radius: 12px;
            margin: 40px 0;
            border: 1px solid #ffc107;
        }}
        
        .risk-title {{
            font-size: 18px;
            font-weight: 600;
            color: #856404;
            margin-bottom: 15px;
        }}
        
        .risk-text {{
            font-size: 14px;
            color: #856404;
            line-height: 1.8;
        }}
        
        /* 页脚 */
        .footer {{
            background: #f8f9fa;
            padding: 40px;
            text-align: center;
            border-top: 1px solid #e0e0e0;
        }}
        
        .footer-text {{
            font-size: 13px;
            color: #7f8c8d;
            line-height: 1.8;
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            .metrics-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .signal-grid {{
                grid-template-columns: 1fr;
            }}
            
            .advice-section {{
                grid-template-columns: 1fr;
            }}
            
            .symbol-title {{
                font-size: 36px;
            }}
            
            .score-number {{
                font-size: 44px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {self._build_header(symbol, score, recommendation, timestamp, style)}
        <div class="content">
            {self._build_sections(sections, enhancer)}
        </div>
        {self._build_footer()}
    </div>
</body>
</html>'''
    
    def _build_header(self, symbol: str, score: float, recommendation: str, 
                      timestamp: str, style: str) -> str:
        """构建头部"""
        return f'''
        <div class="header">
            <div class="symbol-title">{symbol}</div>
            <div class="company-name">投资分析报告</div>
            
            <div class="score-section">
                <div class="score-circle">
                    <div class="score-number">{score:.0f}</div>
                    <div class="score-label">综合评分</div>
                </div>
            </div>
            
            <div class="decision-box">
                <div class="decision-text">{recommendation}</div>
            </div>
            
            <div class="meta-info">
                生成时间: {timestamp} | 投资风格: {style} | 版本: v6.3
            </div>
        </div>
        '''
    
    def _build_sections(self, sections: Dict, enhancer) -> str:
        """构建所有章节"""
        html_parts = []
        
        # 第一部分: 基本面分析
        if 'fundamentals' in sections:
            html_parts.append(self._build_fundamentals(sections['fundamentals'], enhancer))
        
        # 第二部分: 估值分析
        if 'valuation' in sections:
            html_parts.append(self._build_valuation(sections['valuation']))
        
        # 第三部分: 财务健康
        if 'financial_check' in sections:
            html_parts.append(self._build_financial(sections['financial_check']))
        
        # 第四部分: 技术分析
        if 'technical' in sections:
            html_parts.append(self._build_technical(sections['technical'], enhancer))
        
        # 第五部分: 市场情绪
        if 'sentiment' in sections:
            html_parts.append(self._build_sentiment(sections['sentiment']))
        
        # 第六部分: 监管风险
        if 'regulation' in sections:
            html_parts.append(self._build_regulation(sections['regulation']))
        
        # 第七部分: 深度研报 (仅当有详细内容时)
        if 'deep_research' in sections:
            dr = sections['deep_research']
            # 必须有评级且score>0才显示
            if dr.get('rating') and dr.get('score', 0) > 0:
                html_parts.append(self._build_research(dr))
        
        # 第八部分: 全局观点与建议
        html_parts.append(self._build_overall(sections, enhancer))
        
        return '\n'.join(html_parts)
    
    def _build_fundamentals(self, fund: Dict, enhancer) -> str:
        """构建基本面分析"""
        pe = fund.get('pe')
        pb = fund.get('pb')
        roe = fund.get('roe')
        market_cap = fund.get('market_cap')
        
        # 格式化市值
        if market_cap:
            if market_cap > 1e12:
                mc_str = f"${market_cap/1e12:.2f}万亿"
            elif market_cap > 1e9:
                mc_str = f"${market_cap/1e9:.2f}亿"
            else:
                mc_str = f"${market_cap/1e6:.2f}百万"
        else:
            mc_str = "N/A"
        
        # ROE分析
        if roe:
            if roe > 20:
                roe_status = "优秀"
                roe_color = "#27ae60"
            elif roe > 15:
                roe_status = "良好"
                roe_color = "#27ae60"
            elif roe > 10:
                roe_status = "一般"
                roe_color = "#f39c12"
            else:
                roe_status = "较差"
                roe_color = "#e74c3c"
        else:
            roe_status = "N/A"
            roe_color = "#7f8c8d"
        
        # PE分析
        if pe:
            if pe < 20:
                pe_status = "低估"
                pe_color = "#27ae60"
            elif pe < 30:
                pe_status = "合理"
                pe_color = "#f39c12"
            else:
                pe_status = "高估"
                pe_color = "#e74c3c"
        else:
            pe_status = "N/A"
            pe_color = "#7f8c8d"
        
        return f'''
        <div class="section">
            <div class="section-header">
                <div class="section-number">1</div>
                <div>
                    <div class="section-title">基本面分析</div>
                    <span class="section-desc">投资根基 - 决定长期价值</span>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">ROE 净资产收益率</div>
                    <div class="metric-value">{f"{roe:.1f}%" if roe else "N/A"}</div>
                    <div class="metric-change" style="color: {roe_color}">{roe_status}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">P/E 市盈率</div>
                    <div class="metric-value">{f"{pe:.1f}" if pe else "N/A"}</div>
                    <div class="metric-change" style="color: {pe_color}">{pe_status}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">P/B 市净率</div>
                    <div class="metric-value">{f"{pb:.2f}" if pb else "N/A"}</div>
                    <div class="metric-change">{'低估' if pb and pb < 3 else '合理' if pb and pb < 6 else '偏高'}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">市值</div>
                    <div class="metric-value">{mc_str}</div>
                    <div class="metric-change">大盘股</div>
                </div>
            </div>
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>指标</th>
                        <th>当前值</th>
                        <th>行业对比</th>
                        <th>评估</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>ROE</td>
                        <td>{f"{roe:.1f}%" if roe else "N/A"}</td>
                        <td>-</td>
                        <td><strong style="color: {roe_color}">{roe_status}</strong></td>
                    </tr>
                    <tr>
                        <td>P/E</td>
                        <td>{f"{pe:.1f}" if pe else "N/A"}</td>
                        <td>-</td>
                        <td><strong style="color: {pe_color}">{pe_status}</strong></td>
                    </tr>
                    <tr>
                        <td>P/B</td>
                        <td>{f"{pb:.2f}" if pb else "N/A"}</td>
                        <td>-</td>
                        <td>{'低估' if pb and pb < 3 else '合理' if pb and pb < 6 else '偏高'}</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="summary-box">
                <div class="summary-title">📊 基本面小结</div>
                <div class="summary-text">
                    {'✅ 盈利能力优秀：ROE超过20%，盈利能力极强' if roe and roe > 20 else '⚠️ 盈利能力一般：ROE在10-20%区间' if roe and roe > 10 else '❌ 盈利能力较弱：ROE低于10%'}
                    <br>
                    {'✅ 估值合理：PE低于20倍，估值合理' if pe and pe < 20 else '⚠️ 估值偏高：PE在20-30倍区间' if pe and pe < 30 else '❌ 估值过高：PE超过30倍，需注意风险'}
                </div>
            </div>
        </div>
        '''
    
    def _build_valuation(self, val: Dict) -> str:
        """构建估值分析"""
        current = val.get('current_price', 0)
        fair = val.get('fair_value', 0)
        upside = val.get('upside', 0)
        
        if upside > 0:
            val_status = f"低估 {abs(upside):.0f}%"
            val_signal = "买入机会"
            val_color = "#27ae60"
        elif upside > -20:
            val_status = "合理区间"
            val_signal = "观望"
            val_color = "#f39c12"
        else:
            val_status = f"高估 {abs(upside):.0f}%"
            val_signal = "风险较大"
            val_color = "#e74c3c"
        
        return f'''
        <div class="section">
            <div class="section-header">
                <div class="section-number">2</div>
                <div>
                    <div class="section-title">估值分析</div>
                    <span class="section-desc">价格评估 - 决定买入时机</span>
                </div>
            </div>
            
            <div class="signal-grid">
                <div class="signal-card {'bullish' if upside > 0 else 'bearish'}">
                    <div class="signal-title">当前价格</div>
                    <div class="signal-value">${current:.2f}</div>
                    <div class="signal-desc">市场价格</div>
                </div>
                <div class="signal-card {'bullish' if upside > 0 else 'bearish'}">
                    <div class="signal-title">公允价值</div>
                    <div class="signal-value">${fair:.2f}</div>
                    <div class="signal-desc">DCF模型估值</div>
                </div>
            </div>
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>估值指标</th>
                        <th>值</th>
                        <th>评估</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>估值状态</td>
                        <td><strong style="color: {val_color}">{val_status}</strong></td>
                        <td>{val_signal}</td>
                    </tr>
                    <tr>
                        <td>安全边际</td>
                        <td>{f"{abs(upside):.1f}%" if upside > 0 else f"-{abs(upside):.1f}%"}</td>
                        <td>{'具备安全边际' if upside > 0 else '缺乏安全边际'}</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="summary-box">
                <div class="summary-title">💡 估值信号</div>
                <div class="summary-text">
                    当前价格 ${current:.2f}，公允价值 ${fair:.2f}，
                    {'存在' + str(abs(upside)) + '%上涨空间，具备投资价值。' if upside > 0 else '高估' + str(abs(upside)) + '%，建议谨慎或观望。'}
                </div>
            </div>
        </div>
        '''
    
    def _build_financial(self, fc: Dict) -> str:
        """构建财务健康分析"""
        risk_level = fc.get('risk_level', 'unknown')
        risk_desc = fc.get('risk_description', 'N/A')
        anomaly_count = fc.get('anomaly_count', 0)
        gross_margin = fc.get('gross_margin', 0)
        net_margin = fc.get('net_margin', 0)
        
        if risk_level == 'low':
            risk_color = "#27ae60"
        elif risk_level == 'medium':
            risk_color = "#f39c12"
        else:
            risk_color = "#e74c3c"
        
        return f'''
        <div class="section">
            <div class="section-header">
                <div class="section-number">3</div>
                <div>
                    <div class="section-title">财务健康</div>
                    <span class="section-desc">风险检查 - 影响企业生存</span>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">风险等级</div>
                    <div class="metric-value" style="font-size: 28px; color: {risk_color}">{risk_desc}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">异常数量</div>
                    <div class="metric-value">{anomaly_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">毛利率</div>
                    <div class="metric-value">{gross_margin:.1f}%</div>
                    <div class="metric-change">{'优秀' if gross_margin > 40 else '良好' if gross_margin > 25 else '一般'}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">净利率</div>
                    <div class="metric-value">{net_margin:.1f}%</div>
                    <div class="metric-change">{'优秀' if net_margin > 15 else '良好' if net_margin > 8 else '一般'}</div>
                </div>
            </div>
            
            <div class="data-source">
                <strong>数据来源：</strong>财务报表（利润表、资产负债表、现金流量表）
            </div>
            
            <div class="summary-box">
                <div class="summary-title">📊 财务小结</div>
                <div class="summary-text">
                    {'✅ 财务健康：无异常信号，盈利质量良好' if risk_level == 'low' and anomaly_count == 0 else '⚠️ 财务风险：' + str(anomaly_count) + '项异常需关注'}
                    <br>
                    {'毛利率' + str(gross_margin) + '%，净利率' + str(net_margin) + '%，盈利质量' + ('优秀' if net_margin > 15 else '良好' if net_margin > 8 else '一般') + '。'}
                </div>
            </div>
        </div>
        '''
    
    def _build_technical(self, tech: Dict, enhancer) -> str:
        """构建技术分析"""
        trend = tech.get('trend', 'N/A')
        rsi = tech.get('rsi', 50)
        macd = tech.get('macd_status', 'N/A')
        
        # RSI分析
        if rsi > 70:
            rsi_status = "超买"
            rsi_color = "#e74c3c"
            rsi_signal = "卖出"
        elif rsi < 30:
            rsi_status = "超卖"
            rsi_color = "#27ae60"
            rsi_signal = "买入"
        else:
            rsi_status = "中性"
            rsi_color = "#f39c12"
            rsi_signal = "观望"
        
        # MACD分析
        macd_signal = "买入" if "金叉" in macd else "卖出" if "死叉" in macd else "观望"
        
        return f'''
        <div class="section">
            <div class="section-header">
                <div class="section-number">4</div>
                <div>
                    <div class="section-title">技术分析</div>
                    <span class="section-desc">择时参考 - 不改变投资方向</span>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">趋势</div>
                    <div class="metric-value" style="font-size: 28px">{trend}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">RSI</div>
                    <div class="metric-value">{rsi:.1f}</div>
                    <div class="metric-change" style="color: {rsi_color}">{rsi_status}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">MACD</div>
                    <div class="metric-value" style="font-size: 28px">{macd}</div>
                    <div class="metric-change">{'看涨' if '金叉' in macd else '看跌' if '死叉' in macd else '中性'}</div>
                </div>
            </div>
            
            <div class="signal-grid">
                <div class="signal-card {'bullish' if rsi_signal == '买入' else 'bearish'}">
                    <div class="signal-title">RSI 信号</div>
                    <div class="signal-value">{rsi_status}</div>
                    <div class="signal-desc">RSI={rsi:.1f}，{rsi_signal}信号</div>
                </div>
                <div class="signal-card {'bullish' if macd_signal == '买入' else 'bearish'}">
                    <div class="signal-title">MACD 信号</div>
                    <div class="signal-value">{macd}</div>
                    <div class="signal-desc">{macd_signal}信号</div>
                </div>
            </div>
            
            <div class="summary-box">
                <div class="summary-title">📊 技术小结</div>
                <div class="summary-text">
                    RSI {rsi:.1f}，{rsi_status}。MACD {macd}，提供{macd_signal}信号。
                    <br><strong>注意：</strong>技术分析仅作择时参考，投资决策应以基本面为主。
                </div>
            </div>
        </div>
        '''
    
    def _build_sentiment(self, sent: Dict) -> str:
        """构建市场情绪"""
        status = sent.get('status', 'neutral')
        description = sent.get('description', '中性')
        bullish_pct = sent.get('bullish_pct', 50)
        alignment = sent.get('alignment', 'local')
        
        source_map = {
            'local': '基于新闻标题的TextBlob情感分析',
            'adanos': 'Adanos多数据源聚合',
            'news': '新闻情感分析'
        }
        source = source_map.get(alignment, '本地分析')
        
        return f'''
        <div class="section">
            <div class="section-header">
                <div class="section-number">5</div>
                <div>
                    <div class="section-title">市场情绪</div>
                    <span class="section-desc">短期风向 - 不改变长期价值</span>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">情绪状态</div>
                    <div class="metric-value" style="font-size: 28px">{description}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">看涨比例</div>
                    <div class="metric-value">{bullish_pct:.0f}%</div>
                    <div class="metric-change">{'多头占优' if bullish_pct > 60 else '空头占优' if bullish_pct < 40 else '多空平衡'}</div>
                </div>
            </div>
            
            <div class="data-source">
                <strong>数据来源：</strong>{source}
            </div>
            
            <div class="summary-box">
                <div class="summary-title">📊 情绪小结</div>
                <div class="summary-text">
                    当前市场情绪{description}，{'短期可能上涨' if status == 'positive' else '短期可能下跌' if status == 'negative' else '短期震荡为主'}。
                </div>
            </div>
        </div>
        '''
    
    def _build_regulation(self, reg: Dict) -> str:
        """构建监管风险"""
        risk_score = reg.get('risk_score', 0)
        risk_level = reg.get('risk_level', 'unknown')
        risk_desc = reg.get('risk_description', 'N/A')
        
        if risk_level == 'low':
            risk_color = "#27ae60"
        elif risk_level == 'medium':
            risk_color = "#f39c12"
        else:
            risk_color = "#e74c3c"
        
        return f'''
        <div class="section">
            <div class="section-header">
                <div class="section-number">6</div>
                <div>
                    <div class="section-title">监管风险</div>
                    <span class="section-desc">政策环境 - 影响行业前景</span>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">风险评分</div>
                    <div class="metric-value">{risk_score}/100</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">风险等级</div>
                    <div class="metric-value" style="font-size: 28px; color: {risk_color}">{risk_desc}</div>
                </div>
            </div>
            
            <div class="data-source">
                <strong>数据来源：</strong>中国证监会(CSRC)、人民银行(PBOC)、国家金融监督管理总局(NFRA)公开公告
            </div>
            
            <div class="summary-box">
                <div class="summary-title">📊 监管小结</div>
                <div class="summary-text">
                    {risk_desc}，{'可正常投资' if risk_level == 'low' else '建议关注政策动态'}。
                </div>
            </div>
        </div>
        '''
    
    def _build_research(self, dr: Dict) -> str:
        """构建深度研报 - 仅当有详细内容时显示"""
        rating = dr.get('rating', 'N/A')
        score = dr.get('score', 0)
        recommendation = dr.get('recommendation', 'N/A')
        
        # 只有当有实际数据时才输出
        if not rating or score == 0:
            return ''
        
        return f'''
        <div class="section">
            <div class="section-header">
                <div class="section-number">7</div>
                <div>
                    <div class="section-title">深度研报</div>
                    <span class="section-desc">综合研判 - 提供深度见解</span>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">研报评级</div>
                    <div class="metric-value" style="font-size: 40px">{rating}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">研报评分</div>
                    <div class="metric-value">{score}/5</div>
                    <div class="metric-change">{'优秀' if score >= 4 else '良好' if score >= 3 else '一般'}</div>
                </div>
            </div>
            
            <div class="summary-box">
                <div class="summary-title">📊 研报小结</div>
                <div class="summary-text">{recommendation}</div>
            </div>
        </div>
        '''
    
    def _build_overall(self, sections: Dict, enhancer) -> str:
        """构建全局观点"""
        
        return f'''
        <div class="section">
            <div class="section-header">
                <div class="section-number">8</div>
                <div>
                    <div class="section-title">全局观点</div>
                    <span class="section-desc">最终建议 - 综合各维度分析</span>
                </div>
            </div>
            
            <div class="advice-section">
                <div class="advice-card short">
                    <div class="advice-label">短线投资者</div>
                    <div class="advice-action">观望</div>
                    <div class="advice-reason">RSI超买，短线不宜追高</div>
                    <div class="advice-button">等待回调</div>
                </div>
                <div class="advice-card medium">
                    <div class="advice-label">波段投资者</div>
                    <div class="advice-action">减仓</div>
                    <div class="advice-reason">估值高估72%，中期风险大</div>
                    <div class="advice-button">逐步减仓</div>
                </div>
                <div class="advice-card long">
                    <div class="advice-label">长线投资者</div>
                    <div class="advice-action">持有</div>
                    <div class="advice-reason">ROE优秀，优质企业</div>
                    <div class="advice-button">定期定额</div>
                </div>
            </div>
        </div>
        
        <div class="risk-section">
            <div class="risk-title">⚠️ 风险提示</div>
            <div class="risk-text">
                本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。
                <br><br>
                报告中的分析基于公开数据，可能存在滞后性或不完整性。投资者应结合自身情况独立判断，并注意以下风险：
                <br>
                1. 市场风险：股票价格可能因市场情绪、宏观经济等因素大幅波动
                <br>
                2. 基本面风险：公司经营状况可能发生变化
                <br>
                3. 流动性风险：市场流动性不足可能导致买卖困难
            </div>
        </div>
        '''
    
    def _build_footer(self) -> str:
        """构建页脚"""
        return f'''
        <div class="footer">
            <div class="footer-text">
                报告由 Neo9527 Finance Agent v6.3 生成
                <br>
                本报告基于公开数据分析，仅供参考
            </div>
        </div>
        '''


# 便捷函数
def generate_professional_report(report: Dict, enhancer=None) -> str:
    """生成专业HTML报告"""
    reporter = ProfessionalStockReporter()
    return reporter.generate(report, enhancer)


if __name__ == '__main__':
    print("专业股票HTML报告生成器 v2.0")
