// pages/api/run-fortran.js
import { spawn } from 'child_process';
import { join } from 'path';

export default function handler(req, res) {
  if (req.method === 'POST') {
    const { val, a, b, lambda2, lambda3, lambda1_step, lambda1_max, lambda1_min } = req.body;
    const exePath = join(__dirname, '../../../../compiled_executable');

    // Spawn the Fortran executable with input parameters
    const child = spawn(exePath, [val, a, b, lambda2, lambda3, lambda1_step, lambda1_max, lambda1_min]);

    child.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
    });

    child.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });

    child.on('close', (code) => {
      console.log(`child process exited with code ${code}`);
      res.status(200).json({ message: `Fortran code executed with code ${code}` });
    });
    res.status(200).json({message:'Done'})
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}
