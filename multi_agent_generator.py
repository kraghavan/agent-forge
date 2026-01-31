#!/usr/bin/env python3
"""
Multi-Agent System Generator
Automatically generates complete multi-agent systems from natural language specifications
using the Claude API.
"""

import anthropic
import os
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse


class MultiAgentGenerator:
    """Generate multi-agent systems from specifications using Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the generator
        
        Args:
            api_key: Anthropic API key. If not provided, will try to get from ANTHROPIC_API_KEY env var
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter"
            )
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
    def generate_system(
        self, 
        spec: str, 
        output_dir: str = "./generated-system",
        auto_execute: bool = False
    ) -> Dict[str, str]:
        """
        Generate a complete multi-agent system from a specification
        
        Args:
            spec: Natural language specification of the system
            output_dir: Directory to write generated files
            auto_execute: Whether to automatically run docker-compose up after generation
            
        Returns:
            Dictionary mapping file paths to their contents
        """
        print("🤖 Generating multi-agent system using Claude API...")
        print(f"📝 Spec length: {len(spec)} characters")
        
        # Estimate input tokens
        estimated_spec_tokens = len(spec) // 4  # ~4 chars per token
        print(f"📊 Estimated spec tokens: ~{estimated_spec_tokens:,}")
        print()
        
        # Create the prompt for Claude
        prompt = self._build_generation_prompt(spec)
        
        # Call Claude API
        import time
        start_time = time.time()
        
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=16000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        elapsed_time = time.time() - start_time
        
        # Print token usage statistics
        usage = response.usage
        total_tokens = usage.input_tokens + usage.output_tokens
        
        # Calculate cost (Sonnet 4.5 pricing as of Jan 2026)
        input_cost = (usage.input_tokens / 1_000_000) * 3.00   # $3 per million input tokens
        output_cost = (usage.output_tokens / 1_000_000) * 15.00  # $15 per million output tokens
        total_cost = input_cost + output_cost
        
        print("\n" + "="*60)
        print("📊 TOKEN USAGE REPORT")
        print("="*60)
        print(f"⏱️  Generation time:    {elapsed_time:.1f} seconds")
        print(f"📥 Input tokens:        {usage.input_tokens:,}")
        print(f"📤 Output tokens:       {usage.output_tokens:,}")
        print(f"📊 Total tokens:        {total_tokens:,}")
        print(f"💰 Input cost:          ${input_cost:.4f}")
        print(f"💰 Output cost:         ${output_cost:.4f}")
        print(f"💵 Total cost:          ${total_cost:.4f}")
        print("="*60)
        print()
        
        # Extract generated content
        content = response.content[0].text
        
        # Parse files from Claude's response
        files = self._parse_files_from_response(content)
        
        if not files:
            print("⚠️  Warning: No files were generated. Response was:")
            print(content)
            return {}
        
        # Write files to disk
        self._write_files(files, output_dir)
        
        print(f"✅ Generated {len(files)} files in {output_dir}/")
        
        # Auto-execute if requested
        if auto_execute:
            self._execute_system(output_dir)
        
        return files
    
    def _build_generation_prompt(self, spec: str) -> str:
        """Build the prompt for Claude to generate the system"""
        return f"""I need you to generate a complete multi-agent system based on the following specification.

SPECIFICATION:
{spec}

REQUIREMENTS:
1. Generate ALL necessary files including:
   - docker-compose.yml
   - Dockerfiles for each agent
   - Python scripts for each agent
   - Any initialization scripts needed
   - A README.md with instructions
   - A start.sh script for easy execution

2. For each file, use this EXACT format:
   ```filename: path/to/file.ext
   [file contents here]
   ```

3. Ensure proper directory structure (e.g., agent1/Dockerfile, agent2/script.py)

4. Include proper error handling, logging, and health checks

5. Make sure dependencies are properly ordered (use depends_on with conditions)

6. Follow best practices for Docker, Python, and the technologies specified

IMPORTANT FOR RABBITMQ SYSTEMS:
- If the system uses RabbitMQ, DO NOT use rabbitmqadmin for setup
- Instead, create a Python script that uses the pika library to create exchanges and queues
- The setup script should have proper retry logic (wait up to 60 seconds for RabbitMQ)
- Use a python:3.9-slim container for the setup, not the rabbitmq image
- Example setup service in docker-compose:
  ```yaml
  rabbitmq-setup:
    image: python:3.9-slim
    volumes:
      - ./setup-rabbitmq.py:/setup.py
    command: bash -c "pip install pika --quiet && python /setup.py"
  ```

