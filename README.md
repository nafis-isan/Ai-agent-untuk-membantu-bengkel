# BengkelAI

BengkelAI adalah sistem manajemen bengkel berbasis web yang mengintegrasikan backend FastAPI, frontend Nuxt, database, dan AI assistant dari Google Gemini. Project ini dirancang untuk membantu operasional bengkel seperti pencatatan pelanggan, kendaraan, jadwal servis, stok suku cadang, serta analisis performa bengkel dengan bantuan AI.

## Ringkasan fitur

- Manajemen pelanggan
- Manajemen kendaraan
- Manajemen mekanik
- Manajemen suku cadang / sparepart
- Manajemen service order
- Manajemen appointment / janji temu
- Dashboard dan insight operasi bengkel
- AI chat berbasis Gemini
- Histori percakapan per `session_id`
- Autentikasi admin untuk endpoint tertentu
- Fallback database otomatis dari PostgreSQL ke SQLite
- Dokumentasi API otomatis dengan FastAPI
- Docker Compose untuk menjalankan seluruh stack

## Teknologi utama

- Backend: Python, FastAPI, SQLAlchemy, Pydantic
- Frontend: Nuxt.js, Vue 3, Pinia, Tailwind CSS, Nuxt UI
- Database: PostgreSQL dan SQLite
- AI: Google Gemini via `google-genai`
- Container: Docker, Docker Compose
- Testing: Pytest

## Arsitektur aplikasi

```text
BengkelAI
├── app/
│   ├── agent/                  # Logic AI agent dan orchestration
│   │   ├── agent.py
│   │   ├── memory.py
│   │   ├── prompts.py
│   │   └── tools.py
│   ├── api/                   # Endpoint FastAPI
│   │   ├── appointments.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── customers.py
│   │   ├── insights.py
│   │   ├── services.py
│   │   ├── spareparts.py
│   │   └── vehicles.py
│   ├── database/              # Model, koneksi, migrasi, seed
│   │   ├── connection.py
│   │   ├── dependencies.py
│   │   ├── init_db.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── seed.py
│   ├── auth.py                # Admin auth + JWT-like token
│   ├── main.py                # App FastAPI utama
│   └── ...
├── frontend/                  # Aplikasi Nuxt frontend
│   ├── app.vue
│   ├── assets/
│   ├── composables/
│   ├── layouts/
│   ├── pages/
│   ├── plugins/
│   ├── stores/
│   ├── Dockerfile
│   ├── nuxt.config.ts
│   └── package.json
├── tests/
│   └── test_api_crud.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── bengkel.db
├── test_bengkel.db
└── presentation_english.md
```

## Persyaratan sistem

- Python 3.12+
- Node.js 22+
- npm
- Docker Desktop (opsional, untuk menjalankan dengan Docker)
- API key Google Gemini
- Akses ke PostgreSQL atau SQLite untuk penyimpanan data

## Konfigurasi environment

Buat file `.env` berdasarkan template `.env.example`:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-this-password
ADMIN_TOKEN_SECRET=change-this-secret
ADMIN_TOKEN_TTL_SECONDS=28800
GEMINI_DAILY_BUDGET_USD=0
GEMINI_INPUT_COST_PER_1M=0
GEMINI_OUTPUT_COST_PER_1M=0
POSTGRES_DB=bengkel
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
FRONTEND_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Penjelasan singkat:

- `GEMINI_API_KEY` wajib untuk fitur AI chat
- `ADMIN_USERNAME` dan `ADMIN_PASSWORD` dipakai untuk login admin
- `ADMIN_TOKEN_SECRET` wajib agar token autentikasi dibuat dan diverifikasi dengan aman
- Jika `POSTGRES_DB`, `POSTGRES_USER`, dan `POSTGRES_PASSWORD` terisi, aplikasi akan mencoba menggunakan PostgreSQL
- Jika PostgreSQL tidak tersedia, aplikasi otomatis fallback ke SQLite

## Menjalankan backend lokal

1. Buat virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

2. Install dependency

```bash
pip install -r requirements.txt
```

3. Copy environment file

```bash
copy .env.example .env
```

4. Jalankan server backend

```bash
python -m uvicorn app.main:app --reload
```

Server akan aktif di:

```text
http://localhost:8000
```

## Login admin

Aplikasi memiliki autentikasi admin untuk endpoint yang dilindungi, termasuk chat AI dan operasi tertentu. Login dilakukan melalui endpoint:

```http
POST /auth/login
```

Request body:

