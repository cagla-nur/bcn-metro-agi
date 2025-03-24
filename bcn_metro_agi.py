from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx  # İstasyonun kimlik numarası
        self.ad = ad  # İstasyonun adı
        self.hat = hat  # İstasyonun bağlı olduğu hat
        self.komsular = []  # Komşu istasyonları ve aralarındaki süreleri saklar
    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))
    def __repr__(self):
        #nesnenin okunabilir bir temsilini döndürür
         return f"Istasyon({self.idx}, {self.ad}, {self.hat})"
    def komsu_listesi(self):
         #istasyonun komşularını listeler
        return [(komsu.ad, sure) for komsu, sure in self.komsular]
        #return:komşu istasyonların adları ve süreleri içeren bir liste
    
    def __lt__(self, other: 'Istasyon'):
        return self.ad < other.ad  # Sıralama için ad bazlı karşılaştırma

# 1)Barcelona Metro İstasyonlarını Tanımla
ist1 = Istasyon("L2", "Clot", "Mor Hat")
ist2 = Istasyon("L1", "Clot", "Kırmızı Hat")
ist3 = Istasyon("L5", "Sagrada Familia", "Mavi Hat")
ist4 = Istasyon("L2", "Sagrada Familia", "Mor Hat")
ist5 = Istasyon("L1", "Arc De Triomf", "Kırmızı Hat")
ist6 = Istasyon("L5", "Verdauger", "Mavi Hat")
ist7 = Istasyon("L5", "Diagonal", "Mavi Hat")
ist8 = Istasyon("L3", "Diagonal", "Yeşil Hat")
ist9 = Istasyon("L2", "Passeig de Gracia", "Mor Hat")
ist10 = Istasyon("L2", "Passeig de Gracia", "Yeşil Hat")
ist11 = Istasyon("L1", "Universitat", "Kırmızı Hat")
ist12 = Istasyon("L2", "Universitat", "Mor Hat")
ist13 = Istasyon("L2", "Paralel", "Mor Hat")
ist14 = Istasyon("L3", "Paralel", "Yeşil Hat")
ist15 = Istasyon("L3", "Espanya", "Yeşil Hat")
ist16 = Istasyon("L1", "Espanya", "Kırmızı Hat")
ist17 = Istasyon("L1", "Torrassa", "Kırmızı Hat")
ist18 = Istasyon("L5", "Plaça de Sants", "Mavi Hat")
ist19 = Istasyon("L5", "Collblanc", "Mavi Hat")
ist20 = Istasyon("L3", "Zona Universitària", "Yeşil Hat")
ist21 = Istasyon("L9", "Zona Universitària", "Turuncu Hat")
ist22 = Istasyon("L9", "Collblanc", "Turuncu Hat")
ist23 = Istasyon("L9", "Torrassa", "Turuncu Hat")
ist24 = Istasyon("L9", "Aeroport T1", "Turuncu Hat")




# 2)Komşu istasyonları ekle
ist3.komsu_ekle(ist6, 2)   # Sagrada Familia -> Verdauger (2 dakika)
ist6.komsu_ekle(ist7, 3)   # Verdauger -> Diagonal (3 dakika)
ist8.komsu_ekle(ist10, 7)   # Diagonal -> Passeig De Gracia (7 dakika)
ist9.komsu_ekle(ist12, 3)   # Passeig de Gracia -> Universitat (3 dakika)
ist21.komsu_ekle(ist22, 6)   # Zona Universitària -> Collblanc (6 dakika)
ist22.komsu_ekle(ist23, 7)   # Collblanc -> Torrassa (7 dakika)




print(ist1)
print(ist2)
print(ist3)
print(ist4)
print(ist5)
print(ist6)
print(ist7)
print(ist8)
print(ist9)
print(ist10)
print(ist11)
print(ist12)
print(ist13)
print(ist14)
print(ist15)
print(ist16)
print(ist17)
print(ist18)
print(ist19)
print(ist20)
print(ist21)
print(ist22)
print(ist23)
print(ist24)

