import { APP_NAME } from "@/lib/brand";

export function BrandWordmark() {
  const splitAt = Math.max(1, APP_NAME.length - 3);

  return (
    <span className="wordmark" aria-label={APP_NAME}>
      <span aria-hidden="true">{APP_NAME.slice(0, splitAt)}</span>
      <span className="wordmark-highlight" aria-hidden="true">
        {APP_NAME.slice(splitAt)}
      </span>
    </span>
  );
}
