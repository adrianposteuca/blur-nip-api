AI NSFW Blur API
Acesta este un microserviciu API, construit în Python cu Flask și împachetat în Docker. Folosește un model AI YOLO (erax-ai/EraX-Anti-NSFW-V1.1) pentru a detecta mameloanele în imagini și a aplica automat un filtru de blur peste zonele detectate.

Funcționalități
Detecție de obiecte folosind un model AI pre-antrenat.

Aplicare automată a unui filtru Gaussian Blur pe zonele detectate.

Parametri configurabili prin API pentru:

Intensitatea blur-ului (blur_radius).

Mărimea fixă a zonei de blur (padding).

Pragul de încredere al detecției (confidence).

Scalarea imaginii înainte de procesare (scale).

Rotirea imaginii înainte de procesare (rotation).

Endpoint API
Method: POST

URL: https://[adresa_ta_publica]/api/blur-nipples

Exemplu: https://blur.49.12.99.26.nip.io/api/blur-nipples

Cererea trebuie să fie de tip multipart/form-data.

Parametri
Toți parametrii, cu excepția celui de image, sunt opționali.

Nume Parametru	Tip	Obligatoriu?	Valoare Implicită	Descriere
image	File	Da	-	Fișierul imagine de procesat.
padding	Integer	Nu	0	Un selector pentru mărimea fixă a chenarului de blur. 0 = dimensiunea detectată, 1 = 100x100px, 2 = 200x200px etc.
blur_radius	Integer	Nu	35	Controlează intensitatea blur-ului. O valoare mai mare înseamnă un blur mai puternic.
confidence	Float	Nu	0.70	Pragul de încredere (între 0.0 și 1.0). Blur-ul se aplică doar dacă modelul este mai sigur de detecție decât această valoare.
scale	Float	Nu	1.0	Un factor de scalare pentru a micșora imaginea înainte de procesare (ex: 0.5 pentru a o înjumătăți).
rotation	Integer	Nu	0	Rotește imaginea înainte de procesare. Valori acceptate: 90, 180, 270.
Exemplu de Utilizare (curl)
Acesta este un exemplu de cum poți apela API-ul din linia de comandă, folosind valorile specificate de tine.

Bash

curl -X POST \
  https://blur.49.12.99.26.nip.io/api/blur-nipples \
  -F "image=@/calea/catre/imaginea/ta.jpg" \
  -F "scale=0.5" \
  -F "confidence=0.5" \
  -F "padding=2" \
  -F "blur_radius=20" \
  -F "rotation=90" \
  --output imagine_rezultat.png
Publicare (Deployment) pe un server
Cerințe: Server Linux (ex: Ubuntu) cu Docker și Docker Compose instalate.

Clonează repository-ul:

Bash

git clone https://github.com/numele-tau/blur-nip-api.git /opt/blur-api
cd /opt/blur-api
Creează fișierul docker-compose.yml în folderul /opt/blur-api cu următorul conținut:

YAML

services:
  blur-api:
    build: .
    restart: always
    container_name: blur-api-1
    networks:
      - default

networks:
  default:
    name: shared-network
    external: true
Pornește serviciul:

Bash

docker compose up -d --build
Configurează un Reverse Proxy (ex: Nginx Proxy Manager) pentru a face serviciul accesibil public și a adăuga un certificat SSL.

Domain: blur.adresa-ip.nip.io

Forward Hostname: blur-api-1

Forward Port: 8000
