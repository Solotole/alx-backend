import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const port = 1245;

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

let reservationEnabled = true;
await setAsync('available_seats', 50);

const queue = kue.createQueue();
app.use(express.json());

app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: availableSeats });
});

const reserveSeat = async (number) => {
    await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
    const seats = await getAsync('available_seats');
    return seats ? parseInt(seats, 10) : 0;
};

app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservations are blocked' });
    }
    const job = queue.create('reserve_seat').save((err) => {
        if (!err) {
            return res.json({ status: 'Reservation in process' });
        }
        return res.json({ status: 'Reservation failed' });
    });
});

queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats > 0) {
	await reserveSeat(availableSeats - 1);
	if (availableSeats - 1 === 0) {
	    reservationEnabled = false;
	}
	console.log(`Seat reservation job ${job.id} completed`);
	done();
    } else {
        done(new Error('Not enough seats available'));
    }
});

queue.on('job failed', (id, err) => {
    console.log(`Seat reservation job ${id} failed: ${err.message}`);
});

app.get('/process', (req, res) => {
    res.json({ status: 'Queue processing' });
    queue.process();
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
