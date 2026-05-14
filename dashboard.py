import json
import logging
import streamlit as st
from botocore.exceptions import ClientError
from storage import MinIOStorage

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Crypto KPI Dashboard", page_icon="📊")
st.title("Crypto KPI Dashboard")

storage = MinIOStorage()

try:
    logger.info("Loading KPI data from MinIO...")
    obj = storage.load()
    data = json.loads(obj["Body"].read())
    logger.info("KPI data loaded successfully")
except ClientError as e:
    logger.error("Could not load KPI data: %s", e.response["Error"]["Message"])
    st.error(f"Could not load KPI data: {e.response['Error']['Message']}")
    st.stop()

st.caption(f"Last updated: {data['timestamp']}")

col1, col2 = st.columns(2)
col1.metric("Total Market Cap", f"${data['total_market_cap_usd']:,.0f}")
col2.metric("Avg Market Cap ", f"${data['average_market_cap_usd']:,.0f}")

st.subheader("📈 Top Gainers (24h)")
for coin in reversed(data["top_gainers"]):
    st.write(f"**{coin['name']}** ({coin['symbol'].upper()}): {coin['change_24h']:+.2f}%")

st.subheader("📉 Top Losers (24h)")
for coin in data["top_losers"]:
    st.write(f"**{coin['name']}** ({coin['symbol'].upper()}): {coin['change_24h']:+.2f}%")
