# Multi-Agent System Generator

Automatically generate complete multi-agent systems from natural language specifications using the Claude API.

## Features

✨ **Spec-to-Code**: Write what you want in plain English, get a complete working system  
🐳 **Docker-First**: All systems are containerized with docker-compose  
🔄 **Iterative**: Make changes to existing systems with simple commands  
📁 **Complete**: Generates all files - Dockerfiles, scripts, configs, READMEs  
🚀 **Auto-Execute**: Optionally start your system immediately after generation

## Installation

```bash
# Install required packages
pip install anthropic

# Set your API key
# export ANTHROPIC_API_KEY='your-api-key-here'
```

## Quick Start

### Method 1: Command Line with Inline Spec

```bash
python multi_agent_generator.py "Create a 2-agent system with rabbitmq and a Python worker that processes jobs"
```

### Method 2: Command Line with Spec File

```bash
python multi_agent_generator.py @examples/rabbitmq_spec.txt
```

### Method 3: Python Script

```python
from multi_agent_generator import MultiAgentGenerator

generator = MultiAgentGenerator()

spec = """
Agent 1: MongoDB database on port 27017
Agent 2: Python script that inserts 100 random documents every 5 seconds
Agent 3: Python script that queries and prints document count every 10 seconds
"""

files = generator.generate_system(spec, output_dir="./my-system")
```

## Usage Examples

### Basic Generation

```bash
python multi_agent_generator.py "Create a simple web scraper agent system" -o ./scraper-system
```

### Generate and Auto-Execute

```bash
python multi_agent_generator.py @my_spec.txt --execute
```

### Custom Output Directory

```bash
python multi_agent_generator.py "Your spec here" -o /path/to/output
```

### Iterate on Existing System

```bash
# First, generate the system
python multi_agent_generator.py @examples/rabbitmq_spec.txt -o ./my-system

# Then, modify it
python multi_agent_generator.py @examples/rabbitmq_spec.txt \
  --iterate "Add a fourth agent that logs all messages to a file" \
  -o ./my-system
```

## Example Specifications

### RabbitMQ Message Queue System

```
Agent 1: RabbitMQ broker with exchange 'tasks' and queue 'work_queue'
Agent 2: Python publisher that sends 10 messages per second
Agent 3: Python consumer that processes messages and logs them
```

### Redis Cache with Workers

```
Agent 1: Redis server on default port
Agent 2: Python producer that adds jobs to Redis queue every 3 seconds
Agent 3: Python worker that processes jobs from the queue
Agent 4: Python monitor that displays queue statistics every 10 seconds
```

### Database + API System

```
Agent 1: MySQL database with 'app' database and 'users' table
Agent 2: Python FastAPI service with CRUD endpoints on port 8000
Agent 3: Python script that creates test users every 5 seconds
```
### Multi agent to publish/consume from rabbimtq about books, influx database that monitors the rabbitmq metrics and graphana dashboard

```
# Generate the complete 5-agent monitoring system
python multi_agent_generator.py @examples/monitoring_system_spec.txt -o ./monitoring-system

# Run it
cd monitoring-system
docker-compose up --build
```


## Command Line Options

```
usage: multi_agent_generator.py [-h] [-o OUTPUT] [-k API_KEY] [--execute] [--iterate ITERATE] spec

Generate multi-agent systems from specifications using Claude API

positional arguments:
  spec                  Specification text or path to spec file (prefix with @ for file)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: ./generated-system)
  -k API_KEY, --api-key API_KEY
                        Anthropic API key (or set ANTHROPIC_API_KEY env var)
  --execute             Automatically run docker-compose up after generation
  --iterate ITERATE     Modification to make to existing system
```

## Programmatic Usage

### Basic Generation

```python
from multi_agent_generator import MultiAgentGenerator

generator = MultiAgentGenerator(api_key="your-key")

spec = """
Create a monitoring system:
- Agent 1: Prometheus
- Agent 2: Python exporter that exposes metrics
- Agent 3: Grafana for visualization
"""

files = generator.generate_system(
    spec=spec,
    output_dir="./monitoring-system",
    auto_execute=False
)

print(f"Generated {len(files)} files")
```

### Iterative Development

