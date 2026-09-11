# Odabaşı Dayanıklı Tüketim — Web Sitesi

Statik HTML paketi. Herhangi bir hostinge (Netlify, Vercel, cPanel, Cloudflare Pages) olduğu gibi yüklenir.
Veritabanı, PHP veya build adımı gerektirmez.

---

## 1. Yayına almadan önce doldurulacaklar

Sitenin tamamı `build.py` ve `data.py` dosyalarından üretiliyor. Aşağıdaki alanlar `data.py` içindeki
`SITE` sözlüğünde **TODO** olarak işaretli. Bunları doldurup `python3 build.py` komutunu çalıştırmak
yeterli — tüm sayfalar, schema kayıtları, sitemap ve llms.txt yeniden üretilir.

| Alan | Şu anki değer | Ne yazılmalı |
|---|---|---|
| `domain` | `https://www.odabasidayanikli.com` | Gerçek alan adı (canonical, OG ve sitemap buradan üretiliyor) |
| `phone_display` | `0232 000 00 00` | Mağaza telefonu, görünen format |
| `phone_tel` | `+902320000000` | Aynı numara, `tel:` formatında |
| `whatsapp` | `905000000000` | WhatsApp numarası, ülke kodu ile, başında + ve boşluk olmadan |
| `email` | `info@odabasidayanikli.com` | Kurumsal e-posta |
| `address_line` | `Çankaya ve Eşrefpaşa, İzmir` | Kısa özet metni; şube detayları `BRANCHES` içinde |
| `street` / `postal` | Boş | Sadece schema.org kaydı için. Boş bırakılırsa schema'ya yazılmaz |
| `lat` / `lng` | İzmir merkez | Mağazanın Google Haritalar koordinatı. **Hizmet haritasındaki kırmızı mağaza işareti bu değerden geliyor**, doğru koordinatı girmek önemli |
| `founded` | `2005` | Kuruluş yılı |
| `hours` | `Pazartesi - Cumartesi 09:00 - 19:00` | Gerçek çalışma saatleri |
| `instagram` / `facebook` | Boş profil linki | Sosyal medya adresleri |

### Şubeler

`data.py` içindeki `BRANCHES` listesi iki şubeyi tanımlıyor: **LG Shop Çankaya** ve
**Uğur Shop Eşrefpaşa** (ikisi de Konak / İzmir). Her şubede doldurulacak alanlar:

| Alan | Ne yazılmalı |
|---|---|
| `street` | Açık adres — `Şair Eşref Bulvarı No: 00` gibi |
| `postal` | Posta kodu |
| `phone_display` / `phone_tel` | Şubeye ait ayrı numara varsa. Boş bırakılırsa genel numara gösterilir |
| `maps` | Google Haritalar bağlantısı. Boş bırakılırsa "Haritada aç" düğmesi çıkmaz |

Şubeler footer'da, iletişim sayfasında, hakkımızda sayfasında ve ana sayfadaki teklif bloğunda
görünüyor; ayrıca her biri için ayrı bir `Store` schema kaydı üretiliyor (ana işletmeye
`parentOrganization` ile bağlı). "Bize sorun" bölümünde de iki mağaza adıyla anılıyor.

Şube sayısı değişirse listeye eleman ekleyip çıkarmanız yeterli — site geneli otomatik güncellenir.
Yeni bir şubenin `brand` alanına marka slug'ı yazarsanız (örn. `"grundig"`), o markanın logosu
şube kartında görünür ve marka sayfasına bağlanır.

**Not:** Şubeler İzmir merkezde birbirine çok yakın olduğu için bölge haritasında tek bir mağaza
işareti gösteriliyor — o ölçekte iki ayrı pin üst üste binerdi. Şube ayrımı listelerde yapılıyor.

> **Not — "Buca" nereden geliyor?** İlk sürümde mağaza adresi bilinmediği için Buca örnek olarak
> kullanılmıştı; kaldırıldı. Sitede kalan `bolge/izmir-buca.html` ise mağaza adresi değil, **hizmet
> verdiğiniz ilçe için açılmış yerel SEO sayfası** — "buca beyaz eşya" gibi aramalar için. Diğer 12 ilçe
> sayfası da aynı mantıkta. Hizmet vermediğiniz bir ilçe varsa `data.py` içindeki `LOCATIONS` listesinden
> çıkarmanız yeterli.

