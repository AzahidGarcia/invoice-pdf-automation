# Ejemplo de uso

Este directorio contiene datos de ejemplo para probar el proyecto.

## El archivo `sample_input.csv`

Contiene 20 facturas ficticias de **Papelería La Esquina**, un negocio mexicano genérico.
Los datos son 100% ficticios y solo para demostración.

### Formato del CSV

```
invoice_id,client_name,client_rfc,issue_date,due_date,items,category
```

- `invoice_id`: Identificador único de factura
- `client_name`: Nombre del cliente
- `client_rfc`: RFC del cliente (formato genérico XAXX010101000)
- `issue_date`: Fecha de emisión (AAAA-MM-DD)
- `due_date`: Fecha de vencimiento (AAAA-MM-DD, opcional)
- `items`: Items separados por `;;`, cada item con formato `descripcion|cantidad|precio`
- `category`: Categoría del producto

## Cómo usarlo

```bash
# Desde la raíz del proyecto
pip install -e .

python -m invoice_automation generate \
    --input examples/sample_input.csv \
    --output ./outputs
```

Esto generará:
- `outputs/pdfs/FAC-001.pdf` hasta `FAC-020.pdf`
- `outputs/resumen.xlsx`

## Datos ficticios

- **Negocio**: Papelería La Esquina
- **RFC**: XAXX010101000
- **Dirección**: Av. Principal #123, Col. Centro, Ciudad de México
- **Clientes**: Nombres genéricos (Cliente 001, Distribuidora ABC, etc.)
- **RFCs**: Formato genérico XAXX010101000 (no reales)