```python
generator = MultiAgentGenerator()

# Initial generation
spec = "Agent 1: PostgreSQL, Agent 2: Python API"
files = generator.generate_system(spec, output_dir="./app")

# Add a feature
files = generator.iterate_on_system(
    spec=spec,
    modification="Add authentication with JWT tokens",
    existing_files=files,
    output_dir="./app"
)

# Add another feature
files = generator.iterate_on_system(
    spec=spec,
    modification="Add rate limiting with Redis",
    existing_files=files,
    output_dir="./app"
)
```

### Load Spec from File

```python
from multi_agent_generator import MultiAgentGenerator, load_spec_from_file

spec = load_spec_from_file("./specs/my_system.txt")
generator = MultiAgentGenerator()
files = generator.generate_system(spec)
```

## Writing Good Specifications

### ✅ Good Specifications

**Be specific about:**
- Number of agents
- Technology stack (Python, Node.js, etc.)
- Ports and networking
- Data formats and schemas
- Timing/intervals for periodic tasks
- Dependencies between agents

**Example:**
```
Agent 1: RabbitMQ on port 5672 with exchange 'logs' (topic type)
Agent 2: Python script using pika library, publishes JSON logs every 5s
Agent 3: Python consumer that filters ERROR level logs and writes to file
Message format: {"level": "INFO", "message": "text", "timestamp": "ISO8601"}
```

### ❌ Avoid Vague Specifications

```
Make a messaging system
```

This is too vague - what kind of messages? How many agents? What technology?

## Output Structure

Generated systems typically have this structure:

```
generated-system/
├── README.md                 # Complete documentation
├── docker-compose.yml        # Orchestration file
├── start.sh                  # Quick start script
├── agent1/
│   ├── Dockerfile
│   └── script.py
├── agent2/
│   ├── Dockerfile
│   └── script.py
└── agent3/
    ├── Dockerfile
    └── script.py
```

## Tips & Tricks

### 1. Start Simple, Then Iterate

```bash
# Generate basic system
python multi_agent_generator.py "2 agents: Redis and Python worker"

# Add complexity
python multi_agent_generator.py "..." \
  --iterate "Add monitoring with Prometheus"
```

### 2. Use Spec Files for Complex Systems

Create a `my_spec.txt` file with your full specification, then:

```bash
python multi_agent_generator.py @my_spec.txt
```

### 3. Review Generated Files Before Running

```bash
python multi_agent_generator.py @spec.txt -o ./review-me
# Check the files
cd review-me && cat README.md
# Then run
docker-compose up
```

### 4. Specify Data Formats Explicitly

Include JSON schemas or example data in your spec:

```
Message format:
{
  "id": "uuid",
  "type": "user_action",
  "data": {...}
}
```

## Troubleshooting

**No files generated:**
- Check your API key is valid
- Ensure spec is detailed enough
- Check API response in error message

**Generated system doesn't work:**
- Review the README.md in generated directory
- Check docker-compose logs
- Try iterating with more specific requirements

**API key errors:**
```bash
export ANTHROPIC_API_KEY='your-key'
# or
python multi_agent_generator.py --api-key your-key "spec"
```

## New: Staged Multi-Agent Generator (multi_agent_generator_staged.py)

This repository includes an improved "staged" multi-agent system generator that avoids token limits by generating files in multiple passes and can optionally download raw assistant responses for audit/debugging.

Highlights
- Staged generation: manifest → grouped/batched file generation → per-file fallback → final verification.
- Batched requests to the LLM keep prompts smaller and make generation more robust.
- Optional download of the raw Claude responses for each generated file, useful for auditing and re-running generation.
- Tracks estimated token usage and approximate cost.

How it works (high level)
1. Phase 1 — Manifest: The tool reads your specification and asks the model to return a JSON array of all files to generate.
2. Phase 2 — Grouped generation: Files are grouped (infrastructure, publishers, consumers, config, etc.) and generated in small batches to avoid token truncation.
3. Phase 3 — Fallback & verification: Any missing files are generated individually using available context; finally all files are written to disk.
4. Optional — Download responses: If enabled, the raw model responses used to create each file are saved for inspection.

CLI usage examples
- Basic generation:
  ```
  python3 multi_agent_generator_staged.py @spec.txt -o ./generated-system
  ```

