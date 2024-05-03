import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import timeit
from limit_order.limit_order import LimitOrder
from limit_order.personal_data import WALLET_ADDRESS
from return_types.orders import NonceResponse

async def get_nonce() -> NonceResponse:
    limit_order = LimitOrder()
    nonce = await limit_order.get_nonce(WALLET_ADDRESS)
    print(nonce)

async def run_code():
    start_time = timeit.default_timer()
    await get_nonce()
    end_time = timeit.default_timer()
    print(f"Execution time: {end_time - start_time} seconds")

def main():
    asyncio.run(run_code())

if __name__ == '__main__':
    main()