print("\n========================")
# 3)Komşu listelerini yazdır
print(f"{ist3.ad} komşuları: {ist3.komsu_listesi()}")
print(f"{ist6.ad} komşuları: {ist6.komsu_listesi()}")
print(f"{ist8.ad} komşuları: {ist8.komsu_listesi()}")
print(f"{ist9.ad} komşuları: {ist9.komsu_listesi()}")
print(f"{ist21.ad} komşuları: {ist21.komsu_listesi()}")
print(f"{ist22.ad} komşuları: {ist22.komsu_listesi()}")

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}  # İstasyonları saklayan sözlük
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)  # Hatlara göre istasyon listeleri
    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None: #metro ağına yeni bir istasyon ekler
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)
    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None: #iki istasyon arasında bağlantı ekler
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

     # BFS Algoritması: En Az Aktarmalı Rota
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List['Istasyon']]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = set()

        while kuyruk:
            mevcut_istasyon, yol = kuyruk.popleft()
            if mevcut_istasyon == hedef:
                return yol
            for komsu, _ in mevcut_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    kuyruk.append((komsu, yol + [komsu]))

        return None  # Rota bulunamazsa None döndür

    # A* Algoritması: En Hızlı Rota
    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List['Istasyon'], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        pq = [(0, id(baslangic), baslangic, [baslangic])]
        ziyaret_edildi = {}

        while pq:
            toplam_sure, _, mevcut_istasyon, yol = heapq.heappop(pq)
            if mevcut_istasyon == hedef:
                return yol, toplam_sure
            if mevcut_istasyon in ziyaret_edildi and ziyaret_edildi[mevcut_istasyon] <= toplam_sure:
                continue
            ziyaret_edildi[mevcut_istasyon] = toplam_sure
            for komsu, sure in mevcut_istasyon.komsular:
                heapq.heappush(pq, (toplam_sure + sure, id(komsu), komsu, yol + [komsu]))

        return None  # Eğer hedefe ulaşılamıyorsa None döndür

metro = MetroAgi()

# 4)Önemli istasyonları ekle
metro.istasyon_ekle("L2-Clot", "Clot", "Mor Hat")
metro.istasyon_ekle("L1-Clot", "Clot", "Kırmızı Hat")
metro.istasyon_ekle("L5-Sagrada Familia", "Sagrada Familia", "Mavi Hat")
metro.istasyon_ekle("L2-Sagrada Familia", "Sagrada Familia", "Mor Hat")
metro.istasyon_ekle("L5-Verdauger", "Verdauger", "Mavi Hat")
metro.istasyon_ekle("L5-Diagonal", "Diagonal", "Mavi Hat")
metro.istasyon_ekle("L3-Diagonal", "Diagonal", "Yeşil Hat")
metro.istasyon_ekle("L1-Arc De Triomf", "Arc De Triomf", "Kırmızı Hat") 
metro.istasyon_ekle("L2-Passeig de Gracia", "Passeig de Gracia", "Mor Hat")
metro.istasyon_ekle("L1-Universitat", "Universitat", "Kırmızı Hat")
metro.istasyon_ekle("L2-Universitat", "Universitat", "Mor Hat")
metro.istasyon_ekle("L2-Paralel", "Paralel", "Mor Hat")
metro.istasyon_ekle("L3-Paralel", "Paralel", "Yeşil Hat")
metro.istasyon_ekle("L3-Espanya", "Espanya", "Yeşil Hat")
metro.istasyon_ekle("L1-Espanya", "Espanya", "Kırmızı Hat")
metro.istasyon_ekle("L1-Torrassa", "Torrassa", "Kırmızı Hat")
metro.istasyon_ekle("L9-Torrassa", "Torrassa", "Turuncu Hat")
metro.istasyon_ekle("L5-Plaça de Sants", "Plaça de Sants", "Mavi Hat")
metro.istasyon_ekle("L5-Collblanc", "Collblanc", "Mavi Hat")
metro.istasyon_ekle("L9-Collblanc", "Collblanc", "Turuncu Hat")
metro.istasyon_ekle("L3-Zona Universitària", "Zona Universitària", "Yeşil Hat")
metro.istasyon_ekle("L9-Zona Universitària", "Zona Universitària", "Turuncu Hat")
metro.istasyon_ekle("L9-Aeroport T1", "Aeroport T1", "Turuncu Hat")

# 5) Bağlantıları dk cinsinden ekle
#L1 kırmızı hat bağlantıları
metro.baglanti_ekle("L1-Clot", "L1-Arc De Triomf", 5)
metro.baglanti_ekle("L1-Arc De Triomf", "L1-Universitat", 7)
metro.baglanti_ekle("L1-Universitat", "L1-Espanya", 4)
metro.baglanti_ekle("L1-Espanya", "L1-Torrassa", 7)
#L2 mor hat bağlantıları
metro.baglanti_ekle("L2-Clot", "L2-Sagrada Familia", 6)
metro.baglanti_ekle("L2-Sagrada Familia", "L2-Passeig de Gracia", 5)
metro.baglanti_ekle("L2-Passeig de Gracia", "L2-Universitat", 3)
metro.baglanti_ekle("L2-Universitat", "L2-Paralel", 3)
#L3 yeşil hat bağlantıları
metro.baglanti_ekle("L3-Paralel", "L3-Espanya", 3)
metro.baglanti_ekle("L3-Espanya", "L3-Zona Universitària", 13)
#L5 mavi hat bağlantıları
metro.baglanti_ekle("L5-Sagrada Familia", "L5-Verdauger", 2)
metro.baglanti_ekle("L5-Verdauger", "L5-Diagonal", 3)
metro.baglanti_ekle("L5-Diagonal", "L5-Plaça de Sants", 8)
metro.baglanti_ekle("L5-Plaça de Sants", "L5-Collblanc", 5)
#L9 turuncu hat bağlantıları
metro.baglanti_ekle("L9-Torrassa", "L9-Collblanc", 6)
metro.baglanti_ekle("L9-Collblanc", "L9-Zona Universitària", 7)
metro.baglanti_ekle("L9-Zona Universitària", "L9-Aeroport T1", 36)


