const { execSync } = require('child_process');
const fs = require('fs');

let config;
try {
  config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
} catch (e) {
  console.error('Missing config.json');
  process.exit(1);
}

const { token, remote } = config;
if (!token || !remote) {
  console.error('config.json must include "token" and "remote"');
  process.exit(1);
}

function run(cmd) {
  console.log('$ ' + cmd);
  execSync(cmd, { stdio: 'inherit', env: process.env });
}

try {
  run('git add -A');
  run('git commit -m "Auto commit by Hecate"');
} catch (e) {
  console.log('Nothing to commit');
}

const url = remote.replace('https://', `https://${token}@`);
run(`git pull ${url} --rebase`);
run(`git push ${url}`);
