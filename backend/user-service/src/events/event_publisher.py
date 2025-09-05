import json
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ServiceEndpoint:
    name: str
    url: str
    events: List[str]

class EventPublisher:
    _instance = None
    _service_endpoints: List[ServiceEndpoint] = []
    _event_log: List[Dict] = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls):
        """Initialize event publisher with service endpoints"""
        cls._instance._service_endpoints = [
            ServiceEndpoint(
                name="notification-service",
                url="http://localhost:8002/events",
                events=["user.created", "user.state_changed", "user.role_assigned"]
            ),
            ServiceEndpoint(
                name="enrollment-service", 
                url="http://localhost:8003/events",
                events=["user.created", "user.state_changed"]
            ),
            ServiceEndpoint(
                name="reporting-service",
                url="http://localhost:8004/events", 
                events=["user.created", "user.updated", "user.state_changed"]
            )
        ]
        print("✅ Event Publisher initialized (HTTP-based)")
    
    def publish(self, event_type: str, payload: Dict[str, Any]):
        """Publish event to interested services via HTTP"""
        event = {
            'id': self._generate_event_id(),
            'type': event_type,
            'payload': payload,
            'timestamp': datetime.now().isoformat(),
            'service': 'user-service',
            'version': '1.0'
        }
        
        # Log event locally
        self._event_log.append(event)
        print(f"📡 Publishing event: {event_type}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        # Send to interested services asynchronously
        asyncio.create_task(self._send_to_services(event))
    
    async def _send_to_services(self, event: Dict[str, Any]):
        """Send event to all interested services"""
        event_type = event['type']
        
        for service in self._service_endpoints:
            if event_type in service.events:
                try:
                    await self._send_http_event(service, event)
                except Exception as e:
                    print(f"⚠️ Failed to send event to {service.name}: {e}")
    
    async def _send_http_event(self, service: ServiceEndpoint, event: Dict[str, Any]):
        """Send event to a service via HTTP POST"""
        timeout = aiohttp.ClientTimeout(total=5)  # 5 second timeout
        
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    service.url,
                    json=event,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    if response.status == 200:
                        print(f"✅ Event sent to {service.name}")
                    else:
                        print(f"⚠️ {service.name} responded with status {response.status}")
        except asyncio.TimeoutError:
            print(f"⏰ Timeout sending event to {service.name}")
        except aiohttp.ClientError as e:
            print(f"🌐 Network error sending to {service.name}: {e}")
    
    def get_event_log(self) -> List[Dict[str, Any]]:
        """Get local event log"""
        return self._event_log.copy()
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        import uuid
        return str(uuid.uuid4())