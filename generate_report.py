#!/usr/bin/env python3
"""
Meta Ads Campaign Report Generator

Genera reportes ejecutivos para cualquier campaña de Meta Ads.
Estructura: 4 pestañas (General, Creativos, Ad Sets, Proyecciones)

Uso:
  python3 generate_report.py \
    --campaign-id 120239305936170318 \
    --campaign-name "Test Manual SEO Local Pablo" \
    --output ./reports/
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

def load_json(filepath):
    """Carga JSON file."""
    try:
        with open(filepath) as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return None

def filter_campaign_data(all_ads, campaign_id):
    """Filtra ads de una campaña específica."""
    # Los ad_ids de Meta empiezan con el campaign_id
    campaign_prefix = str(campaign_id)[:12]
    return [ad for ad in all_ads if str(ad.get('ad_id', '')).startswith(campaign_prefix)]

def generate_adset_mapping(ads):
    """Genera mapeo automático de ad_ids a nombres descriptivos."""
    mapping = {}
    for i, ad in enumerate(sorted(ads, key=lambda x: x['cpm'])):
        audience_type = get_audience_type(ad)
        cpm_category = "CPM bajo" if ad['cpm'] < 5 else "CPM medio" if ad['cpm'] < 15 else "CPM alto"
        mapping[ad['ad_id']] = f"Audiencia {chr(65+i)} - {audience_type} ({cpm_category})"
    return mapping

def get_audience_type(ad):
    """Estima el tipo de audiencia basado en métricas."""
    if ad['leads'] > 5:
        return "Premium (conversiones altas)"
    elif ad['cpm'] < 3:
        return "Presupuesto (CPM muy bajo)"
    elif ad['retention_25'] > 10:
        return "Engagement (good hook)"
    elif ad['leads'] == 0 and ad['spend'] > 10:
        return "Test (sin conversión)"
    else:
        return "Estándar"

def calculate_kpis(daily_data, ads):
    """Calcula KPIs globales."""
    total_spend = sum(d['spend'] for d in daily_data)
    total_leads = sum(d['leads'] for d in daily_data)
    total_clicks = sum(d['clicks'] for d in daily_data)
    total_impressions = sum(d['impressions'] for d in daily_data)
    
    return {
        'total_spend': total_spend,
        'total_leads': total_leads,
        'total_clicks': total_clicks,
        'total_impressions': total_impressions,
        'cpl': total_spend / max(1, total_leads),
        'ctr': (total_clicks / max(1, total_impressions)) * 100,
        'cpm': (total_spend / max(1, total_impressions)) * 1000
    }

def generate_html_report(campaign_id, campaign_name, daily_data, ads, adset_mapping, output_dir):
    """Genera el archivo HTML del reporte."""
    
    kpis = calculate_kpis(daily_data, ads)
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    
    creative_agg = {}
    for ad in ads:
        name = ad['ad_name']
        if name not in creative_agg:
            creative_agg[name] = {
                'spend': 0, 'plays': 0, 'leads': 0,
                'plays_25': 0, 'plays_50': 0, 'plays_75': 0, 'plays_100': 0
            }
        creative_agg[name]['spend'] += ad['spend']
        creative_agg[name]['plays'] += ad['plays']
        creative_agg[name]['leads'] += ad['leads']
        creative_agg[name]['plays_25'] += ad['plays_25']
        creative_agg[name]['plays_50'] += ad['plays_50']
        creative_agg[name]['plays_75'] += ad['plays_75']
        creative_agg[name]['plays_100'] += ad['plays_100']
    
    # Convertir a JSON embebido
    daily_json = json.dumps(daily_data)
    ads_json = json.dumps(ads)
    mapping_json = json.dumps(adset_mapping)
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard {campaign_name}</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f7fa;
        }}
        .header {{
            background: white;
            padding: 40px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }}
        .header h1 {{ font-size: 2.5em; color: #050912; font-weight: 900; }}
        .header p {{ color: #666; }}
        .tabs {{
            display: flex;
            background: white;
            border-bottom: 3px solid #e5e7eb;
            padding: 0 20px;
        }}
        .tab-btn {{
            padding: 16px 25px;
            border: none;
            background: none;
            font-size: 1em;
            font-weight: 700;
            color: #999;
            cursor: pointer;
            border-bottom: 4px solid transparent;
        }}
        .tab-btn.active {{ color: #2563EB; border-bottom-color: #2563EB; }}
        .tab-content {{
            display: none;
            padding: 40px;
            max-width: 1600px;
            margin: 0 auto;
        }}
        .tab-content.active {{ display: block; }}
        .section {{
            background: white;
            padding: 35px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        .section-title {{
            font-size: 1.6em;
            color: #050912;
            font-weight: 900;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 4px solid #2563EB;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .kpi-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            border-top: 5px solid #2563EB;
            box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        }}
        .kpi-value {{
            font-size: 2.8em;
            font-weight: 900;
            color: #2563EB;
            margin-bottom: 8px;
        }}
        .kpi-label {{ font-size: 0.75em; color: #999; text-transform: uppercase; font-weight: 800; }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}
        .chart-box {{
            background: #fafbfc;
            border-radius: 12px;
            padding: 12px;
            min-height: 380px;
        }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.9em; }}
        thead {{ background: #f0f7ff; border-bottom: 3px solid #2563EB; }}
        th {{ padding: 12px; text-align: center; font-weight: 800; }}
        td {{ padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: center; }}
        td:first-child {{ text-align: left; font-weight: 700; }}
        tbody tr:hover {{ background: #f9fafb; }}
        .metric-good {{ color: #10B981; font-weight: 800; }}
        .metric-bad {{ color: #EF4444; font-weight: 800; }}
        .insight {{
            background: #f0fdf4;
            border-left: 5px solid #10B981;
            padding: 20px;
            border-radius: 12px;
            font-size: 0.95em;
            line-height: 1.7;
            margin-top: 25px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 {campaign_name}</h1>
        <p>Dashboard Ejecutivo | {timestamp}</p>
    </div>

    <div class="tabs">
        <button class="tab-btn active" onclick="openTab(event, 'general')">📊 General</button>
        <button class="tab-btn" onclick="openTab(event, 'creativos')">🎬 Creativos</button>
        <button class="tab-btn" onclick="openTab(event, 'adsets')">🎯 Ad Sets</button>
        <button class="tab-btn" onclick="openTab(event, 'proyecciones')">📈 Proyecciones</button>
    </div>

    <div id="general" class="tab-content active">
        <div class="section">
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-value">${kpis['total_spend']:.2f}</div>
                    <div class="kpi-label">Inversión Total</div>
                </div>
                <div class="kpi-card" style="border-top-color: #10B981;">
                    <div class="kpi-value" style="color: #10B981;">{kpis['total_leads']}</div>
                    <div class="kpi-label">Leads</div>
                </div>
                <div class="kpi-card" style="border-top-color: #F59E0B;">
                    <div class="kpi-value" style="color: #F59E0B;">${kpis['cpl']:.2f}</div>
                    <div class="kpi-label">CPL Promedio</div>
                </div>
                <div class="kpi-card" style="border-top-color: #10B981;">
                    <div class="kpi-value" style="color: #10B981;">{kpis['ctr']:.2f}%</div>
                    <div class="kpi-label">CTR</div>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="section-title">📈 Gráficos (próxima versión)</div>
            <p style="color: #666;">Los gráficos se cargarán aquí. Por ahora, revisa la tabla de datos en Ad Sets.</p>
        </div>
    </div>

    <div id="creativos" class="tab-content">
        <div class="section">
            <div class="section-title">🎬 Análisis por Creativo</div>
            <p style="color: #666; margin-bottom: 20px;">Suma de todos sus ad sets.</p>
            <table>
                <thead>
                    <tr>
                        <th>Creativo</th>
                        <th>Reproducciones</th>
                        <th>Presupuesto</th>
                        <th>Leads</th>
                        <th>CPL</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for name in sorted(creative_agg.keys(), key=lambda x: creative_agg[x]['leads'], reverse=True):
        c = creative_agg[name]
        cpl = f"${c['spend']/c['leads']:.2f}" if c['leads'] > 0 else "-"
        html += f"""                    <tr>
                        <td>{name}</td>
                        <td>{c['plays']:,}</td>
                        <td>${c['spend']:.2f}</td>
                        <td class="{'metric-good' if c['leads'] > 0 else 'metric-bad'}">{c['leads']}</td>
                        <td>{cpl}</td>
                    </tr>
