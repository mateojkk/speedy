const valTime = document.getElementById('val-time');
const valScanned = document.getElementById('val-scanned');
const valNet = document.getElementById('val-net');
const badgeStatus = document.getElementById('badge-status');
const heatmapContainer = document.getElementById('sector-heatmap');
const signalsFeed = document.getElementById('signals-feed');
const sysLogs = document.getElementById('sys-logs');
const btnExecute = document.getElementById('btn-execute');

let execMode = false;
let knownMarketIds = new Set();
let previousState = null;

btnExecute.addEventListener('click', () => {
    execMode = !execMode;
    btnExecute.textContent = execMode ? 'Simulation: ON' : 'Simulation: OFF';
    btnExecute.className = execMode ? 'btn-primary' : 'btn-outline';
    logMsg(`Simulation toggled to: ${execMode ? 'ACTIVE' : 'OFF'}`);
});

function logMsg(msg) {
    const div = document.createElement('div');
    const now = new Date();
    const timeStr = now.toISOString().substring(11, 19);
    
    div.className = 'log-line';
    div.innerHTML = `[${timeStr}] ${msg}`;
    
    sysLogs.appendChild(div);
    sysLogs.scrollTop = sysLogs.scrollHeight;
    
    if (sysLogs.children.length > 50) {
        sysLogs.removeChild(sysLogs.firstChild);
    }
}

function renderHeatmap(sectors) {
    heatmapContainer.innerHTML = '';

    sectors.forEach(sec => {
        const div = document.createElement('div');
        div.className = 'card-base';
        
        div.innerHTML = `
            <div class="status-badge">${sec.sector}</div>
            <h3 class="card-title">${sec.avg_mom > 0 ? '+' : ''}${sec.avg_mom.toFixed(1)}% Momentum</h3>
            <p class="card-tagline">Aggregated across active markets</p>
            <div class="card-metrics">
                <div class="metric-line">Volume: <strong>$${sec.vol.toLocaleString()}</strong></div>
            </div>
        `;
        heatmapContainer.appendChild(div);
    });
}

function renderFeed(signals) {
    signalsFeed.innerHTML = '';

    if (signals.length === 0) {
        signalsFeed.innerHTML = '<div style="color: var(--muted); padding: 1.75rem;">No active opportunities currently matching criteria.</div>';
        return;
    }

    signals.forEach(sig => {
        const isNew = !knownMarketIds.has(sig.id);
        if (isNew) knownMarketIds.add(sig.id);

        const row = document.createElement('a');
        row.href = `https://polymarket.com/event/${sig.slug || ''}`;
        row.target = '_blank';
        row.className = 'card-base';

        row.innerHTML = `
            <div class="tag-cloud">
               ${sig.tags.map(t => `<span class="chip">${t.toLowerCase()}</span>`).join('')}
               <span class="chip">${sig.type.replace('_', ' ').toLowerCase()}</span>
            </div>
            
            <h3 class="card-title">${sig.question}</h3>
            <div class="card-tagline">Tradability Score: ${Math.round(sig.score)}/100</div>

            <div class="card-metrics">
                <div class="metric-line">Depth: <strong>$${sig.metrics.liquidity.toLocaleString()}</strong></div>
                <div class="metric-line">Spread: <strong>$${sig.metrics.spread.toFixed(3)}</strong></div>
                <div class="metric-line">EV Cap: <strong>$${sig.metrics.est_ev_cap.toFixed(2)}</strong></div>
            </div>
        `;
        signalsFeed.appendChild(row);

        if (execMode && isNew && sig.score > 70) {
            logMsg(`Alert: Fired simulated order on '${sig.id.substring(0,8)}...' (EV: $${sig.metrics.est_ev_cap.toFixed(2)})`);
        }
    });

    if (valScanned) valScanned.textContent = signals.length + ' active execution targets';
}

function updateState(data) {
    // Hidden values used just for logic now
    if (valTime) {
        const d = new Date(data.last_updated);
        valTime.textContent = d.toISOString().substring(11, 19);
    }

    renderHeatmap(data.heatmap);
    renderFeed(data.signals);

    if (!previousState || previousState.last_updated !== data.last_updated) {
        logMsg(`Sync complete: indexed ${data.signals.length} actionable markets.`);
        previousState = data;
    }
}

function fetchCore() {
    fetch('signals.json?t=' + Date.now())
        .then(res => {
            if (!res.ok) throw new Error('Network response failure');
            return res.json();
        })
        .then(data => {
            if (valNet) valNet.textContent = 'Stable Connection';
            updateState(data);
        })
        .catch(err => {
            if (valNet) valNet.textContent = 'Connection Dropped';
            logMsg(`Connection Error: ${err.message}`);
        });
}

fetchCore();
setInterval(fetchCore, 5000);
