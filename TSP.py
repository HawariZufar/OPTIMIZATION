# 1: Import Library
import pulp as lp
from geopy.distance import geodesic

# 2: Data koordinat kota
kota = ['blitar', 'malang', 'surabaya', 'pasuruan', 'batu']
koordinat = {
    'blitar': (-8.1014651, 112.1676820),
    'malang': (-7.9772720, 112.6340990),
    'surabaya': (-7.2392846, 112.7362112),
    'pasuruan': (-7.6425806, 112.9104354),
    'batu': (-7.8671000, 112.5239030)
}

# 3: Jarak Antar Kota
def hitung_jarak(kota1, kota2):
    return geodesic(koordinat[kota1], koordinat[kota2]).km

# 3a: Matriks jarak antar kota
jarak = {}
for i in kota:
    for j in kota:
        if i != j:
            jarak[(i, j)] = hitung_jarak(i, j)

# 4: Definisikan Masalah TSP
problem = lp.LpProblem("TSP", lp.LpMinimize)

# 5: Variabel Keputusan
rute = lp.LpVariable.dicts('rute', jarak, 0, 1, lp.LpBinary)
urutan = lp.LpVariable.dicts('urutan', kota, 0, len(kota)-1, lp.LpInteger)

# 6: Fungsi Tujuan
problem += lp.lpSum([jarak[(i, j)] * rute[(i, j)] for i in kota for j in kota if i != j])

# 7: Constraints 
# 7a: Setiap kota hanya menjadi tujuan sekali
for k in kota:
    problem += lp.lpSum([rute[(k, j)] for j in kota if j != k]) == 1, f"Ke_{k}"

# 7b: Setiap kota hanya menjadi asal sekali
    problem += lp.lpSum([rute[(i, k)] for i in kota if i != k]) == 1, f"Dari_{k}"

# 7c: Menghindari tur yang terputus atau memutar
n = len(kota)
for i in kota:
    for j in kota:
        if i != j and (i != 'blitar' and j != 'blitar'):
            problem += urutan[i] - urutan[j] + n * rute[(i, j)] <= n - 1

# 8: Menyelesaikan Masalah TSP
status = problem.solve(lp.PULP_CBC_CMD(msg=False))

# 9: Menampilkan Hasil
print("Status:", lp.LpStatus[status])

# 9a: Menampilkan rute optimal yang ditemukan
for i in problem.variables():
    if i.varValue == 1:
        print(i.name, ":", i.varValue)

print("Total Jarak:", lp.value(problem.objective))

# 10: Mengambil rute optimal berdasarkan solusi
rute_optimal = ['blitar']

# 10a: Menentukan urutan kota berdasarkan solusi yang ditemukan
while len(rute_optimal) < len(kota):
    last_city = rute_optimal[-1]
    for next_city in kota:
        if next_city != last_city:
            route_var = rute[(last_city, next_city)]
            if route_var.varValue == 1:
                rute_optimal.append(next_city)
                break

# 10b: Menampilkan rute optimal
print("Rute Optimal:", " -> ".join(rute_optimal))