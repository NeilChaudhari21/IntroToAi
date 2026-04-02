const STORAGE_KEY = 'workoutTrackerEntries';

const form = document.getElementById('exercise-form');
const nameInput = document.getElementById('exercise-name');
const weightInput = document.getElementById('exercise-weight');
const setsInput = document.getElementById('exercise-sets');
const repsInput = document.getElementById('exercise-reps');
const dateInput = document.getElementById('exercise-date');
const logBody = document.getElementById('log-body');
const stats = document.getElementById('stats');
const chartCtx = document.getElementById('progress-chart').getContext('2d');
let chart;

const parseEntries = () => JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
const saveEntries = (entries) => localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));

const formatDateString = (date) => {
  const d = new Date(date);
  if (isNaN(d)) return date;
  return d.toLocaleDateString([], { year: 'numeric', month: 'short', day: 'numeric' });
};

function renderLog() {
  const entries = parseEntries().sort((a,b) => new Date(a.date) - new Date(b.date));
  logBody.innerHTML = '';
  let totalVolume = 0;
  let maxWeight = 0;
  let maxSets = 0;
  let maxReps = 0;

  for (const entry of entries) {
    const row = document.createElement('tr');
    const volume = entry.weight * entry.sets * entry.reps;
    totalVolume += volume;
    maxWeight = Math.max(maxWeight, entry.weight);
    maxSets = Math.max(maxSets, entry.sets);
    maxReps = Math.max(maxReps, entry.reps);

    const rowHtml = `
      <td>${formatDateString(entry.date)}</td>
      <td>${entry.name}</td>
      <td>${entry.weight}</td>
      <td>${entry.sets}</td>
      <td>${entry.reps}</td>
      <td>${volume}</td>
      <td><button class="remove-btn" data-id="${entry.id}">Remove</button></td>
    `;
    row.innerHTML = rowHtml;
    logBody.appendChild(row);
  }

  stats.innerHTML = entries.length === 0
    ? '<span>No entries yet. Add your first workout!</span>'
    : `<span>Total Sessions: ${entries.length}</span>
       <span>Total Volume: ${totalVolume}</span>
       <span>PR Weight: ${maxWeight} lbs</span>
       <span>Max Sets: ${maxSets}</span>
       <span>Max Reps: ${maxReps}</span>`;

  document.querySelectorAll('.remove-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      deleteEntry(id);
    })
  });

  drawChart(entries);
}

function deleteEntry(id) {
  const entries = parseEntries().filter((e) => e.id !== id);
  saveEntries(entries);
  renderLog();
}

function drawChart(entries) {
  const dateKeys = [...new Set(entries.map((e) => e.date))].sort((a, b) => new Date(a) - new Date(b));
  const dateLabels = dateKeys.map((d) => formatDateString(d));

  const series = {};
  entries.forEach((entry) => {
    if (!series[entry.name]) series[entry.name] = {};
    const existing = series[entry.name][entry.date];
    series[entry.name][entry.date] = existing ? Math.max(existing, entry.weight) : entry.weight;
  });

  const datasets = Object.entries(series).map(([exercise, values], idx) => {
    const colors = ['#2563eb', '#ea580c', '#16a34a', '#db2777', '#0ea5e9', '#78350f', '#1d4ed8', '#047857'];
    return {
      label: exercise,
      data: dateKeys.map((date) => (values[date] ?? null)),
      borderColor: colors[idx % colors.length],
      backgroundColor: colors[idx % colors.length],
      tension: 0.2,
      fill: false,
      borderWidth: 2,
      pointRadius: 5,
      spanGaps: true,
    };
  });

  const chartData = {
    labels: dateLabels,
    datasets,
  };

  const options = {
    responsive: true,
    scales: {
      x: { title: { display: true, text: 'Date' } },
      y: { beginAtZero: true, title: { display: true, text: 'Max Weight (lbs)' } }
    },
    plugins: { legend: { position: 'top' }, tooltip: { mode: 'index', intersect: false } }
  };

  if (!chart) {
    chart = new Chart(chartCtx, { type: 'line', data: chartData, options });
  } else {
    chart.data = chartData;
    chart.options = options;
    chart.update();
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const newEntry = {
    id: crypto.randomUUID(),
    name: nameInput.value.trim(),
    weight: Number(weightInput.value),
    sets: Number(setsInput.value),
    reps: Number(repsInput.value),
    date: dateInput.value,
    createdAt: new Date().toISOString(),
  };

  if (!newEntry.name) return;

  const entries = parseEntries();
  entries.push(newEntry);
  saveEntries(entries);

  form.reset();
  dateInput.valueAsDate = new Date();
  renderLog();
});

dateInput.valueAsDate = new Date();
renderLog();
