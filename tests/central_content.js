import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 20 }, // simulate ramp-up of traffic from 1 to 20 users over 30 seconds
        { duration: '1m', target: 20 }, // stay at 20 users for 1 minute
        { duration: '10s', target: 0 }, // ramp-down to 0 users
    ],
    thresholds: {
        'http_req_duration': ['p(99)<1500'], // 99% of requests must complete below 1.5s
    },
};

export default function () {
    const filename = 'file.txt'; // replace with a valid filename
    let res = http.get(`http://localhost:5000/content/${filename}`);
    check(res, { 'status was 200': (r) => r.status === 200 });
    sleep(1);
}
