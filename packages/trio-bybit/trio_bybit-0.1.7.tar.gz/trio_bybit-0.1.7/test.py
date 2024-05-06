import trio

from trio_bybit import AsyncClient


async def main():
    client = await AsyncClient.create(
        api_key='oJwzV0le5qsjkfslCf',
        api_secret='p2UKmTzwkkY4buKgr8ROr0SGhrp2sWd3XL2h',
    )
    order_args = {'category': 'spot', 'symbol': 'SOLUSDT', 'side': 'Buy', 'orderType': 'Limit',
                  'timeInForce': 'PostOnly', 'qty': '0.1', 'price': '134.99', 'marketUnit': 'baseCoin',
                  'orderLinkId': '14083-1714987999-be73914d-8e79-40c4-'}

    resp = await client.place_order(**order_args)

    print(resp)

    order_args = {'category': 'linear', 'symbol': 'SOLUSDT', 'side': 'Buy', 'orderType': 'Limit',
                  'timeInForce': 'PostOnly', 'qty': '0.1', 'price': '134.99', 'marketUnit': 'baseCoin',
                  'orderLinkId': '14083-1714987999-be73914d-8e79-40c5-'}

    resp = await client.place_order(**order_args)

    print(resp)


if __name__ == "__main__":
    trio.run(main)
