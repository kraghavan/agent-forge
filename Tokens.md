# Understanding Tokens in Agent-Forge Requests

## What is a Token?

A token is roughly a "piece" of a word. Here's how text breaks into tokens:

```
TEXT:    "Hello, how are you doing today?"
TOKENS:  ["Hello", ",", " how", " are", " you", " doing", " today", "?"]
COUNT:   8 tokens
```

**Rule of thumb:**
- 1 token ≈ 4 characters in English
- 1 token ≈ 0.75 words
- 100 tokens ≈ 75 words

## Your Request Has THREE Parts

When you call the API, tokens are counted from ALL of these:

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR API REQUEST                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. SYSTEM PROMPT (Claude's instructions)              │
│     - Size: ~20,000 tokens                             │
│     - You don't write this, Anthropic does             │
│     - Tells me how to behave                           │
│                                                         │
│  2. YOUR PROMPT (your spec + generator instructions)   │
│     - Size: Variable (500-5,000 tokens)                │
│     - Your spec file content                           │
│     - Generator's template instructions                │
│                                                         │
│  3. MY RESPONSE (generated code/files)                 │
│     - Size: Variable (3,000-16,000 tokens)             │
│     - All the code I generate                          │
│     - Based on max_tokens setting                      │
│                                                         │
└─────────────────────────────────────────────────────────┘

TOTAL TOKENS = Part 1 + Part 2 + Part 3
```

## Visual Breakdown of YOUR Specific Request

Let me show you what happens when you run:

```python
python multi_agent_generator.py @monitoring-system-spec.txt
```

### Step 1: Input Tokens (What Goes IN)

```
┌──────────────────────────────────────────────────────────────┐
│                      INPUT TOKENS                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [SYSTEM PROMPT - Hidden from you]                          │
│  ┌────────────────────────────────────────┐                 │
│  │ You are Claude, created by Anthropic   │                 │
│  │ When generating multi-agent systems... │                 │
│  │ Follow best practices for Docker...    │                 │
│  │ ... (continues for 20,000 tokens)      │                 │
│  └────────────────────────────────────────┘                 │
│  Tokens: ~20,000                                             │
│                                                              │
│  [YOUR GENERATOR'S TEMPLATE]                                 │
│  ┌────────────────────────────────────────┐                 │
│  │ I need you to generate a complete      │                 │
│  │ multi-agent system based on the        │                 │
│  │ following specification.               │                 │
│  │                                        │                 │
│  │ REQUIREMENTS:                          │                 │
│  │ 1. Generate ALL necessary files...     │                 │
│  │ 2. For each file, use this EXACT...    │                 │
│  │ ... (continues)                        │                 │
│  └────────────────────────────────────────┘                 │
│  Tokens: ~1,500                                              │
│                                                              │
│  [YOUR SPEC FILE CONTENT]                                    │
│  ┌────────────────────────────────────────┐                 │
│  │ Agent 1 will create a docker           │                 │
│  │ container running RabbitMQ...          │                 │
│  │                                        │                 │
│  │ Agent 2 is a normal ubuntu 20...       │                 │
│  │ ... (your full spec)                   │                 │
│  └────────────────────────────────────────┘                 │
│  Tokens: ~1,800 (for monitoring-system-spec.txt)            │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  TOTAL INPUT TOKENS: ~23,300                                 │
└──────────────────────────────────────────────────────────────┘
```

### Step 2: Output Tokens (What I Generate)

```
┌──────────────────────────────────────────────────────────────┐
│                     OUTPUT TOKENS                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [GENERATED CODE - What I create]                            │
│                                                              │
│  File 1: docker-compose.yml                                  │
│  ┌────────────────────────────────────────┐                 │
│  │ version: '3.8'                         │                 │
│  │ services:                              │                 │
│  │   rabbitmq:                            │                 │
│  │     image: rabbitmq:3-management       │                 │
│  │     ...                                │                 │
│  └────────────────────────────────────────┘                 │
│  Tokens: ~800                                                │
│                                                              │
│  File 2: publisher/publisher.py                              │
│  ┌────────────────────────────────────────┐                 │
│  │ import pika                            │                 │
│  │ import json                            │                 │
│  │ from influxdb_client import...        │                 │
│  │ ... (full script ~200 lines)           │                 │
│  └────────────────────────────────────────┘                 │
│  Tokens: ~2,500                                              │
│                                                              │
│  File 3: consumer/consumer.py                                │
│  Tokens: ~2,500                                              │
│                                                              │
│  File 4: setup-influxdb.py                                   │
│  Tokens: ~1,200                                              │
│                                                              │
│  File 5: setup-rabbitmq.py                                   │
│  Tokens: ~800                                                │
│                                                              │
│  File 6: publisher/Dockerfile                                │
│  Tokens: ~150                                                │
│                                                              │
│  File 7: consumer/Dockerfile                                 │
│  Tokens: ~150                                                │
│                                                              │
│  File 8: grafana/dashboards/overview.json                    │
│  Tokens: ~2,000                                              │
│                                                              │
│  File 9: README.md                                           │
│  Tokens: ~1,500                                              │
│                                                              │
│  File 10: start.sh                                           │
│  Tokens: ~200                                                │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  TOTAL OUTPUT TOKENS: ~11,800                                │
│  (Limited by max_tokens=16000)                               │
└──────────────────────────────────────────────────────────────┘
```

### Step 3: Total Token Usage

```
┌──────────────────────────────────────────────────────────────┐
│                  COMPLETE REQUEST BREAKDOWN                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  INPUT TOKENS:  23,300 tokens                                │
│  OUTPUT TOKENS: 11,800 tokens                                │
│  ─────────────────────────────────                           │
│  TOTAL:         35,100 tokens                                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## How Anthropic Charges You

```
┌─────────────────────────────────────────────────────────┐
│                    PRICING BREAKDOWN                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Model: claude-sonnet-4-5-20250929                      │
│                                                         │
│  INPUT PRICING:  $3 per million tokens                  │
│  OUTPUT PRICING: $15 per million tokens                 │
│                                                         │
│  YOUR REQUEST:                                          │
│  ┌───────────────────────────────────────────┐          │
│  │ Input:  23,300 tokens × $3/M  = $0.07     │          │
│  │ Output: 11,800 tokens × $15/M = $0.18     │          │
│  │ ─────────────────────────────────────     │          │
│  │ TOTAL COST: $0.25                         │          │
│  └───────────────────────────────────────────┘          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Flow Diagram: Token Journey

```
START
  │
  ▼
┌─────────────────────────────────────────┐
│ You run: python multi_agent_generator.py│
│         @monitoring-system-spec.txt     │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ Generator reads your spec file          │
│ Size: 1,800 tokens                      │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ Generator builds prompt with template   │
│ + 1,500 tokens (instructions)           │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ Send to Anthropic API                   │
│ Input: 3,300 tokens (your part)         │
│      + 20,000 tokens (system prompt)    │
│ = 23,300 input tokens                   │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ Claude generates response               │
│ Token by token until complete           │
│ Limited by max_tokens=16,000            │
│                                         │
│ Token 1:    "```"                       │
│ Token 2:    "filename"                  │
│ Token 3:    ":"                         │
│ ...                                     │
│ Token 11800: "```"                      │
│                                         │
│ Output: 11,800 tokens generated         │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ Response sent back to you               │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ API response includes usage stats:      │
│ {                                       │
│   "usage": {                            │
│     "input_tokens": 23300,              │
│     "output_tokens": 11800              │
│   }                                     │
│ }                                       │
└─────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────┐
│ Your script parses files and writes     │
│ them to disk                            │
└─────────────────────────────────────────┘
  │
  ▼
END
```

## How to Calculate Tokens for YOUR Specs

### Method 1: Rough Estimation

```python
def estimate_tokens(text):
    """
    Quick estimation:
    - 1 token ≈ 4 characters
    - 1 token ≈ 0.75 words
    """
    char_count = len(text)
    word_count = len(text.split())
    
    estimate_from_chars = char_count / 4
    estimate_from_words = word_count / 0.75
    
    # Average them
    return int((estimate_from_chars + estimate_from_words) / 2)

# Example
spec = open('monitoring-system-spec.txt').read()
print(f"Estimated tokens: {estimate_tokens(spec)}")
# Output: ~1,800 tokens
```

### Method 2: Actual API Response

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    messages=[{"role": "user", "content": spec}]
)

# Check actual usage
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Total cost: ${calculate_cost(response.usage)}")
```

### Method 3: Use Anthropic's Tokenizer

```python
import anthropic

# Official way to count tokens
client = anthropic.Anthropic(api_key="...")

# Count tokens before sending
token_count = client.count_tokens(text)
print(f"This text is {token_count} tokens")
```

## Size Comparison Chart

```
Request Type          Input Tokens    Output Tokens    Total      Cost
───────────────────────────────────────────────────────────────────────
Simple (2 agents)     ~21,500         ~3,000          ~24,500    $0.11
Medium (3-4 agents)   ~22,500         ~8,000          ~30,500    $0.19  
Complex (5+ agents)   ~23,500         ~12,000         ~35,500    $0.25
Iteration (small)     ~25,000         ~2,000          ~27,000    $0.11
Iteration (large)     ~30,000         ~5,000          ~35,000    $0.18

Legend:
  Input  = System prompt + Your prompt + (Previous conversation if iterating)
  Output = Generated code
  Cost   = Input×$3/M + Output×$15/M (for Sonnet 4.5)
```

## Visual: Where Tokens Are REALLY Used

```
                    YOUR REQUEST TOKEN BREAKDOWN

    ┌────────────────────────────────────────────────────┐
    │                  TOTAL: ~35,000 tokens              │
    ├────────────────────────────────────────────────────┤
    │                                                    │
    │  ████████████████████ 57% System Prompt (20k)      │
    │  Hidden from you, set by Anthropic                 │
    │                                                    │
    │  ███ 9% Your Instructions (3.3k)                   │
    │  Template + your spec file                         │
    │                                                    │
    │  ████████████████ 34% My Response (11.8k)          │
    │  All the generated code                            │
    │                                                    │
    └────────────────────────────────────────────────────┘

    COST BREAKDOWN:

    ┌────────────────────────────────────────────────────┐
    │  Input (23.3k):   $0.07  ▓▓▓░░░░░░░ 28%            │
    │  Output (11.8k):  $0.18  ▓▓▓▓▓▓▓▓░░ 72%            │
    │  ─────────────────────────────────────             │
    │  Total:           $0.25                            │
    └────────────────────────────────────────────────────┘

    KEY INSIGHT: Output tokens cost 5× more than input!
```

## Optimization Tips

### 1. Reduce Input Tokens
```python
# Before (verbose)
spec = """
Agent 1 will be responsible for creating a docker container.
Inside this container, it will run RabbitMQ...
"""
# Tokens: ~2,000

# After (concise)  
spec = """
Agent 1: RabbitMQ in Docker on port 5672
Exchange: books (direct), Queues: fictional, non-fictional
"""
# Tokens: ~800

SAVINGS: 1,200 tokens = $0.004 per request
```

### 2. Reduce Output Tokens
```python
# Use smaller max_tokens for simple tasks
max_tokens=8000   # Instead of 16000
# Saves: Up to 8,000 tokens × $15/M = $0.12 per request
```

### 3. Batch Multiple Changes
```python
# Bad: 3 separate requests
generate("basic system")           # 35k tokens
iterate("add logging")             # 38k tokens  
iterate("add monitoring")          # 40k tokens
# Total: 113k tokens = $0.75

# Good: 1 request
generate("system with logging and monitoring")
# Total: 38k tokens = $0.26

SAVINGS: $0.49
```

## Add Token Tracking to Your Generator

```python
class MultiAgentGenerator:
    def generate_system(self, spec, output_dir):
        print("🤖 Generating multi-agent system...")
        
        # Estimate before
        estimated = len(spec) / 4
        print(f"📊 Estimated input: ~{estimated:.0f} tokens")
        
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=16000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Actual usage
        usage = response.usage
        total = usage.input_tokens + usage.output_tokens
        cost = (usage.input_tokens * 3 + usage.output_tokens * 15) / 1_000_000
        
        print(f"📊 Token Usage:")
        print(f"   Input:  {usage.input_tokens:,} tokens")
        print(f"   Output: {usage.output_tokens:,} tokens")
        print(f"   Total:  {total:,} tokens")
        print(f"   Cost:   ${cost:.3f}")
        
        return self._parse_files_from_response(response.content[0].text)
```

## Summary: The Math

```
SIMPLE FORMULA:

Total Tokens = System Prompt + Your Prompt + Generated Response
             = 20,000       + (Template + Spec) + Output
             = 20,000       + 3,300             + 11,800
             = 35,100 tokens

Total Cost = (Input Tokens × $3/M) + (Output Tokens × $15/M)
           = (23,300 × $3/M) + (11,800 × $15/M)
           = $0.07 + $0.18
           = $0.25

WHERE:
- System Prompt = Fixed by Anthropic (~20k tokens)
- Your Prompt = Template (1.5k) + Spec file (variable)
- Output = What I generate (limited by max_tokens)
- Input Tokens = System + Your prompt
- Output Tokens = My response
```

# Token Tracking Output Example

When you run your generator now, you'll see output like this:

## Example 1: Simple System Generation

```bash
$ python multi_agent_generator.py @examples/rabbitmq_spec.txt -o ./demo-system
```

**Output:**
```
🤖 Generating multi-agent system using Claude API...
📝 Spec length: 847 characters
📊 Estimated spec tokens: ~211

============================================================
📊 TOKEN USAGE REPORT
============================================================
⏱️  Generation time:    45.3 seconds
📥 Input tokens:        21,456
📤 Output tokens:       8,234
📊 Total tokens:        29,690
💰 Input cost:          $0.0644
💰 Output cost:         $0.1235
💵 Total cost:          $0.1879
============================================================

  ✓ docker-compose.yml
  ✓ setup-rabbitmq.py
  ✓ publisher/Dockerfile
  ✓ publisher/publisher.py
  ✓ consumer/Dockerfile
  ✓ consumer/consumer.py
  ✓ README.md
  ✓ start.sh

✅ Generated 8 files in ./demo-system/
```

## Example 2: Complex System (Monitoring)

```bash
$ python multi_agent_generator.py @monitoring-system-spec.txt -o ./monitoring
```

**Output:**
```
🤖 Generating multi-agent system using Claude API...
📝 Spec length: 2,143 characters
📊 Estimated spec tokens: ~535

============================================================
📊 TOKEN USAGE REPORT
============================================================
⏱️  Generation time:    127.8 seconds
📥 Input tokens:        23,567
📤 Output tokens:       14,892
📊 Total tokens:        38,459
💰 Input cost:          $0.0707
💰 Output cost:         $0.2234
💵 Total cost:          $0.2941
============================================================

  ✓ docker-compose.yml
  ✓ setup-influxdb.py
  ✓ setup-rabbitmq.py
  ✓ publisher/Dockerfile
  ✓ publisher/publisher.py
  ✓ consumer/Dockerfile
  ✓ consumer/consumer.py
  ✓ grafana/dashboards/overview.json
  ✓ grafana/provisioning/datasources/influxdb.yml
  ✓ README.md
  ✓ start.sh

✅ Generated 11 files in ./monitoring/
```

## Example 3: Iteration (Adding Feature)

```bash
$ python multi_agent_generator.py @rabbitmq_spec.txt \
    --iterate "Add logging to files for all agents" \
    -o ./demo-system
```

**Output:**
```
🔄 Iterating on system: Add logging to files for all agents

============================================================
📊 ITERATION TOKEN USAGE REPORT
============================================================
⏱️  Generation time:    52.1 seconds
📥 Input tokens:        28,934
📤 Output tokens:       5,123
📊 Total tokens:        34,057
💰 Input cost:          $0.0868
💰 Output cost:         $0.0768
💵 Total cost:          $0.1636
============================================================

  ✓ publisher/publisher.py
  ✓ consumer/consumer.py
  ✓ docker-compose.yml

✅ Updated 3 files
```

## What Each Field Means

- **⏱️ Generation time:** How long the API call took
- **📥 Input tokens:** System prompt + your spec + template
- **📤 Output tokens:** Generated code
- **📊 Total tokens:** Input + Output
- **💰 Input cost:** Input tokens × $3 per million
- **💰 Output cost:** Output tokens × $15 per million
- **💵 Total cost:** Total amount charged for this request

## Tracking Costs Over Time

You can keep a log:

```bash
# Run multiple generations and track
python multi_agent_generator.py @spec1.txt >> costs.log 2>&1
python multi_agent_generator.py @spec2.txt >> costs.log 2>&1
python multi_agent_generator.py @spec3.txt >> costs.log 2>&1

# Then analyze
grep "Total cost" costs.log
# Output:
# 💵 Total cost:          $0.1879
# 💵 Total cost:          $0.2941
# 💵 Total cost:          $0.1636
# Total: ~$0.65
```

## Budget Planning

Based on typical usage:

| Activity | Tokens | Cost | Frequency | Monthly Cost |
|----------|--------|------|-----------|--------------|
| Initial generation | ~30k | $0.20 | 5/month | $1.00 |
| Iterations | ~35k | $0.18 | 10/month | $1.80 |
| Testing/experiments | ~25k | $0.15 | 20/month | $3.00 |
| **Total** | - | - | - | **~$5.80/month** |

For active development, expect $5-15/month depending on how much you iterate.