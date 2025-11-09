#!/usr/bin/env python3
"""
Module Inventory Generator for Odoo 15→18 Migration
Scans Odoo installation and generates comprehensive module inventory
"""

import os
import ast
import csv
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ModuleInventory:
    """Generate comprehensive module inventory for migration"""

    def __init__(self, odoo_root: str):
        self.odoo_root = Path(odoo_root)
        self.modules = []

    def get_addon_paths(self) -> List[Path]:
        """Get all addon paths from Odoo installation"""
        addon_paths = [
            self.odoo_root / 'addons',
            self.odoo_root / 'addons_custom',
            self.odoo_root / 'common',
            self.odoo_root / 'reports15',
            self.odoo_root / 'themes15',
        ]
        return [p for p in addon_paths if p.exists()]

    def parse_manifest(self, manifest_path: Path) -> Dict[str, Any]:
        """Parse module manifest file (__manifest__.py or __openerp__.py)"""
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
                manifest_dict = ast.literal_eval(content)
                return manifest_dict
        except Exception as e:
            print(f"Error parsing {manifest_path}: {e}")
            return {}

    def get_module_category(self, module_path: Path) -> str:
        """Determine module category (Core/Custom/Third-Party)"""
        path_str = str(module_path)

        if 'addons_custom' in path_str:
            return 'Custom'
        elif 'common' in path_str:
            return 'Custom'
        elif 'reports15' in path_str:
            return 'Custom'
        elif 'themes15' in path_str:
            return 'Theme'
        elif 'addons' in path_str:
            # Check if it's a standard Odoo module
            module_name = module_path.name
            # Standard Odoo modules typically don't have external authors
            manifest = self.get_manifest_file(module_path)
            if manifest:
                manifest_data = self.parse_manifest(manifest)
                author = manifest_data.get('author', '')
                if 'Odoo' in author or 'OpenERP' in author:
                    return 'Core'
                else:
                    return 'Third-Party'
            return 'Core'

        return 'Unknown'

    def get_manifest_file(self, module_path: Path) -> Path:
        """Get manifest file path (__manifest__.py or __openerp__.py)"""
        manifest = module_path / '__manifest__.py'
        if manifest.exists():
            return manifest

        openerp = module_path / '__openerp__.py'
        if openerp.exists():
            return openerp

        return None

    def is_valid_module(self, module_path: Path) -> bool:
        """Check if directory is a valid Odoo module"""
        if not module_path.is_dir():
            return False

        # Must have manifest file
        if not self.get_manifest_file(module_path):
            return False

        # Skip hidden directories and common non-module directories
        if module_path.name.startswith('.'):
            return False
        if module_path.name in ['__pycache__', 'static', 'tests']:
            return False

        return True

    def scan_modules(self):
        """Scan all addon paths and collect module information"""
        addon_paths = self.get_addon_paths()

        for addon_path in addon_paths:
            print(f"Scanning: {addon_path}")

            # Handle nested report directories
            if 'reports15' in str(addon_path):
                # reports15 has subdirectories
                for item in addon_path.iterdir():
                    if item.is_dir():
                        self._scan_directory(item)
            else:
                self._scan_directory(addon_path)

    def _scan_directory(self, directory: Path):
        """Scan a directory for modules"""
        for module_path in directory.iterdir():
            if not self.is_valid_module(module_path):
                continue

            manifest_file = self.get_manifest_file(module_path)
            manifest_data = self.parse_manifest(manifest_file)

            module_info = {
                'name': module_path.name,
                'display_name': manifest_data.get('name', module_path.name),
                'version': manifest_data.get('version', '15.0.1.0.0'),
                'category': self.get_module_category(module_path),
                'technical_category': manifest_data.get('category', 'Uncategorized'),
                'author': manifest_data.get('author', 'Unknown'),
                'summary': manifest_data.get('summary', ''),
                'description': manifest_data.get('description', '')[:200],  # First 200 chars
                'depends': ', '.join(manifest_data.get('depends', [])),
                'auto_install': manifest_data.get('auto_install', False),
                'installable': manifest_data.get('installable', True),
                'application': manifest_data.get('application', False),
                'path': str(module_path.relative_to(self.odoo_root)),
                'manifest_file': manifest_file.name,
            }

            self.modules.append(module_info)

    def generate_csv(self, output_file: str):
        """Generate CSV report of modules"""
        fieldnames = [
            'name', 'display_name', 'version', 'category', 'technical_category',
            'author', 'summary', 'description', 'depends', 'auto_install', 'installable',
            'application', 'path', 'manifest_file'
        ]

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.modules)

        print(f"CSV report generated: {output_file}")

    def generate_json(self, output_file: str):
        """Generate JSON report of modules"""
        data = {
            'generated_at': datetime.now().isoformat(),
            'odoo_version': '15.0',
            'total_modules': len(self.modules),
            'modules_by_category': self.get_category_summary(),
            'modules': self.modules
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"JSON report generated: {output_file}")

    def get_category_summary(self) -> Dict[str, int]:
        """Get count of modules by category"""
        summary = {}
        for module in self.modules:
            category = module['category']
            summary[category] = summary.get(category, 0) + 1
        return summary

    def generate_markdown_report(self, output_file: str):
        """Generate Markdown summary report"""
        total = len(self.modules)
        category_summary = self.get_category_summary()

        # Get custom modules for detailed listing
        custom_modules = [m for m in self.modules if m['category'] == 'Custom']

        report = f"""# Odoo 15 Module Inventory Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Total Modules**: {total}
- **Core Modules**: {category_summary.get('Core', 0)}
- **Custom Modules**: {category_summary.get('Custom', 0)}
- **Third-Party Modules**: {category_summary.get('Third-Party', 0)}
- **Theme Modules**: {category_summary.get('Theme', 0)}

## Modules by Category

"""

        for category, count in sorted(category_summary.items()):
            report += f"- **{category}**: {count} modules\n"

        report += "\n## Custom Modules Detail\n\n"
        report += "These modules require migration to Odoo 18:\n\n"
        report += "| Module Name | Display Name | Version | Dependencies |\n"
        report += "|-------------|--------------|---------|-------------|\n"

        for module in sorted(custom_modules, key=lambda x: x['name']):
            deps = module['depends'][:50] + '...' if len(module['depends']) > 50 else module['depends']
            report += f"| {module['name']} | {module['display_name']} | {module['version']} | {deps} |\n"

        report += f"\n## Core Modules ({category_summary.get('Core', 0)} modules)\n\n"
        core_modules = [m for m in self.modules if m['category'] == 'Core']

        # Group by technical category
        core_by_category = {}
        for module in core_modules:
            tech_cat = module['technical_category']
            if tech_cat not in core_by_category:
                core_by_category[tech_cat] = []
            core_by_category[tech_cat].append(module['name'])

        for tech_cat, modules in sorted(core_by_category.items()):
            report += f"### {tech_cat}\n"
            report += f"{', '.join(sorted(modules))}\n\n"

        report += "\n## Next Steps\n\n"
        report += "1. Review custom modules for Odoo 18 compatibility\n"
        report += "2. Identify deprecated APIs in custom modules\n"
        report += "3. Check third-party modules for Odoo 18 availability\n"
        report += "4. Plan migration order based on dependencies\n"
        report += "5. Proceed to Phase 2: Core Module Validation\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"Markdown report generated: {output_file}")

    def print_summary(self):
        """Print summary to console"""
        total = len(self.modules)
        category_summary = self.get_category_summary()

        print("\n" + "="*60)
        print("MODULE INVENTORY SUMMARY")
        print("="*60)
        print(f"Total Modules: {total}")
        print("\nBy Category:")
        for category, count in sorted(category_summary.items()):
            print(f"  {category:20s}: {count:3d} modules")
        print("="*60 + "\n")


def main():
    """Main execution"""
    # Get Odoo root directory (parent of this script's directory)
    script_dir = Path(__file__).parent
    odoo_root = script_dir.parent.parent  # migration/inventory -> migration -> odoo_root

    print(f"Odoo Root: {odoo_root}")
    print(f"Scanning modules...")

    # Create inventory
    inventory = ModuleInventory(str(odoo_root))
    inventory.scan_modules()

    # Generate reports
    output_dir = script_dir
    inventory.generate_csv(output_dir / 'odoo15_modules.csv')
    inventory.generate_json(output_dir / 'odoo15_modules.json')
    inventory.generate_markdown_report(output_dir / 'MODULE_INVENTORY.md')

    # Print summary
    inventory.print_summary()

    print("\nInventory generation complete!")
    print(f"Reports saved to: {output_dir}")


if __name__ == '__main__':
    main()
