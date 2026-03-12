export default function AuditForm({ onSubmit, loading }) {
  function handleSubmit(e) {
    e.preventDefault()
    const url = e.target.url.value.trim()
    if (url) onSubmit(url)
  }

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <h2 className="text-lg font-semibold text-white mb-1">Audit a Webpage</h2>
      <p className="text-sm text-gray-500 mb-4">Enter a URL to extract metrics and generate AI-powered insights.</p>
      <form onSubmit={handleSubmit} className="flex gap-3">
        <input
          name="url"
          type="url"
          required
          placeholder="https://example.com"
          className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-900 disabled:text-blue-400 text-white text-sm font-medium rounded-lg transition"
        >
          {loading ? 'Analysing...' : 'Run Audit'}
        </button>
      </form>
    </div>
  )
}
