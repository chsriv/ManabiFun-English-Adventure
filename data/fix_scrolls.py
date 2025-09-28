#!/usr/bin/env python3
"""
🔮 Ancient Scroll Restoration Spell 🔮
Repairs the damaged CSV scrolls by removing corrupted header lines
"""

import pandas as pd
import os

def repair_ancient_scrolls():
    """Repair the damaged CSV by removing the corrupted header line"""
    input_file = "manabifun_questions.csv"
    backup_file = "manabifun_questions_backup.csv"
    
    print("🧙‍♂️ Beginning the ancient scroll restoration ritual...")
    
    # Create backup
    if os.path.exists(input_file):
        print(f"📜 Creating backup: {backup_file}")
        os.rename(input_file, backup_file)
    
    print("✨ Reading the damaged scrolls line by line...")
    
    # Read the file line by line and filter out corrupted lines
    clean_lines = []
    expected_headers = "topic,question,option_a,option_b,option_c,option_d,correct_answer,difficulty"
    
    with open(backup_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Count fields
            fields = line.split(',')
            
            # Skip if this is a duplicate header line (but keep the first one)
            if line == expected_headers and line_num > 1:
                print(f"🔍 Found duplicate header at line {line_num}, removing...")
                continue
            
            # Keep lines with exactly 8 fields or the header
            if len(fields) == 8 or line == expected_headers:
                clean_lines.append(line)
            else:
                print(f"⚡ Corrupted line {line_num} removed: {len(fields)} fields instead of 8")
                print(f"   Content preview: {line[:100]}...")
    
    print(f"📚 Restored {len(clean_lines)} clean lines (including header)")
    
    # Write the cleaned data
    with open(input_file, 'w', encoding='utf-8', newline='') as f:
        for line in clean_lines:
            f.write(line + '\n')
    
    print(f"✅ Ancient scrolls have been restored! Saved as: {input_file}")
    
    # Validate the repair
    try:
        df = pd.read_csv(input_file)
        print(f"🎉 Validation successful! Loaded {len(df)} questions across {df['topic'].nunique()} realms")
        print(f"📊 Realms discovered: {list(df['topic'].unique())}")
        return True
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

if __name__ == "__main__":
    repair_ancient_scrolls()