- With explicit API key (or set env var ANTHROPIC_API_KEY):
  ```
  python3 multi_agent_generator_staged.py @spec.txt -o ./generated-system --api-key $ANTHROPIC_API_KEY
  ```

- Enable saving raw model responses (new flag):
  ```
  python3 multi_agent_generator_staged.py @spec.txt -o ./generated-system --download-responses
  ```

Note: The `@` prefix reads the spec from a file (e.g., `@spec.txt`).

Output layout and downloaded responses
- Project files are written to the output directory (default: `./generated-system`).
- If response download is enabled, raw model responses are stored under:
  - `./generated-system/claude-responses/` — one file per model call (JSON or .txt), named for the phase and target (e.g. `manifest.json`, `batch-infra-1.json`, `single-file-<sanitized-path>.txt`).
- Generated files and raw responses can be used together to reproduce or debug generation decisions.

Spec best practices
- Provide a clear, focused specification. The generator estimates tokens and will split work into batches, but concise specs make generation more reliable.
- If you need the tool to include additional files (configs, Dockerfiles, etc.), list them in the spec or in an explicit "files" section.

Environment & costs
- Set ANTHROPIC_API_KEY in your environment or pass `--api-key`.
- The generator reports estimated token usage and an approximate cost summary when finished. Monitor usage if you have a budget.

Troubleshooting
- Failure to parse manifest: ensure the spec prompts the model to return a pure JSON array of file paths.
- Missing files after generation: Run again with `--download-responses` to inspect the model outputs and re-run individual file generation as needed.
- Permission/file system errors: ensure the output directory is writable.

Security & auditing
- Downloaded model responses allow you to audit the exact text the model returned. Treat these artifacts as potentially sensitive (they may contain spec text or generated secrets).
- Rotate and secure API keys; do not commit downloaded responses or API keys to source control.

Examples and next steps
- Start with a small spec that requests only a few files, verify the outputs, then expand the spec to generate the full system.
- Use the response files to iterate on prompts or to seed local tests that validate generated code.

## Using both generators: original and staged

This repo provides two generator entry points:

- multi_agent_generator.py — single-call generator that asks Claude for the full project in one response (good for smaller specs).
- multi_agent_generator_staged.py — staged/iterative generator that builds a manifest, generates files in batches, falls back to single-file generation, and can optionally save raw model responses for auditing.

Quick CLI examples

- Original (single-call):
```
python multi_agent_generator.py @spec.txt -o ./generated-system --execute
```

- Staged (batched generation, save raw responses):
```
python3 multi_agent_generator_staged.py @spec.txt -o ./generated-system --download-responses
```

Programmatic usage examples

- Using the original generator (multi_agent_generator.py):
```python
from multi_agent_generator import MultiAgentGenerator

gen = MultiAgentGenerator(api_key="YOUR_KEY")
spec = "Two agents: RabbitMQ broker and a Python worker that processes jobs."
files = gen.generate_system(spec, output_dir="./out-single")
print(f"Generated {len(files)} files")
```

- Using the staged generator (multi_agent_generator_staged.py):
```python
from multi_agent_generator_staged import ImprovedMultiAgentGenerator

gen = ImprovedMultiAgentGenerator(api_key="YOUR_KEY")
spec = "Three agents: broker, publisher, consumer. Include monitoring stack."
files = gen.generate_system(spec, output_dir="./out-staged")
# If using CLI --download-responses, raw model responses are saved under ./out-staged/claude-responses/
print(f"Generated {len(files)} files (staged)")
```

Notes
- Pick the single-call generator for short, well-bounded specs. Use the staged generator for larger systems or when token limits/errors become a concern.
- The staged generator's downloaded responses (when enabled) are useful for debugging parsing failures or iterating on prompts.

## Contributing

Feel free to extend this tool! Some ideas:

- Add support for Kubernetes manifests
- Generate tests automatically
- Add CI/CD pipeline generation
- Support for more languages (Go, Rust, etc.)

## License

MIT License - feel free to use and modify!

## API Costs

Using Claude API costs money. Approximate costs:
- Simple system (2-3 agents): ~$0.10-0.30
- Complex system (5+ agents): ~$0.50-1.00
- Iteration: ~$0.10-0.50

Check current pricing at https://www.anthropic.com/pricing
