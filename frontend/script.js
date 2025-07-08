document.getElementById('queryForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const query = document.getElementById('userQuery').value;
  const responseText = document.getElementById('responseText');
  const graphInfoTable = document.getElementById('graphInfoTable');
  const graphVisualization = document.getElementById('graph-visualization');

  responseText.textContent = "Loading...";
  graphInfoTable.textContent = "";
  graphVisualization.innerHTML = "";

  try {
    // 1) POST /query per ottenere la risposta testuale
    const res = await fetch('/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });

    const data = await res.json();

    responseText.textContent = data.response || 'No answer';
    // graphInfo.textContent = JSON.stringify(data.graph_info, null, 2) || 'No graph info';
    renderGraphInfoTable(data.graph_info);

    // Usa direttamente i nodi e gli archi restituiti dalla stessa risposta
    if (data.nodes && data.edges) {
      console.log("NODES", data.nodes);
      console.log("EDGES", data.edges);
      drawGraph(data.nodes, data.edges);
    } else {
      graphVisualization.innerHTML = "<p>No graph data available</p>";
    }


  } catch (err) {
    responseText.textContent = 'Error: ' + err.message;
  }
});


function drawGraph(nodes, edges) {
  const container = document.getElementById('graph-visualization');

  // ⚠️ vis-network vuole "from" e "to", NON "from_"
  const correctedEdges = edges.map(e => ({
    from: e.from,
    to: e.to,
    label: e.label
  }));

  const data = {
    nodes: new vis.DataSet(nodes),
    edges: new vis.DataSet(correctedEdges),
  };

  const options = {
    layout: {
      improvedLayout: true
    },
    edges: {
      arrows: { to: { enabled: true, scaleFactor: 0.5 } },
      smooth: {
        type: "dynamic"
      }
    },
    nodes: {
      shape: 'dot',
      size: 15,
      font: {
        size: 14,
        color: '#000'
      },
    },
    physics: {
      stabilization: false,
      barnesHut: {
        gravitationalConstant: -30000,
        springLength: 100
      }
    }
  };

  const network = new vis.Network(container, data, options);
}

function renderGraphInfoTable(graphInfoTable) {
  const container = document.getElementById('graphInfoTable');
  container.innerHTML = ''; // svuota prima

  if (!graphInfoTable || graphInfoTable.length === 0) {
    container.innerHTML = "<p>No graph info available</p>";
    return;
  }

  // Ottieni tutte le keys uniche come intestazioni colonne
  const columns = [...new Set(graphInfoTable.flatMap(obj => Object.keys(obj)))];

  // Crea tabella
  const table = document.createElement('table');
  table.style.width = "100%";
  table.style.borderCollapse = "collapse";

  // Header
  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  columns.forEach(col => {
    const th = document.createElement('th');
    th.classList.add('pokedex-th');
    if (col === 'p.name' || col === 'count(p)') {
      th.textContent = 'Pokémon';
    } else if (col === 't.type' || col === 'count(t)') {
      th.textContent = 'Types';
    } else {
      th.textContent = col;
    }
    th.style.border = "1px solid #ccc";
    th.style.padding = "8px";
    th.style.backgroundColor = "#f0f0f0";
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Body
  const tbody = document.createElement('tbody');
  graphInfoTable.forEach(row => {
    const tr = document.createElement('tr');
    columns.forEach(col => {
      const td = document.createElement('td');
      td.textContent = row[col] !== undefined ? row[col] : '';
      td.style.border = "1px solid #ccc";
      td.style.padding = "6px";
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  container.appendChild(table);
}
