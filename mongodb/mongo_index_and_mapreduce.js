// MongoDB index creation and mapReduce example (word frequency in reviews)
const { MongoClient } = require('mongodb');
const url = process.env.MONGO_URL || 'mongodb://localhost:27017';
const dbName = 'hotel_ms';

async function run() {
  const client = new MongoClient(url);
  try {
    await client.connect();
    const db = client.db(dbName);
    const reviews = db.collection('reviews');

    // Create an index on customerId for faster lookups
    await reviews.createIndex({ customerId: 1 });
    console.log('Created index on reviews.customerId');

    // MapReduce example: word frequency in review comments (simple)
    const map = function() {
      if (this.comment) {
        this.comment.split(/\s+/).forEach(function(word) {
          word = word.replace(/[^a-zA-Z]/g, '').toLowerCase();
          if (word) emit(word, 1);
        });
      }
    };
    const reduce = function(key, values) { return Array.sum(values); };

    const out = await reviews.mapReduce(map, reduce, { out: { inline: 1 } });
    console.log('MapReduce word frequencies sample:', out);

  } catch (err) {
    console.error('Index/mapReduce error:', err);
  } finally {
    await client.close();
  }
}

if (require.main === module) run();
