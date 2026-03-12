const INSIGHT_LABELS = {
  seo_structure: 'SEO Structure',
  messaging_clarity: 'Messaging Clarity',
  cta_usage: 'CTA Usage',
  content_depth: 'Content Depth',
  ux_concerns: 'UX & Structural Concerns',
}

export default function InsightsPanel({ insights, recommendations }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-base font-semibold text-gray-300 mb-3 uppercase tracking-wide">AI Insights</h2>
        <div className="space-y-3">
          {Object.entries(insights).map(([key, value]) => (
            <div key={key} className="bg-gray-900 border border-gray-800 rounded-lg p-4">
              <p className="text-xs font-semibold text-blue-400 uppercase tracking-wide mb-1">{INSIGHT_LABELS[key]}</p>
              <p className="text-sm text-gray-300 leading-relaxed">{value}</p>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-base font-semibold text-gray-300 mb-3 uppercase tracking-wide">Recommendations</h2>
        <div className="space-y-3">
          {recommendations.map((rec) => (
            <div key={rec.priority} className="bg-gray-900 border border-gray-800 rounded-lg p-4 flex gap-4">
              <div className="flex-shrink-0 w-7 h-7 rounded-full bg-blue-600 text-white text-xs font-bold flex items-center justify-center">
                {rec.priority}
              </div>
              <div>
                <p className="text-sm font-medium text-white mb-1">{rec.recommendation}</p>
                <p className="text-sm text-gray-400 leading-relaxed">{rec.reasoning}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
