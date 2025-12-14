# GCD Docker Setup (Windows)

**Prerequisiti**: 
- Docker Desktop installato
- Docker Desktop **deve essere in esecuzione** (avvia l'app prima di usare docker-compose)

## Setup iniziale (solo una volta)
```bash
docker-compose build    # Crea l'immagine Docker (scarica branch beta)
docker-compose up -d    # Avvia i container in background
docker-compose run --rm web python gcd-django/manage.py migrate  # Crea database
docker-compose run --rm web python gcd-django/manage.py createsuperuser  # Admin user
```

## Riavvio successivo
```bash
docker-compose up -d    # Avvia tutto
```

## Comandi utili
```bash
docker-compose logs -f web      # Vedi i log in tempo reale
docker-compose down             # Ferma i container
docker-compose down -v          # Ferma e cancella i volumi (dati)
docker-compose restart web      # Riavvia solo il container web
```

## Accesso
- Admin Django: http://localhost:8000/admin/
- Username/Password: quelli creati con `createsuperuser`

## Note
- Il Dockerfile clona automaticamente il branch **beta** di gcd-django
- Le modifiche a `settings_local.py` sono già incluse per disabilitare memcached/elasticsearch
- Il database è persistente nel volume Docker (sopravvive ai restart)