metro.baglanti_ekle("L2-Clot", "L1-Clot", 2)  # Clot (L2 ↔ L1)
metro.baglanti_ekle("L2-Sagrada Familia", "L5-Sagrada Familia", 2)  # Sagrada Familia (L2 ↔ L5)
metro.baglanti_ekle("L3-Diagonal", "L5-Diagonal", 2)  # Diagonal (L3 ↔ L5)
metro.baglanti_ekle("L2-Universitat", "L1-Universitat", 2)  # Universitat (L2 ↔ L1)
metro.baglanti_ekle("L2-Paralel", "L3-Paralel", 2)  # Paralel (L2 ↔ L3)
metro.baglanti_ekle("L3-Espanya", "L1-Espanya", 2)  # Espanya (L3 ↔ L1)
metro.baglanti_ekle("L1-Torrassa", "L9-Torrassa", 2)  # Torrassa (L1 ↔ L9)
metro.baglanti_ekle("L5-Collblanc", "L9-Collblanc", 2)  # Collblanc (L5 ↔ L9)
metro.baglanti_ekle("L3-Zona Universitària", "L9-Zona Universitària", 2)  # Zona Universitària (L3 ↔ L9)


for hat, istasyonlar in metro.hatlar.items():
    print(f"\n🛤 {hat}: {', '.join(i.ad for i in istasyonlar)}")

# 8) Test Senaryoları
if __name__ == "__main__":
    
    print("\n========================")
    print("🚇 SAGRADA FAMILIA ➝ AEROPORT T1 ROTA TESTLERİ")
    print("========================")

    # En az aktarmalı rotalar
    print("\n📌 [L2] Sagrada Familia'dan Aeroport T1'e (En Az Aktarmalı Rota):")
    rota1 = metro.en_az_aktarma_bul("L2-Sagrada Familia", "L9-Aeroport T1")
    if rota1:
        print(" → ".join(f"{i.ad} ({i.idx})" for i in rota1))
    else:
        print("Rota bulunamadı.")

    print("\n[L5] Sagrada Familia'dan Aeroport T1'e (En Az Aktarmalı Rota):")
    rota2 = metro.en_az_aktarma_bul("L5-Sagrada Familia", "L9-Aeroport T1")
    if rota2:
        print(" → ".join(f"{i.ad} ({i.idx})" for i in rota2))
    else:
        print("Rota bulunamadı.")

    # En hızlı rotalar
    print("\n[L2] Sagrada Familia'dan Aeroport T1'e (En Hızlı Rota):")
    hizli1 = metro.en_hizli_rota_bul("L2-Sagrada Familia", "L9-Aeroport T1")
    if hizli1:
        yol, sure = hizli1
        print(f"Süre: {sure} dk")
        print(" → ".join(f"{i.ad} ({i.idx})" for i in yol))
    else:
        print("Rota bulunamadı.")

    print("\n[L5] Sagrada Familia'dan Aeroport T1'e (En Hızlı Rota):")
    hizli2 = metro.en_hizli_rota_bul("L5-Sagrada Familia", "L9-Aeroport T1")
    if hizli2:
        yol, sure = hizli2
        print(f"Süre: {sure} dk")
        print(" → ".join(f"{i.ad} ({i.idx})" for i in yol))
    else:
        print("Rota bulunamadı.")
print("\n========================")
print("🚇 SAGRADA FAMILIA ➝ ARC DE TRIOMF TESTLERİ")        
print("========================")
# En az aktarmalı rota
print("\n[L5] Sagrada Familia'dan Arc de Triomf'a (En Az Aktarmalı Rota):")
rota1 = metro.en_az_aktarma_bul("L5-Sagrada Familia", "L1-Arc De Triomf")
if rota1:
    print(" → ".join(f"{i.ad} ({i.idx})" for i in rota1))
else:
    print("Rota bulunamadı.")

# En hızlı rota
print("\n[L5] Sagrada Familia'dan Arc de Triomf'a (En Hızlı Rota):")
hizli1 = metro.en_hizli_rota_bul("L5-Sagrada Familia", "L1-Arc De Triomf")
if hizli1:
    yol, sure = hizli1
    print(f"Süre: {sure} dk")
    print(" → ".join(f"{i.ad} ({i.idx})" for i in yol))
else:
    print("Rota bulunamadı.")
   

  

    

  

