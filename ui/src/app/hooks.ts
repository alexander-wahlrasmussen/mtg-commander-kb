import { useEffect, useState } from "react";
import { track } from "./inflight";

export interface Status {
  text: string;
  variant: "default" | "busy" | "ok" | "err";
}

/** Run `fetcher` (debounced) whenever `deps` change; expose data + a status badge state. */
export function useDebouncedData<T>(
  fetcher: () => Promise<T>,
  deps: unknown[],
  okText: (d: T) => string,
  ms = 220,
) {
  const [data, setData] = useState<T | null>(null);
  const [status, setStatus] = useState<Status>({ text: "ready", variant: "default" });
  useEffect(() => {
    let alive = true;
    const t = setTimeout(async () => {
      setStatus({ text: "running…", variant: "busy" });
      try {
        const d = await track(fetcher());
        if (!alive) return;
        setData(d);
        setStatus({ text: okText(d), variant: "ok" });
      } catch (e) {
        if (alive) setStatus({ text: "error: " + (e as Error).message, variant: "err" });
      }
    }, ms);
    return () => {
      alive = false;
      clearTimeout(t);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return { data, status };
}

export const kfmt = (n: number) => (n >= 1000 ? n / 1000 + "k" : "" + n);
