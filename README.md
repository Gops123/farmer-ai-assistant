# 🌱 Farmer - AI Agriculture Assistant

**Farmer** is a comprehensive, production-ready AI-powered agriculture chatbot designed to help farmers make informed decisions about their farming practices. Built with modern Python practices, comprehensive logging, and a scalable architecture.

## ✨ Features

### 🎯 **Core Capabilities**
- **Multi-language Support** - Available in 10 Indian languages
- **Database Integration** - PostgreSQL with SQLAlchemy ORM
- **Redis Caching** - Fast response times with Redis
- **Enhanced AI Responses** - Context-aware agriculture expertise
- **Offline Fallback** - Basic responses when AI services are unavailable
- **Comprehensive Logging** - Structured logging with rotation and multiple outputs

### 🌤️ **Weather & Climate**
- **Real-time Weather Data** - Get current weather conditions for any location
- **Farming Recommendations** - Weather-based crop and farming advice
- **Location-based Insights** - Personalized recommendations for your area

### 🌾 **Crop Management**
- **Smart Crop Recommendations** - Based on location, soil type, and weather
- **Seasonal Guidance** - Kharif, Rabi, and Zaid season information
- **Soil Type Analysis** - Tailored advice for different soil conditions

### 🔍 **Disease Detection**
- **Image Upload & Analysis** - Upload crop images for disease detection
- **Computer Vision Analysis** - Basic image processing for crop health
- **Treatment Recommendations** - Advice based on detected issues

### 📊 **Market Intelligence**
- **Real-time Prices** - Current agricultural commodity prices
- **Price Trends** - Market direction indicators
- **Crop Economics** - Help with crop selection based on market conditions

### 💬 **Enhanced Chat Experience**
- **Voice Input/Output** - Speak to the bot and hear responses
- **Chat History** - Save and retrieve all conversations
- **Export Functionality** - Download chat logs as CSV
- **Modern UI/UX** - Beautiful, responsive design

## 🏗️ Project Structure

```
farmer/
├── src/
│   └── farmer/
│       ├── __init__.py          # Package initialization
│       ├── app.py               # Flask application factory
│       ├── cli.py               # Command-line interface
│       ├── api/                 # API endpoints and routes
│       ├── core/                # Core functionality (database, redis, middleware)
│       ├── models/              # Database models
│       ├── services/            # Business logic services
│       ├── utils/               # Utility functions
│       └── config/              # Configuration management
├── templates/                   # HTML templates
├── static/                      # Static assets
├── logs/                        # Application logs
├── uploads/                     # File uploads
├── main.py                      # Main entry point
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Production Docker Compose setup
├── docker-compose.dev.yml       # Development Docker Compose setup
├── nginx.conf                   # Nginx configuration
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key
- Hugging Face API key
- OpenWeatherMap API key (optional)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd farmer-ai-assistant
   ```

2. **Set up environment variables**
   Create a `.env` file with your API keys:
   ```bash
   # Required API Keys
   OPENAI_API_KEY=your_openai_api_key_here
   HUGGINGFACE_KEY=your_huggingface_api_key_here
   
   # Optional API Keys
   WEATHER_API_KEY=your_openweathermap_api_key_here
   
   # Flask Configuration
   FARMER_SECRET_KEY=your_secret_key_here_change_this_in_production
   ```

3. **Deploy with Docker Compose**
   ```bash
   # Production deployment
   docker-compose up -d
   
   # Development deployment
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. **Access the application**
   Open your browser and go to `http://localhost:8000`

### Option 2: Local Development

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd farmer-ai-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with your API keys (see above)

4. **Run the application**
   ```bash
   python main.py
   ```

## 🐳 Docker Services

### Production Services
- **farmer-ai-app**: Main Flask application
- **postgres**: PostgreSQL database
- **redis**: Redis cache
- **nginx**: Reverse proxy

### Development Services
- **farmer-ai-dev**: Main Flask application (with volume mounting)
- **postgres**: PostgreSQL database
- **redis**: Redis cache

## 🎮 Usage

### Web Interface
- Open your browser and navigate to `http://localhost:8000`
- Use the intuitive interface to interact with the AI assistant

### Command Line Interface
The project includes a comprehensive CLI tool:

```bash
# Show available commands
python -m farmer.cli --help

# Run the server
python -m farmer.cli run --host 0.0.0.0 --port 5000

# Initialize database
python -m farmer.cli init-db

# Health check
python -m farmer.cli health-check

# Show configuration
python -m farmer.cli show-config
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `HUGGINGFACE_KEY`: Your Hugging Face API key
- `WEATHER_API_KEY`: Your OpenWeatherMap API key (optional)
- `FARMER_SECRET_KEY`: Flask secret key
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_HOST`: Redis host address
- `REDIS_PORT`: Redis port (default: 6379)

### Database Configuration
- **Database**: PostgreSQL 15
- **User**: farmer_user
- **Password**: farmer_password
- **Database**: farmer (production) / farmer_dev (development)

### Redis Configuration
- **Host**: redis
- **Port**: 6379
- **Database**: 0

## 📝 API Endpoints

- `GET /`: Main application page
- `GET /health`: Health check endpoint
- `POST /chat`: Chat with AI assistant
- `GET /api/v1/health`: API health check
- `POST /api/v1/chat`: API chat endpoint

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=farmer
```

## 📊 Monitoring

- **Health Checks**: Built-in health checks for all services
- **Logging**: Comprehensive logging with rotation
- **Metrics**: Application metrics via health endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request