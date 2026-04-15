#!/usr/bin/env python3
"""
Data Fetcher - 整合多个数据源
- A 股/港股：agent-stock (东方财富) + akshare
- 美股：yfinance
"""

import sys
import os
import subprocess
import json

def get_quote(symbol):
    """获取实时行情"""
    symbol = str(symbol).upper()
    
    # 判断市场
    if symbol.startswith('6') or symbol.startswith('0') or symbol.startswith('3'):
        # A 股 - 使用 agent-stock
        return _get_quote_agent_stock(symbol)
    elif symbol.endswith('.HK') or (len(symbol) == 5 and symbol.isdigit()):
        # 港股
        return _get_quote_agent_stock(symbol)
    else:
        # 美股 - 使用 yfinance
        return _get_quote_yfinance(symbol)

def _get_quote_agent_stock(symbol):
    """使用 agent-stock 获取 A 股/港股行情"""
    try:
        # 清理股票代码
        clean_symbol = symbol.replace('.HK', '').replace('.SS', '').replace('.SZ', '')
        
        result = subprocess.run(
            ['python', '-m', 'stock', 'quote', clean_symbol],
            capture_output=True,
            text=True,
            cwd=r'C:\Users\Administrator\.openclaw\workspace\.agents\skills\agent-stock',
            timeout=30
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def _get_quote_yfinance(symbol):
    """使用 yfinance 获取美股行情"""
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        current = info.get('regularMarketPrice') or info.get('currentPrice')
        prev_close = info.get('regularMarketPreviousClose') or info.get('previousClose')
        
        if current is None:
            return f"未找到股票：{symbol}"
        
        change = current - prev_close
        pct_change = (change / prev_close) * 100 if prev_close else 0
        
        color = "green" if change >= 0 else "red"
        sign = "+" if change >= 0 else ""
        
        return f"""
┌────────────────────────────────┐
│  {info.get('longName', symbol)}
├────────────────────────────────┤
│  当前价：{current:,.2f} {info.get('currency', 'USD')}
│  涨跌：{sign}{change:,.2f} ({sign}{pct_change:.2f}%)
│  市值：{info.get('marketCap', 0)/1e9:,.1f}B
│  市盈率：{info.get('forwardPE', 'N/A')}
└────────────────────────────────┘
"""
    except Exception as e:
        return f"Error: {str(e)}"

def get_heatmap(market):
    """获取行业热力图"""
    try:
        result = subprocess.run(
            ['python', '-m', 'stock', 'heatmap', '--market', market],
            capture_output=True,
            text=True,
            cwd=r'C:\Users\Administrator\.openclaw\workspace\.agents\skills\agent-stock',
            timeout=60
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_fundflow(symbol):
    """获取资金流向"""
    try:
        clean_symbol = str(symbol).replace('.HK', '').replace('.SS', '').replace('.SZ', '')
        
        result = subprocess.run(
            ['python', '-m', 'stock', 'fundflow', clean_symbol],
            capture_output=True,
            text=True,
            cwd=r'C:\Users\Administrator\.openclaw\workspace\.agents\skills\agent-stock',
            timeout=30
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_kline_data(symbol, period='1mo'):
    """
    获取K线数据
    
    Args:
        symbol: 股票代码
        period: 时间周期 (1w/1mo/3mo)
    
    Returns:
        list: [{date, open, high, low, close, volume}, ...]
    """
    try:
        clean_symbol = str(symbol).replace('.HK', '').replace('.SS', '').replace('.SZ', '')
        
        # 计算天数
        days_map = {'1w': 7, '1mo': 30, '3mo': 90}
        days = days_map.get(period, 30)
        
        result = subprocess.run(
            ['python', '-m', 'stock', 'kline', clean_symbol, '--count', str(days)],
            capture_output=True,
            text=True,
            cwd=r'C:\Users\Administrator\.openclaw\workspace\.agents\skills\agent-stock',
            timeout=30
        )
        
        if result.returncode == 0:
            # 解析 K 线数据
            output = result.stdout
            kline_data = _parse_kline_output(output)
            return kline_data
        else:
            # 尝试使用 akshare
            return _get_kline_akshare(clean_symbol, days)
    except Exception as e:
        # 尝试备用数据源
        try:
            return _get_kline_akshare(symbol, days)
        except:
            return []

def _parse_kline_output(output):
    """解析 agent-stock 的 K 线输出"""
    kline_data = []
    lines = output.strip().split('\n')
    
    for line in lines:
        # 跳过标题行和分隔符
        if '时间' in line or '开盘价' in line or '收盘价' in line or line.startswith('```'):
            continue
        
        # 解析 CSV 格式: 日期,开盘价,收盘价,最高价,最低价,成交量,成交额
        if ',' in line:
            try:
                import re
                # 提取数字
                parts = line.split(',')
                
                if len(parts) >= 5:
                    # 清理数据（去掉中文单位）
                    date = parts[0].strip()
                    # 提取数字（去掉可能的中文后缀）
                    open_price = float(re.match(r'[\d.]+', parts[1]).group())
                    close_price = float(re.match(r'[\d.]+', parts[2]).group())
                    high_price = float(re.match(r'[\d.]+', parts[3]).group())
                    low_price = float(re.match(r'[\d.]+', parts[4]).group())
                    volume = int(float(re.match(r'[\d.]+', parts[5]).group())) if len(parts) > 5 else 0
                    
                    kline_data.append({
                        'date': date,
                        'open': open_price,
                        'high': high_price,
                        'low': low_price,
                        'close': close_price,
                        'volume': volume
                    })
            except Exception as e:
                continue
    
    return kline_data

def _get_kline_akshare(symbol, days):
    """使用 akshare 获取 K 线数据（备用）"""
    try:
        import akshare as ak
        import pandas as pd
        
        # 获取股票历史数据
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="qfq")
        
        if df is not None and len(df) > 0:
            # 取最近 N 天
            df = df.tail(days)
            
            kline_data = []
            for _, row in df.iterrows():
                kline_data.append({
                    'date': str(row['日期']),
                    'open': float(row['开盘']),
                    'high': float(row['最高']),
                    'low': float(row['最低']),
                    'close': float(row['收盘']),
                    'volume': int(row['成交量'])
                })
            
            return kline_data
    except Exception as e:
        print(f"akshare 获取失败: {e}")
    
    return []

if __name__ == '__main__':
    # 测试
    print("测试 A 股行情:")
    print(get_quote('600519'))
    
    print("\n测试美股行情:")
    print(get_quote('AAPL'))
    
    print("\n测试行业热力图:")
    print(get_heatmap('ab'))
