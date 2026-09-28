type QuotaNotice = {
  resetsOn: string | null;
};

export function QuotaDialog({ notice, onClose }: { notice: QuotaNotice; onClose: () => void }) {
  const when = notice.resetsOn ? formatResetDate(notice.resetsOn) : "one month from your last window";
  return (
    <div className="fixed inset-0 z-20 flex items-center justify-center bg-[#0c1f1a]/40 p-4" role="presentation" onClick={onClose}>
      <div
        className="w-full max-w-md rounded-xl bg-white p-6 shadow-lg"
        role="dialog"
        aria-modal="true"
        aria-labelledby="quota-title"
        onClick={(event) => event.stopPropagation()}
      >
        <h2 id="quota-title" className="text-lg font-bold text-[#0c1f1a]">
          Out of quota for the free trial
        </h2>
        <ul className="mt-3 space-y-2 text-sm text-[#35584a]">
          <li>Wait until {when} for the allowance to reset.</li>
          <li>Or upgrade to the Pro plan.</li>
        </ul>
        <button type="button" className="mt-5 rounded-lg bg-[#0c1f1a] px-4 py-2 text-sm text-white" onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
}

function formatResetDate(iso: string): string {
  const [year, month, day] = iso.split("-").map(Number);
  if (!year || !month || !day) return iso;
  return new Date(year, month - 1, day).toLocaleDateString(undefined, {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}
