#!/usr/bin/env python3
"""
Performance optimization module for Winpatable
Includes caching, benchmarking, and profiling utilities
"""

import time
import json
import functools
from pathlib import Path
from typing import Dict, Any, Callable, Optional
from datetime import datetime, timedelta
import statistics


class PerformanceCache:
    """Simple caching system for expensive operations"""
    
    def __init__(self, cache_dir: str = None):
        """Initialize cache"""
        if cache_dir is None:
            cache_dir = str(Path.home() / ".cache" / "winpatable")
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "perf_cache.json"
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load cache from disk"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except:
            pass
    
    def get(self, key: str, max_age_hours: int = 24) -> Optional[Any]:
        """Get cached value if not expired"""
        if key not in self.cache:
            return None
        
        cached = self.cache[key]
        age = datetime.now() - datetime.fromisoformat(cached['timestamp'])
        
        if age > timedelta(hours=max_age_hours):
            del self.cache[key]
            self._save_cache()
            return None
        
        return cached['value']
    
    def set(self, key: str, value: Any):
        """Cache a value"""
        self.cache[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        self._save_cache()
    
    def invalidate(self, key: str = None):
        """Invalidate cache entry or all cache"""
        if key:
            self.cache.pop(key, None)
        else:
            self.cache.clear()
        self._save_cache()


class PerformanceBenchmark:
    """Measure and log performance metrics"""
    
    def __init__(self):
        """Initialize benchmark tracker"""
        self.metrics: Dict[str, list] = {}
        self.start_times: Dict[str, float] = {}
    
    def start(self, name: str):
        """Start timing a metric"""
        self.start_times[name] = time.time()
    
    def end(self, name: str) -> float:
        """End timing and record metric"""
        if name not in self.start_times:
            return 0.0
        
        elapsed = time.time() - self.start_times[name]
        
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append(elapsed)
        del self.start_times[name]
        
        return elapsed
    
    def get_stats(self, name: str) -> Dict[str, float]:
        """Get statistics for a metric"""
        if name not in self.metrics or not self.metrics[name]:
            return {}
        
        times = self.metrics[name]
        return {
            'count': len(times),
            'min': min(times),
            'max': max(times),
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0.0
        }
    
    def get_all_stats(self) -> Dict[str, Dict]:
        """Get all statistics"""
        return {name: self.get_stats(name) for name in self.metrics}
    
    def print_summary(self):
        """Print performance summary"""
        print("\n" + "="*70)
        print("PERFORMANCE SUMMARY")
        print("="*70 + "\n")
        
        for name, stats in self.get_all_stats().items():
            if not stats:
                continue
            print(f"{name}:")
            print(f"  Count: {stats['count']}")
            print(f"  Min:   {stats['min']*1000:.2f}ms")
            print(f"  Max:   {stats['max']*1000:.2f}ms")
            print(f"  Mean:  {stats['mean']*1000:.2f}ms")
            print(f"  Median:{stats['median']*1000:.2f}ms")
            if stats['stdev'] > 0:
                print(f"  StdDev:{stats['stdev']*1000:.2f}ms")
            print()


def cached(max_age_hours: int = 24, cache_dir: str = None):
    """Decorator for caching function results"""
    cache = PerformanceCache(cache_dir)
    
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and args
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            result = cache.get(cache_key, max_age_hours)
            if result is not None:
                return result
            
            # Compute and cache
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result
        
        return wrapper
    return decorator


def timed(benchmark: PerformanceBenchmark = None):
    """Decorator for timing function execution"""
    if benchmark is None:
        benchmark = PerformanceBenchmark()
    
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            benchmark.start(func.__name__)
            result = func(*args, **kwargs)
            benchmark.end(func.__name__)
            return result
        
        return wrapper
    return decorator


class ConfigurationProfile:
    """Pre-built configuration profiles for different use cases"""
    
    PROFILES = {
        'gaming': {
            'name': 'Gaming Optimization',
            'description': 'Optimized for game compatibility and performance',
            'settings': {
                'esync': True,
                'fsync': True,
                'dxvk': True,
                'gpu_acceleration': True,
                'audio_lowlatency': True,
                'wine_min': '8.0',
                'proton_min': '8.0'
            },
            'recommended_apps': ['ea-app', 'valorant', 'r6siege', 'unity', 'unreal'],
            'tweaks': [
                'Enable ESYNC for better performance',
                'Enable FSYNC if kernel supports it',
                'Use DXVK for DirectX acceleration',
                'Enable GPU acceleration',
                'Reduce audio latency for competitive gaming'
            ]
        },
        'creative': {
            'name': 'Creative Professional',
            'description': 'Optimized for creative applications (Adobe, 3D, video)',
            'settings': {
                'esync': True,
                'dxvk': True,
                'gpu_acceleration': True,
                'cuda_support': True,
                'color_management': True,
                'wine_min': '7.5',
                'proton_min': '7.0'
            },
            'recommended_apps': [
                'photoshop', 'lightroom', 'illustrator', 'aftereffects', 'indesign',
                'premiere', 'paintnet', 'figma', '3dsmax', 'maya'
            ],
            'tweaks': [
                'Enable GPU acceleration for faster rendering',
                'Configure color management for accurate reproduction',
                'Increase memory limits for large projects',
                'Enable ESYNC for smooth interaction',
                'Use high-performance GPU drivers'
            ]
        },
        'business': {
            'name': 'Business & Productivity',
            'description': 'Optimized for office and business applications',
            'settings': {
                'esync': True,
                'dxvk': False,
                'gpu_acceleration': False,
                'stability': True,
                'wine_min': '7.0',
                'proton_min': '6.5'
            },
            'recommended_apps': [
                'office', 'visio', 'teams', 'sharepoint', 'access',
                'quickbooks', 'turbotax', 'tableau', 'powerbi'
            ],
            'tweaks': [
                'Focus on stability over performance',
                'Enable basic ESYNC for responsiveness',
                'Disable GPU acceleration (not needed)',
                'Use standard CSMT settings',
                'Keep Wine environment clean'
            ]
        },
        'development': {
            'name': 'Development & Programming',
            'description': 'Optimized for IDEs and development tools',
            'settings': {
                'esync': True,
                'dxvk': False,
                'gpu_acceleration': False,
                'wine_min': '7.0',
                'proton_min': '6.5'
            },
            'recommended_apps': [
                'visualstudio', 'jetbrains', 'notepad++', 'unity', 'unreal'
            ],
            'tweaks': [
                'Enable ESYNC for editor responsiveness',
                'Disable GPU features (not needed)',
                'Use standard Wine configuration',
                'Ensure .NET runtime compatibility',
                'Configure debugger support'
            ]
        },
        'audio': {
            'name': 'Audio Production',
            'description': 'Optimized for DAWs and audio software',
            'settings': {
                'esync': True,
                'fsync': True,
                'audio_lowlatency': True,
                'rtc_priority': True,
                'wine_min': '7.2',
                'proton_min': '6.5'
            },
            'recommended_apps': [
                'protools', 'cubase', 'reason', 'ableton', 'audition'
            ],
            'tweaks': [
                'Enable ESYNC and FSYNC for low latency',
                'Configure JACK for professional audio',
                'Increase RT priority for audio threads',
                'Use high-performance audio drivers',
                'Disable unnecessary background processes'
            ]
        }
    }
    
    @classmethod
    def get_profile(cls, name: str) -> Optional[Dict]:
        """Get a configuration profile"""
        return cls.PROFILES.get(name.lower())
    
    @classmethod
    def list_profiles(cls) -> Dict:
        """List all available profiles"""
        return {
            name: {
                'description': profile['description'],
                'apps': len(profile['recommended_apps'])
            }
            for name, profile in cls.PROFILES.items()
        }
    
    @classmethod
    def apply_profile(cls, name: str) -> bool:
        """Apply a configuration profile"""
        profile = cls.get_profile(name)
        if not profile:
            return False
        
        print(f"\nApplying profile: {profile['name']}")
        print(f"Description: {profile['description']}\n")
        
        print("Configuration settings:")
        for key, value in profile['settings'].items():
            print(f"  {key}: {value}")
        
        print("\nRecommended tweaks:")
        for i, tweak in enumerate(profile['tweaks'], 1):
            print(f"  {i}. {tweak}")
        
        print(f"\nRecommended applications ({len(profile['recommended_apps'])}):")
        for app in profile['recommended_apps']:
            print(f"  • {app}")
        
        return True


if __name__ == "__main__":
    # Demo: Show all profiles
    print("\n" + "="*70)
    print("WINPATABLE CONFIGURATION PROFILES")
    print("="*70 + "\n")
    
    profiles = ConfigurationProfile.list_profiles()
    for name, info in profiles.items():
        print(f"{name.upper()}")
        print(f"  Description: {info['description']}")
        print(f"  Recommended apps: {info['apps']}\n")
