import http from 'k6/http';
import { check } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.0.0/index.js';

export let options = {
    vus: 20,       // 20 virtual users
    duration: '1s' // Run for 1 seconds
};

export default function () {
    // Generate random file content
    let fileContent = randomString(20); // Random string of 20 characters
    // Generate a unique filename for each virtual user and iteration
    let filename = `file_${__VU}_${__ITER}.txt`;

    // Prepare the file for upload
    let data = {
        file: http.file(fileContent, filename),
    };

    // Make the POST request to the upload endpoint
    let res = http.post('http://127.0.0.1:5000/upload', data);

    // Check if the response is 201 Created
    check(res, {
        'is status 201': (r) => r.status === 201,
        'is not status 400': (r) => r.status !== 400,
    });
}
