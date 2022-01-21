"""Token bucket algorithm implementation and example application/consumer."""
import argparse
import asyncio
import datetime
import random

from loguru import logger


class TokenBucket:
    def __init__(self, tokens_per_second: int):
        self.tokens_per_second = tokens_per_second
        self.refresh_time = 1 / self.tokens_per_second
        self.tokens = 0

    async def start(self):
        """Drip tokens into the bucket."""
        self.tokens = self.tokens_per_second
        while True:
            start = datetime.datetime.utcnow()
            await asyncio.sleep(self.refresh_time)
            end = datetime.datetime.utcnow()
            elapsed = (end - start).total_seconds()
            # There's no guarantee when the asyncio runtime will drop back into
            # this method after the sleep, so we must compute how long we were
            # asleep for and fill up with an appropriate number of tokens
            tokens_to_add = self.tokens_per_second * elapsed
            self.tokens = min(self.tokens + tokens_to_add, self.tokens_per_second)

    async def get_token(self):
        """Take one token from the bucket.

        Awaits on a token being available.
        """
        while self.tokens < 1:
            await asyncio.sleep(self.refresh_time)
        self.tokens -= 1


async def start_bucket(bucket: TokenBucket):
    await bucket.start()


async def start_app(bucket: TokenBucket, api_calls_per_second: int):
    period_start = datetime.datetime.utcnow()
    period_calls = 0
    # Exponential moving average coefficient
    alpha = 0.5
    ncalls_average = 0.0
    while True:
        period_calls += 1
        # Wait until a token is available
        await bucket.get_token()
        # Simulate an API call
        await asyncio.sleep(delay=1 / api_calls_per_second)
        time_delta = (datetime.datetime.utcnow() - period_start).total_seconds()
        # Log statistics every second
        if time_delta > 1:
            period_ncalls = period_calls / time_delta
            ncalls_average = alpha * period_ncalls + (1 - alpha) * ncalls_average
            logger.info(f"{ncalls_average:.2f} calls/second")
            # Reset counters
            period_calls = 0
            period_start = datetime.datetime.utcnow()


async def main(tokens_per_second: int, api_calls_per_second: int):
    logger.info("Starting app")
    logger.info(f"API target: {api_calls_per_second} per second")
    logger.info(f"Rate limit: {tokens_per_second} per second")
    bucket = TokenBucket(tokens_per_second=tokens_per_second)
    await asyncio.gather(
        start_bucket(bucket),
        start_app(bucket, api_calls_per_second=api_calls_per_second),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        help="Number of 'API' calls per second to attempt to make.",
        type=int,
        default=20,
    )
    parser.add_argument(
        "--limit",
        help="Per-second rate limit to apply to API calls.",
        type=int,
        default=10,
    )
    args = parser.parse_args()

    asyncio.run(main(tokens_per_second=args.limit, api_calls_per_second=args.target))
