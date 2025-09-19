#!/usr/bin/env python3
"""
Documentation Registry Compatibility Checker
Checks version compatibility and ensures documentation sources are accessible
"""

import sys
import yaml
import os
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

class DocsCompatibilityChecker:
    """Checks documentation registry compatibility and accessibility"""
    
    def __init__(self, registry_path: str, verbose: bool = False):
        self.registry_path = Path(registry_path)
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.info = []
        self.data = None
        
    def check_compatibility(self) -> bool:
        """Main compatibility check method. Returns True if compatible."""
        if not self._load_registry():
            return False
            
        # Run all compatibility checks
        self._check_framework_version()
        self._check_tech_stack_versions()
        self._check_source_accessibility()
        self._check_internal_paths()
        
        return len(self.errors) == 0
        
    def _load_registry(self) -> bool:
        """Load and parse the registry file"""
        if not self.registry_path.exists():
            self.errors.append(f"Registry file not found: {self.registry_path}")
            return False
            
        try:
            with open(self.registry_path, 'r') as f:
                self.data = yaml.safe_load(f)
            return True
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML syntax: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Failed to read registry file: {e}")
            return False
            
    def _check_framework_version(self):
        """Check Agent OS framework version compatibility"""
        metadata = self.data.get('metadata', {})
        framework_version = metadata.get('framework_version', '')
        
        if not framework_version:
            self.warnings.append("Framework version not specified in metadata")
            return
            
        # Check against current framework version (from known constants)
        current_version = "1.4.0"  # Could be read from config or environment
        
        if self._compare_versions(framework_version, current_version) < 0:
            self.warnings.append(f"Registry created with older framework version {framework_version}, current is {current_version}")
        elif self._compare_versions(framework_version, current_version) > 0:
            self.warnings.append(f"Registry created with newer framework version {framework_version}, current is {current_version}")
        else:
            self.info.append(f"Framework version {framework_version} matches current version")
            
    def _compare_versions(self, version1: str, version2: str) -> int:
        """Compare two semantic versions. Returns -1, 0, or 1"""
        def version_tuple(v):
            try:
                return tuple(map(int, v.split('.')))
            except ValueError:
                # If not numeric, treat as string
                return (v,)
                
        v1_parts = version_tuple(version1)
        v2_parts = version_tuple(version2)
        
        # Pad shorter version with zeros
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts += (0,) * (max_len - len(v1_parts))
        v2_parts += (0,) * (max_len - len(v2_parts))
        
        if v1_parts < v2_parts:
            return -1
        elif v1_parts > v2_parts:
            return 1
        else:
            return 0
            
    def _check_tech_stack_versions(self):
        """Check tech stack version compatibility"""
        tech_stack = self.data.get('tech_stack', {})
        
        for name, config in tech_stack.items():
            if not isinstance(config, dict):
                continue
                
            version = config.get('version')
            tech_type = config.get('type')
            
            if version:
                self._check_specific_tech_version(name, version, tech_type)
            else:
                self.info.append(f"No version specified for {name} - consider adding for better compatibility tracking")
                
    def _check_specific_tech_version(self, name: str, version: str, tech_type: str):
        """Check specific technology version compatibility"""
        # This could be expanded with specific compatibility matrices
        known_compatibility = {
            'react': {
                'deprecated_below': '16.8.0',
                'recommended_minimum': '18.0.0'
            },
            'fastapi': {
                'deprecated_below': '0.68.0',
                'recommended_minimum': '0.100.0'
            },
            'python': {
                'deprecated_below': '3.8.0',
                'recommended_minimum': '3.10.0'
            }
        }
        
        if name.lower() in known_compatibility:
            compat = known_compatibility[name.lower()]
            
            if 'deprecated_below' in compat:
                if self._compare_versions(version, compat['deprecated_below']) < 0:
                    self.warnings.append(f"{name} version {version} is deprecated (minimum supported: {compat['deprecated_below']})")
                    
            if 'recommended_minimum' in compat:
                if self._compare_versions(version, compat['recommended_minimum']) < 0:
                    self.info.append(f"{name} version {version} is below recommended minimum {compat['recommended_minimum']}")
                    
        self.info.append(f"Checked {name} version {version}")
        
    def _check_source_accessibility(self):
        """Check if external sources are accessible"""
        # Check all sections with sources
        for section_name in ['tech_stack', 'external_apis', 'compliance', 'pocketflow_patterns']:
            section = self.data.get(section_name, {})
            for name, config in section.items():
                if not isinstance(config, dict):
                    continue
                    
                source = config.get('source')
                if source:
                    self._check_source(name, source, section_name)
                    
    def _check_source(self, name: str, source: str, section: str):
        """Check accessibility of a specific source"""
        if self._is_url(source):
            self._check_url_accessibility(name, source, section)
        else:
            self._check_local_path(name, source, section)
            
    def _is_url(self, source: str) -> bool:
        """Check if source is a URL"""
        try:
            result = urlparse(source)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
            
    def _check_url_accessibility(self, name: str, url: str, section: str):
        """Check if URL is accessible"""
        try:
            # Quick HEAD-style request with timeout using urllib
            response = urlopen(url, timeout=10)
            status_code = response.getcode()
            response.close()
            
            if status_code == 200:
                self.info.append(f"{section}.{name}: URL accessible ({url})")
            elif status_code == 404:
                self.errors.append(f"{section}.{name}: URL not found (404): {url}")
            elif status_code >= 400:
                self.warnings.append(f"{section}.{name}: URL returned {status_code}: {url}")
            else:
                self.info.append(f"{section}.{name}: URL accessible with status {status_code}: {url}")
                
        except HTTPError as e:
            if e.code == 404:
                self.errors.append(f"{section}.{name}: URL not found (404): {url}")
            elif e.code >= 400:
                self.warnings.append(f"{section}.{name}: URL returned {e.code}: {url}")
            else:
                self.info.append(f"{section}.{name}: URL accessible with status {e.code}: {url}")
        except URLError as e:
            if "timed out" in str(e).lower():
                self.warnings.append(f"{section}.{name}: URL timeout (may be slow): {url}")
            else:
                self.errors.append(f"{section}.{name}: Cannot connect to URL: {url} ({e})")
        except Exception as e:
            self.warnings.append(f"{section}.{name}: Unexpected error checking URL: {url} ({e})")
            
    def _check_local_path(self, name: str, path: str, section: str):
        """Check if local path exists and is accessible"""
        # Make path relative to registry directory if not absolute
        if not os.path.isabs(path):
            registry_dir = self.registry_path.parent
            full_path = registry_dir / path
        else:
            full_path = Path(path)
            
        if full_path.exists():
            if full_path.is_file():
                self.info.append(f"{section}.{name}: Local file accessible ({path})")
            elif full_path.is_dir():
                self.info.append(f"{section}.{name}: Local directory accessible ({path})")
        else:
            self.errors.append(f"{section}.{name}: Local path not found: {path}")
            
    def _check_internal_paths(self):
        """Check internal standards paths"""
        internal_standards = self.data.get('internal_standards', {})
        
        for name, config in internal_standards.items():
            if not isinstance(config, dict):
                continue
                
            source = config.get('source')
            if source and not self._is_url(source):
                self._check_local_path(name, source, 'internal_standards')
                
    def print_results(self):
        """Print compatibility check results"""
        if self.errors:
            print("❌ COMPATIBILITY ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
                
        if self.warnings:
            print("⚠️  COMPATIBILITY WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
                
        if self.verbose and self.info:
            print("ℹ️  COMPATIBILITY INFO:")
            for info in self.info:
                print(f"  - {info}")
                
        if not self.errors and not self.warnings:
            print("✅ All documentation sources are compatible and accessible!")
        elif not self.errors:
            print("✅ Documentation registry is compatible (with warnings)")
            
        # Summary
        print(f"\nSummary: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} checks passed")


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Check documentation registry compatibility')
    parser.add_argument('registry', help='Path to docs-registry.yaml file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    print(f"Checking documentation registry compatibility: {args.registry}")
    print("-" * 60)
    
    checker = DocsCompatibilityChecker(args.registry, verbose=args.verbose)
    is_compatible = checker.check_compatibility()
    checker.print_results()
    
    sys.exit(0 if is_compatible else 1)


if __name__ == "__main__":
    main()