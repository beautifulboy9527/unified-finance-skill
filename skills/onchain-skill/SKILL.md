---
name: onchain-whale-skill
description: |
  链上鲸鱼数据分析 - TVL变化、资金流、协议排名、DeFi健康度。
  使用 DeFiLlama 免费 API，无需 API Key。
  输出标准 JSON 格式，可被 Agent 直接调用。
metadata:
  openclaw:
    emoji: "🐋"
    triggers:
      - "链上"
      - "鲸鱼"
      - "TVL"
      - "DeFi"
      - "资金流"
      - "协议"
      - "Ethereum"
    inputs:
      chain:
        type: string
        description: 链名称
        default: Ethereum
        enum: [Ethereum, BSC, Polygon, Arbitrum, Optimism]
    outputs:
      tvl:
        type: number
        description: 总锁仓量
      tvl_change_1d:
        type: number
        description: 24小时变化率
      score:
        type: number
        description: 健康度评分 (0-100)
      signals:
        type: array
        description: 链上信号
---

# Onchain Whale Skill

链上鲸鱼数据分析 Skill，符合 OpenClaw Skills 规范。

## 快速开始

### Agent 调用

```python
from skills.base_skill import SkillInput, SkillRegistry

output = SkillRegistry.execute(
    'OnchainWhaleSkill',
    SkillInput(symbol='Ethereum', market='crypto')
)

print(f"TVL: ${output.data['tvl']:,.0f}")
print(f"Score: {output.score}/100")
```

### CLI 调用

```bash
neo-finance onchain Ethereum
```

## 功能

| 功能 | API | 说明 |
|------|-----|------|
| 链级TVL | `/v2/chains` | 总锁仓量 |
| 协议资金流 | `/protocols` | 资金流向 |
| Top协议 | `/protocols` | 排名 |
| 稳定币 | `/stablecoins` | 市场稳定度 |
| 健康度分析 | 综合 | 评分+信号 |

## 信号生成

### TVL变化信号

| 条件 | 信号 | 强度 |
|------|------|------|
| 24h > 10% | bullish | +4 |
| 24h > 3% | bullish | +2 |
| 24h < -10% | bearish | -4 |
| 24h < -3% | bearish | -2 |
| 7d > 20% | bullish | +3 |
| 7d < -20% | bearish | -3 |

### 集中度信号

| 条件 | 信号 | 强度 |
|------|------|------|
| Top1 > 60% | bearish | -2 |

## 输出示例

```json
{
  "skill_name": "OnchainWhaleSkill",
  "success": true,
  "score": 45,
  "data": {
    "chain": "Ethereum",
    "tvl": 55446579084,
    "tvl_change_1d": 0.0,
    "tvl_change_7d": 0.0,
    "top_protocols": [
      {"name": "Binance CEX", "tvl": 153711505104},
      {"name": "Aave V3", "tvl": 25519356232}
    ]
  },
  "signals": [
    {
      "type": "concentration",
      "signal": "bearish",
      "strength": -2,
      "desc": "协议集中度过高 (64.6%)"
    }
  ]
}
```

## 数据来源

- **DeFiLlama** (免费，无需 API Key)
- 完全免费
- 无速率限制
- 实时数据

## 依赖

```bash
pip install requests
```

## 注意事项

- DeFiLlama 数据有 5-10 分钟延迟
- 某些小链可能无数据
- 协议名称可能变化
