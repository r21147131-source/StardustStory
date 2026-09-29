"""Align the Consumed Ep1 script (ported from Ep5's align_vo.py) to the voiceover without a transcript.

Usage: python align_vo.py SCRIPT.txt SILENCES.txt DURATION OUT.json

SILENCES.txt is ffmpeg silencedetect output reduced to "silence_start: X" /
"silence_end: Y" lines (-35dB, d=0.18). Each sentence break is snapped to one
detected pause; a DP picks the pauses so each sentence's speech time best
matches its share of the characters, and section breaks ("—— ——") prefer long
pauses. Accurate to within a word or two where the reading is even.
"""
import json, re, sys

script, silf, total, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]

sents, breaks, heads = [], set(), {}
for block in open(script).read().split("\n"):
    block = block.strip()
    if not block or block.startswith("#"):
        continue
    if block.startswith("["):  # section heading, e.g. [ACT 1: THE POET'S SON]
        breaks.add(len(sents)); heads[len(sents)] = block.strip("[]")
        continue
    for s in re.split(r"(?<=[.?!])\s+(?=[A-Z\"“])", block):
        if s.strip():
            sents.append(s.strip())

vals = [float(l.split()[1]) for l in open(silf)]
pauses = [(vals[i], vals[i + 1]) for i in range(0, len(vals) - 1, 2)]
if pauses and pauses[0][0] < 0.05:
    lead = pauses.pop(0)[1]
else:
    lead = 0.0
if pauses and pauses[-1][1] > total - 0.05:
    pauses.pop()

# speech prefix: speech seconds from `lead` up to time t
def speech_between(a, b, ia, ib):
    return (b - a) - sum(p[1] - p[0] for p in pauses[ia:ib])

weight = [len(re.sub(r"[^A-Za-z0-9]", "", s)) + 6 for s in sents]
speech_total = (total - lead) - sum(p[1] - p[0] for p in pauses)
rate = speech_total / sum(weight)

N, M = len(sents), len(pauses)
INF = float("inf")
# node j = pause index j (sentence starts at pauses[j][1]); start node = -1 (lead)
start_t = lambda j: lead if j < 0 else pauses[j][1]
end_t = lambda j: total if j >= M else pauses[j][0]

best = {-1: (0.0, None)}
layers = [best]
for i in range(N):
    last = i == N - 1
    nxt = {}
    for j, (c, _) in layers[-1].items():
        exp = weight[i] * rate
        cands = [M] if last else range(j + 1, min(M, j + 40))
        for k in cands:
            a, b = start_t(j), end_t(k)
            dur = speech_between(a, b, j + 1, k)
            cost = (dur - exp) ** 2 / (exp + 1.0)
            inner = sum(max(0, (p[1] - p[0]) - 0.7) for p in pauses[j + 1:k])
            cost += 4 * inner
            if not last:
                plen = pauses[k][1] - pauses[k][0]
                cost -= (3.0 if (i + 1) in breaks else 0.6) * min(plen, 2.0)
            tot = c + cost
            if k not in nxt or tot < nxt[k][0]:
                nxt[k] = (tot, j)
    # prune
    keep = sorted(nxt.items(), key=lambda kv: kv[1][0])[:120]
    layers.append(dict(keep))
    if last and M not in nxt:
        sys.exit("alignment failed")

path, k = [], M
for i in range(N, 0, -1):
    j = layers[i][k][1]
    path.append(j)
    k = j
path.reverse()
res = [{"i": i, "t": round(start_t(path[i]), 2), "section": heads.get(i), "text": s} for i, s in enumerate(sents)]
json.dump(res, open(out, "w"), indent=0, ensure_ascii=False)
print(f"{N} sentences, {M} pauses, rate {1/rate:.1f} chars/s")
for i in sorted(breaks | {0}):
    if i < N:
        j = path[i]
        pl = 0 if j < 0 else pauses[j][1] - pauses[j][0]
        print(f"section @ s{i} t={res[i]['t']:7.2f} pause={pl:.2f}  {sents[i][:50]}")
