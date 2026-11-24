# -*- coding: utf-8 -*-
"""dablabs.ai kurulum rehberleri (/rehber/).

Yeni rehber eklemek:
  1. PDF'i rehber/pdf/<slug>-kurulum-rehberi.pdf adıyla koy.
  2. Aşağıdaki REHBERLER listesinin EN ÜSTÜNE bir kayıt ekle (en yeni üstte).
  3. python araclar/uret.py  (kapak önizlemesi, sayfa sayısı ve boyut otomatik)

DM/otomasyon linki: https://dablabs.net/rehber/<slug>/  (yayına çıktıktan sonra slug değiştirilmez)
"""

REHBERLER = [
    {
        'slug': 'voicestudio',
        'baslik': 'VoiceStudio: Sesini ücretsiz klonla',
        'ozet': "ElevenLabs'in yaptığı ses klonlama, dublaj, yazıya dökme ve sesli kitap işlerini ücretsiz ve kendi "
                "bilgisayarında yapan açık kaynak programı kur. Windows, Mac ve Linux kurulumu ile ilk klon adımları içinde.",
        'etiketler': ['Ses', 'Yapay Zekâ', 'Açık Kaynak'],
        'tarih': '2026-11-24',
    },
    {
        'slug': 'hiring-panel',
        'baslik': "Hiring Panel: CV'ni 7 Claude'a reddettir",
        'ozet': "CV'ni ve iş ilanını yedi farklı değerlendirici Claude'a okutan, hataları tek listede toplayıp CV'ni "
                "aynı bilgilerle baştan yazan ücretsiz skill'i kur. Kullanım komutu ve ipuçları da içinde.",
        'etiketler': ['Kariyer', 'Claude Code', 'Skill'],
        'tarih': '2026-11-24',
    },
    {
        'slug': 'whatsapp-asistan',
        'baslik': 'Claude ile WhatsApp asistanı',
        'ozet': "Müşteri mesajlarına senin yerine cevap veren, fiyat söyleyen ve randevu alan yapay zekâ asistanını "
                "Claude Code ve Kapso ile kur. Maliyetler, numara bağlama ve esnafa satarken dikkat edilecekler de içinde.",
        'etiketler': ['WhatsApp', 'Claude Code', 'Otomasyon'],
        'tarih': '2026-11-23',
    },
    {
        'slug': 'claude-mem',
        'baslik': "claude-mem: Claude'a kalıcı hafıza",
        'ozet': "Claude Code'un oturumlar arasında her şeyi unutmasını bitiren ücretsiz eklentiyi kur. "
                "Yaptıklarını kaydedip özetliyor, yeni oturumda kaldığın yerden devam ediyor. Gizlilik ayarları da içinde.",
        'etiketler': ['Claude Code', 'Eklenti', 'Hafıza'],
        'tarih': '2026-11-23',
    },
    {
        'slug': 'youtube-agent',
        'baslik': 'YouTube Agent: YouTube için ücretsiz Claude ekibi',
        'ozet': "YouTube videoların için haftalık plan, senaryo, kurgu listesi, izlenme analizi ve nişindeki viral "
                "videoları Claude'a hazırlatan ücretsiz eklentiyi kur. Claude Code ve Claude.ai kurulumu içinde.",
        'etiketler': ['YouTube', 'Claude Code', 'Eklenti'],
        'tarih': '2026-11-22',
    },
    {
        'slug': 'superpowers',
        'baslik': "Superpowers: Claude'a süper güç veren eklenti",
        'ozet': "Claude Code'un koda dalmadan önce soru sormasını, plan yapmasını, testle ilerlemesini ve "
                "hataları kök nedeninden çözmesini sağlayan eklentiyi kur. Cursor, Codex ve Gemini CLI kurulumu da içinde.",
        'etiketler': ['Claude Code', 'Eklenti', 'Cursor · Codex · Gemini'],
        'tarih': '2026-11-21',
    },
    {
        'slug': 'claude-5-skill',
        'baslik': 'Claude için 5 süper skill',
        'ozet': "Content Research Writer, Frontend Design, Obsidian, Skill Creator ve Remotion'ı "
                "Claude Code ve Claude.ai'de adım adım kur. Sorun giderme ve güvenlik notları da içinde.",
        'etiketler': ['Claude Code', 'Claude.ai', 'Skill'],
        'tarih': '2026-11-20',
    },
    {
        'slug': 'karpathy-skills',
        'baslik': "Karpathy Skills: Claude'u toparlayan tek dosya",
        'ozet': "Claude Code'un gereksiz kod yazmasını, istemediğin yerlere dokunmasını ve test etmeden "
                "\"bitti\" demesini engelleyen CLAUDE.md dosyasını üç farklı yolla kur.",
        'etiketler': ['Claude Code', 'CLAUDE.md'],
        'tarih': '2026-11-20',
    },
]
