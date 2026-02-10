import React from 'react';

export default function ArchitectureDiagram() {
  return (
    <div className="min-h-screen bg-gray-900 p-8 text-white">
      <h1 className="text-3xl font-bold text-center mb-8">AI Multi-Agent System with Vector DB Memory</h1>
      
      <svg viewBox="0 0 1200 800" className="w-full max-w-6xl mx-auto">
        {/* Background sections */}
        <rect x="20" y="20" width="200" height="100" rx="10" fill="#1a1a2e" stroke="#4a4a6a" strokeWidth="2"/>
        <rect x="280" y="20" width="600" height="180" rx="10" fill="#1a1a2e" stroke="#4a4a6a" strokeWidth="2"/>
        <rect x="280" y="220" width="280" height="160" rx="10" fill="#1a1a2e" stroke="#4a4a6a" strokeWidth="2"/>
        <rect x="600" y="220" width="280" height="160" rx="10" fill="#1a1a2e" stroke="#4a4a6a" strokeWidth="2"/>
        <rect x="280" y="400" width="600" height="180" rx="10" fill="#1a1a2e" stroke="#4a4a6a" strokeWidth="2"/>
        <rect x="920" y="20" width="260" height="560" rx="10" fill="#1a1a2e" stroke="#4a4a6a" strokeWidth="2"/>
        
        {/* Section Labels */}
        <text x="120" y="45" textAnchor="middle" fill="#888" fontSize="12">External API</text>
        <text x="580" y="45" textAnchor="middle" fill="#888" fontSize="12">AI Agents</text>
        <text x="420" y="245" textAnchor="middle" fill="#888" fontSize="12">Message Broker</text>
        <text x="740" y="245" textAnchor="middle" fill="#888" fontSize="12">Vector Database</text>
        <text x="580" y="425" textAnchor="middle" fill="#888" fontSize="12">Observability Stack</text>
        <text x="1050" y="45" textAnchor="middle" fill="#888" fontSize="12">Persistent Storage</text>

        {/* Claude API */}
        <rect x="50" y="60" width="140" height="50" rx="8" fill="#ef4444" stroke="#dc2626" strokeWidth="2"/>
        <text x="120" y="90" textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">☁️ Claude API</text>
        
        {/* Publishers */}
        <rect x="300" y="60" width="120" height="60" rx="8" fill="#22c55e" stroke="#16a34a" strokeWidth="2"/>
        <text x="360" y="85" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">📤 Publisher-1</text>
        <text x="360" y="105" textAnchor="middle" fill="white" fontSize="10">AI Decisions</text>
        
        <rect x="440" y="60" width="120" height="60" rx="8" fill="#22c55e" stroke="#16a34a" strokeWidth="2"/>
        <text x="500" y="85" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">📤 Publisher-2</text>
        <text x="500" y="105" textAnchor="middle" fill="white" fontSize="10">AI Decisions</text>
        
        {/* Consumers */}
        <rect x="580" y="60" width="120" height="60" rx="8" fill="#22c55e" stroke="#16a34a" strokeWidth="2"/>
        <text x="640" y="85" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">📥 Consumer-1</text>
        <text x="640" y="105" textAnchor="middle" fill="white" fontSize="10">Vector + AI</text>
        
        <rect x="720" y="60" width="120" height="60" rx="8" fill="#22c55e" stroke="#16a34a" strokeWidth="2"/>
        <text x="780" y="85" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">📥 Consumer-2</text>
        <text x="780" y="105" textAnchor="middle" fill="white" fontSize="10">Vector + AI</text>
        
        {/* Monitor */}
        <rect x="510" y="130" width="140" height="50" rx="8" fill="#22c55e" stroke="#16a34a" strokeWidth="2"/>
        <text x="580" y="155" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">🔍 Monitor</text>
        <text x="580" y="170" textAnchor="middle" fill="white" fontSize="10">Health Analysis</text>
        
        {/* RabbitMQ */}
        <rect x="320" y="270" width="120" height="50" rx="8" fill="#f97316" stroke="#ea580c" strokeWidth="2"/>
        <text x="380" y="295" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">🐰 RabbitMQ</text>
        <text x="380" y="310" textAnchor="middle" fill="white" fontSize="10">Exchange: books</text>
        
        {/* Queues */}
        <rect x="300" y="330" width="80" height="35" rx="5" fill="#fb923c" stroke="#f97316" strokeWidth="1"/>
        <text x="340" y="352" textAnchor="middle" fill="white" fontSize="10">📚 fictional</text>
        
        <rect x="400" y="330" width="100" height="35" rx="5" fill="#fb923c" stroke="#f97316" strokeWidth="1"/>
        <text x="450" y="352" textAnchor="middle" fill="white" fontSize="10">📖 non-fictional</text>
        
        {/* Qdrant */}
        <rect x="620" y="260" width="120" height="50" rx="8" fill="#a855f7" stroke="#9333ea" strokeWidth="2"/>
        <text x="680" y="285" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">🧠 Qdrant</text>
        <text x="680" y="300" textAnchor="middle" fill="white" fontSize="10">Vector DB</text>
        
        {/* Sentence Transformers */}
        <rect x="760" y="260" width="100" height="50" rx="8" fill="#a855f7" stroke="#9333ea" strokeWidth="2"/>
        <text x="810" y="280" textAnchor="middle" fill="white" fontSize="10" fontWeight="bold">🔤 Embeddings</text>
        <text x="810" y="295" textAnchor="middle" fill="white" fontSize="9">all-MiniLM-L6-v2</text>
        <text x="810" y="307" textAnchor="middle" fill="white" fontSize="8">(384 dims)</text>
        
        {/* Collection */}
        <ellipse cx="680" cy="350" rx="60" ry="25" fill="#c084fc" stroke="#a855f7" strokeWidth="2"/>
        <text x="680" y="355" textAnchor="middle" fill="white" fontSize="10">book_messages</text>
        
        {/* InfluxDB */}
        <rect x="300" y="450" width="120" height="50" rx="8" fill="#3b82f6" stroke="#2563eb" strokeWidth="2"/>
        <text x="360" y="475" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">📊 InfluxDB</text>
        <text x="360" y="490" textAnchor="middle" fill="white" fontSize="10">Metrics</text>
        
        {/* Loki */}
        <rect x="440" y="450" width="120" height="50" rx="8" fill="#3b82f6" stroke="#2563eb" strokeWidth="2"/>
        <text x="500" y="475" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">📝 Loki</text>
        <text x="500" y="490" textAnchor="middle" fill="white" fontSize="10">Logs</text>
        
        {/* Promtail */}
        <rect x="440" y="520" width="120" height="40" rx="8" fill="#60a5fa" stroke="#3b82f6" strokeWidth="2"/>
        <text x="500" y="545" textAnchor="middle" fill="white" fontSize="11" fontWeight="bold">📡 Promtail</text>
        
        {/* Grafana */}
        <rect x="580" y="450" width="120" height="50" rx="8" fill="#3b82f6" stroke="#2563eb" strokeWidth="2"/>
        <text x="640" y="475" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">📈 Grafana</text>
        <text x="640" y="490" textAnchor="middle" fill="white" fontSize="10">Dashboards</text>
        
        {/* Storage volumes */}
        {[
          { y: 80, label: "influxdb-data" },
          { y: 140, label: "rabbitmq-data" },
          { y: 200, label: "qdrant-storage" },
          { y: 260, label: "loki-data" },
          { y: 320, label: "grafana-data" }
        ].map((vol, i) => (
          <g key={i}>
            <ellipse cx="1050" cy={vol.y} rx="70" ry="20" fill="#64748b" stroke="#475569" strokeWidth="2"/>
            <text x="1050" y={vol.y + 5} textAnchor="middle" fill="white" fontSize="10">{vol.label}</text>
          </g>
        ))}
        
        {/* Connection lines */}
        {/* Publishers to Claude */}
        <path d="M300 90 L190 85" stroke="#ef4444" strokeWidth="2" fill="none" markerEnd="url(#arrowRed)"/>
        <path d="M440 90 L190 85" stroke="#ef4444" strokeWidth="2" fill="none"/>
        
        {/* Consumers to Claude */}
        <path d="M580 90 L190 85" stroke="#ef4444" strokeWidth="2" strokeDasharray="5,5" fill="none"/>
        <path d="M720 90 L190 85" stroke="#ef4444" strokeWidth="2" strokeDasharray="5,5" fill="none"/>
        
        {/* Publishers to RabbitMQ */}
        <path d="M360 120 L380 270" stroke="#f97316" strokeWidth="2" fill="none"/>
        <path d="M500 120 L380 270" stroke="#f97316" strokeWidth="2" fill="none"/>
        
        {/* RabbitMQ to Consumers */}
        <path d="M380 320 L340 330" stroke="#f97316" strokeWidth="2" fill="none"/>
        <path d="M380 320 L450 330" stroke="#f97316" strokeWidth="2" fill="none"/>
        <path d="M340 365 L640 120" stroke="#f97316" strokeWidth="2" strokeDasharray="3,3" fill="none"/>
        <path d="M450 365 L780 120" stroke="#f97316" strokeWidth="2" strokeDasharray="3,3" fill="none"/>
        
        {/* Consumers to Qdrant */}
        <path d="M640 120 L680 260" stroke="#a855f7" strokeWidth="2" fill="none"/>
        <path d="M780 120 L810 260" stroke="#a855f7" strokeWidth="2" fill="none"/>
        
        {/* Agents to InfluxDB */}
        <path d="M360 120 L360 450" stroke="#3b82f6" strokeWidth="1" strokeDasharray="3,3" fill="none"/>
        <path d="M640 120 L360 450" stroke="#3b82f6" strokeWidth="1" strokeDasharray="3,3" fill="none"/>
        
        {/* InfluxDB & Loki to Grafana */}
        <path d="M420 475 L580 475" stroke="#3b82f6" strokeWidth="2" fill="none"/>
        <path d="M560 475 L580 475" stroke="#3b82f6" strokeWidth="2" fill="none"/>
        
        {/* Arrow markers */}
        <defs>
          <marker id="arrowRed" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <path d="M0,0 L0,6 L9,3 z" fill="#ef4444"/>
          </marker>
        </defs>
        
        {/* Legend */}
        <g transform="translate(300, 620)">
          <text x="0" y="0" fill="#888" fontSize="14" fontWeight="bold">Legend:</text>
          
          <rect x="0" y="15" width="20" height="15" rx="3" fill="#22c55e"/>
          <text x="30" y="27" fill="white" fontSize="11">AI Agents</text>
          
          <rect x="120" y="15" width="20" height="15" rx="3" fill="#f97316"/>
          <text x="150" y="27" fill="white" fontSize="11">Message Broker</text>
          
          <rect x="280" y="15" width="20" height="15" rx="3" fill="#a855f7"/>
          <text x="310" y="27" fill="white" fontSize="11">Vector DB</text>
          
          <rect x="400" y="15" width="20" height="15" rx="3" fill="#3b82f6"/>
          <text x="430" y="27" fill="white" fontSize="11">Observability</text>
          
          <rect x="540" y="15" width="20" height="15" rx="3" fill="#ef4444"/>
          <text x="570" y="27" fill="white" fontSize="11">External API</text>
        </g>
        
        {/* Cost control annotations */}
        <g transform="translate(50, 620)">
          <text x="0" y="60" fill="#888" fontSize="12" fontWeight="bold">Cost Controls:</text>
          <text x="0" y="80" fill="#aaa" fontSize="10">• Publishers: 1 API call / 60s</text>
          <text x="0" y="95" fill="#aaa" fontSize="10">• Consumers: 10% of msgs, 1 call / 30s</text>
          <text x="0" y="110" fill="#aaa" fontSize="10">• Memory Hit {'>'} 0.85 = Skip API call</text>
          <text x="0" y="125" fill="#aaa" fontSize="10">• Monitor: 1 call / 120s</text>
        </g>
        
        <g transform="translate(300, 680)">
          <text x="0" y="0" fill="#888" fontSize="12" fontWeight="bold">Data Flow:</text>
          <text x="0" y="20" fill="#aaa" fontSize="10">1. Publishers → RabbitMQ (books exchange) → Queues</text>
          <text x="0" y="35" fill="#aaa" fontSize="10">2. Consumers ← Queues, generate embeddings, search Qdrant</text>
          <text x="0" y="50" fill="#aaa" fontSize="10">3. If similarity {'>'} 0.85: use cached decision (memory hit)</text>
          <text x="0" y="65" fill="#aaa" fontSize="10">4. Else: call Claude API, store decision in Qdrant</text>
          <text x="0" y="80" fill="#aaa" fontSize="10">5. All agents → metrics to InfluxDB, logs to Loki → Grafana</text>
        </g>
      </svg>
      
      <div className="mt-8 max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
        <div className="bg-green-900/50 p-4 rounded-lg border border-green-700">
          <div className="text-2xl mb-2">5</div>
          <div className="text-sm text-gray-400">AI Agents</div>
        </div>
        <div className="bg-purple-900/50 p-4 rounded-lg border border-purple-700">
          <div className="text-2xl mb-2">384</div>
          <div className="text-sm text-gray-400">Vector Dimensions</div>
        </div>
        <div className="bg-blue-900/50 p-4 rounded-lg border border-blue-700">
          <div className="text-2xl mb-2">85%</div>
          <div className="text-sm text-gray-400">Memory Threshold</div>
        </div>
        <div className="bg-orange-900/50 p-4 rounded-lg border border-orange-700">
          <div className="text-2xl mb-2">9+</div>
          <div className="text-sm text-gray-400">Docker Services</div>
        </div>
      </div>
    </div>
  );
}
