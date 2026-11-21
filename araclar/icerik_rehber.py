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
