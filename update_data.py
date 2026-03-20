#!/usr/bin/env python3
"""
Actualiza data.json con datos reales de Meta API.
Llamado por n8n cada noche a medianoche.
"""

import sys, json, requests
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, '/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/meta-ads-extractor')
from extractor import load_config

REPORT_DIR = Path('/home/ubuntu/.openclaw/workspace/meta-ads-reports')
DATA_FILE = REPORT_DIR / 'data.json'
CAMPAIGN_ID = '120239305936170318'

def get_meta_data():
    config = load_config()
    token = config['meta']['token']
    
    # Últimos 30 días
    end = datetime.now() - timedelta(days=1)
    start = end - timedelta(days=29)
    
    resp = requests.get(f'https://graph.facebook.com/v25.0/{CAMPAIGN_ID}/insights',
        params={
            'access_token': token,
            'date_start': start.strftime('%Y-%m-%d'),
            'date_stop': end.strftime('%Y-%m-%d'),
            'time_increment': '1',
            'fields': 'spend,impressions,clicks,actions,date_start'
        })
    
    return resp.json().get('data', [])

def parse_days(raw_data):
    daily = []
    for day in raw_data:
        spend = float(day.get('spend', 0))
        impressions = int(day.get('impressions', 0))
        clicks = int(day.get('clicks', 0))
        leads = sum(int(a.get('value', 0)) for a in day.get('actions', []) 
                   if a.get('action_type') == 'lead')
        cpl = round(spend / leads, 2) if leads > 0 else 0.0
        
        daily.append({
            'date': day.get('date_start'),
            'spend': round(spend, 2),
            'impressions': impressions,
            'clicks': clicks,
            'leads': leads,
            'cpl': cpl
        })
    return daily

def main():
    print(f"🔄 Actualizando data.json — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    raw = get_meta_data()
    if not raw:
        print("❌ Sin datos de Meta API")
        sys.exit(1)
    
    daily = parse_days(raw)
    
    # Cargar data existente
    data = json.loads(DATA_FILE.read_text()) if DATA_FILE.exists() else {}
    data['daily'] = daily
    data['updated_at'] = datetime.now().isoformat()
    data['campaign_id'] = CAMPAIGN_ID
    
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    
    print(f"✅ data.json actualizado: {len(daily)} días")
    print(f"   Último día: {daily[-1]['date']} | €{daily[-1]['spend']} | {daily[-1]['leads']} leads")
    
    # Imprimir JSON para que n8n pueda usarlo
    print("---JSON---")
    print(json.dumps({'status': 'ok', 'days': len(daily), 'last': daily[-1] if daily else {}}))

if __name__ == '__main__':
    main()
