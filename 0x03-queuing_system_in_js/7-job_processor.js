const kue = require('kue');
const queue = kue.createQueue();
const blacklistedNumbers = ['4153518780', '4153518781'];

const sendNotification = (phoneNumber, message, job, done) => {
  job.progress(0, 100);
  if (blacklistedNumbers.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }
  job.progress(50, 100);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  done();
};

queue.process('push_notification_code_2', 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});

queue.on('job failed', (job, err) => {
  console.log(`Notification job ${job.id} failed: ${err.message}`);
});

queue.on('job complete', (job) => {
  console.log(`Notification job ${job.id} completed`);
});

queue.on('job progress', (job, progress) => {
  console.log(`Notification job ${job.id} ${progress}% complete`);
});
