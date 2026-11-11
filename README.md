# Masal

Masalların okunduğu basit bir web sitesi. GitHub Pages ile ücretsiz yayınlanır.

## Yeni masal eklemek

1. `masallar` klasöründe yeni bir dosya aç, ör. `masallar/bilge-kaplumbaga.md`
   (dosya adında Türkçe karakter ve boşluk kullanma, kelimeleri `-` ile ayır).
2. Dosyanın en başına şu bilgileri yaz:

   ```
   ---
   layout: masal
   title: "Bilge Kaplumbağa"
   ozet: "Tek cümlelik kısa tanıtım."
   sira: 2
   ---
   ```

   `sira` ana sayfadaki sırayı belirler (1 en üstte).
3. Altına masalı düz metin olarak yaz. Paragrafların arasında bir boş satır bırak.
4. Kaydet, GitHub Desktop'ta commit et ve **Push origin** de. Site birkaç dakika içinde güncellenir.

Resim eklemek için resmi `assets/` klasörüne koy ve masalın içine şunu yaz:
`![Açıklama]({{ '/assets/resim-adi.jpg' | relative_url }})`

## Dosyalar

- `_config.yml` – sitenin adı ve açıklaması
- `_layouts/` – sayfa şablonları
- `assets/style.css` – renkler ve yazı tipleri
- `masallar/` – masallar
