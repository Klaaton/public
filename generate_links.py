#!/usr/bin/env python3
"""
Application Links Generator
Generuje HTML start page s linkami načítanými z properties súboru
"""

import os
import sys
from datetime import datetime

class AppLinksGenerator:
    def __init__(self, properties_file="apps.properties", output_file="index.html"):
        self.properties_file = properties_file
        self.output_file = output_file
        self.apps = []
        
    def load_properties(self):
        """Načítanie aplikácií z properties súboru"""
        try:
            if not os.path.exists(self.properties_file):
                print(f"Properties súbor '{self.properties_file}' neexistuje!")
                return False
                
            with open(self.properties_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            self.apps = []
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Preskočiť prázdne riadky a komentáre
                if not line or line.startswith('#'):
                    continue
                    
                # Parsovanie formátu: name=url=active
                parts = line.split('=')
                if len(parts) != 3:
                    print(f"Nesprávny formát na riadku {line_num}: {line}")
                    continue
                    
                name, url, active = parts
                active_bool = active.lower() == 'true'
                
                self.apps.append({
                    'name': name.strip(),
                    'url': url.strip(),
                    'active': active_bool
                })
                
            print(f"Načítaných {len(self.apps)} aplikácií z {self.properties_file}")
            return True
            
        except Exception as e:
            print(f"Chyba pri načítavaní properties súboru: {e}")
            return False
    
    def generate_html(self):
        """Generovanie HTML start page"""
        try:
            # Rozdelenie aplikácií na aktívne a neaktívne
            active_apps = [app for app in self.apps if app['active']]
            inactive_apps = [app for app in self.apps if not app['active']]
            
            html_content = self._get_html_template(active_apps, inactive_apps)
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            print(f"HTML súbor '{self.output_file}' úspešne vygenerovaný!")
            print(f"Aktívne aplikácie: {len(active_apps)}")
            print(f"Neaktívne aplikácie: {len(inactive_apps)}")
            return True
            
        except Exception as e:
            print(f"Chyba pri generovaní HTML: {e}")
            return False
    
    def _get_html_template(self, active_apps, inactive_apps):
        """HTML template bez piktogramov"""
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        
        # Spojené generovanie linkov pre všetky aplikácie
        all_links_html = ""
        
        # Aktívne aplikácie
        for app in active_apps:
            # Oprava linku pre static_report.html
            url = app['url']
            if url == "/static_report.html":
                url = "./static_report.html"
            
            all_links_html += f"""
            <div class="app-link active" onclick="openApp('{url}', '{app['name']}')">
                <div class="app-name">{app['name']}</div>
                <div class="app-url">{url}</div>
                <div class="app-status active">ACTIVE</div>
            </div>
            """
        
        # Neaktívne aplikácie
        for app in inactive_apps:
            # Oprava linku pre static_report.html
            url = app['url']
            if url == "/static_report.html":
                url = "./static_report.html"
                
            all_links_html += f"""
            <div class="app-link inactive">
                <div class="app-name">{app['name']}</div>
                <div class="app-url">{url}</div>
                <div class="app-status inactive">INACTIVE</div>
            </div>
            """
        
        return f"""<!DOCTYPE html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application Links</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .apps-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
        }}
        
        .app-link {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .app-link.active {{
            border-color: #3498db;
            cursor: pointer;
        }}
        
        .app-link.active:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(52, 152, 219, 0.2);
            border-color: #2980b9;
        }}
        
        .app-link.inactive {{
            opacity: 0.6;
            border-color: #dee2e6;
        }}
        
        .app-name {{
            font-size: 1.1em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            line-height: 1.3;
        }}
        
        .app-url {{
            color: #7f8c8d;
            font-size: 0.8em;
            margin-bottom: 12px;
            word-break: break-all;
            line-height: 1.2;
        }}
        
        .app-status {{
            font-size: 0.7em;
            font-weight: bold;
            padding: 4px 10px;
            border-radius: 15px;
            display: inline-block;
        }}
        
        .app-status.active {{
            color: #27ae60;
            background: rgba(39, 174, 96, 0.1);
        }}
        
        .app-status.inactive {{
            color: #95a5a6;
            background: rgba(149, 165, 166, 0.1);
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
            border-top: 1px solid #e9ecef;
        }}
        
        .no-apps {{
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
            font-style: italic;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .apps-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .app-link {{
                padding: 15px;
            }}
            
            .app-name {{
                font-size: 1em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <p>AOS Helper Aplikácie</p>
        </div>
        
        <div class="content">
            <div class="apps-grid">
                {all_links_html if active_apps or inactive_apps else '<div class="no-apps">Žiadne aplikácie</div>'}
            </div>
        </div>
        
        <div class="footer">
            Posledná aktualizácia: {timestamp}
        </div>
    </div>
    
    <script>
        function openApp(url, name) {{
            console.log(`Opening app: ${{name}} at ${{url}}`);
            
            // Pokus o otvorenie v novom tabe
            const newWindow = window.open(url, '_blank');
            
            // Fallback ak sa nepodí otvoría nový tab
            if (!newWindow || newWindow.closed || typeof newWindow.closed == 'undefined') {{
                alert(`Nebolo možné automaticky otvoriť aplikáciu "${{name}}".\\n\\nManuálne prejdite na: ${{url}}`);
            }}
        }}
        
        console.log('Application Dashboard loaded');
        console.log('Active apps: {len(active_apps)}');
        console.log('Inactive apps: {len(inactive_apps)}');
    </script>
</body>
</html>"""

def main():
    """Hlavná funkcia"""
    print("Application Links Generator")
    print("=" * 40)
    
    # Argument parsing
    properties_file = sys.argv[1] if len(sys.argv) > 1 else "apps.properties"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "index.html"
    
    # Vytvorenie generátora
    generator = AppLinksGenerator(properties_file, output_file)
    
    # Načítanie properties
    if not generator.load_properties():
        sys.exit(1)
    
    # Generovanie HTML
    if not generator.generate_html():
        sys.exit(1)
    
    print("=" * 40)
    print(f"Start page vygenerovaná: {output_file}")

if __name__ == "__main__":
    main()
