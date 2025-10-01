const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 8000;

// CORS 설정
app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));

// 정적 파일 서빙
app.use(express.static(path.join(__dirname)));

// 메인 페이지 라우트
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API 라우트들
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        timestamp: new Date().toISOString(),
        message: 'US Economic Dashboard Server is running'
    });
});

// 404 핸들러
app.use((req, res) => {
    res.status(404).json({ 
        error: 'Not Found',
        message: 'The requested resource was not found'
    });
});

// 서버 시작
app.listen(PORT, () => {
    console.log(`🚀 US Economic Dashboard Server running at http://localhost:${PORT}`);
    console.log(`📊 Dashboard: http://localhost:${PORT}/`);
    console.log(`🔍 API Health: http://localhost:${PORT}/api/health`);
    console.log('Press Ctrl+C to stop the server');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down server...');
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Shutting down server...');
    process.exit(0);
});


