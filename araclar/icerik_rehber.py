# -*- coding: utf-8 -*-
"""dablabs.ai kurulum rehberleri (/rehber/).

Yeni rehber eklemek:
  1. PDF'i rehber/pdf/<slug>-kurulum-rehberi.pdf adıyla koy.
  2. Aşağıdaki REHBERLER listesinin EN ÜSTÜNE bir kayıt ekle (en yeni üstte).
  3. python araclar/uret.py  (kapak önizlemesi, sayfa sayısı ve boyut otomatik)

DM'den doğrudan bir rehbere link vermek için: https://dablabs.net/rehber/#<slug>
"""

REHBERLER = [
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
