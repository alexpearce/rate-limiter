Rate limiter
============

A Python implementation of the [token bucket algorithm][alg] using async/await.

## Usage

Create an environment:

```
$ conda env create -f environment.yaml
$ conda activate rate-limiter
```

Run:

```
$ python3 app.py --target 50 --limit 20
2022-01-21 14:57:35.654 | INFO     | __main__:main:68 - Starting app
2022-01-21 14:57:35.654 | INFO     | __main__:main:69 - API target: 50 per second
2022-01-21 14:57:35.654 | INFO     | __main__:main:70 - Rate limit: 20 per second
2022-01-21 14:57:36.679 | INFO     | __main__:start_app:61 - 19.03 calls/second
2022-01-21 14:57:37.721 | INFO     | __main__:start_app:61 - 19.12 calls/second
2022-01-21 14:57:38.728 | INFO     | __main__:start_app:61 - 20.01 calls/second
2022-01-21 14:57:39.765 | INFO     | __main__:start_app:61 - 19.67 calls/second
2022-01-21 14:57:40.776 | INFO     | __main__:start_app:61 - 20.23 calls/second
2022-01-21 14:57:41.842 | INFO     | __main__:start_app:61 - 19.97 calls/second
2022-01-21 14:57:42.850 | INFO     | __main__:start_app:61 - 20.41 calls/second
```

The `--target` argument is how many calls to _attempt_ to make per second. The
`--limit` argument is how many tokens are added to the bucket per second, i.e.
how many calls _should actually_ be made per second.

[alg]: https://en.wikipedia.org/wiki/Token_bucket