**Kritik:** Adres, telefon ve işletme adı (NAP) üçlüsünün Google Business Profile, site ve dizin
kayıtlarında birebir aynı yazılması yerel SEO'nun en belirleyici sinyalidir. Tek harf farkı bile
Google tarafından ayrı işletme olarak yorumlanabilir.

### Ticari vaatler — mutlaka teyit edin

Site genelinde şu üç vaat öne çıkarıldı: **ücretsiz teslimat**, **ücretsiz montaj**, **taksit imkanı**.
Bunlar üst bar, hero, avantaj şeridi, SSS ve tüm kategori/marka/bölge sayfalarında tekrarlanıyor.
Uygulamada farklı çalışıyorsanız (örneğin belirli bir tutarın altında teslimat ücretli, ya da montaj
sadece bazı ürün gruplarında ücretsiz) `data.py` içindeki `PERKS` listesi ve ilgili SSS cevapları
mutlaka güncellenmeli. Tüketici mevzuatı açısından sitede yazan koşul bağlayıcıdır.

### Doğrulanması gereken içerik

Marka sayfalarındaki teknik açıklamalar (garanti süreleri, teknoloji isimleri, ürün grupları) genel
piyasa bilgisine göre yazıldı. Yayına almadan önce özellikle şunları teyit edin:

- Garanti süreleri (metinlerde "genellikle 3 yıl" olarak yazıldı)
- Hangi markalarda hangi ürün gruplarını fiilen satıyorsunuz
- **Rota sayfası kontrol edilmeli.** Gönderdiğiniz logo "RotaClimate" — iklimlendirme markası.
  Sitedeki Rota sayfası ise ankastre fırın, ocak ve davlumbaz anlatıyor. İkisinden biri yanlış;
  hangi Rota ürünlerini sattığınızı söylerseniz sayfa ona göre yeniden yazılır
  (`data.py` içinde `rota` kaydı ve `cats` listesi)
- Yetkili bayilik: LG, Uğur ve Altus olarak işaretli. Değişirse `data.py` içinde ilgili markanın `"authorized"` değerini değiştirin — site genelindeki tüm metinler, rozetler ve "bize sorun" bölümü buna göre otomatik güncellenir
- Ana sayfadaki sayısal iddialar (10 marka, 11 ürün grubu, 3 il, 2 yetkili bayilik) doğru

---

## 2. Marka kimliği

Site, paylaştığınız logoya göre kurgulandı.

| Öğe | Değer |
|---|---|
| Ana renk (neon kırmızı) | `#E60034` |
| Koyu kırmızı (hover) | `#B70328` |
| Siyah | `#0B0C0F` |
| Açık zemin | `#FFFFFF` ve `#F7F9FB` |
| Başlık fontu | Manrope |
| Gövde fontu | Inter |

Logo dosyaları `assets/logo.png` (açık zemin için, siyah + kırmızı) ve `assets/logo-white.png`
(koyu zemin ve footer için, beyaz + kırmızı). İkisi de orijinal PNG'den üretildi. Vektör (SVG veya AI)
dosyanız varsa `assets_src/` içine koyup `build.py` içindeki uzantıyı değiştirmeniz daha keskin sonuç verir.

### Marka duvarı — gri görünüm

Markalar sitede gri gösteriliyor: logo dosyası varsa `grayscale(1)` filtresiyle, yoksa markanın adı gri
yazıyla. Üzerine gelindiğinde renk geri geliyor. Bu, farklı markaların birbirinden çok farklı renkleri
yüzünden oluşan karmaşayı önleyen ve sayfanın kendi kırmızısını öne çıkaran standart yaklaşım.

Yetkili bayi olduğunuz markalar (LG, Uğur, Altus) listenin başında yer alıyor ve köşesinde
"Yetkili Bayi" rozeti taşıyor.

### Marka logoları

Dokuz markanın logosu yerleştirildi: **LG, Uğur, Altus, Grundig, Electrolux, TCL, Şenocak, Kärcher,
Rota.** Eksik olan tek marka **Hoover** — sitede markanın adıyla gri yazı olarak görünüyor,
bozuk görsel çıkmıyor.

