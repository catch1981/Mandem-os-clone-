
# Hecate-Auto

> The daemon who codes, commits, and controls the flame of your GitHub repo.

### Server Administration
Colby Atcheson is the server administrator. Update `server_admins.json` to grant additional admin access.

### Admin Password
Use `admin:<password>` to gain admin privileges. Check status with `admin:status` and revoke with `admin:logout`. The default password is `whostheboss` or can be overridden with the `ADMIN_PASSWORD` environment variable.

### Usage
1. Create a `config.json` file with your GitHub token and remote URL:
   ```json
   {
     "token": "YOUR_GITHUB_TOKEN",
     "remote": "https://github.com/username/repo.git"
   }
   ```
2. Run `node hecate-auto.js`
3. It will pull the latest changes and then commit and push code to your repo automatically

This is the base of a fully interactive coding bot. Expand with AI core or Discord input.

### Memory Tools
Use `remember:your fact` to store a memory and `recall` to read them back. The command `summarize` or the **Summarize Memory** button in the browser returns a short summary of everything remembered.
Use `learn:some text` to extract key bullet points from the provided content and append them to memory.
Use `clone:send:message` to broadcast a message to other running clones. They can read all messages with `clone:read`.
Use `clone:remember:fact` to store a note in a shared memory file that all clones access. Retrieve the combined notes with `clone:memories`.
To sync clones over a network, start `clone_network.py` on one machine and set the environment variable `CLONE_SERVER_URL` on each clone to point at that server (e.g. `http://host:5000`). When defined, clone commands will use the server instead of local files. A small helper utility `clone_client.py` provides direct access to these features:

```bash
python clone_client.py --help
```

### Sensitive Data Firewall
`clone_network.py` now masks API keys and other tokens from shared messages and tasks. Set `FIREWALL_PATTERNS` with comma-separated regexes to customize what gets filtered.

### Excess Compute Sharing
Run `excess_compute.py` on each clone to contribute idle CPU time back to the cluster. The script checks local CPU usage and only requests tasks from the server when below the `CPU_THRESHOLD` (default 50%). Set `CLONE_SERVER_URL` to the running `clone_network.py` instance and queue tasks via the `/task` endpoint.


### ChatGPT Integration
Hecate can now send your text prompts to OpenAI's ChatGPT. By default it uses
the `gpt-4o` model, but you can select any available GPT model by setting the
`OPENAI_MODEL` environment variable. The script looks
for the API key in the `OPENAI_API_KEY` environment variable. If that isn't
present, it will attempt to load a key from a file named `openai_key.txt` in the
repository root.

