import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

const queue = kue.createQueue();

describe('createPushNotificationsJobs', () => {
  before(() => {
    queue.testMode.enter(); // Enter test mode
  });

  after(() => {
    queue.testMode.exit(); // Exit test mode
  });

  afterEach(() => {
    queue.testMode.clearQueue(); // Clear the queue after each test
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(Error, 'Jobs is not an array');
  });

  it('should create two new jobs to the queue', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 5678 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);
    const queuedJobs = queue.testMode.jobs;

    expect(queuedJobs).to.have.lengthOf(2);
    expect(queuedJobs[0].data).to.deep.equal(jobs[0]);
    expect(queuedJobs[1].data).to.deep.equal(jobs[1]);
  });
});
