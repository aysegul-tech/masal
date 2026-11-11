// "Şu an kaç kişi dinliyor" ve "toplam kaç kez dinlendi" sayaçları (Firebase Realtime Database).
// Kişisel bilgi tutulmaz: her dinleyici yalnızca rastgele bir anahtarla, dinlediği süre boyunca görünür.
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getDatabase, ref, push, set, remove, onValue, onDisconnect, runTransaction,
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-database.js";

const ayar = window.MASAL_SAYAC;
const kutu = document.getElementById("sayac");
const canliEl = document.getElementById("sayac-canli");
const toplamEl = document.getElementById("sayac-toplam");

if (ayar && kutu) {
  const db = getDatabase(initializeApp(ayar.firebase));
  const kok = `masallar/${ayar.id}`;
  const dinleyenler = ref(db, `${kok}/dinleyen`);
  const toplam = ref(db, `${kok}/toplam`);
  const sayi = (n) => n.toLocaleString("tr-TR");

  let canli = 0;
  let toplamSayi = 0;
  function yaz() {
    canliEl.textContent = canli > 0
      ? `🎧 Şu an ${sayi(canli)} kişi dinliyor`
      : "🎧 Şu an dinleyen yok";
    canliEl.classList.toggle("var", canli > 0);
    toplamEl.textContent = `Bugüne kadar ${sayi(toplamSayi)} kez dinlendi`;
    kutu.hidden = false;
  }

  onValue(dinleyenler, (s) => { canli = s.size; yaz(); });
  onValue(toplam, (s) => { toplamSayi = s.val() || 0; yaz(); });

  // Bu ziyaretçinin dinleme kaydı
  let benim = null;
  let sayildi = false; // aynı sayfa ziyaretinde toplam yalnızca bir kez artar

  document.addEventListener("masal:dinleme-basladi", async () => {
    if (!sayildi) {
      sayildi = true;
      runTransaction(toplam, (v) => (v || 0) + 1).catch(() => {});
    }
    if (benim) return;
    benim = push(dinleyenler);
    try {
      await onDisconnect(benim).remove(); // sekme kapanırsa ya da bağlantı koparsa kendiliğinden silinir
      await set(benim, true);
    } catch (_) { benim = null; }
  });

  document.addEventListener("masal:dinleme-bitti", () => {
    if (!benim) return;
    const r = benim;
    benim = null;
    onDisconnect(r).cancel().catch(() => {});
    remove(r).catch(() => {});
  });
}