"""
    
    html += """                </tbody>
            </table>
        </div>
    </div>

    <div id="adsets" class="tab-content">
        <div class="section">
            <div class="section-title">🎯 Desglose por Ad Set</div>
            <table style="font-size: 0.8em;">
                <thead>
                    <tr>
                        <th>Audiencia</th>
                        <th>Creativo</th>
                        <th>Presupuesto</th>
                        <th>Leads</th>
                        <th>CPL</th>
                        <th>CPM</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for ad in sorted(ads, key=lambda x: x['leads'], reverse=True):
        audience = adset_mapping.get(ad['ad_id'], f"Ad Set {ad['ad_id'][-6:]}")
        cpl = f"${ad['spend']/ad['leads']:.2f}" if ad['leads'] > 0 else "-"
        html += f"""                    <tr>
                        <td style="color: #2563EB; font-weight: 700;">{audience}</td>
                        <td>{ad['ad_name']}</td>
                        <td>${ad['spend']:.2f}</td>
                        <td class="{'metric-good' if ad['leads'] > 0 else 'metric-bad'}">{ad['leads']}</td>
                        <td>{cpl}</td>
                        <td>${ad['cpm']:.2f}</td>
                    </tr>
"""
    
    html += """                </tbody>
            </table>
        </div>
    </div>

    <div id="proyecciones" class="tab-content">
        <div class="section">
            <div class="section-title">📈 Proyecciones</div>
            <p style="color: #666;">Proyecciones de escalabilidad (próxima versión).</p>
        </div>
    </div>

    <script>
        function openTab(evt, tabName) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            evt.currentTarget.classList.add('active');
        }
    </script>
</body>
</html>
"""
    
    # Guardar HTML
    output_path = Path(output_dir) / f"index.html"
    output_path.write_text(html)
    print(f"✅ Reporte guardado: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Genera reportes ejecutivos Meta Ads')
    parser.add_argument('--campaign-id', required=True, help='Campaign ID')
    parser.add_argument('--campaign-name', required=True, help='Campaign Name')
    parser.add_argument('--daily-data', default='data.json', help='Path to daily data JSON')
    parser.add_argument('--ads-data', default='video-analysis.json', help='Path to ads data JSON')
    parser.add_argument('--output', default='./', help='Output directory')
    
    args = parser.parse_args()
    
    # Cargar datos
    daily_data = load_json(args.daily_data)
    all_ads = load_json(args.ads_data)
    
    if not daily_data or not all_ads:
        print("❌ Error: No se pudieron cargar los datos")
        return
    
    # Filtrar campaña
    ads = filter_campaign_data(all_ads, args.campaign_id)
    print(f"✅ Campaña: {args.campaign_name}")
    print(f"   Ad Sets: {len(ads)}")
    
    # Generar mapping
    adset_mapping = generate_adset_mapping(ads)
    
    # Generar reporte
    generate_html_report(args.campaign_id, args.campaign_name, daily_data, ads, adset_mapping, args.output)
    print(f"\n✅ Reporte completado")

if __name__ == '__main__':
    main()
