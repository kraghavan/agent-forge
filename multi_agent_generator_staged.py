#!/usr/bin/env python3
"""
Improved Multi-Agent System Generator with Iterative File Generation
Avoids token limits by generating files in multiple passes
"""

import anthropic
import os
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import time

class ImprovedMultiAgentGenerator:
    """Generate multi-agent systems iteratively to avoid token limits"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Set ANTHROPIC_API_KEY environment variable")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.total_cost = 0.0
        self.total_tokens = 0
    
    def generate_system(self, spec: str, output_dir: str = "./generated-system") -> Dict[str, str]:
        """
        Generate system using iterative approach
        
        Phase 1: Generate file manifest (list of files to create)
        Phase 2: Generate each file individually
        Phase 3: Verify completeness
        """
        print("🤖 Improved Multi-Agent System Generator")
        print("=" * 60)
        print(f"📝 Spec length: {len(spec)} characters")
        print(f"📊 Estimated tokens: ~{len(spec) // 4:,}")
        print()
        
        # Phase 1: Get file manifest
        print("📋 Phase 1: Generating file manifest...")
        manifest = self._generate_manifest(spec)
        print(f"✓ Found {len(manifest)} files to generate")
        print()
        
        # Phase 2: Generate files iteratively
        print("📝 Phase 2: Generating files...")
        files = {}
        
        # Group files by type for efficient generation
        file_groups = self._group_files(manifest)
        
        for group_name, file_list in file_groups.items():
            print(f"\n  Generating {group_name}...")
            generated = self._generate_file_group(spec, file_list)
            files.update(generated)
            
            # Show progress
            for filepath in file_list:
                if filepath in generated:
                    print(f"    ✓ {filepath}")
                else:
                    print(f"    ⚠ {filepath} (missing, will retry)")
        
        # Phase 3: Verify and fill gaps
        print("\n🔍 Phase 3: Verifying completeness...")
        missing = [f for f in manifest if f not in files]
        
        if missing:
            print(f"  ⚠ {len(missing)} files missing, generating individually...")
            for filepath in missing:
                print(f"    Generating {filepath}...")
                content = self._generate_single_file(spec, filepath, files)
                if content:
                    files[filepath] = content
                    print(f"      ✓ {filepath}")
        
        # Write files to disk
        print(f"\n💾 Writing {len(files)} files to {output_dir}...")
        self._write_files(files, output_dir)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 GENERATION SUMMARY")
        print("=" * 60)
        print(f"📁 Files generated:     {len(files)}/{len(manifest)}")
        print(f"💰 Total cost:          ${self.total_cost:.4f}")
        print(f"📊 Total tokens:        {self.total_tokens:,}")
        print("=" * 60)
        print()
        
        if len(files) < len(manifest):
            missing_files = set(manifest) - set(files.keys())
            print("⚠️  WARNING: Some files were not generated:")
            for f in missing_files:
                print(f"  - {f}")
            print()
        
        return files
    
    def _generate_manifest(self, spec: str) -> List[str]:
        """Phase 1: Generate list of files that should be created"""
        
        prompt = f"""Based on this specification, list ALL files that need to be generated.

Specification:
{spec}

Respond ONLY with a JSON array of file paths (relative to project root):
["file1.txt", "folder/file2.py", ...]

Include:
- docker-compose.yml
- All Python files (publisher.py, consumer.py, monitor.py, etc.)
- All Dockerfiles
- All requirements.txt files
- Setup scripts
- Config files (loki-config.yaml, promtail-config.yaml, etc.)

Do NOT include:
- README.md or documentation
- Test files (unless specified)"""

        response = self._call_claude(prompt, max_tokens=2000)
        
        try:
            # Extract JSON from response
            text = response.content[0].text.strip()
            text = text.replace('```json', '').replace('```', '').strip()
            manifest = json.loads(text)
            return manifest
        except Exception as e:
            print(f"❌ Failed to parse manifest: {e}")
            print(f"Response: {response.content[0].text[:500]}")
            sys.exit(1)
    
    def _group_files(self, manifest: List[str]) -> Dict[str, List[str]]:
        """Group files by type for efficient batch generation"""
        
        groups = {
            "infrastructure": [],
            "publishers": [],
            "consumers": [],
            "monitor": [],
            "config": []
        }
        
        for filepath in manifest:
            if "docker-compose" in filepath:
                groups["infrastructure"].append(filepath)
            elif "publisher" in filepath:
                groups["publishers"].append(filepath)
            elif "consumer" in filepath:
                groups["consumers"].append(filepath)
            elif "monitor" in filepath:
                groups["monitor"].append(filepath)
            else:
                groups["config"].append(filepath)
        
        # Remove empty groups
        return {k: v for k, v in groups.items() if v}
    
    def _generate_file_group(self, spec: str, file_list: List[str]) -> Dict[str, str]:
        """Generate a group of related files in one API call"""
        
        if not file_list:
            return {}
        
        # Limit to 5 files per batch to avoid token limits
        if len(file_list) > 5:
            results = {}
            for i in range(0, len(file_list), 5):
                batch = file_list[i:i+5]
                results.update(self._generate_file_group(spec, batch))
            return results
        
        prompt = f"""Based on this specification, generate these files:

