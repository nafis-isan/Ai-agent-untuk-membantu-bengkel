# BengkelAI

Aplikasi manajemen operasional bengkel dengan AI Agent. Backend menyediakan REST API untuk pelanggan, kendaraan, servis, suku cadang, dan insight operasional. Frontend menyediakan dashboard Nuxt untuk mengakses data tersebut serta antarmuka chat berbasis Google Gemini.

## Fitur

- Dashboard statistik operasional dan insight kondisi bengkel
- CRUD pelanggan, kendaraan, servis, dan suku cadang
- AI Agent dengan riwayat percakapan per `session_id`
- Konfirmasi sebelum AI menyimpan tindakan servis
- PostgreSQL untuk deployment dan fallback SQLite untuk development lokal
- Dokumentasi API otomatis dari FastAPI

## Teknologi

- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL 16
- **AI:** Google Gemini melalui `google-genai`
- **Frontend:** Nuxt, Vue 3, Pinia, Nuxt UI, Tailwind CSS
- **Deployment:** Docker Compose

## Struktur Proyek

```
.
├── app/
│   ├── agent/          # Agent Gemini, prompt, memory, dan tools
│   ├── api/            # Route customers, vehicles, services, spareparts, chat, insights
│   ├── database/       # Connection, model, schema, inisialisasi, dan seed
│   └── main.py         # Entry point FastAPI
├── frontend/
│   ├── pages/          # Dashboard, customers, vehicles, services, spareparts, chat
│   ├── stores/         # State management Pinia
│   ├── composables/    # Integrasi API
│   └── nuxt.config.ts
├── tests/              # Test API
├── .env.example        # Template konfigurasi environment
├── Dockerfile          # Image backend
├── docker-compose.yml  # PostgreSQL, backend, dan frontend
├── requirements.txt
└── README.md
```

## Prasyarat

- Python 3.12 atau lebih baru
- Node.js 22 atau lebih baru dan npm
- Google Gemini API key untuk fitur chat
- Docker Desktop dan Docker Compose (opsional)

## Menjalankan Secara Lokal

### Backend

1. Buat dan aktifkan virtual environment:

	```powershell
	python -m venv .venv
	.venv\Scripts\Activate.ps1
	```

	Untuk Linux/macOS, gunakan `source .venv/bin/activate`.

2. Install dependency dan salin konfigurasi:

	```powershell
	pip install -r requirements.txt
	Copy-Item .env.example .env
	```

3. Isi `GEMINI_API_KEY` di `.env`. Untuk database lokal tanpa PostgreSQL, biarkan konfigurasi PostgreSQL kosong; aplikasi akan memakai `bengkel.db` secara otomatis.

4. Jalankan API:

	```powershell
	python -m uvicorn app.main:app --reload
	```

	API tersedia di `http://localhost:8000`. Tabel database dibuat otomatis saat aplikasi dimulai.

### Data contoh (opsional)

Setelah backend dapat terhubung ke database, jalankan:

```powershell
python -m app.database.seed
```

Perintah ini menambahkan contoh pelanggan, kendaraan, mekanik, dan suku cadang.

### Frontend

Di terminal lain:

```powershell
cd frontend
npm install
npm run dev
```

Frontend tersedia di `http://localhost:3000`. URL backend dapat diubah melalui `frontend/.env`:

```env
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

Untuk build production frontend:

```powershell
npm run build
npm run preview
```

## Menjalankan dengan Docker Compose

Salin `.env.example` menjadi `.env`, isi `GEMINI_API_KEY`, lalu ubah `POSTGRES_HOST` menjadi `postgres` karena backend berjalan di dalam network Compose:

```env
GEMINI_API_KEY=your-gemini-api-key
POSTGRES_DB=bengkel
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

Jalankan seluruh stack:

```powershell
docker compose up --build
```

Layanan yang tersedia:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

Hentikan container dengan `docker compose down`. Tambahkan `-v` jika ingin menghapus volume database juga.

## API

Dokumentasi interaktif tersedia di:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Semua endpoint memakai path root berikut, tanpa prefix `/api`:

| Resource | Endpoint |
| --- | --- |
| Customers | `GET/POST /customers/`, `GET/PUT/DELETE /customers/{id}` |
| Vehicles | `GET/POST /vehicles/`, `GET/PUT/DELETE /vehicles/{id}` |
| Services | `GET/POST /services/`, `GET/PUT/DELETE /services/{id}` |
| Spareparts | `GET/POST /spareparts/`, `GET/PUT/DELETE /spareparts/{id}` |
| AI chat | `POST /chat/` |
| Insights | `GET /insights/` |

Contoh request chat:

```json
{
  "message": "Tampilkan servis yang masih menunggu",
  "session_id": "budi-001"
}
```

## Testing

Pastikan dependency backend sudah ter-install, lalu jalankan:

```powershell
pytest tests/
```

Test menggunakan database SQLite terpisah di `test_bengkel.db`.

## Konfigurasi Environment

| Variabel | Keterangan | Default |
| --- | --- | --- |
| `GEMINI_API_KEY` | API key Google Gemini; diperlukan untuk chat | - |
| `GEMINI_MODEL` | Model Gemini yang digunakan agent | `gemini-3.5-flash` |
| `POSTGRES_DB` | Nama database PostgreSQL | - |
| `POSTGRES_USER` | User PostgreSQL | - |
| `POSTGRES_PASSWORD` | Password PostgreSQL | - |
| `POSTGRES_HOST` | Host PostgreSQL | `localhost` |
| `POSTGRES_PORT` | Port PostgreSQL | `5432` |

Jika tiga variabel PostgreSQL (`POSTGRES_DB`, `POSTGRES_USER`, dan `POSTGRES_PASSWORD`) tidak lengkap atau PostgreSQL tidak tersedia, backend memakai SQLite lokal.
