# araclar/

Sitedeki çok sayfalı bölümleri üreten Python betikleri. Bu klasör `.vercelignore` ile yayından hariç tutulur.

## Ne zaman çalıştırılır?

Aşağıdakilerden biri değiştiğinde:

- Menü veya footer (`index.html` içindeki `<header class="hdr">` / `<footer class="ftr">`; TR sayfaların hepsi bunu kopyalar)
- Hizmet, vaka, blog veya İngilizce sayfaların içeriği
- Yeni hizmet, vaka çalışması ya da blog yazısı eklendiğinde

```
python araclar/uret.py
```

Sonra `git diff` ile değişiklikleri kontrol edin. Python 3 yeterli, ek paket gerekmez.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `icerik_hizmetler.py` | 6 TR hizmet sayfasının metinleri (`PAGES`) |
| `icerik_calismalar.py` | 8 vaka sayfasının metinleri (`CASES`) |
| `icerik_blog.py` | Blog yazıları (`POSTS`); yeni yazı listeye eklenir |
| `icerik_en.py` | 6 İngilizce hizmet sayfası (`EN_PAGES`) |
| `uret_hizmetler.py` | `/<hizmet>/` sayfaları + `sitemap.xml` |
| `uret_calismalar.py` | `/calismalar/<proje>/` sayfaları |
| `uret_blog.py` | `/blog/` ve `/blog/<yazi>/` sayfaları |
| `uret_analiz.py` | `/ucretsiz-site-analizi/` sayfası (metinler dosyanın içinde) |
| `uret_en.py` | `/en/` ana sayfa ve `/en/<service>/` sayfaları (EN header/footer bu dosyada) |
| `uret.py` | Hepsini sırayla çalıştırır |

## Elle düzenlenen sayfalar

`index.html` (TR ana sayfa) üretilmez, elle düzenlenir ve diğer TR sayfaların header/footer kaynağıdır. İngilizce ana sayfa ise `uret_en.py` içinden üretilir; elle düzenlenirse bir sonraki çalıştırmada üzerine yazılır.
