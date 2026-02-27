#!/usr/bin/env python3
"""
WallpaperChanger Log Viewer
Simple utility to view and analyze debug logs
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import argparse


class LogViewer:
    """Log viewer for WallpaperChanger debug logs"""
    
    def __init__(self, log_dir: Optional[str] = None):
        self.log_dir = Path(log_dir) if log_dir else Path(__file__).parent
        self.debug_log = self.log_dir / "debug.log"
        self.error_log = self.log_dir / "error.log"
    
    def show_recent_logs(self, lines: int = 50, log_type: str = "debug") -> None:
        """Show recent log entries"""
        log_file = self.debug_log if log_type == "debug" else self.error_log
        
        if not log_file.exists():
            print(f"❌ {log_type.title()} log file not found: {log_file}")
            return
        
        print(f"📄 Showing last {lines} lines from {log_type} log:")
        print("=" * 80)
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                
                for line in recent_lines:
                    print(line.rstrip())
        except Exception as e:
            print(f"❌ Error reading log file: {e}")
    
    def show_error_summary(self) -> None:
        """Show summary of recent errors"""
        if not self.error_log.exists():
            print("✅ No error log file found - no errors recorded!")
            return
        
        print("🔍 Recent Error Summary:")
        print("=" * 50)
        
        try:
            with open(self.error_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            if not lines:
                print("✅ No errors found in error log!")
                return
            
            # Group errors by type
            error_types = {}
            recent_errors = []
            
            for line in lines[-50:]:  # Last 50 errors
                line = line.strip()
                if "ERROR" in line:
                    recent_errors.append(line)
                    
                    # Extract error type
                    if ":" in line:
                        error_type = line.split(":")[-1].strip()
                        error_type = error_type.split()[0] if error_type else "Unknown"
                        error_types[error_type] = error_types.get(error_type, 0) + 1
            
            # Show summary
            print(f"Total recent errors: {len(recent_errors)}")
            print("\nError types:")
            for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  {error_type}: {count}")
            
            # Show last 5 errors
            print("\nLast 5 errors:")
            for error in recent_errors[-5:]:
                print(f"  {error}")
                
        except Exception as e:
            print(f"❌ Error analyzing log file: {e}")
    
    def search_logs(self, pattern: str, log_type: str = "debug") -> None:
        """Search for pattern in logs"""
        log_file = self.debug_log if log_type == "debug" else self.error_log
        
        if not log_file.exists():
            print(f"❌ {log_type.title()} log file not found: {log_file}")
            return
        
        print(f"🔍 Searching for '{pattern}' in {log_type} log:")
        print("=" * 80)
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if pattern.lower() in line.lower():
                        print(f"Line {line_num}: {line.rstrip()}")
        except Exception as e:
            print(f"❌ Error searching log file: {e}")
    
    def show_log_stats(self) -> None:
        """Show statistics about log files"""
        print("📊 Log File Statistics:")
        print("=" * 40)
        
        for log_name, log_file in [("Debug", self.debug_log), ("Error", self.error_log)]:
            if log_file.exists():
                try:
                    stat = log_file.stat()
                    size_mb = stat.st_size / (1024 * 1024)
                    modified = datetime.fromtimestamp(stat.st_mtime)
                    
                    print(f"{log_name} Log:")
                    print(f"  File: {log_file}")
                    print(f"  Size: {size_mb:.2f} MB")
                    print(f"  Modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Count lines
                    with open(log_file, 'r', encoding='utf-8') as f:
                        line_count = sum(1 for _ in f)
                    print(f"  Lines: {line_count}")
                    print()
                except Exception as e:
                    print(f"  ❌ Error reading {log_name} log: {e}")
            else:
                print(f"{log_name} Log: ❌ Not found")
                print()
    
    def clear_logs(self, log_type: str = "all") -> None:
        """Clear log files"""
        files_to_clear = []
        
        if log_type in ("all", "debug"):
            files_to_clear.append(self.debug_log)
        if log_type in ("all", "error"):
            files_to_clear.append(self.error_log)
        
        for log_file in files_to_clear:
            try:
                if log_file.exists():
                    log_file.unlink()
                    print(f"✅ Cleared: {log_file.name}")
                else:
                    print(f"ℹ️  File not found: {log_file.name}")
            except Exception as e:
                print(f"❌ Failed to clear {log_file.name}: {e}")
    
    def tail_logs(self, log_type: str = "debug") -> None:
        """Continuously monitor log file (like tail -f)"""
        log_file = self.debug_log if log_type == "debug" else self.error_log
        
        if not log_file.exists():
            print(f"❌ {log_type.title()} log file not found: {log_file}")
            return
        
        print(f"👀 Monitoring {log_type} log (Ctrl+C to stop):")
        print("=" * 80)
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                # Go to end of file
                f.seek(0, 2)
                
                while True:
                    line = f.readline()
                    if line:
                        print(line.rstrip())
                    else:
                        import time
                        time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n👋 Stopped monitoring.")
        except Exception as e:
            print(f"❌ Error monitoring log: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="WallpaperChanger Log Viewer")
    parser.add_argument("action", choices=["recent", "errors", "search", "stats", "clear", "tail"],
                       help="Action to perform")
    parser.add_argument("--lines", type=int, default=50,
                       help="Number of lines to show (for recent action)")
    parser.add_argument("--type", choices=["debug", "error"], default="debug",
                       help="Log type to analyze")
    parser.add_argument("--pattern", help="Search pattern (for search action)")
    parser.add_argument("--clear-type", choices=["debug", "error", "all"], default="all",
                       help="Type of logs to clear (for clear action)")
    
    args = parser.parse_args()
    
    viewer = LogViewer()
    
    try:
        if args.action == "recent":
            viewer.show_recent_logs(args.lines, args.type)
        elif args.action == "errors":
            viewer.show_error_summary()
        elif args.action == "search":
            if not args.pattern:
                print("❌ Search pattern required for search action")
                sys.exit(1)
            viewer.search_logs(args.pattern, args.type)
        elif args.action == "stats":
            viewer.show_log_stats()
        elif args.action == "clear":
            viewer.clear_logs(args.clear_type)
        elif args.action == "tail":
            viewer.tail_logs(args.type)
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
