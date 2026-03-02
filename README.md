# Quantum Key Distribution (QKD): Implementación del Protocolo BB84 en Hardware Real

![Status](https://img.shields.io/badge/Status-Completed-success)
![Platform](https://img.shields.io/badge/Platform-IBM_Quantum-blue)
![Technology](https://img.shields.io/badge/Technology-Qiskit-red)

## 📋 Descripción del Proyecto
Este proyecto presenta la implementación práctica del protocolo **BB84** (Bennett-Brassard 1984) para la Distribución Cuántica de Claves. A diferencia de la criptografía clásica basada en complejidad matemática, este sistema utiliza las leyes de la mecánica cuántica para garantizar la seguridad de la información.

El código ha sido ejecutado con éxito en el procesador cuántico real **ibm_torino** de IBM Quantum Platform.

##  Fundamentos Teóricos
El protocolo BB84 se basa en dos pilares de la física cuántica:
1. **Teorema de No Clonación**: Es imposible crear una copia idéntica de un estado cuántico desconocido.
2. **Colapso de la Función de Onda**: El acto de medir un sistema cuántico altera su estado. Si un espía (Eva) intenta interceptar los qubits, introducirá errores detectables por los usuarios legítimos (Alicia y Bob).

## 🛠️ Estructura del Código
El flujo de trabajo implementado en Python con **Qiskit** sigue estos pasos:

1. **Preparación (Alicia)**: Se generan bits aleatorios y se codifican en bases aleatorias (Rectilínea $|0\rangle, |1\rangle$ o Diagonal $|+\rangle, |-\rangle$) utilizando puertas **X** y **Hadamard (H)**.
2. **Transmisión y Medición (Bob)**: Bob elige bases al azar para medir los qubits recibidos.
3. **Criba (Sifting)**: Se comparan públicamente las bases utilizadas. Solo se conservan los bits donde las bases de Alicia y Bob coinciden.
4. **Análisis de Seguridad (QBER)**: Se calcula la tasa de error (Quantum Bit Error Rate). En hardware real, este valor refleja el ruido cuántico intrínseco del dispositivo.

##  Resultados en Hardware Real
El experimento se realizó utilizando 8 qubits físicos. Los resultados demuestran la viabilidad de la generación de claves, logrando identificar con éxito las coincidencias de bases necesarias para establecer un canal seguro.

### Visualizaciones Incluidas:
* **Circuito Cuántico**: Representación de las puertas lógicas aplicadas a cada qubit.
* **Gráfico de Sifting**: Comparativa visual de las bases de Alicia y Bob con marcado de coincidencias exitosas.

## 🛠️ Cómo ejecutar en Hardware Real de IBM

Si deseas replicar este experimento utilizando los procesadores cuánticos de IBM, sigue estos pasos para configurar tu entorno y obtener tus credenciales:

### 1. Registro en IBM Quantum
Para acceder a los dispositivos físicos (como el `ibm_torino` utilizado en este proyecto), debes crear una cuenta gratuita en [IBM Quantum Platform](https://quantum.ibm.com/).

### 2. Generar tu API Token
Una vez dentro de tu Dashboard:
1. Localiza la sección **API Key** en el panel izquierdo.
2. Haz clic en **"Create +"** para generar una nueva llave de acceso única.
3. Copia el token generado (guárdalo de forma segura y **nunca lo compartas**, tienes un límite de 10 minutos, y podrían gastártelos).

## 📦 Requisitos
Para replicar este experimento, es necesario instalar:
```bash
pip install qiskit qiskit-ibm-runtime matplotlib pylatexenc


Para replicar este experimento, es necesario instalar:
```bash
pip install qiskit qiskit-ibm-runtime matplotlib pylatexenc
