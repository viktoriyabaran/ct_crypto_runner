// index.tsx (Railway Function)
import { Hono } from "hono@4";
import { cors } from "hono/cors";
import { Client } from "minio@8";
import { parse } from "csv-parse/sync@5";

const app = new Hono();
app.use("/*", cors());

const minioClient = new Client({
  endPoint: import.meta.env.MINIO_ENDPOINT?.split(":")[0] ?? "localhost",
  port: parseInt(import.meta.env.MINIO_ENDPOINT?.split(":")[1] ?? "9000"),
  useSSL: false,
  accessKey: import.meta.env.MINIO_ACCESS_KEY ?? "minioadmin",
  secretKey: import.meta.env.MINIO_SECRET_KEY ?? "minioadmin",
});

const BUCKET = import.meta.env.MINIO_BUCKET ?? "vb-prices";
const CSV_KEY = "prices/stellar/prices.csv";

async function readCSV(): Promise<
  Array<{ timestamp: string; coin: string; currency: string; price: string }>
> {
  const stream = await minioClient.getObject(BUCKET, CSV_KEY);
  const chunks: Buffer[] = [];
  for await (const chunk of stream) {
    chunks.push(chunk);
  }
  const content = Buffer.concat(chunks).toString("utf-8");
  return parse(content, { columns: true, skip_empty_lines: true });
}

function filterByTimeRange(
  rows: Array<{ timestamp: string; coin: string; currency: string; price: string }>,
  from?: string,
  to?: string
) {
  return rows.filter((r) => {
    const t = new Date(r.timestamp).getTime();
    if (from && t < new Date(from).getTime()) return false;
    if (to && t > new Date(to).getTime()) return false;
    return true;
  });
}

// Health check
app.get("/", (c) => c.json({ status: "ok", service: "vb-analytics" }));

// Get raw price history
app.get("/api/prices", async (c) => {
  try {
    const rows = await readCSV();
    const from = c.req.query("from");
    const to = c.req.query("to");
    const limit = parseInt(c.req.query("limit") ?? "100");
    const filtered = filterByTimeRange(rows, from, to);
    return c.json({ data: filtered.slice(-limit) });
  } catch (e) {
    return c.json({ error: String(e) }, 500);
  }
});

// Candlestick OHLC data (Japanese chart)
app.get("/api/candlestick", async (c) => {
  try {
    const rows = await readCSV();
    const from = c.req.query("from");
    const to = c.req.query("to");
    const interval = c.req.query("interval") ?? "1h";
    const filtered = filterByTimeRange(rows, from, to);

    const intervalMs: Record<string, number> = {
      "1h": 3600000,
      "4h": 14400000,
      "1d": 86400000,
    };
    const ms = intervalMs[interval] ?? 3600000;

    const candles: Record<string, number[]> = {};
    for (const row of filtered) {
      const time = new Date(row.timestamp).getTime();
      const bucket = Math.floor(time / ms) * ms;
      const key = new Date(bucket).toISOString();
      if (!candles[key]) candles[key] = [];
      candles[key].push(parseFloat(row.price));
    }

    // Build OHLC
    const ohlc = Object.entries(candles)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([time, prices]) => ({
        time,
        open: prices[0],
        high: Math.max(...prices),
        low: Math.min(...prices),
        close: prices[prices.length - 1],
        volume: prices.length,
      }));

    return c.json({ data: ohlc, interval });
  } catch (e) {
    return c.json({ error: String(e) }, 500);
  }
});

// Metrics / statistics
app.get("/api/metrics", async (c) => {
  try {
    const rows = await readCSV();
    const from = c.req.query("from");
    const to = c.req.query("to");
    const filtered = filterByTimeRange(rows, from, to);
    const prices = filtered.map((r) => parseFloat(r.price));

    if (prices.length === 0) return c.json({ error: "No data" }, 404);

    const mean = prices.reduce((a, b) => a + b, 0) / prices.length;
    const sorted = [...prices].sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    const variance =
      prices.reduce((sum, p) => sum + (p - mean) ** 2, 0) / prices.length;
    const stddev = Math.sqrt(variance);
    const latest = prices[prices.length - 1];
    const oldest = prices[0];
    const changePercent = ((latest - oldest) / oldest) * 100;

    return c.json({
      count: prices.length,
      latest,
      min: sorted[0],
      max: sorted[sorted.length - 1],
      mean: parseFloat(mean.toFixed(6)),
      median,
      stddev: parseFloat(stddev.toFixed(6)),
      change_percent: parseFloat(changePercent.toFixed(2)),
      first_timestamp: filtered[0].timestamp,
      last_timestamp: filtered[filtered.length - 1].timestamp,
    });
  } catch (e) {
    return c.json({ error: String(e) }, 500);
  }
});

Bun.serve({
  port: import.meta.env.PORT ?? 3000,
  fetch: app.fetch,
});