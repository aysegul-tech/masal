// Masalı sayfa sayfa gösterir ve isteğe bağlı olarak kadın sesiyle okur.
(function () {
  const kaynak = document.getElementById("metin");
  const kitap = document.getElementById("kitap");
  if (!kaynak || !kitap) return;

  // --- 1. Metni sayfalara böl: her resim, ardından gelen paragrafla bir sayfa olur.
  const sayfalar = [];
  let bekleyenResim = null;
  for (const el of Array.from(kaynak.children)) {
    const img = el.querySelector("img");
    const sadeceResim = img && el.textContent.trim() === "";
    if (sadeceResim) {
      bekleyenResim = { src: img.getAttribute("src"), alt: img.getAttribute("alt") || "" };
    } else if (el.textContent.trim() !== "") {
      sayfalar.push({ resim: bekleyenResim, html: el.outerHTML, metin: el.textContent.trim() });
      bekleyenResim = null;
    }
  }
  if (sayfalar.length === 0) return;

  kaynak.hidden = true;
  kitap.hidden = false;

  const resimEl = document.getElementById("sahne-resim");
  const sahne = resimEl.parentElement;
  const metinEl = document.getElementById("sahne-metin");
  const noEl = document.getElementById("sayfa-no");
  const onceki = document.getElementById("onceki");
  const sonraki = document.getElementById("sonraki");

  let aktif = 0;

  function sayfaGoster(i, { kaydir = true } = {}) {
    aktif = Math.max(0, Math.min(sayfalar.length - 1, i));
    const s = sayfalar[aktif];
    if (s.resim) {
      sahne.hidden = false;
      resimEl.classList.remove("gorunur");
      resimEl.onload = () => resimEl.classList.add("gorunur");
      resimEl.src = s.resim.src;
      resimEl.alt = s.resim.alt;
      if (resimEl.complete) resimEl.classList.add("gorunur");
    } else {
      sahne.hidden = true;
    }
    metinEl.innerHTML = s.html;
    metinEl.classList.toggle("ilk", aktif === 0);
    noEl.textContent = `${aktif + 1} / ${sayfalar.length}`;
    onceki.disabled = aktif === 0;
    sonraki.disabled = aktif === sayfalar.length - 1;
    history.replaceState(null, "", `#sayfa-${aktif + 1}`);
    if (kaydir) kitap.scrollIntoView({ behavior: "smooth", block: "start" });

    // Bir sonraki resmi önceden yükle
    const n = sayfalar[aktif + 1];
    if (n && n.resim) new Image().src = n.resim.src;

    if (sesAcik) oku();
  }

  onceki.addEventListener("click", () => sayfaGoster(aktif - 1));
  sonraki.addEventListener("click", () => sayfaGoster(aktif + 1));
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") sayfaGoster(aktif + 1);
    if (e.key === "ArrowLeft") sayfaGoster(aktif - 1);
  });

  // Telefonda kaydırarak sayfa çevirme
  let dokunX = null;
  kitap.addEventListener("touchstart", (e) => { dokunX = e.touches[0].clientX; }, { passive: true });
  kitap.addEventListener("touchend", (e) => {
    if (dokunX === null) return;
    const fark = e.changedTouches[0].clientX - dokunX;
    if (Math.abs(fark) > 60) sayfaGoster(aktif + (fark < 0 ? 1 : -1));
    dokunX = null;
  });

  // --- 2. Sesli okuma: her sayfa için kayıtlı ses dosyası (ör. ses/1.mp3, ses/2.mp3 …)
  const dugme = document.getElementById("ses-dugme");
  const sesKlasoru = kitap.dataset.ses; // masalın bilgilerindeki "ses" satırı
  const oynatici = new Audio();
  oynatici.preload = "auto";
  let sesAcik = false;

  function oku() {
    oynatici.pause();
    oynatici.src = `${sesKlasoru}${aktif + 1}.mp3`;
    oynatici.currentTime = 0;
    oynatici.play().catch(() => sesiAyarla(false));
  }

  oynatici.addEventListener("ended", () => {
    if (!sesAcik) return;
    if (aktif < sayfalar.length - 1) {
      setTimeout(() => { if (sesAcik) sayfaGoster(aktif + 1, { kaydir: false }); }, 1200);
    } else {
      sesiAyarla(false);
    }
  });

  function sesiAyarla(acik) {
    sesAcik = acik;
    dugme.setAttribute("aria-pressed", String(acik));
    dugme.classList.toggle("acik", acik);
    dugme.querySelector(".ikon").textContent = acik ? "🔊" : "🔈";
    dugme.querySelector(".yazi").textContent = acik ? "Sesi kapat" : "Masalı dinle";
    if (acik) oku();
    else oynatici.pause();
  }

  if (sesKlasoru) {
    dugme.hidden = false;
    dugme.addEventListener("click", () => sesiAyarla(!sesAcik));
  }

  // --- Başlangıç: adresteki #sayfa-N varsa oradan aç
  const m = location.hash.match(/sayfa-(\d+)/);
  sayfaGoster(m ? parseInt(m[1], 10) - 1 : 0, { kaydir: false });
})();
