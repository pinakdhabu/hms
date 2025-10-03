/**
 * MongoDB CRUD examples for Hotel Management System
 * Requires: npm install mongodb
 * Target: MongoDB 6.x
 */

const { MongoClient, ObjectId } = require('mongodb');
const url = process.env.MONGO_URL || 'mongodb://localhost:27017';
const dbName = 'hotel_ms';

async function run() {
  const client = new MongoClient(url);
  try {
    await client.connect();
    const db = client.db(dbName);
    const reviews = db.collection('reviews');
    const feedback = db.collection('feedback');
    const logs = db.collection('logs');

    // 1) Insert guest feedback
    const fbResult = await feedback.insertOne({
      customerId: 1,
      reservationId: 101,
      comment: 'Great stay, friendly staff',
      score: 5,
      createdAt: new Date()
    });
    console.log('Inserted feedback id=', fbResult.insertedId);

    // 2) Update review score
    const updateResult = await reviews.updateOne({ _id: ObjectId('000000000000000000000000') }, { $set: { score: 4 } });
    console.log('Update matched=', updateResult.matchedCount, 'modified=', updateResult.modifiedCount);

    // 3) Delete outdated logs (older than 90 days)
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - 90);
    const delResult = await logs.deleteMany({ createdAt: { $lt: cutoff } });
    console.log('Deleted logs count=', delResult.deletedCount);

    // 4) Retrieve all feedback for a given customer
    const custFeedback = await feedback.find({ customerId: 1 }).toArray();
    console.log('Feedback for customer 1:', custFeedback);

  } catch (err) {
    console.error('MongoDB error:', err);
  } finally {
    await client.close();
  }
}

if (require.main === module) run();
