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

## Resimli sayfalar

Masal sayfa sayfa okunur: **her resim, altındaki paragrafla birlikte bir sayfa olur.**
Resmi `assets/` altında masala ait bir klasöre koy ve ilgili paragrafın hemen üstüne yaz:

`![Resmin kısa açıklaması]({{ '/assets/klasor-adi/1.jpg' | relative_url }})`

Ana sayfadaki kartta görünecek resim için en üstteki bilgilere `kapak: /assets/klasor-adi/1.jpg` ekle.
Resimler en iyi 3:2 oranında (ör. 1200×800) görünür. Kendi suluboya resimlerinin fotoğrafını da koyabilirsin.

## Sesli okuma

Sağ alttaki **Sesli oku** düğmesi masalı tarayıcının Türkçe kadın sesiyle okur ve her sayfanın sonunda
kendiliğinden sonraki sayfaya geçer. Mac ve iPhone'da "Yelda" sesi kullanılır. Düğmeye tekrar basınca ses kapanır.

`_araclar/suluboya.py` örnek masalın resimlerini üreten betiktir.

## Dosyalar

- `_config.yml` – sitenin adı ve açıklaması
- `_layouts/` – sayfa şablonları
- `assets/style.css` – renkler ve yazı tipleri
- `masallar/` – masallar
