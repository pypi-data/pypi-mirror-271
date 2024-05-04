from datetime import datetime, timedelta
from fibrous_limit_order.src.limit_order.order_types import Order

def convert_date_to_unix_timestamp(days):
    return int((datetime.now() + timedelta(days=days)).timestamp())

mock_order = Order(
    signer='0x00F28CDD1f902402CAB752904D855fA52608d5aE63f1c69ED038049260Cad3D7',
    maker_asset='0x03e85bfbb8e2a42b7bead9e88e9a1b19dbccf661471061807292120462396ec9',
    taker_asset='0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7',
    maker_amount= 1000000000000000000,
    taker_amount= 1000000000000000000,
    order_price= 2770000000000000000000,
    expiration= convert_date_to_unix_timestamp(days = 2),
    use_solver=False,
    partial_fill=True
)

ACCOUNT_PRIVATE_KEY = '0x03d810bd29e7c6fae9957c1602621747d7b38e3d6104b589d55bca46e837aa87'
ACCOUNT_PUBLIC_KEY = '0x00F28CDD1f902402CAB752904D855fA52608d5aE63f1c69ED038049260Cad3D7'
RPC_URL = 'https://starknet-mainnet.blastapi.io/83e0811d-e14f-42b0-b556-65246d733267/rpc/v0.4'
