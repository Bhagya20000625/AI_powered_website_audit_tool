function MetricCard({ label, value, highlight }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
      <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">{label}</p>
      <p className={`text-2xl font-bold ${highlight ? 'text-red-400' : 'text-white'}`}>{value}</p>
    </div>
  )
}

export default function MetricsPanel({ metrics }) {
  return (
    <div>
      <h2 className="text-base font-semibold text-gray-300 mb-3 uppercase tracking-wide">Factual Metrics</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
        <MetricCard label="Word Count" value={metrics.word_count} />
        <MetricCard label="H1 / H2 / H3" value={`${metrics.h1_count} / ${metrics.h2_count} / ${metrics.h3_count}`} />
        <MetricCard label="CTAs" value={metrics.cta_count} />
        <MetricCard label="Internal Links" value={metrics.internal_links} />
        <MetricCard label="External Links" value={metrics.external_links} />
        <MetricCard label="Images" value={metrics.image_count} />
        <MetricCard
          label="Missing Alt Text"
          value={`${metrics.images_missing_alt_pct}%`}
          highlight={metrics.images_missing_alt_pct > 50}
        />
      </div>
      <div className="bg-gray-900 border border-gray-800 rounded-lg p-4 space-y-2">
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wide mb-0.5">Meta Title</p>
          <p className="text-sm text-white">{metrics.meta_title || <span className="text-red-400">Missing</span>}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wide mb-0.5">Meta Description</p>
          <p className="text-sm text-white">{metrics.meta_description || <span className="text-red-400">Missing</span>}</p>
        </div>
      </div>
    </div>
  )
}
