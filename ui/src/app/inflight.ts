import { useEffect, useState } from "react";

// Global in-flight counter so the top ProgressBar reflects any pending request.
let count = 0;
const subs = new Set<(busy: boolean) => void>();
const emit = () => subs.forEach((f) => f(count > 0));

export function track<T>(p: Promise<T>): Promise<T> {
  count++;
  emit();
  return p.finally(() => {
    count--;
    emit();
  });
}

export function useBusy(): boolean {
  const [busy, setBusy] = useState(count > 0);
  useEffect(() => {
    subs.add(setBusy);
    return () => {
      subs.delete(setBusy);
    };
  }, []);
  return busy;
}
