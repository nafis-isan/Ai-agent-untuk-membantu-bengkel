# Bengkel AI Agent

Sistem AI Agent untuk manajemen bengkel (workshop) yang mengintegrasikan pelanggan, kendaraan, dan layanan.

## Fitur Utama

- 🤖 AI Agent untuk memproses permintaan pelanggan
- 👥 Manajemen data pelanggan
- 🚗 Tracking kendaraan
- 🔧 Manajemen layanan dan perbaikan
- 🗄️ Database SQLite/PostgreSQL
- 🔌 REST API dengan FastAPI
- 🐳 Docker & Docker Compose support

## Struktur Proyek

```
bengkel-ai-agent/
├── app/
│   ├── agent/          # AI Agent logic
│   ├── database/       # Database models & schemas
│   ├── api/            # API endpoints
│   └── main.py         # Application entry point
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
└── README.md          # Documentation
```

## Prerequisites

- Python 3.11+
- pip atau Poetry
- Docker & Docker Compose (optional)

## Instalasi

### 1. Clone repository
```bash
git clone <repository-url>
cd bengkel-ai-agent
```

### 2. Setup Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment
```bash
cp .env.example .env
# Edit .env sesuai kebutuhan
```

## Menjalankan Aplikasi

### Development Mode
```bash
python -m uvicorn app.main:app --reload
```

Server akan berjalan di `http://localhost:8000`

### Production Mode
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Menggunakan Docker
```bash
docker-compose up -d
```

## API Documentation

Akses dokumentasi API interaktif:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Customers
- `GET /api/customers` - Dapatkan semua pelanggan
- `GET /api/customers/{id}` - Dapatkan pelanggan spesifik
- `POST /api/customers` - Buat pelanggan baru
- `PUT /api/customers/{id}` - Update pelanggan
- `DELETE /api/customers/{id}` - Hapus pelanggan

### Vehicles
- `GET /api/vehicles` - Dapatkan semua kendaraan
- `GET /api/vehicles/{id}` - Dapatkan kendaraan spesifik
- `POST /api/vehicles` - Buat kendaraan baru
- `PUT /api/vehicles/{id}` - Update kendaraan
- `DELETE /api/vehicles/{id}` - Hapus kendaraan

### Services
- `GET /api/services` - Dapatkan semua layanan
- `GET /api/services/{id}` - Dapatkan layanan spesifik
- `POST /api/services` - Buat layanan baru
- `PUT /api/services/{id}` - Update layanan
- `DELETE /api/services/{id}` - Hapus layanan

### AI Agent
- `POST /agent/chat` - Chat dengan AI Agent

## Testing

```bash
pytest tests/
```

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - lihat file LICENSE untuk detail

## Support

Untuk pertanyaan dan dukungan, silakan buat issue di repository.
