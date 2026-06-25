import urllib.request, json, sys
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
display_date = datetime.utcnow().strftime("%A, %B %-d, %Y")

leagues = [
    ("4956", "FIFA World Cup 2026"),
    ("4424", "MLB"),
    ("4411", "WNBA"),
    ("4401", "PGA Tour"),
    ("4686", "LPGA Tour"),
    ("4681", "Wimbledon"),
]

games_html = ""

for league_id, league_name in leagues:
    try:
        url = "https://www.thesportsdb.com/api/v1/json/123/eventsday.php?d=" + today + "&l=" + league_id
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
        events = data.get("events") or []
        for e in events:
            if e.get("dateEvent") == today:
                home = e.get("strHomeTeam", "")
                away = e.get("strAwayTeam", "")
                raw_time = e.get("strTime", "")
                try:
                    t = datetime.strptime(raw_time[:5], "%H:%M")
                    time_str = t.strftime("%-I:%M %p") + " ET"
                except Exception:
                    time_str = raw_time
                games_html += (
                    '<div class="game">'
                    '<div class="league">' + league_name + '</div>'
                    '<div class="matchup">' + away + ' vs ' + home + '</div>'
                    '<div class="time">' + time_str + '</div>'
                    '</div>'
                )
    except Exception as ex:
        print("Could not fetch " + league_name + ": " + str(ex), file=sys.stderr)

if not games_html.strip():
    games_html = '<p class="no-games">No major games scheduled today — but Pawn Shop will always have something worth watching.</p>'

html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Pawn Shop - Today's Games</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
    h1 { font-size: 26px; margin-bottom: 4px; }
    .date { color: #888; margin-bottom: 24px; font-size: 15px; }
    .game { padding: 14px 0; border-bottom: 1px solid #eee; }
    .league { font-weight: bold; color: #c0392b; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matchup { font-size: 20px; font-weight: bold; }
    .time { color: #555; font-size: 14px; margin-top: 4px; }
    .no-games { color: #888; font-size: 17px; }
  </style>
</head>
<body>
  <h1>Pawn Shop — Games Today</h1>
  <p class="date">""" + display_date + """</p>
  """ + games_html + """
</body>
</html>"""

with open("index.html", "w") as f:
    f.write(html)

print("Done — index.html written.")
