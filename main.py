import asyncio
import logging
from fetcher import CoinGeckoClient
from kpis import KPIComputer
from storage import MinIOStorage

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    fetcher = CoinGeckoClient()
    computer = KPIComputer()
    storage = MinIOStorage()

    logger.info("Fetching coins...")
    coins = asyncio.run(fetcher.fetch())
    logger.info("Fetched %d coins", len(coins))

    logger.info("Computing KPIs...")
    kpis = computer.compute(coins)

    logger.info("Saving to MinIO...")
    storage.save(kpis)

    logger.info("Done!")


if __name__ == "__main__":
    main()
