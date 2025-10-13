# HUNGER Restaurant Mobile App

Role-based mobile application for restaurant billing with real-time updates via WebSocket.

## Architecture

- **Backend**: FastAPI + WebSocket (Python)
- **Mobile**: Flutter (single app, role-based UI)
- **Database**: SQLite (shared with desktop app)
- **Real-time**: WebSocket for live updates

## Setup

### 1. Backend Server

```bash
cd mobile_backend
pip install -r requirements.txt
python main.py
```

Or on Windows:
```bash
start_server.bat
```

Server runs on `http://localhost:8000`

### 2. Mobile App

```bash
cd mobile_app
flutter pub get
flutter run
```

## Features

### Captain Role
- View table status (available/occupied)
- Create new orders
- Add items to orders
- Send orders to kitchen
- Request bill generation

### Admin/Super Admin Role
- Live sales dashboard
- Menu management
- User management
- Order oversight
- Reports and analytics

## Real-time Updates

WebSocket events:
- `order_created`: New order placed
- `order_paid`: Order marked as paid
- `table_status_changed`: Table status updated
- `menu_updated`: Menu items changed

## API Endpoints

- `POST /api/auth/login` - User authentication
- `GET /api/menu` - Get menu items
- `GET /api/orders/open` - Get open orders
- `POST /api/orders` - Create new order
- `POST /api/orders/{invoice}/paid` - Mark order as paid
- `GET /api/orders/{invoice}` - Get order details
- `WS /ws/{user_id}` - WebSocket connection

## Configuration

Update server IP in mobile app:
- `lib/services/auth_service.dart` - API base URL
- `lib/services/websocket_service.dart` - WebSocket URL

## Development

### Backend
- FastAPI with automatic API documentation at `/docs`
- JWT authentication
- WebSocket for real-time updates
- Shared database with desktop app

### Mobile
- Flutter with Provider state management
- Role-based navigation
- Material Design UI
- Offline capability (planned)

## License

Licensed to Varchaswaa Media Pvt Ltd
