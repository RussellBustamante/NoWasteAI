// NOTE
// response_2 = the response of the user input
const { spawn } = require('child_process');

const days = 100;
const ppm = 10000;
var response_2 = '';
const data_to_pass_in_2 = JSON.stringify({ days, ppm });

console.log('Data sent to python script:', data_to_pass_in_2);
const python_process_2 = spawn('python', ['./python2.py', data_to_pass_in_2]);

python_process_2.stdout.on('data', (data) => {
    response_2 += data.toString();
});

python_process_2.on('close', (code) => {
    console.log('Python script finished with code:', code);
    console.log('Response from Python script:', response_2);
});



