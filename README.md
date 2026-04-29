# invoice-automation

> Genera facturas PDF profesionales y resúmenes Excel desde un CSV en segundos. Para PyMEs mexicanas que quieren automate su facturación sin pagar software costoso.

## Demo

![Demo](docs/demo.gif)

## What problem this solves

PyME owners — papelerías, despachos, e-commerce pequeño — tienen un CSV mensual de ventas pero pierden horas:
- Creando facturas una por una en Word/Excel
- Copiando datos entre sistemas
- Calculando totales a mano

**invoice-pdf-automation** lee tu CSV y genera PDFs listos para enviar + un Excel con resumen de ventas en menos de un segundo.

## Features

- ✅ Generación batch de PDFs profesionales desde CSV
- ✅ Resumen Excel con totales por cliente, mes y categoría
- ✅ CLI intuitiva con modo verbose
- ✅ Validación de datos con errores claros
- ✅ Diseño profesional: header con branding, tabla de items, IVA 16%, totales
- ✅ Sin dependencias externas — todo local

## Tech stack

- **Language:** Python 3.11+
- **Libraries:** pandas (CSV), reportlab (PDF), openpyxl (Excel), pydantic (validación), click (CLI)
- **Tests:** pytest, mypy, ruff

## Quick start

```bash
git clone https://github.com/[your-username]/invoice-pdf-automation
cd invoice-pdf-automation
pip install -e .

# Generar todas las facturas + summary
python -m invoice_automation generate \
    --input examples/sample_input.csv \
    --output ./outputs

# Solo el resumen Excel
python -m invoice_automation summary \
    --input examples/sample_input.csv \
    --output ./outputs/resumen.xlsx

# Con logs detallados
python -m invoice_automation generate --input examples/sample_input.csv --output ./outputs --verbose
```

## Sample output

### PDF por factura
Cada PDF incluye:
- Header con nombre del negocio y logo placeholder
- Datos del cliente y fecha
- Tabla de items (descripción, cantidad, precio unitario, subtotal)
- Subtotal, IVA 16%, Total
- Footer con información del negocio

```
[DEMO_PDF_PLACEHOLDER — screenshot de ejemplo]
Caption: Demo PDF — Factura de Papelería La Esquina
```

### Excel resumen
Cuatro hojas:
1. **Resumen general** — totales globales del periodo
2. **Por cliente** — tabla pivote de ventas por cliente
3. **Por mes** — totales mensuales
4. **Por categoría** — desglose por categoría de producto

```
[DEMO_EXCEL_PLACEHOLDER — screenshot de ejemplo]
Caption: Demo Excel — Resumen de ventas abril 2026
```

## Configuration

No requiere variables de entorno para funcionar. Los valores por defecto están en `src/invoice_automation/config.py`.

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `BUSINESS_NAME` | "Papelería La Esquina" | Nombre del negocio |
| `IVA_RATE` | 0.16 | Tasa de IVA |
| `DEFAULT_CURRENCY` | "MXN" | Moneda |

Para personalizar colores y branding, edita `src/invoice_automation/config.py`.

## How it works

```
CSV (datos de facturas)
    │
    ▼
┌─────────────┐
│  reader.py  │  ← Valida y parsea CSV con pandas
└─────────────┘
    │
    ▼
┌─────────────┐
│ models.py   │  ← Pydantic valida tipos y campos
└─────────────┘
    │
    ├──────────────────────┐
    ▼                      ▼
┌─────────────┐    ┌─────────────┐
│pdf_generator│    │excel_summary│
│ (ReportLab) │    │  (OpenPyXL) │
└─────────────┘    └─────────────┘
    │                      │
    ▼                      ▼
 PDFs individuales    summary.xlsx
```

## Use cases

1. **Papelería de barrio** — Tiene 200+ ventas mensuales en CSV. Genera facturas PDF para clientes que lo piden y lleva su contabilidad en Excel sin Excel.

2. **Despacho contable pequeño** — Recibe un CSV de ventas de 5 clientes PyME. En 5 minutos tiene 5 resúmenes Excel listos para entregar en lugar de 2 horas de trabajo manual.

3. **E-commerce pequeño** — Exporta órdenes de su plataforma a CSV. Genera facturas PDF automáticas para cada pedido y un resumen mensual para sus reportes.

## Roadmap

- [x] Generación batch de PDFs desde CSV
- [x] Resumen Excel con múltiples vistas
- [x] CLI con comandos generate y summary
- [ ] Soporte para facturas con múltiples páginas
- [ ] Template de email para enviar PDFs directamente
- [ ] Integración con APIs de PAC para timbrado fiscal
- [ ] GUI simple para usuarios no técnicos

## License

MIT — see [LICENSE](LICENSE)

---

*Part of [Strivark](https://strivark.com)'s portfolio of automation tools.*
