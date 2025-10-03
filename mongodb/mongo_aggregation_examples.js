// MongoDB aggregation examples (MongoDB 6.x compatible)
const { MongoClient } = require('mongodb');
const url = process.env.MONGO_URL || 'mongodb://localhost:27017';
const dbName = 'hotel_ms';

async function run() {
  const client = new MongoClient(url);
  try {
    await client.connect();
    const db = client.db(dbName);
    const reviews = db.collection('reviews');

    // 1) Average review score by room type
    const avgByRoomType = await reviews.aggregate([
      { $group: { _id: '$roomType', avgScore: { $avg: '$score' }, count: { $sum: 1 } } },
      { $sort: { avgScore: -1 } }
    ]).toArray();
    console.log('Average score by room type:', avgByRoomType);

    // 2) Top 3 most active customers (by number of reviews + feedback)
    const activity = await db.collection('reviews').aggregate([
      { $group: { _id: '$customerId', reviews: { $sum: 1 } } },
      { $sort: { reviews: -1 } },
      { $limit: 3 }
    ]).toArray();
    console.log('Top 3 active customers:', activity);

  } catch (err) {
    console.error('Aggregation error:', err);
  } finally {
    await client.close();
  }
}

if (require.main === module) run();
