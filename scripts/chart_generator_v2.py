#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Financial Chart Generator - 金融图表生成器
支持资金流向图、业务占比图、股价均线图、可比公司对比图
"""

import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Windows 编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = r'D:\OpenClaw\outputs\charts'
os.makedirs(OUTPUT_DIR, exist_ok=True)


class FinancialChartGenerator:
    """金融图表生成器"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        
    def generate_fundflow_chart(self, days: int = 10) -> str:
        """
        生成资金流向折线图
        
        Returns:
            图表文件路径
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            import numpy as np
            
            # 获取资金流向数据
            fundflow_data = self._get_fundflow_history(days)
            
            if not fundflow_data:
                return None
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(12, 6))
            
            dates = [d['date'] for d in fundflow_data]
            main_flow = [d['main_flow'] / 1e8 for d in fundflow_data]  # 转换为亿
            retail_flow = [d['retail_flow'] / 1e8 for d in fundflow_data]
            
            x = range(len(dates))
            
            # 绘制线条
            ax.plot(x, main_flow, 'b-', linewidth=2, label='主力资金', marker='o', markersize=5)
            ax.plot(x, retail_flow, 'g-', linewidth=2, label='散户资金', marker='s', markersize=5)
            
            # 添加零线
            ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
            
            # 填充区域
            ax.fill_between(x, main_flow, 0, where=[v > 0 for v in main_flow], 
                           color='red', alpha=0.3, interpolate=True)
            ax.fill_between(x, main_flow, 0, where=[v < 0 for v in main_flow], 
                           color='green', alpha=0.3, interpolate=True)
            
            # 设置标签
            ax.set_xlabel('日期', fontsize=12)
            ax.set_ylabel('资金净流入（亿元）', fontsize=12)
            ax.set_title(f'{self.symbol} 近{days}日资金流向', fontsize=14, fontweight='bold')
            
            # 设置X轴
            ax.set_xticks(x[::2])  # 每隔一个显示
            ax.set_xticklabels(dates[::2], rotation=45, ha='right')
            
            # 图例
            ax.legend(loc='best', fontsize=10)
            
            # 网格
            ax.grid(True, alpha=0.3)
            
            # 调整布局
            plt.tight_layout()
            
            # 保存
            filepath = os.path.join(OUTPUT_DIR, f'{self.symbol}_fundflow_{days}d.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except ImportError:
            # matplotlib 未安装，使用文本图表
            return self._generate_fundflow_text_chart(days)
        except Exception as e:
            print(f"图表生成失败: {e}")
            return None
    
    def _get_fundflow_history(self, days: int) -> List[Dict]:
        """获取资金流向历史数据"""
        try:
            from data_fetcher import get_quote
            
            # 简化实现：使用模拟数据
            # 实际应该从 agent-stock 获取历史数据
            today = datetime.now()
            data = []
            
            for i in range(days):
                date = today - timedelta(days=i)
                # 这里应该从真实数据源获取
                data.append({
                    'date': date.strftime('%m-%d'),
                    'main_flow': 0,  # 需要真实数据
                    'retail_flow': 0
                })
            
            return list(reversed(data))
            
        except Exception as e:
            return []
    
    def _generate_fundflow_text_chart(self, days: int) -> str:
        """生成文本格式资金流向图"""
        # ASCII 艺术图表
        return "text_chart_placeholder"
    
    def generate_business_pie_chart(self) -> str:
        """
        生成业务占比饼图
        
        Returns:
            图表文件路径
        """
        try:
            import matplotlib.pyplot as plt
            
            # 获取业务分部数据
            segments = self._get_business_segments()
            
            if not segments:
                return None
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(10, 8))
            
            labels = [s['name'] for s in segments]
            sizes = [s['ratio'] for s in segments]
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
            explode = [0.05] * len(segments)  # 略微突出每个扇区
            
            # 绘制饼图
            wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, 
                                              colors=colors[:len(segments)],
                                              autopct='%1.1f%%',
                                              shadow=True, startangle=90)
            
            # 设置文字属性
            for text in texts:
                text.set_fontsize(11)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            ax.set_title(f'{self.symbol} 业务结构', fontsize=14, fontweight='bold')
            
            # 添加图例（显示收入）
            legend_labels = [f"{s['name']}: {s['revenue']:.1f}亿" for s in segments]
            ax.legend(wedges, legend_labels, title="业务收入", 
                     loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            plt.tight_layout()
            
            # 保存
            filepath = os.path.join(OUTPUT_DIR, f'{self.symbol}_business_pie.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except ImportError:
            return None
        except Exception as e:
            print(f"饼图生成失败: {e}")
            return None
    
    def _get_business_segments(self) -> List[Dict]:
        """获取业务分部数据"""
        try:
            from financial_data_fetcher import FinancialDataFetcher
            
            fetcher = FinancialDataFetcher(self.symbol)
            result = fetcher.get_business_segment()
            
            return result.get('segments', [])
            
        except Exception as e:
            return []
    
    def generate_price_ma_chart(self, days: int = 180) -> str:
        """
        生成股价与均线叠加图
        
        Returns:
            图表文件路径
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            import numpy as np
            
            # 获取K线数据
            kline_data = self._get_kline_data(days)
            
            if not kline_data:
                return None
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(14, 7))
            
            # 提取数据
            dates = range(len(kline_data))
            closes = [k['close'] for k in kline_data]
            
            # 计算均线
            ma5 = self._calculate_ma(closes, 5)
            ma10 = self._calculate_ma(closes, 10)
            ma20 = self._calculate_ma(closes, 20)
            
            # 绘制K线（简化为折线图）
            ax.plot(dates, closes, 'k-', linewidth=1.5, label='收盘价', alpha=0.8)
            
            # 绘制均线
            ax.plot(dates, ma5, 'r-', linewidth=1.2, label='MA5', alpha=0.7)
            ax.plot(dates, ma10, 'g-', linewidth=1.2, label='MA10', alpha=0.7)
            ax.plot(dates, ma20, 'b-', linewidth=1.2, label='MA20', alpha=0.7)
            
            # 设置标签
            ax.set_xlabel('交易日', fontsize=12)
            ax.set_ylabel('价格（元）', fontsize=12)
            ax.set_title(f'{self.symbol} 股价与均线 ({days}天)', fontsize=14, fontweight='bold')
            
            # 图例
            ax.legend(loc='best', fontsize=10)
            
            # 网格
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # 保存
            filepath = os.path.join(OUTPUT_DIR, f'{self.symbol}_price_ma_{days}d.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except ImportError:
            return None
        except Exception as e:
            print(f"均线图生成失败: {e}")
            return None
    
    def _get_kline_data(self, days: int) -> List[Dict]:
        """获取K线数据"""
        try:
            from data_fetcher import get_kline_data
            
            period = '3mo' if days <= 90 else '6mo'
            return get_kline_data(self.symbol, period)
            
        except Exception as e:
            return []
    
    def _calculate_ma(self, prices: List[float], period: int) -> List[float]:
        """计算移动平均线"""
        ma = []
        for i in range(len(prices)):
            if i < period - 1:
                ma.append(None)
            else:
                ma.append(sum(prices[i-period+1:i+1]) / period)
        return ma
    
    def generate_peer_comparison_chart(self, peers: List[str] = None) -> str:
        """
        生成可比公司对比图
        
        Returns:
            图表文件路径
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            # 获取可比公司数据
            from financial_data_fetcher import FinancialDataFetcher
            
            fetcher = FinancialDataFetcher(self.symbol)
            result = fetcher.get_peer_comparison(peers)
            
            if not result.get('peers'):
                return None
            
            peers_data = result['peers']
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 创建图表
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            
            names = [p['name'] for p in peers_data]
            x = np.arange(len(names))
            
            # PE 对比
            ax1 = axes[0, 0]
            pes = [p.get('pe', 0) for p in peers_data]
            colors = ['#ff6b6b' if i == 0 else '#4ecdc4' for i in range(len(names))]
            ax1.bar(x, pes, color=colors, alpha=0.8)
            ax1.set_xlabel('公司', fontsize=10)
            ax1.set_ylabel('PE', fontsize=10)
            ax1.set_title('市盈率对比', fontsize=12, fontweight='bold')
            ax1.set_xticks(x)
            ax1.set_xticklabels(names, rotation=15, ha='right')
            ax1.grid(True, alpha=0.3, axis='y')
            
            # PB 对比
            ax2 = axes[0, 1]
            pbs = [p.get('pb', 0) for p in peers_data]
            ax2.bar(x, pbs, color=colors, alpha=0.8)
            ax2.set_xlabel('公司', fontsize=10)
            ax2.set_ylabel('PB', fontsize=10)
            ax2.set_title('市净率对比', fontsize=12, fontweight='bold')
            ax2.set_xticks(x)
            ax2.set_xticklabels(names, rotation=15, ha='right')
            ax2.grid(True, alpha=0.3, axis='y')
            
            # 市值对比
            ax3 = axes[1, 0]
            caps = [p.get('market_cap', 0) for p in peers_data]
            ax3.bar(x, caps, color=colors, alpha=0.8)
            ax3.set_xlabel('公司', fontsize=10)
            ax3.set_ylabel('市值（亿）', fontsize=10)
            ax3.set_title('市值对比', fontsize=12, fontweight='bold')
            ax3.set_xticks(x)
            ax3.set_xticklabels(names, rotation=15, ha='right')
            ax3.grid(True, alpha=0.3, axis='y')
            
            # 涨跌幅对比
            ax4 = axes[1, 1]
            changes = [p.get('change_pct', 0) for p in peers_data]
            colors_change = ['#ff6b6b' if c < 0 else '#51cf66' for c in changes]
            ax4.bar(x, changes, color=colors_change, alpha=0.8)
            ax4.set_xlabel('公司', fontsize=10)
            ax4.set_ylabel('涨跌幅（%）', fontsize=10)
            ax4.set_title('今日涨跌幅', fontsize=12, fontweight='bold')
            ax4.set_xticks(x)
            ax4.set_xticklabels(names, rotation=15, ha='right')
            ax4.axhline(y=0, color='gray', linestyle='-', linewidth=0.8)
            ax4.grid(True, alpha=0.3, axis='y')
            
            plt.suptitle(f'{self.symbol} 可比公司对比', fontsize=14, fontweight='bold', y=1.00)
            plt.tight_layout()
            
            # 保存
            filepath = os.path.join(OUTPUT_DIR, f'{self.symbol}_peer_comparison.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except ImportError:
            return None
        except Exception as e:
            print(f"对比图生成失败: {e}")
            return None
    
    def generate_all_charts(self, peers: List[str] = None) -> Dict[str, str]:
        """
        生成所有图表
        
        Returns:
            图表路径字典
        """
        return {
            'fundflow': self.generate_fundflow_chart(10),
            'business_pie': self.generate_business_pie_chart(),
            'price_ma': self.generate_price_ma_chart(180),
            'peer_comparison': self.generate_peer_comparison_chart(peers)
        }


def generate_charts(symbol: str, peers: List[str] = None) -> Dict[str, str]:
    """生成金融图表"""
    generator = FinancialChartGenerator(symbol)
    return generator.generate_all_charts(peers)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='金融图表生成')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--type', choices=['fundflow', 'business', 'price', 'peer', 'all'],
                       default='all', help='图表类型')
    parser.add_argument('--peers', nargs='+', help='可比公司代码')
    
    args = parser.parse_args()
    
    generator = FinancialChartGenerator(args.symbol)
    
    if args.type == 'fundflow':
        path = generator.generate_fundflow_chart()
    elif args.type == 'business':
        path = generator.generate_business_pie_chart()
    elif args.type == 'price':
        path = generator.generate_price_ma_chart()
    elif args.type == 'peer':
        path = generator.generate_peer_comparison_chart(args.peers)
    else:
        paths = generator.generate_all_charts(args.peers)
        print(json.dumps(paths, indent=2, ensure_ascii=False))
        sys.exit(0)
    
    if path:
        print(f"图表已生成: {path}")
    else:
        print("图表生成失败")
