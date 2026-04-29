# Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        invoice_automation                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  cli.py                                                          │
│    └──> read_invoices_from_csv() ──────────────────────────────┐ │
│                                                               │ │
│  reader.py ──────────────────────────────────────────────────>│ │
│    └──> Invoice (Pydantic model)                               │ │
│                                                               │ │
│         ┌──────────────────────┬───────────────────────────────┤
│         │                      │                                │
│         ▼                      ▼                                │
│  ┌─────────────┐    ┌─────────────────┐                        │
│  │pdf_generator│    │ excel_summary   │                        │
│  │ (ReportLab) │    │   (OpenPyXL)    │                        │
│  └─────────────┘    └─────────────────┘                        │
│         │                      │                                │
│         ▼                      ▼                                │
│    PDFs individuales     summary.xlsx                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Flujo de datos

1. **Input**: CSV con datos de facturas
2. **reader.py**: Lee y valida el CSV usando pandas, retorna lista de `Invoice` (Pydantic)
3. **models.py**: Define la estructura de datos con validación de tipos
4. **pdf_generator.py**: Genera PDFs profesionales usando ReportLab
5. **excel_summary.py**: Genera workbook Excel con 4 hojas usando OpenPyXL

## Dependencias

| Módulo | Dependencia | Uso |
|--------|-------------|-----|
| reader.py | pandas | Lectura de CSV |
| pdf_generator.py | reportlab | Generación de PDFs |
| excel_summary.py | openpyxl | Generación de Excel |
| models.py | pydantic | Validación de datos |
| cli.py | click | Interface CLI |
