#!/usr/bin/env python3
"""
Repository Final Cleanup - Move Development Artifacts

This script moves development artifacts, one-time use scripts, and temporary files
to .ai_development to leave only the clean SOLID architecture in production.

Educational Notes:
- Demonstrates proper separation of development vs production files
- Shows systematic approach to repository cleanup
- Illustrates explosive recursive decomposition for complete cleanup
- Provides template for maintaining clean production repositories

Cleanup Categories:
1. Development Reports → .ai_development/session_2025_08_08/
2. One-time Scripts → .ai_development/session_2025_08_08/scripts/
3. Backup Files → .ai_development/session_2025_08_08/backups/
4. Build Artifacts → Complete removal
5. Redundant Files → Analysis and removal
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class FinalRepositoryCleanup:
    """
    Performs final cleanup to achieve clean SOLID architecture.

    Educational Notes:
    - Uses systematic approach to identify and categorize files
    - Maintains audit trail of all operations
    - Preserves development history in organized structure
    - Ensures production repository contains only essential files
    """

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.session_dir = self.base_path / ".ai_development" / "session_2025_08_08"
        self.operations_log: List[str] = []
        self.moved_files = 0
        self.removed_files = 0

    def execute_final_cleanup(self):
        """Execute complete final cleanup with detailed logging."""
        try:
            print("🧹 Starting Final Repository Cleanup...")
            print(
                "🎯 Goal: Clean SOLID architecture with development artifacts properly organized"
            )

            # Create session directory for this cleanup
            self._create_session_structure()

            # Phase 1: Move development reports
            self._move_development_reports()

            # Phase 2: Move one-time use scripts
            self._move_one_time_scripts()

            # Phase 3: Move backup files
            self._move_backup_files()

            # Phase 4: Remove build artifacts completely
            self._remove_build_artifacts()

            # Phase 5: Remove redundant directories
            self._remove_redundant_directories()

            # Phase 6: Explosive recursive decomposition analysis
            self._analyze_decomposition_opportunities()

            print("✅ Final cleanup completed successfully!")
            self._print_cleanup_summary()

        except Exception as e:
            print(f"❌ Error during final cleanup: {e}")
            print("📋 Operations log:")
            for op in self.operations_log:
                print(f"  - {op}")
            raise

    def _create_session_structure(self):
        """Create organized structure for this cleanup session."""
        directories = [
            "scripts",
            "backups",
            "reports",
            "analysis",
        ]

        self.session_dir.mkdir(parents=True, exist_ok=True)

        for directory in directories:
            dir_path = self.session_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self._log_operation(f"Created session directory: {directory}")

    def _move_development_reports(self):
        """Move development reports to .ai_development."""
        print("📊 Phase 1: Moving development reports...")

        reports_to_move = [
            "CLEAN_ARCHITECTURE_SUCCESS.md",
            "REORGANIZATION_REPORT.md",
        ]

        reports_dir = self.session_dir / "reports"

        for report_file in reports_to_move:
            source_path = self.base_path / report_file
            if source_path.exists():
                target_path = reports_dir / report_file
                shutil.move(str(source_path), str(target_path))
                self.moved_files += 1
                self._log_operation(f"Moved {report_file} to session reports")

    def _move_one_time_scripts(self):
        """Move one-time use scripts to .ai_development."""
        print("⚙️ Phase 2: Moving one-time use scripts...")

        one_time_scripts = [
            "comprehensive_cleanup.py",
            "decompose_monolithic_files.py",
            "reorganize_src_structure.py",
            "validate_clean_architecture.py",  # Can be moved as it's validation only
        ]

        scripts_dir = self.session_dir / "scripts"
        source_scripts_dir = self.base_path / "scripts"

        for script_file in one_time_scripts:
            source_path = source_scripts_dir / script_file
            if source_path.exists():
                target_path = scripts_dir / script_file
                shutil.move(str(source_path), str(target_path))
                self.moved_files += 1
                self._log_operation(f"Moved {script_file} to session scripts")

    def _move_backup_files(self):
        """Move backup files to .ai_development."""
        print("💾 Phase 3: Moving backup files...")

        backups_dir = self.session_dir / "backups"

        # Find backup files
        backup_patterns = ["*.backup", "*_old*", "*~"]

        for pattern in backup_patterns:
            backup_files = list(self.base_path.glob(f"**/{pattern}"))
            for backup_file in backup_files:
                if backup_file.is_file():
                    # Preserve directory structure in backups
                    relative_path = backup_file.relative_to(self.base_path)
                    target_path = backups_dir / relative_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)

                    shutil.move(str(backup_file), str(target_path))
                    self.moved_files += 1
                    self._log_operation(f"Moved backup: {relative_path}")

    def _remove_build_artifacts(self):
        """Remove build artifacts completely."""
        print("🗑️ Phase 4: Removing build artifacts...")

        artifacts_to_remove = [
            ".pytest_cache",
        ]

        for artifact in artifacts_to_remove:
            artifact_path = self.base_path / artifact
            if artifact_path.exists():
                if artifact_path.is_dir():
                    shutil.rmtree(artifact_path)
                else:
                    artifact_path.unlink()
                self.removed_files += 1
                self._log_operation(f"Removed build artifact: {artifact}")

    def _remove_redundant_directories(self):
        """Remove redundant directories."""
        print("🔄 Phase 5: Removing redundant directories...")

        # Check if scripts/public is redundant with frontend/public
        scripts_public = self.base_path / "scripts" / "public"
        frontend_public = self.base_path / "frontend" / "public"

        if scripts_public.exists() and frontend_public.exists():
            # Compare content to see if redundant
            scripts_data = scripts_public / "data"
            frontend_data = frontend_public / "data"

            if scripts_data.exists() and frontend_data.exists():
                # If they contain similar files, remove scripts/public
                scripts_files = {f.name for f in scripts_data.glob("*")}
                frontend_files = {f.name for f in frontend_data.glob("*")}

                if scripts_files.issubset(frontend_files):
                    shutil.rmtree(scripts_public)
                    self.removed_files += 1
                    self._log_operation(
                        "Removed redundant scripts/public/ (duplicate of frontend/public/)"
                    )

    def _analyze_decomposition_opportunities(self):
        """Analyze opportunities for explosive recursive decomposition."""
        print("🔍 Phase 6: Analyzing decomposition opportunities...")

        analysis_file = self.session_dir / "analysis" / "decomposition_analysis.md"

        # Analyze large files
        large_files = []
        for py_file in self.base_path.glob("**/*.py"):
            if py_file.is_file() and not str(py_file).startswith(str(self.session_dir)):
                try:
                    line_count = len(py_file.read_text().splitlines())
                    if line_count > 300:  # Files over 300 lines
                        large_files.append((py_file, line_count))
                except Exception:
                    pass  # Skip files that can't be read

        # Sort by size
        large_files.sort(key=lambda x: x[1], reverse=True)

        # Analyze configuration structure
        config_analysis = self._analyze_config_structure()

        # Analyze test structure
        test_analysis = self._analyze_test_structure()

        # Create comprehensive analysis report
        analysis_content = self._create_analysis_report(
            large_files, config_analysis, test_analysis
        )

        analysis_file.write_text(analysis_content)
        self._log_operation("Created comprehensive decomposition analysis")

    def _analyze_config_structure(self) -> Dict[str, int]:
        """Analyze configuration file structure."""
        config_dir = self.base_path / "config"
        analysis = {}

        if config_dir.exists():
            for config_subdir in config_dir.iterdir():
                if config_subdir.is_dir():
                    yaml_files = list(config_subdir.glob("*.yaml"))
                    analysis[config_subdir.name] = len(yaml_files)

        return analysis

    def _analyze_test_structure(self) -> Dict[str, int]:
        """Analyze test file structure."""
        tests_dir = self.base_path / "tests"
        analysis = {}

        if tests_dir.exists():
            for test_subdir in tests_dir.iterdir():
                if test_subdir.is_dir():
                    py_files = list(test_subdir.glob("**/*.py"))
                    analysis[test_subdir.name] = len(py_files)

        return analysis

    def _create_analysis_report(
        self, large_files, config_analysis, test_analysis
    ) -> str:
        """Create comprehensive analysis report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""# Repository Decomposition Analysis

