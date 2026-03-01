## Endpoints

### GET /

Health check.

Response

```json
{ "status": "ok", "service": "vb-analytics" }
```

---

### GET /api/prices

Returns raw price history rows (most recent last).

| Param   | Type   | Default | Description                  |
|---------|--------|---------|------------------------------|
| `limit` | number | `100`   | Number of most-recent rows   |

**Response**

```json
{
  "data": [
    { "timestamp": "2025-05-01T12:00:00Z", "coin": "stellar", "currency": "usd", "price": "0.123456" }
  ]
}
```

---

### GET /api/candlestick

Returns OHLC candlestick data grouped by time interval.

| Param      | Type   | Default | Description                        |
|------------|--------|---------|------------------------------------|
| interval | string | 1h    | Bucket size: 1h, 4h, or 1d  |

**Response**

```json
{
  "data": [
    { "time": "2025-05-01T12:00:00.000Z", "open": 0.12, "high": 0.13, "low": 0.11, "close": 0.125, "volume": 42 }
  ],
  "interval": "1h"
}
```

volume is the number of price points in that candle.

---

### GET /api/metrics

Returns statistical metrics computed over all stored price data.

**Response**

```json
{
  "count": 1000,
  "latest": 0.123456,
  "min": 0.100000,
  "max": 0.150000,
  "mean": 0.125000,
  "median": 0.124000,
  "stddev": 0.005000,
  "change_percent": 2.35,
  "first_timestamp": "2025-04-01T00:00:00Z",
  "last_timestamp": "2025-05-01T12:00:00Z"
}
```

| Field              | Description                                      |
|--------------------|--------------------------------------------------|
| count            | Total number of price data points                |
| latest           | Most recent price                                |
| min / max      | Minimum and maximum prices                       |
| mean             | Arithmetic mean                                  |
| median           | Median price                                     |
| stddev           | Standard deviation                               |
| change_percent   | Percentage change from oldest to latest price    |
| first_timestamp  | Timestamp of the earliest data point             |
| last_timestamp   | Timestamp of the most recent data point          |