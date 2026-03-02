from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.visualization import circuit_drawer
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. CONFIGURACIÓN DE ALICIA Y BOB
# ==========================================
num_bits = 8
alice_bits = np.random.randint(2, size=num_bits)
alice_bases = np.random.randint(2, size=num_bits)
bob_bases = np.random.randint(2, size=num_bits)

print("--- DATOS INICIALES ---")
print(f"Bits de Alicia:  {alice_bits}")
print(f"Bases Alicia:    {alice_bases} (0=Rectilínea, 1=Diagonal)")
print(f"Bases Bob:       {bob_bases} (0=Rectilínea, 1=Diagonal)\n")

# ==========================================
# 2. CREACIÓN DEL CIRCUITO CUÁNTICO
# ==========================================
qc = QuantumCircuit(num_bits)

for i in range(num_bits):
    # Alicia prepara los qubits
    if alice_bits[i] == 1:
        qc.x(i)
    if alice_bases[i] == 1:
        qc.h(i)
    # Bob mide (aplica Hadamard si su base es diagonal)
    if bob_bases[i] == 1:
        qc.h(i)

qc.measure_all()

# --- GRÁFICA 1: Dibujo del Circuito ---
print("Generando esquema del circuito cuántico...")
display(qc.draw('mpl', style='iqp'))


# ==========================================
# 3. CONEXIÓN Y EJECUCIÓN EN HARDWARE DE IBM
# ==========================================
service = QiskitRuntimeService(
    channel="ibm_quantum_platform", 
    token="TU_TOKEN_AQUI" # ¡Protege tu clave!
)

backend = service.least_busy(operational=True, simulator=False)
print(f"\n🚀 Conectando y enviando trabajo al ordenador físico: {backend.name}...")

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)

sampler = Sampler(mode=backend)
job = sampler.run([isa_circuit], shots=1)
print(f"⏳ Trabajo en cola. ID: {job.job_id()}")
print("Esperando resultados del hardware real...\n")

result = job.result()
pub_result = result[0]
measured_counts = pub_result.data.meas.get_counts()
measured_bits_str = list(measured_counts.keys())[0]

# Invertimos el string (Qiskit lee de derecha a izquierda)
bob_results = [int(bit) for bit in reversed(measured_bits_str)]
print(f"Resultados de la medición de Bob: {bob_results}\n")

# ==========================================
# 4. CRIBA DE CLAVES (SIFTING) Y ANÁLISIS
# ==========================================
alice_key = []
bob_key = []

for i in range(num_bits):
    if alice_bases[i] == bob_bases[i]:
        alice_key.append(alice_bits[i])
        bob_key.append(bob_results[i])

print("--- CLAVE SECRETA FINAL ---")
print(f"Clave de Alicia: {alice_key}")
print(f"Clave de Bob:    {bob_key}")

# --- GRÁFICA 2: Tabla Visual de Sifting (CORREGIDA) ---
fig, ax = plt.subplots(figsize=(10, 4))
indices = np.arange(num_bits)
ax.scatter(indices, [2]*num_bits, c=['#2ca02c' if b==0 else '#1f77b4' for b in alice_bases], marker='s', s=150, label='Bases Alicia (Verde=Rectilínea / Azul=Diagonal)')
ax.scatter(indices, [1]*num_bits, c=['#2ca02c' if b==0 else '#1f77b4' for b in bob_bases], marker='o', s=150, label='Bases Bob (Verde=Rectilínea / Azul=Diagonal)')

for i in range(num_bits):
    if alice_bases[i] == bob_bases[i]:
        ax.axvline(x=i, color='gray', linestyle='--', alpha=0.5)
        ax.text(i, 1.5, "OK", ha='center', fontsize=11, fontweight='bold', color='#2ca02c')

ax.set_yticks([1, 2])
ax.set_yticklabels(['Bob', 'Alicia'])
ax.set_ylim(0.5, 2.5)
ax.set_xlabel("Índice del Qubit")
plt.title("Proceso de Sifting: Coincidencia de Bases")

# Leyenda ajustada abajo para evitar solapamientos
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=1)

plt.tight_layout()
plt.show()

# ==========================================
# 5. CÁLCULO DE ERROR CUÁNTICO (QBER)
# ==========================================
if len(alice_key) > 0:
    errors = sum(1 for a, b in zip(alice_key, bob_key) if a != b)
    qber = (errors / len(alice_key)) * 100
    print(f"\n📊 ANÁLISIS DE SEGURIDAD:")
    print(f"Tasa de Error de Bit Cuántico (QBER): {qber:.2f}%")
    if qber == 0:
        print("✅ QBER del 0%: Transmisión perfecta. Clave 100% segura.")
    elif qber < 11:
        print("⚠️ QBER bajo: El error se debe al ruido cuántico del procesador (Decoherencia). La clave aún puede ser segura tras aplicar corrección de errores.")
    else:
        print("🚨 QBER alto: Posible interceptación de un espía (Eva) o demasiado ruido térmico en el chip.")
else:
    print("\n⚠️ No hubo coincidencias de bases, no se pudo generar una clave.")
