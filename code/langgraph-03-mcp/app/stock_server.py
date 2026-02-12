import requests
import os
from fastmcp import FastMCP


mcp = FastMCP("Stock API")

if "STOCK_API_KEY" not in os.environ:
    raise ValueError("Error: Required environment variable STOCK_API_KEY not set.") 

@mcp.tool()
def get_stock_data(symbol: str):
    """Get Stock information for symbol."""
    api_key = os.environ["STOCK_API_KEY"]
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    return data


if __name__ == "__main__":
    #ttp_transport_instance = HTTPTransport(host='0.0.0.0', port=8086)
    mcp.run(transport="http", host="0.0.0.0", port=8086)