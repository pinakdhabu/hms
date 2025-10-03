// MongoDB seed script for Hotel Management System
// Usage: node mongo_seed.js (requires npm i mongodb)

const { MongoClient } = require('mongodb');
const url = process.env.MONGO_URL || 'mongodb://localhost:27017';
const dbName = 'hotel_ms';

async function seed() {
  const client = new MongoClient(url);
  try {
    await client.connect();
    const db = client.db(dbName);

    const reviews = db.collection('reviews');
    const feedback = db.collection('feedback');
    const logs = db.collection('logs');

    await reviews.insertMany([
      { customerId: 1, roomType: 'Single', score: 5, comment: 'Cozy and clean', createdAt: new Date() },
      { customerId: 2, roomType: 'Double', score: 4, comment: 'Good value', createdAt: new Date() },
      { customerId: 3, roomType: 'Suite', score: 5, comment: 'Luxurious stay', createdAt: new Date() }
    ]);

    await feedback.insertMany([
      { customerId: 1, reservationId: 1, comment: 'Quick check-in', score: 5, createdAt: new Date() },
      { customerId: 2, reservationId: 2, comment: 'Breakfast was OK', score: 3, createdAt: new Date() }
    ]);

    await logs.insertMany([
      { level: 'INFO', message: 'Reservation created', reservationId: 1, createdAt: new Date() },
      { level: 'INFO', message: 'Payment recorded', reservationId: null, createdAt: new Date() }
    ]);

    console.log('MongoDB seed completed.');
  } catch (err) {
    console.error('Seed error:', err);
  } finally {
    await client.close();
  }
}

if (require.main === module) seed();
