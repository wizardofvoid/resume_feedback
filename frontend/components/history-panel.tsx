import { formatDate } from "@/lib/format";
import type { HistoryItem } from "@/lib/types";

type Props = {
  items: HistoryItem[];
  loading: boolean;
  onClear: () => void;
  clearing: boolean;
};

export function HistoryPanel({ items, loading, onClear, clearing }: Props) {
  return (
    <section className="history-section shell" id="history" aria-labelledby="history-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow"><span /> Previous runs</p>
          <h2 id="history-title">Recent analyses</h2>
        </div>
        {items.length > 0 && (
          <button className="text-button danger" type="button" onClick={onClear} disabled={clearing}>
            {clearing ? "Clearing…" : "Clear history"}
          </button>
        )}
      </div>

      <div className="history-table" role="table" aria-label="Recent resume analyses">
        <div className="history-row history-head" role="row">
          <span role="columnheader">Date</span>
          <span role="columnheader">Contact</span>
          <span role="columnheader">Score</span>
        </div>
        {loading ? (
          <div className="history-empty">Loading history…</div>
        ) : items.length === 0 ? (
          <div className="history-empty">
            <strong>No saved runs yet.</strong>
            <span>Your completed analyses will appear here.</span>
          </div>
        ) : (
          items.map((item) => (
            <div className="history-row" role="row" key={item.id}>
              <span role="cell">{formatDate(item.created_at)}</span>
              <span role="cell" className="history-email">{item.email || "Not detected"}</span>
              <strong role="cell">{Number(item.score).toFixed(0)}</strong>
            </div>
          ))
        )}
      </div>
    </section>
  );
}
