const fasteners = [
  {
    id: 'hex-bolt',
    name: 'Hex Bolt',
    description:
      'A six-sided headed bolt used with a nut or tapped hole. Ideal for machine assemblies, tooling, and structural connections where high clamping force is required.',
    applications: ['Heavy equipment', 'Machine frames', 'Tooling plates'],
    materials: ['Alloy steel', 'Stainless steel', 'Zinc-plated steel'],
    specs: {
      Thread: 'Metric coarse M6–M24 or UNC 1/4"–1"',
      Head: 'Hex external drive',
      Standard: 'ISO 4014 / ASME B18.2.1',
      Finish: 'Plain, zinc, or black oxide',
    },
    image: 'assets/fasteners/hex-bolt.svg',
    script: 'python/python_fastener_export.py --fastener hex_bolt --diameter 12 --length 45',
  },
  {
    id: 'socket-cap-screw',
    name: 'Socket Head Cap Screw',
    description:
      'A cylindrical head fastener with an internal hex drive. Provides high tensile strength and the ability to be installed in tight spaces with an Allen key.',
    applications: [
      'Robotics and automation assemblies',
      'Fixtures and modular tooling',
      'Precision mechanical assemblies',
    ],
    materials: ['Alloy steel (12.9)', 'Stainless steel', 'Titanium'],
    specs: {
      Thread: 'Metric M3–M20 or UNC #4–3/4"',
      Head: 'Cylindrical, internal hex',
      Standard: 'ISO 4762 / ASME B18.3',
      Finish: 'Plain, black oxide, passivated',
    },
    image: 'assets/fasteners/socket-cap-screw.svg',
    script: 'python/python_fastener_export.py --fastener socket_cap --diameter 8 --length 30',
  },
  {
    id: 'hex-nut',
    name: 'Hex Nut',
    description:
      'A hexagonal nut that pairs with bolts or threaded rods. Commonly used to clamp assemblies together and often combined with washers to distribute load.',
    applications: ['General fabrication', 'Structural frames', 'Maintenance'],
    materials: ['Low-carbon steel', 'Stainless steel', 'Nylon insert variants'],
    specs: {
      Thread: 'Metric M6–M30 or UNC 1/4"–1-1/4"',
      Height: '0.8× to 1× nominal thread size',
      Standard: 'ISO 4032 / ASME B18.2.2',
      Finish: 'Plain, zinc, galvanized',
    },
    image: 'assets/fasteners/hex-nut.svg',
    script: 'python/python_fastener_export.py --fastener hex_nut --diameter 16',
  },
  {
    id: 'flat-washer',
    name: 'Flat Washer',
    description:
      'A thin, flat disk with a central hole placed under bolt or screw heads. Distributes clamping load, prevents surface damage, and covers oversized holes.',
    applications: ['Sheet metal work', 'Wood assemblies', 'Maintenance repair'],
    materials: ['Mild steel', 'Stainless steel', 'Nylon'],
    specs: {
      Standard: 'ISO 7089 / ASME B18.21.1',
      Type: 'Type A wide pattern',
      Thickness: '1.6 mm – 3.0 mm typical',
      Finish: 'Plain, zinc-plated, black oxide',
    },
    image: 'assets/fasteners/flat-washer.svg',
    script: 'python/python_fastener_export.py --fastener flat_washer --diameter 12 --outer 24',
  },
  {
    id: 'blind-rivet',
    name: 'Blind Rivet',
    description:
      'A permanent mechanical fastener installed from one side. Pulling the mandrel expands the rivet body, clamping sheets or components together.',
    applications: ['Sheet metal enclosures', 'Aerospace skins', 'Appliance fabrication'],
    materials: ['Aluminum', 'Steel', 'Monel'],
    specs: {
      Body: 'Open end, dome head',
      GripRange: '1.6 mm – 6.4 mm',
      Standard: 'ISO 15979 / IFI 114',
      Tooling: 'Compatible with standard blind rivet pullers',
    },
    image: 'assets/fasteners/blind-rivet.svg',
    script: 'python/python_fastener_export.py --fastener blind_rivet --diameter 4.8 --grip 6.0',
  },
];

const selectEl = document.querySelector('#fastener-select');
const detailsEl = document.querySelector('#fastener-details');
const imageEl = document.querySelector('#fastener-image');
const metaEl = document.querySelector('#fastener-meta');

function renderSelect() {
  selectEl.innerHTML = fasteners
    .map(
      (fastener) =>
        `<option value="${fastener.id}">${fastener.name}</option>`
    )
    .join('');
}

function renderDetails(fastener) {
  const applicationTags = fastener.applications
    .map((app) => `<span class="tag">${app}</span>`)
    .join('');

  const materialTags = fastener.materials
    .map((material) => `<span class="tag">${material}</span>`)
    .join('');

  detailsEl.innerHTML = `
    <p class="details__desc">${fastener.description}</p>
    <div>
      <h3>Common applications</h3>
      <div class="tag-list">${applicationTags}</div>
    </div>
    <div>
      <h3>Typical materials</h3>
      <div class="tag-list">${materialTags}</div>
    </div>
  `;
}

function renderPreview(fastener) {
  imageEl.src = fastener.image;
  imageEl.alt = `${fastener.name} preview`;

  const specRows = Object.entries(fastener.specs)
    .map(
      ([label, value]) =>
        `<tr><th>${label}</th><td>${value}</td></tr>`
    )
    .join('');

  metaEl.innerHTML = `
    <div>
      <h3>Specification snapshot</h3>
      <table class="spec-table">
        <tbody>
          ${specRows}
        </tbody>
      </table>
    </div>
    <div>
      <h3>FreeCAD export command</h3>
      <pre class="code-block">${fastener.script}</pre>
      <p class="details__desc">
        Use the <code>python_fastener_export.py</code> helper script to export
        neutral <code>.step</code> and <code>.stl</code> references. Replace the
        parameters to match your production hardware, then refresh the gallery.
      </p>
    </div>
  `;
}

function updateFastener() {
  const fastener = fasteners.find((item) => item.id === selectEl.value);
  if (!fastener) {
    return;
  }
  renderDetails(fastener);
  renderPreview(fastener);
}

selectEl.addEventListener('change', updateFastener);

renderSelect();
selectEl.value = fasteners[0].id;
updateFastener();
