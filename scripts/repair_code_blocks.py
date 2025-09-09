#!/usr/bin/env python3
"""
Repair script to fix malformed [code] blocks in existing Workato SDK documentation.

This script fixes the issue where [code] blocks were not properly converted
to standard Markdown code blocks during the initial HTML-to-Markdown conversion.
"""

import re
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def fix_code_blocks(content: str) -> tuple[str, int]:
    """
    Fix malformed [code] blocks in Markdown content.
    
    Returns:
        tuple: (fixed_content, number_of_fixes_made)
    """
    original_content = content
    fixes_made = 0
    
    # Pattern 1: [code] with content on the same line followed by more content
    # Example: [code] $ ruby -v
    #          ruby 2.7.X
    #          ```
    pattern1 = r'\[code\]\s*([^\n]*)\n([^`\[]*)```'
    
    def replace_malformed_block(match):
        nonlocal fixes_made
        first_line = match.group(1).strip()
        rest_content = match.group(2).rstrip()
        
        # Determine language based on content
        if first_line.startswith('$') or first_line.startswith('#'):
            lang = 'bash'
        elif 'fields:' in first_line or 'lambda' in first_line:
            lang = 'ruby'
        else:
            lang = 'ruby'  # Default for Workato SDK docs
        
        fixes_made += 1
        
        # Reconstruct the code block
        if rest_content:
            return f'```{lang}\n{first_line}\n{rest_content}\n```'
        else:
            return f'```{lang}\n{first_line}\n```'
    
    content = re.sub(pattern1, replace_malformed_block, content, flags=re.MULTILINE)
    
    # Pattern 2: [code] followed by content on the next line(s) without proper closing
    # Example: [code]fields: lambda do |_connection, _config_fields|
    #          ...
    #          end
    #          ```
    pattern2 = r'\[code\]([^`\[]+?)```'
    
    def replace_code_block(match):
        nonlocal fixes_made
        code_content = match.group(1).strip()
        
        # Determine language
        if code_content.strip().startswith('$') or code_content.strip().startswith('#'):
            lang = 'bash'
        elif 'lambda' in code_content or 'def ' in code_content or 'end' in code_content:
            lang = 'ruby'
        else:
            lang = 'ruby'
        
        fixes_made += 1
        return f'```{lang}\n{code_content}\n```'
    
    content = re.sub(pattern2, replace_code_block, content, flags=re.MULTILINE | re.DOTALL)
    
    # Pattern 3: Standalone [code] tags that might remain
    if '[code]' in content:
        # Look for [code] followed by any content until we hit a natural break
        pattern3 = r'\[code\]\s*([^\[]*?)(?=\n\n|\Z)'
        
        def replace_standalone(match):
            nonlocal fixes_made
            code_content = match.group(1).strip()
            if not code_content:
                return ''  # Remove empty [code] tags
            
            # Determine language
            if code_content.startswith('$') or code_content.startswith('#'):
                lang = 'bash'
            else:
                lang = 'ruby'
            
            fixes_made += 1
            return f'```{lang}\n{code_content}\n```'
        
        content = re.sub(pattern3, replace_standalone, content, flags=re.MULTILINE | re.DOTALL)
    
    # Clean up any orphaned [/code] tags
    if '[/code]' in content:
        content = content.replace('[/code]', '')
        fixes_made += 1
    
    # Final check: if we still have [code] tags, log a warning
    if '[code]' in content:
        remaining = content.count('[code]')
        logger.warning(f"Still {remaining} [code] tags remaining after fixes")
    
    return content, fixes_made


def process_markdown_file(file_path: Path) -> bool:
    """
    Process a single Markdown file to fix code blocks.
    
    Returns:
        bool: True if fixes were made, False otherwise
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Check if file needs fixing
        if '[code]' not in content and '[/code]' not in content:
            return False
        
        logger.info(f"Processing: {file_path.name}")
        
        # Fix the content
        fixed_content, fixes_made = fix_code_blocks(content)
        
        if fixes_made > 0:
            # Back up original (just in case)
            backup_path = file_path.with_suffix('.md.backup')
            if not backup_path.exists():
                file_path.rename(backup_path)
                # Write fixed content
                file_path.write_text(fixed_content, encoding='utf-8')
                logger.info(f"  Fixed {fixes_made} code block(s). Original backed up to {backup_path.name}")
            else:
                # Backup already exists, just update the file
                file_path.write_text(fixed_content, encoding='utf-8')
                logger.info(f"  Fixed {fixes_made} code block(s)")
            return True
        else:
            logger.info(f"  No fixes needed")
            return False
            
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to repair all documentation files."""
    start_time = datetime.now()
    logger.info("Starting code block repair process")
    
    # Find docs directory
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / 'docs'
    
    if not docs_dir.exists():
        logger.error(f"Docs directory not found: {docs_dir}")
        return 1
    
    logger.info(f"Scanning directory: {docs_dir}")
    
    # Find all markdown files
    md_files = list(docs_dir.glob('*.md'))
    logger.info(f"Found {len(md_files)} Markdown files")
    
    # Process each file
    files_fixed = 0
    files_checked = 0
    
    for md_file in md_files:
        files_checked += 1
        if process_markdown_file(md_file):
            files_fixed += 1
    
    # Summary
    duration = datetime.now() - start_time
    logger.info("\n" + "="*50)
    logger.info(f"Repair completed in {duration}")
    logger.info(f"Files checked: {files_checked}")
    logger.info(f"Files fixed: {files_fixed}")
    logger.info(f"Files unchanged: {files_checked - files_fixed}")
    
    if files_fixed > 0:
        logger.info(f"\n✅ Successfully repaired {files_fixed} file(s)")
        logger.info("Backup files created with .backup extension")
    else:
        logger.info("\n✅ No files needed repair")
    
    return 0


if __name__ == "__main__":
    exit(main())
