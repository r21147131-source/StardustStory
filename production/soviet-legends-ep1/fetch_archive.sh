#!/usr/bin/env bash
# Run on your own machine: pip install internetarchive  (then: ia configure, optional)
# Step 1:  ./fetch_archive.sh search   -> archive_candidates.csv (only PD / CC-licensed movies)
# Step 2:  put chosen identifiers, one per line, in archive_picks.txt, then:
#          ./fetch_archive.sh download -> clips/archive/<identifier>/*.mp4
# Always open each item's page and confirm the license before use; log credits in archive_picks.txt as "id|credit".
set -eu
QUERIES=(
  'soviet newsreel'
  'Soyuzkinozhurnal'
  'Moscow Olympics 1980'
  'Cannes 1958 festival'
  'Soviet cinema documentary'
)
case "${1:-}" in
  search)
    echo "identifier,title,licenseurl" > archive_candidates.csv
    for q in "${QUERIES[@]}"; do
      ia search "mediatype:movies AND ($q) AND (licenseurl:*publicdomain* OR licenseurl:*creativecommons*)" \
        --itemlist >/dev/null 2>&1 || true
      ia search "mediatype:movies AND ($q) AND (licenseurl:*publicdomain* OR licenseurl:*creativecommons*)" \
        -f identifier -f title -f licenseurl 2>/dev/null \
        | python3 -c 'import sys,json,csv; w=csv.writer(sys.stdout)
for l in sys.stdin:
    d=json.loads(l); w.writerow([d.get("identifier",""),d.get("title",""),d.get("licenseurl","")])' \
        >> archive_candidates.csv
    done
    sort -u archive_candidates.csv -o archive_candidates.csv
    wc -l archive_candidates.csv ;;
  download)
    mkdir -p clips/archive
    while IFS='|' read -r id credit; do
      [ -z "$id" ] && continue
      ia download "$id" --glob "*.mp4" --destdir clips/archive && echo "ok $id ($credit)"
    done < archive_picks.txt ;;
  *) echo "usage: $0 search|download"; exit 1 ;;
esac
