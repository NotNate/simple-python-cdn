import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 50, // Number of virtual users
    duration: '30s', // Duration of the test
};

export default function () {
    const filename = 'file.txt';
    let res = http.get(`http://localhost:5001/content/${filename}`);
    check(res, { 'status was 200 or 404': (r) => [200, 404].includes(r.status) });
    sleep(1);
}
