import React, { useEffect, useState } from 'react'
import { useBus } from './../patterns/observer/EventBus'


export default function NotificationsPanel() {
const bus = useBus()
const [items, setItems] = useState<string[]>([])
useEffect(() => bus.on('NOTIFY', (msg) => setItems(i => [String(msg), ...i].slice(0, 3))), [])
return (
<div className="flex items-center gap-2">
<span>🔔</span>
<div className="text-sm">{items[0] ?? 'No new notifications'}</div>
</div>
)
}