Please generate the complete system now. Remember to use the exact format with ```filename: path``` for each file."""

    def _parse_files_from_response(self, content: str) -> Dict[str, str]:
        """
        Parse files from Claude's response
        
        Expected format:
        ```filename: path/to/file.ext
        file contents
        ```
        """
        files = {}
        
        # Pattern to match code blocks with filename
        pattern = r'```(?:filename:\s*)?([^\n]+)\n(.*?)```'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            filepath = match.group(1).strip()
            file_content = match.group(2).strip()
            
            # Skip language identifiers like 'python', 'yaml', etc.
            if filepath.lower() in ['python', 'yaml', 'yml', 'bash', 'sh', 'dockerfile', 'json', 'markdown', 'md']:
                continue
            
            # Clean up the filepath
            filepath = filepath.replace('filename:', '').strip()
            
            files[filepath] = file_content
        
        return files
    
    def _write_files(self, files: Dict[str, str], output_dir: str, clean: bool = False):
        """Write generated files to disk"""
        output_path = Path(output_dir)
        
        # Optionally clean the directory first
        if clean and output_path.exists():
            import shutil
            shutil.rmtree(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for filepath, content in files.items():
            full_path = output_path / filepath
            
            # Create parent directories if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the file
            full_path.write_text(content)
            
            # Make .sh files executable
            if filepath.endswith('.sh'):
                os.chmod(full_path, 0o755)
            
            print(f"  ✓ {filepath}")
    
    def _execute_system(self, output_dir: str):
        """Execute the generated system using docker-compose"""
        import subprocess
        
        print("\n🚀 Auto-executing system...")
        
        try:
            result = subprocess.run(
                ['docker-compose', 'up', '--build'],
                cwd=output_dir,
                check=True
            )
            print("✅ System started successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error executing system: {e}")
        except FileNotFoundError:
            print("❌ docker-compose not found. Please install Docker Compose.")
    
    def iterate_on_system(
        self,
        spec: str,
        modification: str,
        existing_files: Dict[str, str],
        output_dir: str = "./generated-system"
    ) -> Dict[str, str]:
        """
        Iterate on an existing system with modifications
        
        Args:
            spec: Original specification
            modification: What to change/add
            existing_files: Current system files
            output_dir: Output directory
            
        Returns:
            Updated files dictionary
        """
        print(f"🔄 Iterating on system: {modification}")
        print()
        
        # Build iteration prompt
        files_context = "\n\n".join([
            f"FILE: {path}\n```\n{content}\n```"
            for path, content in existing_files.items()
        ])
        
        prompt = f"""I have an existing multi-agent system. Here are the current files:

{files_context}

ORIGINAL SPEC:
{spec}

MODIFICATION REQUEST:
{modification}

Please provide the UPDATED files that incorporate this modification. Only include files that changed.
Use the same format as before:
```filename: path/to/file.ext
[updated contents]
```
"""
        
        import time
        start_time = time.time()
        
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=16000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        elapsed_time = time.time() - start_time
        
        # Print token usage statistics
        usage = response.usage
        total_tokens = usage.input_tokens + usage.output_tokens
        
        # Calculate cost
        input_cost = (usage.input_tokens / 1_000_000) * 3.00
        output_cost = (usage.output_tokens / 1_000_000) * 15.00
        total_cost = input_cost + output_cost
        
        print("\n" + "="*60)
        print("📊 ITERATION TOKEN USAGE REPORT")
        print("="*60)
        print(f"⏱️  Generation time:    {elapsed_time:.1f} seconds")
        print(f"📥 Input tokens:        {usage.input_tokens:,}")
        print(f"📤 Output tokens:       {usage.output_tokens:,}")
        print(f"📊 Total tokens:        {total_tokens:,}")
        print(f"💰 Input cost:          ${input_cost:.4f}")
        print(f"💰 Output cost:         ${output_cost:.4f}")
        print(f"💵 Total cost:          ${total_cost:.4f}")
        print("="*60)
        print()
        
        content = response.content[0].text
        updated_files = self._parse_files_from_response(content)
        
        # Merge with existing files
        for filepath, content in updated_files.items():
            existing_files[filepath] = content
        
        # Write updated files
        self._write_files(updated_files, output_dir)
        
        print(f"✅ Updated {len(updated_files)} files")
        
        return existing_files


def load_spec_from_file(filepath: str) -> str:
    """Load specification from a file"""
    with open(filepath, 'r') as f:
        return f.read()


def main():
    """CLI interface for the generator"""
    parser = argparse.ArgumentParser(
        description='Generate multi-agent systems from specifications using Claude API'
    )
    parser.add_argument(
        'spec',
        help='Specification text or path to spec file (prefix with @ for file)'
    )
    parser.add_argument(
        '-o', '--output',
        default='./generated-system',
        help='Output directory (default: ./generated-system)'
    )
    parser.add_argument(
        '-k', '--api-key',
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Automatically run docker-compose up after generation'
    )
    parser.add_argument(
        '--iterate',
        help='Modification to make to existing system'
    )
    
    args = parser.parse_args()
    
    # Load spec from file if needed
    if args.spec.startswith('@'):
        spec = load_spec_from_file(args.spec[1:])
    else:
        spec = args.spec
    
    # Create generator
    try:
        generator = MultiAgentGenerator(api_key=args.api_key)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # Generate or iterate
    if args.iterate:
        # Load existing files
        output_path = Path(args.output)
        if not output_path.exists():
            print(f"❌ Output directory {args.output} does not exist")
            sys.exit(1)
        
        # Reconstruct existing files
        existing_files = {}
        for filepath in output_path.rglob('*'):
            if filepath.is_file() and not filepath.name.startswith('.'):
                relative_path = filepath.relative_to(output_path)
                existing_files[str(relative_path)] = filepath.read_text()
        
        generator.iterate_on_system(
            spec=spec,
            modification=args.iterate,
            existing_files=existing_files,
            output_dir=args.output
        )
    else:
        generator.generate_system(
            spec=spec,
            output_dir=args.output,
            auto_execute=args.execute
        )


if __name__ == "__main__":
    main()
