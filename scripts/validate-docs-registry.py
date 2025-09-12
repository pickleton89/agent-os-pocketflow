#!/usr/bin/env python3
"""
Documentation Registry Validation Script
Validates the structure and content of .agent-os/docs-registry.yaml files
"""

import sys
import yaml
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class DocsRegistryValidator:
    """Validates documentation registry files"""
    
    REQUIRED_TOP_LEVEL_KEYS = {
        'version', 'last_updated', 'tech_stack', 'external_apis', 
        'internal_standards', 'compliance', 'pocketflow_patterns', 
        'discovery_settings', 'metadata'
    }
    
    REQUIRED_DISCOVERY_SETTINGS = {
        'auto_discover', 'scan_paths', 'include_patterns', 'exclude_patterns'
    }
    
    REQUIRED_METADATA = {
        'created_by', 'framework_version', 'registry_format_version'
    }
    
    VALID_TECH_STACK_TYPES = {'framework', 'library', 'tool'}
    VALID_API_TYPES = {'rest', 'graphql', 'websocket', 'custom'}
    VALID_STANDARD_TYPES = {'architecture', 'style', 'security', 'compliance'}
    VALID_COMPLIANCE_TYPES = {'regulatory', 'security', 'industry'}
    
    def __init__(self, registry_path: str):
        self.registry_path = Path(registry_path)
        self.errors = []
        self.warnings = []
        
    def validate(self) -> bool:
        """Main validation method. Returns True if valid."""
        if not self.registry_path.exists():
            self.errors.append(f"Registry file not found: {self.registry_path}")
            return False
            
        try:
            with open(self.registry_path, 'r') as f:
                self.data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML syntax: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Failed to read registry file: {e}")
            return False
            
        if not isinstance(self.data, dict):
            self.errors.append("Registry must be a YAML dictionary")
            return False
            
        # Run all validation checks
        self._validate_structure()
        self._validate_version()
        self._validate_last_updated()
        self._validate_tech_stack()
        self._validate_external_apis()
        self._validate_internal_standards()
        self._validate_compliance()
        self._validate_pocketflow_patterns()
        self._validate_discovery_settings()
        self._validate_metadata()
        self._check_staleness()
        
        return len(self.errors) == 0
        
    def _validate_structure(self):
        """Validate top-level structure"""
        missing_keys = self.REQUIRED_TOP_LEVEL_KEYS - set(self.data.keys())
        if missing_keys:
            self.errors.append(f"Missing required top-level keys: {missing_keys}")
            
    def _validate_version(self):
        """Validate version format"""
        version = self.data.get('version')
        if not version:
            return
            
        if not isinstance(version, str):
            self.errors.append("Version must be a string")
        elif not version.count('.') >= 1:
            self.warnings.append("Version should follow semantic versioning (e.g., '1.0.0')")
            
    def _validate_last_updated(self):
        """Validate last_updated format"""
        last_updated = self.data.get('last_updated')
        if not last_updated:
            return
            
        # Handle both string dates and datetime.date objects from YAML parsing
        if isinstance(last_updated, str):
            try:
                datetime.strptime(last_updated, '%Y-%m-%d')
            except ValueError:
                self.errors.append("last_updated must be in YYYY-MM-DD format")
        elif hasattr(last_updated, 'year'):  # datetime.date object
            # YAML parsed it correctly as a date, which is valid
            pass
        else:
            self.errors.append("last_updated must be a date in YYYY-MM-DD format")
            
    def _validate_tech_stack(self):
        """Validate tech_stack section"""
        tech_stack = self.data.get('tech_stack', {})
        if not isinstance(tech_stack, dict):
            self.errors.append("tech_stack must be a dictionary")
            return
            
        for name, config in tech_stack.items():
            self._validate_tech_stack_entry(name, config)
            
    def _validate_tech_stack_entry(self, name: str, config: Dict[str, Any]):
        """Validate individual tech stack entry"""
        if not isinstance(config, dict):
            self.errors.append(f"Tech stack entry '{name}' must be a dictionary")
            return
            
        # Check required fields
        required_fields = {'type', 'source'}
        missing_fields = required_fields - set(config.keys())
        if missing_fields:
            self.errors.append(f"Tech stack '{name}' missing required fields: {missing_fields}")
            
        # Validate type
        if config.get('type') not in self.VALID_TECH_STACK_TYPES:
            self.warnings.append(f"Tech stack '{name}' has unexpected type: {config.get('type')}")
            
        # Validate relevance is a list
        if 'relevance' in config and not isinstance(config['relevance'], list):
            self.errors.append(f"Tech stack '{name}' relevance must be a list")
            
    def _validate_external_apis(self):
        """Validate external_apis section"""
        external_apis = self.data.get('external_apis', {})
        if not isinstance(external_apis, dict):
            self.errors.append("external_apis must be a dictionary")
            return
            
        for name, config in external_apis.items():
            self._validate_external_api_entry(name, config)
            
    def _validate_external_api_entry(self, name: str, config: Dict[str, Any]):
        """Validate individual external API entry"""
        if not isinstance(config, dict):
            self.errors.append(f"External API entry '{name}' must be a dictionary")
            return
            
        # Check required fields
        required_fields = {'type', 'source'}
        missing_fields = required_fields - set(config.keys())
        if missing_fields:
            self.errors.append(f"External API '{name}' missing required fields: {missing_fields}")
            
        # Validate type
        if config.get('type') not in self.VALID_API_TYPES:
            self.warnings.append(f"External API '{name}' has unexpected type: {config.get('type')}")
            
    def _validate_internal_standards(self):
        """Validate internal_standards section"""
        internal_standards = self.data.get('internal_standards', {})
        if not isinstance(internal_standards, dict):
            self.errors.append("internal_standards must be a dictionary")
            return
            
        for name, config in internal_standards.items():
            self._validate_internal_standard_entry(name, config)
            
    def _validate_internal_standard_entry(self, name: str, config: Dict[str, Any]):
        """Validate individual internal standard entry"""
        if not isinstance(config, dict):
            self.errors.append(f"Internal standard entry '{name}' must be a dictionary")
            return
            
        # Check required fields
        required_fields = {'type', 'source'}
        missing_fields = required_fields - set(config.keys())
        if missing_fields:
            self.errors.append(f"Internal standard '{name}' missing required fields: {missing_fields}")
            
        # Validate type
        if config.get('type') not in self.VALID_STANDARD_TYPES:
            self.warnings.append(f"Internal standard '{name}' has unexpected type: {config.get('type')}")
            
    def _validate_compliance(self):
        """Validate compliance section"""
        compliance = self.data.get('compliance', {})
        if not isinstance(compliance, dict):
            self.errors.append("compliance must be a dictionary")
            return
            
        for name, config in compliance.items():
            self._validate_compliance_entry(name, config)
            
    def _validate_compliance_entry(self, name: str, config: Dict[str, Any]):
        """Validate individual compliance entry"""
        if not isinstance(config, dict):
            self.errors.append(f"Compliance entry '{name}' must be a dictionary")
            return
            
        # Check required fields
        required_fields = {'type', 'source'}
        missing_fields = required_fields - set(config.keys())
        if missing_fields:
            self.errors.append(f"Compliance '{name}' missing required fields: {missing_fields}")
            
        # Validate type
        if config.get('type') not in self.VALID_COMPLIANCE_TYPES:
            self.warnings.append(f"Compliance '{name}' has unexpected type: {config.get('type')}")
            
    def _validate_pocketflow_patterns(self):
        """Validate pocketflow_patterns section"""
        pocketflow_patterns = self.data.get('pocketflow_patterns', {})
        if not isinstance(pocketflow_patterns, dict):
            self.errors.append("pocketflow_patterns must be a dictionary")
            return
            
        for name, config in pocketflow_patterns.items():
            self._validate_pocketflow_pattern_entry(name, config)
            
    def _validate_pocketflow_pattern_entry(self, name: str, config: Dict[str, Any]):
        """Validate individual PocketFlow pattern entry"""
        if not isinstance(config, dict):
            self.errors.append(f"PocketFlow pattern entry '{name}' must be a dictionary")
            return
            
        # Check required fields
        required_fields = {'type', 'source'}
        missing_fields = required_fields - set(config.keys())
        if missing_fields:
            self.errors.append(f"PocketFlow pattern '{name}' missing required fields: {missing_fields}")
            
        # Validate type (similar to internal standards)
        if config.get('type') not in self.VALID_STANDARD_TYPES:
            self.warnings.append(f"PocketFlow pattern '{name}' has unexpected type: {config.get('type')}")
            
        # Validate relevance is a list
        if 'relevance' in config and not isinstance(config['relevance'], list):
            self.errors.append(f"PocketFlow pattern '{name}' relevance must be a list")
            
    def _validate_discovery_settings(self):
        """Validate discovery_settings section"""
        discovery_settings = self.data.get('discovery_settings', {})
        if not isinstance(discovery_settings, dict):
            self.errors.append("discovery_settings must be a dictionary")
            return
            
        # Check required fields
        missing_fields = self.REQUIRED_DISCOVERY_SETTINGS - set(discovery_settings.keys())
        if missing_fields:
            self.errors.append(f"discovery_settings missing required fields: {missing_fields}")
            
        # Validate auto_discover is boolean
        if 'auto_discover' in discovery_settings:
            if not isinstance(discovery_settings['auto_discover'], bool):
                self.errors.append("discovery_settings.auto_discover must be a boolean")
                
        # Validate paths are lists
        for path_field in ['scan_paths', 'include_patterns', 'exclude_patterns']:
            if path_field in discovery_settings:
                if not isinstance(discovery_settings[path_field], list):
                    self.errors.append(f"discovery_settings.{path_field} must be a list")
                    
    def _validate_metadata(self):
        """Validate metadata section"""
        metadata = self.data.get('metadata', {})
        if not isinstance(metadata, dict):
            self.errors.append("metadata must be a dictionary")
            return
            
        # Check required fields
        missing_fields = self.REQUIRED_METADATA - set(metadata.keys())
        if missing_fields:
            self.errors.append(f"metadata missing required fields: {missing_fields}")
            
    def _check_staleness(self):
        """Check if registry might be stale"""
        last_updated = self.data.get('last_updated')
        if not last_updated:
            return
            
        try:
            # Handle both string dates and datetime.date objects from YAML parsing
            if isinstance(last_updated, str):
                last_update_date = datetime.strptime(last_updated, '%Y-%m-%d')
            elif hasattr(last_updated, 'year'):  # datetime.date object
                last_update_date = datetime.combine(last_updated, datetime.min.time())
            else:
                return  # Cannot process this format
            days_since_update = (datetime.now() - last_update_date).days
            
            if days_since_update > 90:
                self.warnings.append(f"Registry hasn't been updated in {days_since_update} days - consider reviewing")
            elif days_since_update > 30:
                self.warnings.append(f"Registry is {days_since_update} days old - consider reviewing")
        except ValueError:
            # Already handled in _validate_last_updated
            pass
            
    def print_results(self):
        """Print validation results"""
        if self.errors:
            print("❌ VALIDATION ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
                
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
                
        if not self.errors and not self.warnings:
            print("✅ Documentation registry is valid!")
        elif not self.errors:
            print("✅ Documentation registry structure is valid (with warnings)")


def main():
    """Main CLI entry point"""
    if len(sys.argv) != 2:
        print("Usage: python validate-docs-registry.py <registry-file>")
        print("Example: python validate-docs-registry.py .agent-os/docs-registry.yaml")
        sys.exit(1)
        
    registry_path = sys.argv[1]
    
    print(f"Validating documentation registry: {registry_path}")
    print("-" * 50)
    
    validator = DocsRegistryValidator(registry_path)
    is_valid = validator.validate()
    validator.print_results()
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()