{', '.join(file_list)}

Specification:
{spec}

CRITICAL: Generate COMPLETE, WORKING code for each file. Do not truncate or summarize.

Respond with ONLY this JSON structure (no markdown, no explanation):
{{
  "file1.py": "complete file content here...",
  "file2.txt": "complete file content here..."
}}

For Python files:
- Include ALL imports
- Include COMPLETE class definitions
- Include COMPLETE function bodies
- Include error handling
- No placeholders like "# rest of code..." or "# implementation here"
"""

        response = self._call_claude(prompt, max_tokens=8000)
        
        try:
            text = response.content[0].text.strip()
            
            # Try to extract JSON even if wrapped in markdown
            if '```json' in text:
                json_start = text.find('```json') + 7
                json_end = text.rfind('```')
                text = text[json_start:json_end].strip()
            elif '```' in text:
                json_start = text.find('```') + 3
                json_end = text.rfind('```')
                text = text[json_start:json_end].strip()
            
            files = json.loads(text)
            return files
        
        except Exception as e:
            print(f"    ⚠ Failed to parse batch: {e}")
            # Fall back to individual generation
            return {}
    
    def _generate_single_file(self, spec: str, filepath: str, existing_files: Dict[str, str]) -> Optional[str]:
        """Generate a single file (fallback for missing files)"""
        
        # Build context from existing files
        context = "Existing files:\n"
        for existing_path in sorted(existing_files.keys())[:10]:  # Show first 10
            context += f"  - {existing_path}\n"
        
        prompt = f"""Based on this specification, generate the file: {filepath}

Specification:
{spec}

{context}

CRITICAL: Generate COMPLETE, WORKING code. Do not truncate.

Respond with ONLY the file content (no JSON, no markdown fences, no explanation).
Start your response with the FIRST LINE of the file.
"""

        response = self._call_claude(prompt, max_tokens=4000)
        
        content = response.content[0].text.strip()
        
        # Remove markdown fences if present
        if content.startswith('```'):
            lines = content.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            content = '\n'.join(lines)
        
        return content
    
    def _call_claude(self, prompt: str, max_tokens: int = 4000) -> any:
        """Call Claude API and track costs"""
        
        start_time = time.time()
        
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Track costs
        usage = response.usage
        input_cost = (usage.input_tokens / 1_000_000) * 3.00
        output_cost = (usage.output_tokens / 1_000_000) * 15.00
        self.total_cost += input_cost + output_cost
        self.total_tokens += usage.input_tokens + usage.output_tokens
        
        return response
    
    def _write_files(self, files: Dict[str, str], output_dir: str):
        """Write generated files to disk"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for filepath, content in files.items():
            full_path = output_path / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w') as f:
                f.write(content)
        
        print(f"  ✓ Wrote {len(files)} files to {output_dir}")


def main():
    parser = argparse.ArgumentParser(description='Improved Multi-Agent System Generator')
    parser.add_argument('spec_file', help='Specification file (use @filename to read from file)')
    parser.add_argument('-o', '--output', default='./generated-system', help='Output directory')
    parser.add_argument('--api-key', help='Anthropic API key (or set ANTHROPIC_API_KEY)')
    
    args = parser.parse_args()
    
    # Read spec from file
    spec_path = args.spec_file
    if spec_path.startswith('@'):
        spec_path = spec_path[1:]
    
    try:
        with open(spec_path, 'r') as f:
            spec = f.read()
    except FileNotFoundError:
        print(f"❌ Spec file not found: {spec_path}")
        sys.exit(1)
    
    # Generate system
    generator = ImprovedMultiAgentGenerator(api_key=args.api_key)
    generator.generate_system(spec, output_dir=args.output)


if __name__ == "__main__":
    main()
