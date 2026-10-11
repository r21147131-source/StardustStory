#!/usr/bin/env node
// Minimal TMDB client. Usage:
//   node scripts/tmdb.mjs search "query"            -> multi-search (movies/tv/people)
//   node scripts/tmdb.mjs get /movie/603            -> any TMDB v3 path
// Reads TMDB_ACCESS_TOKEN from the environment.
const token = process.env.TMDB_ACCESS_TOKEN;
if (!token) {
  console.error("TMDB_ACCESS_TOKEN is not set (see .env.example)");
  process.exit(1);
}

const [cmd, arg] = process.argv.slice(2);
let path;
if (cmd === "search" && arg) path = `/search/multi?query=${encodeURIComponent(arg)}`;
else if (cmd === "get" && arg) path = arg;
else {
  console.error('Usage: tmdb.mjs search "query" | tmdb.mjs get /path');
  process.exit(1);
}

const res = await fetch(`https://api.themoviedb.org/3${path}`, {
  headers: { Authorization: `Bearer ${token}`, accept: "application/json" },
});
if (!res.ok) {
  console.error(`TMDB ${res.status}: ${await res.text()}`);
  process.exit(1);
}
console.log(JSON.stringify(await res.json(), null, 2));
