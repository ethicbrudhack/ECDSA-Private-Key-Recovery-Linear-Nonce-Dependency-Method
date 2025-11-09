import ecdsa
from ecdsa.numbertheory import inverse_mod
from ecdsa.ecdsa import generator_secp256k1

# ✅ Konwersja danych do liczb całkowitych
r1 = int("8c7417b1ac540660efca6105f9aea0d80f97dcf95bbe2728f67f51775c5fe570", 16)
s1 = int("6c32f2b0e83a8ab28b39ecb98984f23428412eb104695b4e2da0bb4d8ed79ce3", 16)
z1 = int("229a724d52d0769139faba866c616889bfb53b3e2c30da04684ade4adabe4e6d", 16)

r2 = int("c1e07621089b625414ce56c4254fb53789c63fb5cd32037fccad39166439c6bc", 16)
s2 = int("5425dfcba74f0e5ea6709834b308fd5a475a5fd42d8077c96eb61378ff0ee245", 16)
z2 = int("ef82025de9311d305b777b8f8a866d5cc63772f06192d89eb5183c28454b317d", 16)

# ✅ Stała wartość krzywej secp256k1 (order n)
n = generator_secp256k1.order()

# ✅ Obliczenie `k`
delta_s = (s1 - s2) % n
delta_z = (z1 - z2) % n

if delta_s != 0:
    k = (delta_z * inverse_mod(delta_s, n)) % n
    print(f"\n✅ Wykryto liniową zależność k! k = {hex(k)}")
else:
    print("\n❌ Brak liniowej zależności w k")
    exit()

# ✅ Obliczenie `d`
d1 = ((s1 * k - z1) * inverse_mod(r1, n)) % n
d2 = ((s2 * k - z2) * inverse_mod(r2, n)) % n

if d1 == d2:
    print(f"\n✅ 🔥 Obliczony klucz prywatny d = {hex(d1)}")
else:
    print("\n❌ Coś jest nie tak - d1 ≠ d2! Możliwe, że to błąd w danych.")

