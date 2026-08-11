import sys
import json
import re
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup

USERNAME = "jul2264"

def fetch_contributions(username=USERNAME):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    url = f"https://github.com/users/{username}/contributions"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch contributions for {username}: status {resp.status_code}")

    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Extract total count from header text if available
    total_text = ""
    header_el = soup.find(lambda e: e.name in ["h2", "h3"] and "contributions" in e.get_text().lower())
    if header_el:
        total_text = header_el.get_text(strip=True)

    days = []
    
    # Map for tooltips linked by id
    tooltips = {}
    for tt in soup.select("tool-tip"):
        for_id = tt.get("for")
        if for_id:
            tooltips[for_id] = tt.get_text(strip=True)
            
    day_elements = soup.select(".ContributionCalendar-day, td[data-date], rect[data-date]")
    
    for el in day_elements:
        date_str = el.get("data-date")
        if not date_str:
            continue
            
        level_str = el.get("data-level", "0")
        try:
            level = int(level_str)
        except ValueError:
            level = 0
            
        count = 0
        el_id = el.get("id")
        tooltip_txt = tooltips.get(el_id, "") if el_id else ""
        
        combined_info = " ".join([
            el.get("aria-label", ""),
            el.get("title", ""),
            tooltip_txt,
            el.get_text()
        ])
        
        match = re.search(r'(\d+)\s+contribution', combined_info, re.IGNORECASE)
        if match:
            count = int(match.group(1))
        elif "no contribution" in combined_info.lower() or level == 0:
            count = 0
        else:
            count = level * 2
            
        days.append({
            "date": date_str,
            "count": count,
            "level": level
        })
        
    days.sort(key=lambda d: d["date"])
    
    total_contributions = sum(d["count"] for d in days)
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    best_day = {"date": "", "count": 0}
    
    for d in days:
        cnt = d["count"]
        if cnt > best_day["count"]:
            best_day = {"date": d["date"], "count": cnt}
            
        if cnt > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    for d in reversed(days):
        if d["count"] > 0:
            current_streak += 1
        else:
            if current_streak == 0:
                continue
            else:
                break

    data = {
        "username": username,
        "updated_at": datetime.now().isoformat(),
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": days
    }
    
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "contributions.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"Saved {len(days)} days of contributions for {username} to {out_path}")
    print(f"Total: {total_contributions}, Current Streak: {current_streak}, Longest Streak: {longest_streak}")

if __name__ == "__main__":
    fetch_contributions()
