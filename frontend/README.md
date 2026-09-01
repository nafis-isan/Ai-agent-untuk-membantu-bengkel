# BengkelAI Frontend

Frontend untuk Aplikasi BengkelAI menggunakan Vue 3 + Nuxt dengan TailwindCSS.

## Features

- 🎨 Beautiful UI dengan Nuxt UI & TailwindCSS
- 📱 Responsive Design
- 🔄 Real-time API Integration
- 🤖 AI Chat Interface
- 📊 Dashboard dengan statistik
- 👥 Customer Management
- 🚗 Vehicle Tracking
- 🔧 Service History
- 📦 Spareparts Inventory
- 🎯 State Management dengan Pinia

## Setup

### Install Dependencies

```bash
cd frontend
npm install
```

### Development Mode

```bash
npm run dev
```

Aplikasi akan berjalan di `http://localhost:3000`

### Production Build

```bash
npm run build
npm run preview
```

### Generate Static Site

```bash
npm run generate
```

## Project Structure

```
frontend/
├── app.vue              # Main application file
├── nuxt.config.ts       # Nuxt configuration
├── tailwind.config.js   # TailwindCSS config
├── package.json
│
├── pages/              # Page components
│   ├── index.vue       # Dashboard
│   ├── customers.vue   # Customer management
│   ├── vehicles.vue    # Vehicle tracking
│   ├── services.vue    # Service history
│   ├── spareparts.vue  # Spareparts inventory
│   └── chat.vue        # AI Chat
│
├── layouts/            # Layout components
│   └── default.vue     # Main layout with sidebar
│
├── components/         # Reusable components
├── stores/             # Pinia stores
│   ├── auth.ts
│   ├── customers.ts
│   ├── vehicles.ts
│   ├── chat.ts
│   └── ...
│
├── composables/        # Composables (hooks)
│   └── useAPI.ts
│
├── plugins/            # Plugins
├── assets/             # Static assets
│   └── css/
│       └── main.css
│
└── public/             # Public files
```

## Environment Variables

Create `.env` file:

```env
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

## Features Detail

### 1. Dashboard
- Overview statistik pelanggan, kendaraan, servis, pendapatan
- List servis terbaru
- Alert suku cadang dengan stok rendah

### 2. Customer Management
- Daftar pelanggan dengan search
- Tambah pelanggan baru
- Edit dan hapus pelanggan
- Form validation

### 3. Vehicle Tracking
- Grid view kendaraan
- Search berdasarkan plat nomor
- Tambah kendaraan baru
- Lihat riwayat servis per kendaraan

### 4. Service History
- Timeline view riwayat servis
- Filter berdasarkan status
- Invoice printing
- Detail servis

### 5. Spareparts Inventory
- Grid view suku cadang
- Stock monitoring dengan color coding
- Low stock alerts
- Search functionality

### 6. AI Chat Interface
- Real-time chat dengan AI Agent
- Quick command buttons
- Message history
- Loading states

## API Integration

Semua store menggunakan `ofetch` untuk HTTP requests ke backend FastAPI:

```typescript
// Example dari stores/customers.ts
const response = await $fetch(`${config.public.apiBase}/customers`, {
  method: 'POST',
  body: customer
})
```

## Styling

Project menggunakan TailwindCSS + Nuxt UI dengan custom configuration:

- Primary color: Blue (`#3b82f6`)
- Gray color: Slate
- Responsive breakpoints: sm, md, lg
- Dark mode support (siap untuk development)

## Development Tips

1. **Composables**: Gunakan `composables/` untuk logic reusable
2. **Stores**: Gunakan Pinia store untuk state management
3. **Components**: Buat component di `components/` untuk reusable UI
4. **Pages**: Automatic routing based on file structure
5. **Tailwind**: Gunakan utility classes untuk styling

## Deployment

### Docker

Buat `Dockerfile`:

```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.output ./
EXPOSE 3000
CMD ["node", "server/index.mjs"]
```

### Vercel/Netlify

1. Connect repository ke Vercel/Netlify
2. Build command: `npm run build`
3. Output directory: `.output/public`

## Troubleshooting

### API Connection Issues

- Pastikan backend FastAPI running di port 8000
- Set `NUXT_PUBLIC_API_BASE` ke URL backend yang benar
- Check CORS configuration di backend

### Module Not Found

```bash
# Clear node_modules dan reinstall
rm -rf node_modules
npm install
```

### Build Errors

```bash
# Clear .nuxt cache
rm -rf .nuxt
npm run build
```

## License

MIT

## Support

Untuk bantuan dan pertanyaan, buat issue di repository.
