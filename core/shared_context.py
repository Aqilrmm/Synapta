
import asyncio
import logging
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

class SharedContext:
    """Shared context for inter-agent data sharing"""
    
    def __init__(self):
        self.logger = logging.getLogger("shared_context")
        self._data = {}
        self._locks = {}
        self._timestamps = {}
        self._ttl = {}  # Time-to-live for data
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in shared context"""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        
        async with self._locks[key]:
            self._data[key] = value
            self._timestamps[key] = datetime.now()
            if ttl:
                self._ttl[key] = datetime.now() + timedelta(seconds=ttl)
            
            self.logger.debug(f"📝 Set context: {key}")
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from shared context"""
        # Check TTL
        if key in self._ttl and datetime.now() > self._ttl[key]:
            await self.delete(key)
            return default
        
        if key not in self._locks:
            return default
        
        async with self._locks[key]:
            return self._data.get(key, default)
    
    async def delete(self, key: str):
        """Delete value from shared context"""
        if key in self._locks:
            async with self._locks[key]:
                self._data.pop(key, None)
                self._timestamps.pop(key, None)
                self._ttl.pop(key, None)
            
            del self._locks[key]
            self.logger.debug(f"🗑️  Deleted context: {key}")
    
    async def get_all_keys(self) -> list:
        """Get all available keys"""
        # Clean expired keys first
        await self._cleanup_expired()
        return list(self._data.keys())
    
    async def _cleanup_expired(self):
        """Clean up expired data"""
        now = datetime.now()
        expired_keys = [
            key for key, expiry in self._ttl.items() 
            if now > expiry
        ]
        
        for key in expired_keys:
            await self.delete(key)
    
    async def update(self, key: str, updater_func, default: Any = None):
        """Atomically update a value using a function"""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        
        async with self._locks[key]:
            current_value = self._data.get(key, default)
            new_value = updater_func(current_value)
            self._data[key] = new_value
            self._timestamps[key] = datetime.now()
            
            return new_value