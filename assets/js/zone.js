/**
 * Zone & carte – carte Leaflet interactive (chargement automatique)
 * Villes locales + cercle de couverture + focus depuis la liste.
 */
(function () {
  "use strict";

  const CITIES = [
    { id: "tetouan", name: "Tétouan", lat: 35.5785, lng: -5.3684, local: true },
    { id: "martil", name: "Martil", lat: 35.6167, lng: -5.2750, local: true },
    { id: "mdiq", name: "M’diq", lat: 35.6858, lng: -5.3250, local: true },
    { id: "cabo-negro", name: "Cabo Negro", lat: 35.6700, lng: -5.2800, local: true },
    { id: "fnideq", name: "Fnideq", lat: 35.8490, lng: -5.3570, local: true },
    { id: "tanger", name: "Tanger", lat: 35.7595, lng: -5.8340, local: true },
    { id: "fahs-anjra", name: "Fahs-Anjra", lat: 35.7200, lng: -5.6200, local: true },
    { id: "chefchaouen", name: "Chefchaouen", lat: 35.1714, lng: -5.2697, local: true },
    { id: "rabat", name: "Rabat", lat: 34.0209, lng: -6.8416, local: false },
    { id: "casablanca", name: "Casablanca", lat: 33.5731, lng: -7.5898, local: false },
  ];

  const LOCAL_CENTER = [35.60, -5.35];
  const LOCAL_RADIUS_M = 28000; // ~28 km

  let map = null;
  let markers = {};
  let circle = null;
  let activeId = null;

  function createPinIcon(label, isActive) {
    const cls = isActive ? "zone-pin is-active" : "zone-pin";
    return L.divIcon({
      className: "zone-marker-icon",
      html: `<div class="${cls}"><span class="zone-pin-label">${label}</span></div>`,
      iconSize: [28, 36],
      iconAnchor: [14, 18],
      popupAnchor: [0, -18],
    });
  }

  function setActive(id) {
    activeId = id;
    document.querySelectorAll(".zone-city-btn").forEach((btn) => {
      const on = btn.dataset.city === id;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    Object.keys(markers).forEach((mid) => {
      const c = CITIES.find((x) => x.id === mid);
      if (c && markers[mid]) {
        markers[mid].setIcon(createPinIcon(c.name, mid === id));
      }
    });
  }

  function focusCity(id) {
    const c = CITIES.find((x) => x.id === id);
    if (!c || !map) return;
    setActive(id);
    const zoom = c.local ? 12 : 10;
    map.flyTo([c.lat, c.lng], zoom, { duration: 0.8 });
    if (markers[id]) markers[id].openPopup();
  }

  function initMap() {
    const el = document.getElementById("zone-map");
    if (!el || map) return;

    const placeholder = document.getElementById("zone-map-placeholder");
    if (placeholder) placeholder.hidden = true;

    map = L.map(el, {
      scrollWheelZoom: false,
      zoomControl: true,
    }).setView(LOCAL_CENTER, 10);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 18,
    }).addTo(map);

    circle = L.circle(LOCAL_CENTER, {
      radius: LOCAL_RADIUS_M,
      color: "#2563eb",
      weight: 2,
      fillColor: "#3b82f6",
      fillOpacity: 0.08,
    }).addTo(map);

    CITIES.filter((c) => c.local).forEach((c) => {
      const m = L.marker([c.lat, c.lng], {
        icon: createPinIcon(c.name, false),
        title: c.name,
      }).addTo(map);
      m.bindPopup(
        `<strong>${c.name}</strong><br><span style="font-size:0.85em;color:#64748b">Zone locale · à confirmer</span>`
      );
      m.on("click", () => setActive(c.id));
      markers[c.id] = m;
    });

    const group = L.featureGroup(Object.values(markers).concat([circle]));
    map.fitBounds(group.getBounds().pad(0.12));

    // Fix taille si le conteneur était caché
    setTimeout(function () {
      map.invalidateSize();
    }, 100);

    map.on("focus", () => map.scrollWheelZoom.enable());
    map.on("blur", () => map.scrollWheelZoom.disable());
  }

  /** Charge Leaflet (CSS + JS) puis initialise la carte automatiquement */
  function loadLeafletAndMap() {
    if (typeof L !== "undefined") {
      initMap();
      return;
    }

    // CSS Leaflet
    if (!document.querySelector('link[href*="leaflet"]')) {
      const css = document.createElement("link");
      css.rel = "stylesheet";
      css.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
      css.integrity = "sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=";
      css.crossOrigin = "";
      document.head.appendChild(css);
    }

    // JS Leaflet
    const script = document.createElement("script");
    script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
    script.integrity = "sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=";
    script.crossOrigin = "";
    script.onload = function () {
      initMap();
    };
    script.onerror = function () {
      const ph = document.getElementById("zone-map-placeholder");
      if (ph) {
        ph.hidden = false;
        ph.innerHTML =
          '<p><strong>Impossible de charger la carte</strong></p><p class="meta">Vérifiez votre connexion ou réessayez plus tard.</p>';
      }
    };
    document.head.appendChild(script);
  }

  function bindCityButtons() {
    document.querySelectorAll(".zone-city-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const id = btn.dataset.city;
        if (!map) {
          // Carte pas encore prête : attendre un peu
          const tryFocus = () => {
            if (map) focusCity(id);
            else setTimeout(tryFocus, 150);
          };
          setTimeout(tryFocus, 200);
          return;
        }
        focusCity(id);
      });
    });
  }

  function bindRouteForm() {
    const form = document.getElementById("form-zone");
    const result = document.getElementById("route-result");
    if (!form || !result) return;

    function normalize(s) {
      return (s || "")
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .trim();
    }

    const localNames = new Set(
      CITIES.filter((c) => c.local).map((c) => normalize(c.name))
    );

    function isLocal(text) {
      const n = normalize(text);
      if (!n) return false;
      for (const name of localNames) {
        if (n.includes(name) || name.includes(n)) return true;
      }
      if (n.includes("rabat") || n.includes("casablanca") || n.includes("casa"))
        return "demand";
      return false;
    }

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const depart = form.querySelector("#z-depart")?.value || "";
      const arrivee = form.querySelector("#z-arrivee")?.value || "";
      const d = isLocal(depart);
      const a = isLocal(arrivee);

      result.hidden = false;
      result.className = "route-result";

      if (d === true && a === true) {
        result.classList.add("is-local");
        result.innerHTML =
          "<strong>Zone locale probable.</strong> Les deux points semblent dans la zone de Tétouan et alentours. L’équipe confirmera la faisabilité (accès, véhicule, horaires) après votre demande.";
      } else if (d || a) {
        result.classList.add("is-demand");
        result.innerHTML =
          "<strong>Transfert sur demande.</strong> Au moins une extrémité est hors zone locale (ex. Rabat, Casablanca). L’équipe étudiera le trajet au cas par cas.";
      } else {
        result.classList.add("is-unknown");
        result.innerHTML =
          "<strong>À vérifier.</strong> Décrivez précisément les adresses : l’équipe vous indiquera si le trajet peut être assuré.";
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    loadLeafletAndMap(); // carte visible dès le chargement
    bindCityButtons();
    bindRouteForm();
  });
})();