Generated: {timestamp}

## Executive Summary

This analysis identifies opportunities for explosive recursive decomposition to achieve
a complete fully expanded atomic tree structure following SOLID principles.

## Large Files Analysis

Files over 300 lines that may benefit from decomposition:

"""

        for file_path, line_count in large_files[:10]:  # Top 10
            relative_path = file_path.relative_to(self.base_path)
            report += f"- **{relative_path}**: {line_count} lines\n"

        report += """

## Configuration Structure Analysis

Current configuration organization:

"""

        for config_name, yaml_count in config_analysis.items():
            report += f"- **{config_name}**: {yaml_count} YAML files\n"

        report += """

## Test Structure Analysis

Current test organization:

"""

        for test_category, file_count in test_analysis.items():
            report += f"- **{test_category}**: {file_count} test files\n"

        report += """

## Decomposition Recommendations

### 1. Configuration Decomposition
- Consider atomic configuration files for each concept
- Implement configuration composition patterns
- Create configuration validation layers

### 2. Test Decomposition  
- Ensure each test file tests only one component
- Create atomic test utilities
- Implement proper test fixture organization

### 3. File Size Optimization
- Apply Single Responsibility Principle to large files
- Extract utilities and common functions
- Create focused domain services

### 4. Directory Structure Optimization
- Implement deeper hierarchical organization
- Create atomic concept directories
- Ensure clear separation of concerns