Logolar altı yerde birden kullanılıyor: ana sayfa marka duvarı, kategori sayfalarındaki "bu üründe
çalıştığımız markalar" bloğu, bölge sayfaları, marka sayfası başlığı ve marka listeleri.

**Yeni logo eklemek:** dosyayı `prep_logos.py` ile işleyin, `build.py` çalıştırın.

```bash
python3 prep_logos.py ugur=~/Downloads/ugur-logo.png
python3 build.py
```

`prep_logos.py` şunları yapıyor:

1. **Beyaz zemini siler.** Kenarlardan içeri doğru bağlantılı beyaz alanı şeffaf yapar; logonun
   *içindeki* beyaz alanlar korunur (LG'nin kırmızı dairesi içindeki beyaz yaylar gibi).
2. **Boş kenarları kırpar.**
3. **Optik ağırlığı eşitler.** Her logoyu, kapladığı mürekkep alanı sabit olacak şekilde ölçekleyip
   ortak bir 640×200 kutuya yerleştirir. Bu olmadan Grundig gibi uzun ince bir kelime logosu, LG gibi
   kare bir logonun yanında minicik kalıyor. Tüm dosyalar aynı en-boy oranında olduğu için sitede
   hepsi aynı boyutta gösteriliyor; görünen büyüklüğü mürekkep alanı belirliyor.

Bir logo gözünüze küçük veya büyük geldiyse sonuna ölçek katsayısı ekleyin:
`python3 prep_logos.py karcher=dosya.png@1.15`

**Görünüm:** marka duvarında logolar gri ve yarı saydam (`grayscale` + `opacity`), üzerine gelince
tam renk ve tam opaklıkta. Marka sayfasının başlığında ise beyaz bir kart içinde, orijinal renkleriyle.
Koyu zeminli "bize sorun" kartlarında logolar beyaz bir kutunun içinde, orijinal renkleriyle duruyor —
logoyu koyu zemine göre beyaza çevirmek çoğunda silüete dönüştürdüğü için (LG'nin yüzü kayboluyordu)
bu yol seçildi. Logosu olmayan markada aynı kutuda markanın adı yazıyor.

`python3 build.py` çalıştırdığınızda hangi logoların eksik olduğunu satır satır yazıyor.

**Kaynak önerisi:** SVG bulabiliyorsanız SVG kullanın, her ekranda net çıkar (`prep_logos.py` yerine
doğrudan `assets_src/markalar/<slug>.svg` olarak koyup `build.py` çalıştırmanız yeterli). Doğru kaynak,
yetkili bayi olduğunuz markalarda bayi portalı veya bölge temsilciniz; diğerlerinde üreticinin basın
odası / kurumsal kimlik sayfası ya da distribütör. Üçüncü taraf servis rehberlerindeki logolar
genellikle eski sürüm ve düşük çözünürlüklü oluyor.

`assets_src/markalar/README.txt` teknik önerileri (şeffaf arkaplan, koyu zeminli versiyon kullanmayın)
tekrar ediyor.

Ana sayfadaki beyaz eşya çizimi (buzdolabı, çamaşır makinesi, ankastre fırın, bulaşık makinesi, klima, TV)
tamamen SVG olarak çizildi — dosya boyutu birkaç KB, her ekranda net görünür, fotoğraf gerektirmez.
Neon kırmızı çizgiler markanın kırmızısıyla aynı koddan geliyor. `build.py` içindeki `HERO_ART`
değişkeninden düzenlenebilir.

### Hizmet bölgeleri haritası

Ana sayfada, tüm kategori sayfalarında ve 13 bölge sayfasında Ege bölgesi haritası var.

- **Gerçek il sınırları.** İzmir, Manisa ve Aydın markanın renkleriyle vurgulu; Balıkesir, Çanakkale,
  Bursa, Kütahya, Uşak, Afyonkarahisar, Denizli, Burdur ve Muğla çevre doku olarak açık gri. Batıda
  kalan boşluk gerçek Ege kıyısı — komşu iller kadrajın dışına taşıp kırpıldığı için kara tarafında
  boşluk kalmıyor.
- **İlçeler gerçek koordinatlarından.** Enlem/boylam değerleri, il sınır verisinin koordinat
  sistemine bir dönüşümle taşındı. Dönüşüm batı illerinin merkezleri üzerinde en küçük karelerle
  bulundu, sonra 26 ilçenin doğru il sınırları içine düşmesine göre ince ayar yapıldı
  (26 ilçeden 25'i doğru; Didim yarımada ucunda kaldığı için sınırda).
- Haritadaki noktalar tıklanabilir. Listede bir ilçenin üzerine gelindiğinde haritadaki noktası
  vurgulanıyor, tersi de geçerli. Bölge sayfalarında o ilçe ikisinde de kırmızı işaretli açılıyor.
- Sağ altta küçük bir Türkiye haritası, bölgenin ülke üzerindeki yerini gösteriyor
  (`assets/turkiye-ege.svg`, ayrı dosya olduğu için bir kez indiriliyor).
- Kırmızı mağaza işareti `data.py` içindeki `lat` / `lng` değerlerinden geliyor.
- 50 km ölçek çubuğu ve kuzey oku var.

**Veri kaynağı:** il sınırları [turkey-map-react](https://github.com/erdigokce/turkey-map-react)
paketinden alındı (MIT lisanslı). `extract_map.py` bu veriden `mapdata.py` ve `assets_src/turkiye-ege.svg`
dosyalarını üretiyor; ikisi de depoda, yeniden çalıştırmanız gerekmiyor.

Yeni ilçe eklemek için `build.py` içindeki `MAP_POINTS` listesine bir satır ekleyin:
`("İzmir", "Ödemiş", 38.23, 27.97, None)`. Son alan bölge sayfasının slug'ı — `None` verirseniz
listede yazı olarak görünür, slug verirseniz haritada tıklanabilir nokta olur (o slug'a ait sayfanın
`LOCATIONS` içinde tanımlı olması gerekir).

---

## 3. Kurulum

```
site/
├── index.html
├── hakkimizda.html
├── servis-ve-destek.html
├── sikca-sorulan-sorular.html
├── iletisim.html
├── 404.html
├── kategori/      11 ürün grubu sayfası
├── marka/         10 marka sayfası
├── bolge/         13 lokasyon sayfası
├── blog/          index + 6 rehber yazısı
├── assets/        style.css, site.js, favicon.svg
├── robots.txt
├── sitemap.xml
├── llms.txt
└── .htaccess
```

Not: `preview.html`, `build.py`, `data.py`, `make_preview.py`, `assets_src/` ve `README.md`
**yayına gitmez** — bunlar kaynak dosyalar. Sunucuya sadece `site/` klasörünün içi yüklenir.

**cPanel / paylaşımlı hosting:** `site/` klasörünün *içindekileri* `public_html` altına yükleyin.
`.htaccess` dosyasının da yüklendiğinden emin olun (gizli dosya, FTP istemcisinde "gizli dosyaları
göster" açık olmalı).

**Netlify / Vercel / Cloudflare Pages:** `site/` klasörünü doğrudan sürükleyip bırakın. Build komutu yok,
publish directory `site`.

Yayına aldıktan sonra:

1. Google Search Console'a mülkiyeti doğrulayın, `sitemap.xml` adresini gönderin.
2. Google Business Profile kaydınıza web sitesi adresini ekleyin.
3. Bing Webmaster Tools'a da ekleyin (Copilot ve bazı AI arama motorları Bing indeksini kullanıyor).

---

## 4. Canlı önizleme ve GitHub

### preview.html — tek dosyada tüm site

`python3 make_preview.py` komutu, 48 sayfanın tamamını tek bir HTML dosyasına (`preview.html`) gömer.
Dosyayı çift tıklayıp açtığınızda site normal şekilde geziliyor: menüler, bağlantılar, SSS açılır
kapanırları, mobil menü hepsi çalışıyor. Altta ayrıca bir sayfa seçici var, 48 sayfaya oradan da
atlayabilirsiniz.

Harici dosya bağımlılığı yok (logolar dosyanın içine gömülü), yani tek dosyayı e-postayla
gönderebilir veya müşteriye WhatsApp'tan atabilirsiniz. Yayına alınacak sürüm bu değil — `site/`
klasörü yayına gider; `preview.html` sadece göstermek için.

### GitHub ve yayın

Proje `github.com/nintendomitt/odabasi` deposunda. Değişiklik sonrası akış:

```bash
python3 build.py && python3 make_preview.py
git add -A && git commit -m "guncelleme: <ne degisti>" && git push
```

`.gitignore` ekran görüntülerini, Python önbelleğini ve `.DS_Store` dosyalarını dışarıda bırakıyor;
`site/`, `preview.html`, üretici scriptler ve logolar depoda.

#### GitHub Pages

`.github/workflows/pages.yml` iş akışı, `main` dalına her push'ta `site/` klasörünü GitHub Pages'e
yayınlıyor. Çalışması için iki ayar gerekiyor:

1. **Depo public olmalı.** GitHub'ın ücretsiz planında Pages yalnızca public depolarda çalışıyor;
   private depodan yayın Pro planı gerektiriyor.
   Settings → General → en altta Danger Zone → Change repository visibility → Public
2. **Pages kaynağı "GitHub Actions" olmalı.**
   Settings → Pages → Build and deployment → Source → **GitHub Actions**

Sonrasında adres: `https://nintendomitt.github.io/odabasi/`

**Önizleme arama motorlarına kapalı.** İş akışındaki "Önizlemeyi dizine kapat" adımı, yayınlanan
kopyada `robots.txt` dosyasını `Disallow: /` yapıyor ve tüm sayfalara `noindex` ekliyor. Bunun sebebi:
sitedeki canonical adresler gerçek alan adını gösteriyor, ayrıca içerikte hâlâ yer tutucu telefon ve
adres var. Bu adım olmasaydı Google taslak kopyayı dizine alabilir ve gerçek site yayına girdiğinde
çift içerik sorunu çıkardı. **Depodaki dosyalara dokunmuyor**, sadece Pages çıktısını değiştiriyor.

Site gerçek alan adında yayına alındığında o adımı `pages.yml` içinden silin.

#### Alternatif: Cloudflare Pages veya Netlify

Depoyu public yapmak istemezseniz her ikisi de ücretsiz planda private depodan yayın yapıyor ve
her push'ta otomatik güncelleniyor. Gerçek alan adını bağlamak da aynı panelden yapılıyor —
yayına alma aşamasında bu yolu değerlendirmek mantıklı olur.

---

## 5. Teklif formu

Form şu an **WhatsApp'a yönlendirme** mantığıyla çalışıyor: kullanıcı formu doldurup gönderince,
bilgiler biçimlendirilmiş bir mesaj olarak WhatsApp'ta açılıyor. Sunucu tarafı gerektirmediği için
statik hostingde sorunsuz çalışır.

E-posta ile toplamak isterseniz, `assets/site.js` içindeki `leadForm` submit bloğunu bir form servisiyle
değiştirin (Formspree, Web3Forms, Basin — hepsi ücretsiz katmana sahip). Tek yapılacak, `fetch` ile
servis endpoint'ine POST atmak.

---

## 6. SEO altyapısı — ne yapıldı

**Teknik**

- Her sayfada tekil `<title>` ve `<meta name="description">` (48 sayfanın hiçbirinde tekrar yok)
- Canonical URL, Open Graph, Twitter Card, `hreflang` yerine `lang="tr"` + `og:locale=tr_TR`
- Coğrafi meta etiketler (`geo.region`, `geo.position`, `ICBM`)
- Semantik başlık hiyerarşisi, sayfa başına tek `H1`
- `sitemap.xml` (47 URL), `robots.txt`, `404.html`, `.htaccess` (gzip + cache header)
- Mobil uyumlu, yatay kaydırma yok, harici JS kütüphanesi yok (hız)
- Breadcrumb navigasyonu + `BreadcrumbList` schema

**Yapısal veri (JSON-LD)**

| Schema | Nerede |
|---|---|
| `Store` + `HomeGoodsStore` | Tüm ana sayfalarda; açılış saatleri, `areaServed`, `brand`, `hasOfferCatalog` ile |
| `WebSite` | Ana sayfa |
| `BreadcrumbList` | 46 sayfa |
| `FAQPage` | 44 sayfa |
| `CollectionPage` + `ItemList` | Kategori ve marka sayfaları |
| `BlogPosting` + `speakable` | 6 blog yazısı |
| `ContactPage` | İletişim |
| `Store` (şube başına) | Ana sayfa, iletişim, hakkımızda — `parentOrganization` ile ana işletmeye bağlı |

Adres alanları boş bırakıldığında schema'ya hiç yazılmaz — eksik bir `streetAddress` yazmaktansa
alanı hiç göndermemek doğru davranıştır. Adresi doldurunca otomatik eklenir.

Yerel bayi sayfalarında `parentOrganization` ile ana mağazaya bağlı ayrı `Store` kaydı tanımlandı —
bu, "Buca beyaz eşya" gibi ilçe bazlı sorgularda bağlamı netleştiriyor.

**Not:** Bilinçli olarak `AggregateRating` / `Review` schema'sı eklenmedi. Gerçek müşteri yorumu
olmadan puan işaretlemek Google'ın yapısal veri politikasına aykırı ve manuel ceza riski taşıyor.
Google yorumlarınız birikince gerçek verilerle eklenebilir.

---

## 7. GEO (AI arama motoru optimizasyonu) — ne yapıldı

Klasik SEO, sıralamada üst sıraya çıkmayı hedefler. GEO ise ChatGPT, Perplexity, Google AI Overviews
ve Claude gibi sistemlerin cevabı üretirken **sizin sayfanızdan alıntı yapmasını** hedefler. Bunun için
uygulananlar:

1. **Kısa cevap blokları.** Her önemli sayfanın en üstünde 40-60 kelimelik, tek başına anlam ifade eden
   doğrudan cevap kutusu var (`[data-answer]`). AI motorları bu bloğu tek parça halinde alıntılamaya
   uygun buluyor.
2. **Soru formatlı başlıklar.** "Kaç BTU klima almalıyım?", "No-Frost ile statik arasındaki fark" gibi
   H2'ler, kullanıcıların AI'ya sorduğu cümlelerle birebir örtüşüyor.
3. **Karşılaştırma tabloları.** Buzdolabı litre tablosu, klima BTU tablosu, kurutma makinesi tip
   karşılaştırması, bulaşık makinesi kapasite tablosu, ankastre ölçü tablosu. Tablolar AI'nın en kolay
   ayrıştırdığı içerik biçimi.
4. **`llms.txt` dosyası.** Sitenin yapısını, işletme bilgilerini ve tüm sayfa listesini AI tarayıcıları
   için sadeleştirilmiş markdown formatında sunar. Kök dizinde yayınlanıyor.
5. **AI tarayıcılarına açık `robots.txt`.** GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot,
   Google-Extended, Applebot-Extended ve CCBot açıkça `Allow` işaretli. Kapatılırsa alıntılanma
   ihtimali sıfırlanır.
6. **Net varlık (entity) tanımları.** "Odabaşı Dayanıklı Tüketim, İzmir merkezli... LG, Uğur ve Altus yetkili
   bayisidir" cümlesi sitede tutarlı biçimde tekrarlanıyor. AI modelleri varlık-ilişki eşleşmesini
   böyle kuruyor.
7. **`speakable` schema** blog yazılarında, sesli asistan alıntılaması için.
8. **Tarih damgası.** Her blog yazısında `datePublished` ve `dateModified`; AI'lar güncelliği sinyal
   olarak kullanıyor.

---

## 8. Anahtar kelime haritası

Her sayfa tek bir ana kelimeye odaklandı; yamyamlaştırma (keyword cannibalization) olmaması için
kelime çakışması yok.

### Kategori sayfaları (ticari niyet)

| Sayfa | Ana kelime | Destek kelimeler |
|---|---|---|
| `kategori/buzdolabi` | buzdolabı modelleri | no-frost buzdolabı, gardırop tipi buzdolabı, kaç litre buzdolabı |
| `kategori/camasir-makinesi` | çamaşır makinesi | 8 kg çamaşır makinesi, çamaşır makinesi devir sayısı, inverter motor |
| `kategori/bulasik-makinesi` | bulaşık makinesi | 13 kişilik bulaşık makinesi, ankastre bulaşık makinesi, kaç dB |
| `kategori/kurutma-makinesi` | kurutma makinesi | ısı pompalı kurutucu, yoğuşmalı kurutma makinesi |
| `kategori/ankastre-set` | ankastre set | ankastre fırın ölçüleri, ankastre ocak tezgah kesimi, davlumbaz emiş gücü |
| `kategori/klima` | klima montaj | kaç BTU klima, inverter klima, klima fiyatları izmir |
| `kategori/derin-dondurucu` | derin dondurucu | sandık tipi derin dondurucu, dikey derin dondurucu |
| `kategori/ticari-sogutma` | ticari soğutma | market reyon dolabı, şişe soğutucu, dondurma kabini, pastane teşhir dolabı |
| `kategori/televizyon` | televizyon modelleri | oled qled farkı, kaç inç televizyon |
| `kategori/kucuk-ev-aletleri` | küçük ev aletleri | elektrikli süpürge, kahve makinesi |
| `kategori/temizlik-ekipmanlari` | basınçlı yıkama makinesi | kärcher, buharlı temizleyici, kaç bar |

### Marka sayfaları (marka + lokasyon niyeti)

`lg bayi izmir`, `uğur bayi izmir`, `uğur ticari soğutma`, `grundig ankastre`, `electrolux ankastre fırın`,
`hoover çamaşır makinesi`, `tcl televizyon`, `altus beyaz eşya`, `şenocak ankastre`, `kärcher izmir`,
`rota ankastre`

### Lokasyon sayfaları (yerel niyet — en yüksek dönüşüm)

`izmir beyaz eşya`, `buca beyaz eşya`, `bornova beyaz eşya`, `karabağlar beyaz eşya`,
`gaziemir beyaz eşya`, `menemen beyaz eşya`, `torbalı beyaz eşya`, `çiğli beyaz eşya`,
`aydın beyaz eşya`, `nazilli beyaz eşya`, `kuşadası beyaz eşya`, `manisa beyaz eşya`,
`turgutlu beyaz eşya`, `salihli beyaz eşya`

### Blog (bilgi niyeti — GEO ve huni üstü)

`buzdolabı nasıl seçilir`, `klima btu hesaplama`, `enerji sınıfları ne anlama geliyor`,
`ankastre set alırken dikkat edilmesi gerekenler`, `ticari soğutucu seçimi`,
`izmir beyaz eşya alırken nelere dikkat etmeli`

**İç linkleme:** Kategori ↔ marka ↔ lokasyon üçgeni çapraz bağlı. Her blog yazısı ilgili kategori
sayfalarına, her kategori sayfası ilgili markalara ve lokasyon hub'larına link veriyor.

---

## 9. Yayın sonrası yol haritası

**İlk hafta**

- Search Console + Bing Webmaster kurulumu, sitemap gönderimi
- Google Business Profile: kategori seçimi ("Beyaz eşya mağazası", "Ev aletleri mağazası"), ürün
  fotoğrafları, açılış saatleri, site linki
- Yerel dizin kayıtları (NAP birebir aynı): Yandex Business, Foursquare, sarı sayfa siteleri

**İlk ay**

- Marka logolarının `assets_src/markalar/` klasörüne eklenmesi
- Gerçek mağaza ve ürün fotoğrafları eklenmesi — şu an sitede fotoğraf yok, ikon tabanlı tasarım var.
  Fotoğraf eklendiğinde `ImageObject` schema ve `og:image` de tanımlanmalı
- Google yorumları toplanmaya başlanması
- Gerçek Google yorumları biriktikten sonra `AggregateRating` schema'sının eklenmesi
- 3-4 yeni blog yazısı: "Çamaşır makinesi kaç kg olmalı", "Bulaşık makinesi kaç kişilik alınmalı",
  "Ankastre mutfak yenileme rehberi", "Market açarken ekipman listesi"

**2-3. ay**

- Lokasyon sayfalarının performansına göre yeni ilçe sayfaları (Menderes, Kemalpaşa, Söke, Didim, Akhisar)
- Ürün detay sayfaları — model bazlı sayfalar `Product` schema ile eklenirse alışveriş sorgularında
  görünürlük ciddi artar
- AI görünürlük takibi: ChatGPT ve Perplexity'de "izmir uğur bayi", "izmir market reyon dolabı"
  gibi sorgularla siteyi arayıp alıntılanıp alıntılanmadığını kontrol edin

---

## 10. Yeniden üretim

```bash
python3 build.py
```

`data.py` içeriği değiştirip komutu çalıştırdığınızda `site/` klasörü sıfırdan üretilir.
Yeni bir kategori, marka, lokasyon veya blog yazısı eklemek için ilgili listeye bir sözlük eklemeniz
yeterli — sayfa, menü, footer, iç linkler, sitemap ve llms.txt otomatik güncellenir.
