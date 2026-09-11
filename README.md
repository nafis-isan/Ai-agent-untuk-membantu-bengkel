# BengkelAI

Sistem manajemen bengkel berbasis web yang menggabungkan backend FastAPI, frontend Nuxt, database, dan AI Agent dari Google Gemini. Project ini dibuat untuk membantu pengelolaan pelanggan, kendaraan, servis, suku cadang, serta informasi operasional bengkel.

## Fitur yang tersedia saat ini

- CRUD pelanggan
- CRUD kendaraan
- CRUD mekanik
- CRUD suku cadang / sparepart
- CRUD service order
- Dashboard dan insight operasional
- AI Chat dengan Google Gemini
- Riwayat percakapan per `session_id`
- Database otomatis fallback dari PostgreSQL ke SQLite
- Dokumentasi API otomatis dengan FastAPI
- Docker Compose untuk menjalankan backend, frontend, dan database sekaligus

## Teknologi yang digunakan

- Backend: Python, FastAPI, SQLAlchemy, Pydantic
- Frontend: Nuxt.js, Vue 3, Pinia, Tailwind CSS, Nuxt UI
- Database: PostgreSQL dan SQLite
- AI: Google Gemini via `google-genai`
- Container: Docker, Docker Compose
- Testing: Pytest

## Struktur project

```text
.
├── app/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── memory.py
│   │   ├── prompts.py
│   │   └── tools.py
│   ├── api/
│   │   ├── chat.py
│   │   ├── customers.py
│   │   ├── insights.py
│   │   ├── services.py
│   │   ├── spareparts.py
│   │   └── vehicles.py
│   ├── database/
│   │   ├── connection.py
│   │   ├── dependencies.py
│   │   ├── init_db.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── seed.py
│   └── main.py
├── frontend/
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
├── build_log.txt
├── presentation_english.md
├── bengkel.db
└── test_bengkel.db
```

## Prasyarat

- Python 3.12+
- Node.js 22+
- npm
- Docker Desktop (opsional, untuk menjalankan via Docker)
- API key Google Gemini untuk fitur AI chat

## Konfigurasi environment

Buat file `.env` dari template `.env.example`:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash
POSTGRES_DB=bengkel
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Catatan:

- Jika `POSTGRES_DB`, `POSTGRES_USER`, dan `POSTGRES_PASSWORD` lengkap, aplikasi akan mencoba menggunakan PostgreSQL.
- Jika PostgreSQL tidak tersedia, aplikasi otomatis fallback ke SQLite.
- Project saat ini belum memiliki autentikasi user / login seperti admin management.

## Menjalankan backend secara lokal

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

3. Salin environment

```bash
copy .env.example .env
```

4. Jalankan server

```bash
python -m uvicorn app.main:app --reload
```

Server akan berjalan di:

```text
http://localhost:8000
```

## Menjalankan frontend secara lokal

```bash
cd frontend
npm install
npm run dev
```

Frontend akan berjalan di:

```text
http://localhost:3000
```

Untuk mengubah base URL backend, dapat dibuat file `.env` di folder frontend:

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

Untuk menghentikan:

```bash
docker compose down
```

## Seed data (opsional)

Untuk menambahkan data contoh pelanggan, kendaraan, mekanik, dan sparepart, jalankan:

```bash
python -m app.database.seed
```

## Endpoint API utama

Semua endpoint utama tidak memakai prefix `/api`.

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

### Servis

- `GET /services/`
- `POST /services/`
- `GET /services/{service_id}`
- `PUT /services/{service_id}`
- `DELETE /services/{service_id}`

### Sparepart

- `GET /spareparts/`
- `POST /spareparts/`
- `GET /spareparts/{id}`
- `PUT /spareparts/{id}`
- `DELETE /spareparts/{id}`

### Chat AI

- `POST /chat/`

### Insight

- `GET /insights/`

## Dokumentasi API

Setelah backend berjalan, dokumentasi interaktif tersedia di:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contoh request chat

```json
{
  "message": "Tampilkan servis yang masih menunggu",
  "session_id": "budi-001"
}
```

## Testing

Project memiliki test CRUD dasar di folder `tests/`.

Untuk menjalankan test, install `pytest` terlebih dahulu:

```bash
pip install pytest
pytest tests/
```

## Catatan implementasi

- Project saat ini fokus pada fitur CRUD dan AI chat.
- Fitur login / autentikasi belum ada di project.
- AI chat hanya akan berfungsi jika `GEMINI_API_KEY` diisi dengan key valid.
- Data hasil chat disimpan dengan `session_id` untuk menjaga konteks percakapan.

## Ringkasan

BengkelAI adalah aplikasi manajemen bengkel yang saat ini mencakup:

- data pelanggan
- data kendaraan
- data mekanik
- data suku cadang
- data servis
- insight operasional
- AI Assistant berbasis Gemini

Project ini sudah siap dipakai untuk pengembangan lebih lanjut sesuai kebutuhan bengkel yang lebih kompleks.
