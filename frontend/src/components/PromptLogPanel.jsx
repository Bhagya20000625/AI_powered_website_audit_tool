import { useState } from 'react'

function LogSection({ title, content }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="border border-gray-800 rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 bg-gray-900 hover:bg-gray-800 transition text-left"
      >
        <span className="text-sm font-medium text-gray-300">{title}</span>
        <span className="text-gray-500 text-xs">{open ? '▲ Hide' : '▼ Show'}</span>
      </button>
      {open && (
        <pre className="bg-gray-950 text-xs text-gray-400 p-4 overflow-x-auto whitespace-pre-wrap leading-relaxed">
          {content}
        </pre>
      )}
    </div>
  )
}

export default function PromptLogPanel({ log }) {
  return (
    <div>
      <h2 className="text-base font-semibold text-gray-300 mb-3 uppercase tracking-wide">Prompt Logs</h2>
      <div className="space-y-2">
        <LogSection title="System Prompt" content={log.system_prompt} />
        <LogSection title="User Prompt (with injected metrics)" content={log.user_prompt} />
        <LogSection title="Raw Model Output" content={log.raw_model_output} />
      </div>
    </div>
  )
}
