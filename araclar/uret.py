# -*- coding: utf-8 -*-
"""Sitedeki üretilen sayfaların hepsini yeniden oluşturur.

Kullanım (repo kökünden):  python araclar/uret.py

Sıra önemli değil ama hepsi index.html'deki TR header/footer'ı kaynak alır.
"""
import os, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for name in ('uret_calismalar', 'uret_blog', 'uret_hizmetler', 'uret_en'):
    print('==', name)
    runpy.run_path(os.path.join(HERE, name + '.py'), run_name='__main__')
print('Bitti. Değişiklikleri "git diff" ile kontrol edin.')