```json
{
  "username": "admin",
  "password": "change-this-password"
}
```

Response:

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

Gunakan token tersebut di header berikut untuk endpoint yang membutuhkan hak admin:

```http
Authorization: Bearer <access_token>
```

## Menjalankan frontend lokal

```bash
cd frontend
npm install
npm run dev
```

Frontend akan berjalan di:

```text
http://localhost:3000
```

Jika backend berjalan di port lain, atur variabel berikut di file `.env` di folder frontend:

```env
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

## Menjalankan dengan Docker Compose

Pastikan file `.env` sudah dibuat terlebih dahulu, lalu jalankan:

```bash
docker compose up --build
```

Layanan yang tersedia:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432

Untuk menghentikan seluruh layanan:

```bash
docker compose down
```

## Seed data (opsional)

Untuk menambahkan data contoh seperti pelanggan, kendaraan, mekanik, dan sparepart, jalankan:

```bash
python -m app.database.seed
```

## Endpoint API utama

Semua endpoint utama tidak memakai prefix `/api`.

### Autentikasi

- `POST /auth/login`

### Pelanggan

- `GET /customers/`
- `POST /customers/`
- `GET /customers/{id}`
- `PUT /customers/{id}`
- `DELETE /customers/{id}`

### Kendaraan

- `GET /vehicles/`
- `POST /vehicles/`
- `GET /vehicles/{id}`
- `PUT /vehicles/{id}`
- `DELETE /vehicles/{id}`

### Sparepart

- `GET /spareparts/`
- `POST /spareparts/`
- `GET /spareparts/{id}`
- `PUT /spareparts/{id}`
- `DELETE /spareparts/{id}`

### Servis / Service Order

- `GET /services/`
- `POST /services/`
- `GET /services/{service_id}`
- `PUT /services/{service_id}`
- `DELETE /services/{service_id}`

### Appointment

- `GET /appointments/`
- `POST /appointments/`
- `PATCH /appointments/{appointment_id}/status`

### AI Chat

- `POST /chat/`

### Insight / Dashboard

- `GET /insights/`

### Health / Monitoring

- `GET /`
- `GET /health`
- `GET /metrics`

## Dokumentasi API interaktif

Setelah backend berjalan, dokumentasi otomatis tersedia di:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contoh request

### Login admin

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"change-this-password"}'
```

### Chat AI

```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "message": "Tampilkan servis yang masih menunggu",
    "session_id": "budi-001"
  }'
```

### Membuat pelanggan baru

```bash
curl -X POST http://localhost:8000/customers/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Budi Santoso",
    "phone": "081234567890",
    "email": "budi@example.com",
    "address": "Jl. Merdeka No. 10"
  }'
```

## Testing

Project memiliki test CRUD dasar di folder `tests/`.

Untuk menjalankan test:

```bash
pip install pytest
pytest tests/
```

## Troubleshooting

### 1. AI chat gagal karena API key invalid

Pastikan `GEMINI_API_KEY` sudah diisi dengan key yang valid dan restart backend setelah perubahan `.env`.

### 2. Admin login gagal

Periksa variabel berikut di `.env`:

- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `ADMIN_TOKEN_SECRET`

### 3. PostgreSQL tidak bisa terhubung

Aplikasi akan otomatis fallback ke SQLite jika koneksi PostgreSQL gagal. Namun untuk lingkungan produksi, pastikan konfigurasi PostgreSQL benar dan port 5432 tidak diblokir.

### 4. Frontend tidak terhubung ke backend

Pastikan `NUXT_PUBLIC_API_BASE` di frontend menunjuk ke URL backend yang benar, misalnya:

```env
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

## Catatan implementasi

- Project saat ini fokus pada fitur operasional bengkel dan AI assistant berbasis Gemini.
- Endpoint yang memerlukan otorisasi admin harus dikirim dengan token bearer yang valid.
- Data chat disimpan berdasarkan `session_id` agar konteks percakapan dapat dipertahankan.
- Struktur aplikasi masih bisa dikembangkan lebih lanjut untuk modul seperti laporan keuangan, stok otomatis, atau role user yang lebih granular.

## Kesimpulan

BengkelAI adalah solusi manajemen bengkel yang cocok untuk lingkungan usaha kecil hingga menengah yang ingin menggabungkan operasional harian dengan dukungan AI. Dengan arsitektur yang terpisah antara frontend, backend, dan database, project ini relatif mudah dikembangkan, diujicoba, dan di-deploy di berbagai lingkungan.
