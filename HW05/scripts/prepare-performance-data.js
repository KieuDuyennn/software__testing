#!/usr/bin/env node

/**
 * Seed deterministic performance-test users through the live EShop API and
 * generate the three CSV pools consumed by the JMeter workflow.
 *
 * Usage:
 *   node scripts/prepare-performance-data.js --count 240 --out data
 *
 * Run this after starting the backend with LOADTEST=1. Registering through the
 * API verifies the same path the application uses instead of writing directly
 * to SQLite and bypassing server behaviour.
 */

const fs = require("fs");
const path = require("path");

function option(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

const base = option("--base", "http://localhost:3000").replace(/\/$/, "");
const count = Number.parseInt(option("--count", "240"), 10);
const outDir = path.resolve(option("--out", "data"));

if (!Number.isInteger(count) || count < 1 || count > 2000) {
  throw new Error("--count must be an integer from 1 to 2000");
}

function csvCell(value) {
  const text = String(value);
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

async function request(route, init = {}) {
  const response = await fetch(`${base}${route}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init.headers || {}) },
  });
  const text = await response.text();
  let body = null;
  try {
    body = JSON.parse(text);
  } catch {
    body = text;
  }
  return { response, body };
}

async function main() {
  const productResult = await request("/api/products");
  if (!productResult.response.ok || !Array.isArray(productResult.body) || productResult.body.length === 0) {
    throw new Error(`cannot read live products: HTTP ${productResult.response.status}`);
  }
  const products = productResult.body;

  const credentials = [["email", "password"]];
  const searches = [["keyword", "product_id", "product_price"]];
  const orders = [["total_amount", "shipping_address"]];

  for (let i = 1; i <= count; i += 1) {
    const suffix = String(i).padStart(3, "0");
    const email = `perf${suffix}@eshop.local`;
    const password = `Perf${suffix}!Aa`;
    const registration = await request("/api/register", {
      method: "POST",
      body: JSON.stringify({ name: `Performance User ${suffix}`, email, password }),
    });

    if (!registration.response.ok) {
      throw new Error(
        `registration failed for ${email}: HTTP ${registration.response.status} ${JSON.stringify(registration.body)}`,
      );
    }

    const product = products[(i - 1) % products.length];
    const keyword = String(product.name).split(/\s+/)[0];
    credentials.push([email, password]);
    searches.push([keyword, product.id, product.price]);
    orders.push([product.price, `${i} Nguyen Van Cu, District 5, HCMC`]);
  }

  const firstLogin = await request("/api/login", {
    method: "POST",
    body: JSON.stringify({ email: credentials[1][0], password: credentials[1][1] }),
  });
  const lastLogin = await request("/api/login", {
    method: "POST",
    body: JSON.stringify({ email: credentials.at(-1)[0], password: credentials.at(-1)[1] }),
  });
  if (!firstLogin.response.ok || !lastLogin.response.ok) {
    throw new Error("verification login failed for the first or last generated account");
  }

  fs.mkdirSync(outDir, { recursive: true });
  const writeCsv = (name, rows) => {
    const content = `${rows.map((row) => row.map(csvCell).join(",")).join("\n")}\n`;
    fs.writeFileSync(path.join(outDir, name), content, "utf8");
  };
  writeCsv("credentials.csv", credentials);
  writeCsv("search_keywords.csv", searches);
  writeCsv("order_payloads.csv", orders);

  console.log(`seeded ${count} users through ${base}/api/register`);
  console.log(`validated ${products.length} live products and boundary-account logins`);
  console.log(`wrote CSV pools to ${outDir}`);
}

main().catch((error) => {
  console.error(`[prepare-performance-data] ${error.message}`);
  process.exit(1);
});

