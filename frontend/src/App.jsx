import { useState } from 'react'
import AuditForm from './components/AuditForm'
import MetricsPanel from './components/MetricsPanel'
import InsightsPanel from './components/InsightsPanel'
import PromptLogPanel from './components/PromptLogPanel'

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleAudit(url) {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await fetch('http://127.0.0.1:8000/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Audit failed')
      }
      const data = await res.json()
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  function handleDownload() {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'audit-report.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-white">Website Audit Tool</h1>
            <p className="text-xs text-gray-500 mt-0.5">Powered by EIGHT25MEDIA &times; Groq AI</p>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-10">
        <AuditForm onSubmit={handleAudit} loading={loading} />

        {error && (
          <div className="mt-6 p-4 bg-red-950 border border-red-700 rounded-lg text-red-300 text-sm">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-10 space-y-8">
            <div className="flex justify-end">
              <button
                onClick={handleDownload}
                className="text-sm px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg border border-gray-700 transition"
              >
                Download JSON Report
              </button>
            </div>
            <MetricsPanel metrics={result.metrics} />
            <InsightsPanel insights={result.insights} recommendations={result.recommendations} />
            <PromptLogPanel log={result.prompt_log} />
          </div>
        )}
      </main>
    </div>
  )
}
