# Cloudflare Worker Code

Copy this code into your Cloudflare Worker editor and deploy.

```javascript
const GMI_BASE = "https://console.gmicloud.ai/api/v1/ie/requestqueue/apikey";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Authorization, Content-Type",
};

export default {
  async fetch(request) {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS });
    }

    // Only proxy /requests paths (or root as /requests)
    let pathname = url.pathname;
    if (pathname === "/" || pathname === "") {
      pathname = "/requests";
    }
    if (!pathname.startsWith("/requests")) {
      return new Response("Not found", { status: 404, headers: CORS });
    }

    const target = GMI_BASE + pathname + url.search;

    const init = {
      method: request.method,
      headers: {
        "Content-Type": "application/json",
        Authorization: request.headers.get("Authorization") || "",
      },
    };

    if (request.method === "POST") {
      init.body = await request.text();
    }

    try {
      const resp = await fetch(target, init);
      const body = await resp.text();

      return new Response(body, {
        status: resp.status,
        headers: {
          ...CORS,
          "Content-Type": "application/json",
        },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 502,
        headers: { ...CORS, "Content-Type": "application/json" },
      });
    }
  },
};
```
