# solver.py - @axiba070281 的 NEAR Intents Solver
from near_intents import IntentListener, SolverClient
from pycoingecko import CoinGeckoAPI
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 Solver 客户端
client = SolverClient(
    private_key=os.getenv("NEAR_PRIVATE_KEY"),
    solver_id="axiba070281-solver-v1"
)
cg = CoinGeckoAPI()

@client.on_intent("swap")
def handle_swap(intent):
    # 只处理 BTC → USDT（最热门）
    if intent.from_asset != "BTC" or intent.to_asset != "USDT":
        return None

    try:
        amount_in = intent.amount
        prices = cg.get_price(ids='bitcoin', vs_currencies='usd')
        btc_price = prices['bitcoin']['usd']
        
        # 模拟最优路径：BTC → NEAR → USDT
        usdt_out = amount_in * btc_price * 0.995  # 0.5% 滑点
        fee = usdt_out * 0.001  # 0.1% 利润

        logger.info(f"报价: {amount_in} BTC → {usdt_out:.2f} USDT (费: ${fee:.4f})")

        return {
            "amount_out": usdt_out,
            "fee": fee,
            "eta_seconds": 8,
            "path": "BTC→NEAR→USDT"
        }
    except Exception as e:
        logger.error(f"报价失败: {e}")
        return None

if __name__ == "__main__":
    print("axiba070281 Solver 启动！监听 BTC→USDT 意图...")
    client.start()
