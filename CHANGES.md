# Changes

## Bugs Fixed

**Gainers and losers reversed.**
`compute_kpis` sorted coins ascending by `price_change_percentage_24h` then assigned `[:3]` to `top_gainers` and `[-3:]` to `top_losers`. The slices were swapped. Fixed by assigning `[:3]` to `top_losers` and `[-3:]` to `top_gainers`.

**Null fields crashing compute.**
Once the dataset grew beyond the original 10 coins, some coins returned `null` for `price_change_percentage_24h`, which crashed the sort with a `TypeError`. A separate `valid_coins` filter existed for `market_cap` but ran after the sort and left the two filters inconsistent. Replaced both with a single filter at the top of `compute` that drops any coin where either field is `None`. The filtered list is used for the sort, the sum, and the divisor.

**No HTTP status check on CoinGecko response.**
`requests.get` was called and `.json()` invoked immediately. A 429 or 500 from CoinGecko returned an error object instead of a list, and the crash happened downstream with a misleading `KeyError`. Added `response.raise_for_status()` so failures surface immediately with the correct status code and response body.

**Bucket never created on first run.**
`save_kpis` called `put_object` directly. On a fresh MinIO instance there was no `crypto-kpis` bucket, so the call raised `NoSuchBucket`. Added `create_bucket` before `put_object`, catching `BucketAlreadyOwnedByYou` and `BucketAlreadyExists` so subsequent runs pass through cleanly.

**`depends_on` race condition.**
Docker Compose `depends_on` waits for the container to start, not for the service inside it to be ready. The pipeline and dashboard containers were starting while MinIO was still initialising and failing to connect. Added a `healthcheck` to the `minio` service that polls `/minio/health/live` every 5 seconds with a 10-second start period, and changed both dependent services to `condition: service_healthy`.

---

## Improvements

**OO refactor.**
Extracted `fetch_top_coins`, `compute_kpis`, and `save_kpis` into three classes across three files: `CoinGeckoClient` in `fetcher.py`, `KPIComputer` in `kpis.py`, and `MinIOStorage` in `storage.py`. `main.py` instantiates all three and calls them in order. `dashboard.py` uses `MinIOStorage` directly. The previous `get_s3_client` helper function is gone; its logic lives in `MinIOStorage.__init__`.

**Env var config via `.env`.**
MinIO credentials (`MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`) were hardcoded in two places. Moved them to `.env`, loaded via `env_file` in docker-compose for `pipeline` and `dashboard`. `MinIOStorage.__init__` reads all three and raises `EnvironmentError` with the names of whichever are missing. Fetch tuning params (`MAX_CONCURRENT`, `TOTAL_PAGES`, `PER_PAGE`) are also in `.env` with sensible defaults so they can be adjusted without touching code.

**Error handling.**
Added a 10-second timeout to the CoinGecko request. `httpx.TimeoutException` and `httpx.HTTPError` are caught in `_fetch_page` and re-raised as `RuntimeError` with the page number included. `ClientError` is caught around `put_object` in `MinIOStorage.save`. In `dashboard.py`, `ClientError` from `storage.load()` is caught and shown as a Streamlit error message before calling `st.stop()`, so the rest of the page does not attempt to render against missing data.

**Python logging.**
Replaced all `print` statements in `main.py` and `dashboard.py` with `logging` calls. `basicConfig` is set at the top of each file with a timestamp and level prefix. Normal flow uses `INFO`. The exception path in `dashboard.py` uses `ERROR` and logs before calling `st.error`, so failures appear in both the server logs and the UI.

**Async concurrent page fetching.**
Replaced `requests` with `httpx`. `CoinGeckoClient.fetch` is now `async` and fetches all pages concurrently using `asyncio.gather`. A `Semaphore` caps concurrent requests at `MAX_CONCURRENT` (default 2). Page count and per-page size are controlled by `TOTAL_PAGES` (default 3) and `PER_PAGE` (default 50), giving 150 coins by default. `asyncio.run` lives in `main.py` at the call site so the async boundary is explicit rather than hidden inside the class.

---

## What I Would Do Next

With another two hours I would add historical snapshots to `MinIOStorage`: instead of overwriting `latest.json` on every run, write a timestamped file alongside it so there is a full record of every pipeline execution and the dashboard can show a trend over time. I would also add retry with exponential backoff to `_fetch_page`, parsing the `Retry-After` header that CoinGecko returns on 429s so the fetcher backs off for the right duration rather than an arbitrary interval. Finally, `KPIComputer.compute` is pure logic with no I/O, which makes it straightforward to unit test; I would add a `tests/test_kpis.py` with a small set of fixtures covering the null filter, the sort order, and the market cap average to lock in that behaviour against future changes.
