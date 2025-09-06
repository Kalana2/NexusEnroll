import React, { createContext, useContext, useMemo, useRef } from "react";

export type EventType = "NOTIFY" | "ENROLLED" | "ERROR";
export type Listener = (payload: unknown) => void;

class Bus {
  private map = new Map<EventType, Set<Listener>>();
  on(type: EventType, fn: Listener) {
    if (!this.map.has(type)) this.map.set(type, new Set());
    this.map.get(type)!.add(fn);
    return () => this.off(type, fn);
  }
  off(type: EventType, fn: Listener) {
    this.map.get(type)?.delete(fn);
  }
  emit(type: EventType, payload?: unknown) {
    this.map.get(type)?.forEach((fn) => fn(payload));
  }
}

const BusContext = createContext<Bus | null>(null);
export const EventBusProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const busRef = useRef(new Bus());
  const value = useMemo(() => busRef.current, []);
  return <BusContext.Provider value={value}>{children}</BusContext.Provider>;
};
export const useBus = () => {
  const bus = useContext(BusContext);
  if (!bus) throw new Error("useBus must be used within EventBusProvider");
  return bus;
};
