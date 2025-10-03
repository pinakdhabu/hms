// Sample Node.js connectivity script for MongoDB + MySQL (demonstrates combined operations)
// Requires: npm i mongodb mysql2

const { MongoClient } = require('mongodb');
const mysql = require('mysql2/promise');

const MONGO_URL = process.env.MONGO_URL || 'mongodb://localhost:27017';
const MYSQL_CONFIG = {
  host: process.env.MYSQL_HOST || 'localhost',
  user: process.env.MYSQL_USER || 'root',
  password: process.env.MYSQL_PASSWORD || '',
  database: 'hotel_ms'
};

async function run() {
  const mclient = new MongoClient(MONGO_URL);
  const conn = await mysql.createConnection(MYSQL_CONFIG);
  try {
    await mclient.connect();
    const db = mclient.db('hotel_ms');

    // Example: fetch reservations from MySQL and log count into MongoDB
    const [rows] = await conn.execute('SELECT COUNT(*) as cnt FROM Reservation');
    const cnt = rows[0].cnt || 0;
    await db.collection('logs').insertOne({ level: 'INFO', message: 'Reservation count fetched', count: cnt, createdAt: new Date() });

    console.log('Logged reservation count to MongoDB');
  } catch (err) {
    console.error('Connectivity sample error:', err.message);
  } finally {
    await conn.end();
    await mclient.close();
  }
}

if (require.main === module) run();