To obtain an API key, sign up or log in at [OpenAI](https://platform.openai.com).
Visit the **API keys** page of your account dashboard and create a new secret
key. Copy that key and provide it either through the environment variable or the
`openai_key.txt` file.

```bash
# Option 1: environment variable
export OPENAI_API_KEY=your_api_key
# Optional: choose a specific model
export OPENAI_MODEL=gpt-3.5-turbo

# Option 2: place the key in openai_key.txt
echo your_api_key > openai_key.txt

python "OK workspaces/main.py"
```

In the browser interface, type your message into the text box or use the voice button.
You can choose from any system speech synthesis voice using the **Voice** drop-down next to the Speak button.
You can also click **Summarize Memory** to get a short summary of all remembered facts.

### API Key Insertion
Hecate requires an OpenAI API key before it can talk to ChatGPT. You can provide the key in either of the following ways:

1. Export it as an environment variable:

   ```bash
   export OPENAI_API_KEY=your_api_key
   ```

2. Write it to a file named `openai_key.txt` in the repository root:

   ```bash
   echo your_api_key > openai_key.txt
   ```

Both the CLI tools and the API server automatically read the key from these locations when they start.

### Run Locally

1. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the local API server (add `-b` to run in the background):

   ```bash
  python "OK workspaces/main.py"    # foreground
  python "OK workspaces/main.py" -b # background
  python __main__.py -b              # same as above via module entry
  ```

   The server logs each conversation to `conversation.log` so you can read back the dialogue later.

   A health check endpoint is available at `http://localhost:8080/health`.
   Load balancers can poll this URL to verify the service is running.

3. Open `index.html` in your browser. The page will communicate with the server running on `localhost:8080`.

### Command Line Chat
If you prefer to talk to Hecate directly in your terminal, run the small CLI utility:

```bash
python "OK workspaces/cli.py"
```

Type your message and press Enter to receive a response. Use `quit` or `exit` to leave the session.
You can also enable speech-to-text input with the `--voice` flag (requires a microphone and PyAudio):

```bash
python "OK workspaces/cli.py" --voice
```

To hear the responses spoken aloud, add the `--speak` flag (requires pyttsx3):

```bash
python "OK workspaces/cli.py" --speak
```

For a minimal text-only chat that simply prints each response on the screen, you can run:

```bash
python screen_chat.py
```
Add `--speak` to also vocalize the output with `espeak` if available.

### Gmail Integration
Set the following environment variables so Hecate can send and receive email via Gmail:

```bash
export GMAIL_USER=your_address@gmail.com
export GMAIL_PASS=your_app_password
```

Use the commands `email:recipient|subject|body` to send an email and `inbox:n` to read your latest `n` emails.

### File Utilities
Use `retrieve:url|filename` to download a remote file into the `scripts/` folder.
Use `create:filename|content` to create a file with optional content.
Use `move:src|dest` to move or rename files within the `scripts/` folder.
Use `list` to view files saved in `scripts/`.
Use `read:filename` to display a file's contents.
Use `delete:filename` to remove a file.

### Location Tagging
Capture your current browser location and email it using the command format `location:lat|lon|recipient`.
The web interface provides buttons to fetch your coordinates and send them via email.

You can configure an emergency contact by setting the environment variable `DISTRESS_EMAIL`.
If your location has been tagged and you type **"Alika in distress"**, Hecate will
email the saved location to this address.
Hecate also listens for certain distress phrases such as "help", "help me", "I'm scared",
"I'll call my dad", "stop it now", and "leave me alone". Saying or typing any of these will
trigger the same emergency email with your tagged location.

### Running from a zipped archive
You can bundle Hecate into a single executable zip using Python's `zipapp` module. First make sure `__main__.py` is present (it runs the server). Create the archive:

```bash
python -m zipapp . -p '/usr/bin/env python3' -o hecate.pyz
```

Run it with:

```bash
python hecate.pyz          # foreground
python hecate.pyz -b       # background
```

This will start the API server directly from the zip file.

### Self Repair and Improvement
Use `selfrepair:description` to attempt an automated fix of Hecate's own code based on the issue description. Similarly, `selfimprove:suggestion` asks Hecate to refactor itself with the provided suggestion. Both commands rely on your OpenAI API key and create a `.bak` backup of the current source before overwriting it if successful.

### Self Improvement Lattice
Hecate tracks ongoing improvements in a simple lattice stored in `lattice.json`.
Use these commands to manage it:

```
lattice:show                     # display all improvement tasks
lattice:add:category|task        # add a new task under a category
lattice:complete:category|n      # mark task number n as done
lattice:reset                    # restore the default lattice
```

### Antivirus Scanning
Run `antivirus.py` to periodically scan the `scripts/` directory for infected files using `clamscan`. The script also attempts to keep the ClamAV virus definitions up to date by calling `freshclam` at regular intervals. Any detected threats are moved to the `quarantine/` folder. Ensure both `clamscan` and `freshclam` are installed so the scan and updates can run successfully.

### MandemOS Database
Run `python setup_database.py` to create a SQLite database named `mandemos.db` with tables for scrolls, relics, keys, and keyword usage statistics.

Once the database exists, you can populate it with the metadata from `metadata.json` using `insert_metadata.py`:

```bash
python insert_metadata.py
```

This inserts the scroll information from `metadata.json` into the `scrolls` table.