## Implementation Priority

1. **High Priority**: Files over 500 lines
2. **Medium Priority**: Files over 300 lines  
3. **Low Priority**: Configuration and test organization
4. **Maintenance**: Regular monitoring for file size growth

This analysis supports the goal of achieving a complete atomic tree structure
where each file has a single, clear responsibility and the entire system
follows SOLID architectural principles.
"""

        return report

    def _print_cleanup_summary(self):
        """Print comprehensive cleanup summary."""
        print("\n📊 Final Cleanup Summary:")
        print(f"  📁 Files moved to .ai_development: {self.moved_files}")
        print(f"  🗑️ Files/directories removed: {self.removed_files}")
        print(f"  📋 Total operations: {len(self.operations_log)}")

        print("\n🎯 Achievement: Clean SOLID Architecture")
        print("  ✅ Development artifacts organized in .ai_development")
        print("  ✅ One-time scripts moved to development session")
        print("  ✅ Build artifacts removed completely")
        print("  ✅ Redundant files eliminated")
        print("  ✅ Decomposition analysis completed")

        print(f"\n📂 Session Directory: {self.session_dir}")
        print("  📊 reports/ - Development reports and summaries")
        print("  ⚙️ scripts/ - One-time use scripts")
        print("  💾 backups/ - Backup files with preserved structure")
        print("  🔍 analysis/ - Decomposition and optimization analysis")

        print("\n🎓 Educational Achievement:")
        print("  Repository now demonstrates proper separation of:")
        print("  - Production code (clean and focused)")
        print("  - Development artifacts (organized and preserved)")
        print("  - Documentation (structured and accessible)")
        print("  - Configuration (domain-organized)")

    def _log_operation(self, message: str):
        """Log an operation for audit trail."""
        self.operations_log.append(message)
        print(f"  ✓ {message}")


def main():
    """Execute final repository cleanup."""
    current_dir = os.getcwd()

    if Path(current_dir).name != "research-paper-aggregator":
        print("❌ Please run this script from the research-paper-aggregator directory")
        exit(1)

    cleanup = FinalRepositoryCleanup(current_dir)
    cleanup.execute_final_cleanup()


if __name__ == "__main__":
    main()
