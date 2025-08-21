# Application Links Generator

Jednoduchá Python aplikácia na generovanie HTML start page s linkami na aplikácie.

## Súbory

- `generate_links.py` - Hlavná aplikácia 
- `apps.properties` - Konfiguračný súbor s aplikáciami
- `index.html` - Vygenerovaná HTML stránka

## Použitie

```bash
# Základné generovanie
python3 generate_links.py

# S vlastným properties súborom
python3 generate_links.py my_apps.properties output.html
```

## Konfigurácia (apps.properties)

Formát každého riadku:
```
nazov_aplikacie=URL=active
```

Príklad:
```properties
# Application Links Configuration
# Format: name=url=active
# active: true/false

MT Analytics=http://localhost:5009=true
TV Automation=http://localhost:8080=true
GS Journal Stats=http://localhost:3000=false
```

## Vlastnosti

- Responzívny dizajn
- Automatické rozdelenie aktívnych/neaktívnych aplikácií
- Clickable linky pre aktívne aplikácie
- Čistý dizajn bez piktogramov