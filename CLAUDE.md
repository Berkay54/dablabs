# DAB Labs — dablabs.net

Bu, DAB Labs'ın tanıtım sitesi. Tek sayfalık, statik ve Türkçe bir site; web tasarım ve yazılım hizmetleri tanıtılıyor. Build adımı ve framework yok: düz HTML, CSS ve vanilla JS. Site Vercel'de yayında.

Çalışırken iki bilgisayar kullanılıyor (ev ve iş). Claude konuşmaları bilgisayarlar arasında eşitlenmiyor, bu yüzden kalıcı bağlam bu dosyada ve git geçmişinde tutuluyor.

## Yapı

- `index.html`: tüm sayfa. Bölümler: hero, `#hizmetler`, `#neden`, `#calismalar`, `#surec`, `#sss`, `#iletisim`. SEO meta etiketleri, canonical (`https://dablabs.net/`) ve JSON-LD de burada.
- `assets/css/style.css`: tek stil dosyası. Renkler `:root` değişkenlerinde (`--bg`, `--txt`, `--mut`, `--dim`, `--blue`, `--grad`…), sitede koyu tema var.
- `assets/js/main.js`: tek IIFE. İçinde header scroll, mobil menü, `.rv` scroll reveal, kart ışığı efekti, hero terminal animasyonu, iletişim formu ve sosyal bağlantılar var.
- `assets/fonts/`: Inter (400/600/800) dosyaları sitenin kendi sunucusunda. Harici font kullanılmıyor, CSP buna izin vermiyor.
- `assets/img/`: logolar, favicon'lar, PWA ikonları, og-image.
- `vercel.json`: güvenlik başlıkları ve önbellek ayarları.
- `robots.txt`, `sitemap.xml`, `site.webmanifest`.

## Ayarlar (`assets/js/main.js` başındaki değişkenler)

- `EMAIL = 'info@dablabs.net'`: yedek iletişim adresi. ImprovMX ile Gmail'e yönlendiriliyor.
- `WEB3FORMS_KEY`: Web3Forms access key. Bu anahtar istemci tarafında kullanılmak için tasarlandı, sitede görünmesi normal.
- `FACEBOOK`: profil URL'si. Boş bırakılırsa `[data-fb]` bağlantıları gizlenir.
- `WHATSAPP`: şimdilik boş. `905551234567` biçiminde numara girilirse `[data-wa]` butonu görünür.

## İletişim formu (`#teklif-formu`)

- Form `https://api.web3forms.com/submit` adresine JSON gönderiyor. Anahtar yoksa `mailto:` ile e-posta açılır.
- Ad ve e-posta doğrulanıyor. Spam botları için gizli bir `botcheck` alanı var. Gönderim sonucu `#form-durum` alanında gösteriliyor.

## Kurallar ve alınan kararlar

- **CSP sıkı tutuluyor:** `script-src 'self'`, satır içi script yok, harici CDN yok. Yeni bir dış servis eklenirse `vercel.json` içindeki CSP'ye (`connect-src`, `img-src` vb.) eklenmeli.
- **COOP başlığı bilerek kaldırıldı.** Lighthouse/PageSpeed ölçümünü bozuyordu, geri eklenmemeli.
- **Kontrast:** `--dim` rengi WCAG AA (4.5:1) için açıldı. Metin renklerini koyulaştırırken kontrastı kontrol et.
- **Görseller:** header ve sayfada `-sm` logolar kullanılıyor (gösterim boyutunun 2 katı). Büyük orijinaller sadece kaynak olarak duruyor.
- **`*.zip` git'e eklenmez.** `dablabs-site.zip` daha önce herkese açık hale gelmişti, bu yüzden kaldırıldı.
- `prefers-reduced-motion` ayarına uyuluyor. Yeni animasyon eklenirse bu ayara uymalı.
- Bölüm, değişken ve commit mesajları Türkçe.

## Çalışmalar bölümü (`#calismalar`)

- Gerçek projeler en üstte, "Canlı demo ↗" etiketli, tıklanabilir kartlar olarak duruyor (`<a class="work-a">`, yeni sekmede açılır). Altta CSS ile çizilmiş "Konsept çalışma" kartları var.
- Yeni proje eklerken: headless Edge ile 1280×760 ekran görüntüsü al, 1040 px genişliğe küçültüp JPEG (kalite 80) olarak `assets/img/works/` klasörüne kaydet. Kartı son canlı demonun arkasına ekle.
- Kartlardaki `style="--d:.1s"` gecikmesi sırayla bir kartta var, bir kartta yok. Kart eklendikten sonra bu sıra yeniden düzenlenmeli.
- Kart sayısı çift olursa düzen bozulmaz (2 sütunlu grid). Gerçek projeler arttıkça konsept kartlar kaldırılıyor. Pizzacı, otomotiv ve kahve kartları kaldırıldı. Son konsept kart (Atlas Lojistik, Instagram'daki önce/sonra reeliyle bağlantılıydı) gerçek Kervan Lojistik demosuyla değiştirildi; şu an konsept kart kalmadı. Yeni demo eklenirken kart sayısı çift kalacak şekilde ikişer ekle ya da başka bir düzen kararı ver.
- Şimdiye kadar eklenen canlı demolar: Veteriner Kliniği (veteriner-klinik-demo.vercel.app), Velora Atelier (velora-lilac-ten.vercel.app), ModaLife e-ticaret (ecommerce-kappa-lyart.vercel.app), Parla Diş Kliniği (parla-ecru.vercel.app, kaynak: github.com/Berkay54/parla), Ne Kadar Uzak? sinematik scroll sitesi (uzay-nine.vercel.app, kaynak: github.com/Berkay54/uzay), Kervan Lojistik kurumsal sitesi (kervan-vert.vercel.app, kaynak: github.com/Berkay54/kervan).
- 3D/WebGL içeren sitelerin ekran görüntüsünde headless Edge'e `--use-angle=swiftshader --enable-unsafe-swiftshader --virtual-time-budget=15000` ver; kısa bütçede giriş animasyonu bitmeden çekiliyor.
- Linkler herkese açık production adresi olmalı. `proje-xxxx-berkay54.vercel.app` biçimindeki önizleme linkleri Vercel girişi istiyor, ziyaretçi siteyi göremez. Eklemeden önce `curl -I` ile 200 döndüğünü kontrol et.

## Yerelde çalıştırma

Build gerekmiyor. Herhangi bir statik sunucu yeterli, örneğin `npx serve .` veya `python -m http.server`. Güvenlik başlıkları yalnızca Vercel'de uygulanır.

## Yapılabilecekler

- WhatsApp numarası eklenebilir (`WHATSAPP`).
