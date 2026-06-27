# InventaPro - Sistema de Gestión de Inventario

Aplicación web de gestión de inventario desarrollada con Flask y SQLAlchemy.

##  Inicio rápido (local)

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecutar la aplicación
```bash
python run.py
```

Abre el navegador en: http://127.0.0.1:5000

### Crear datos de prueba
```bash
python seed.py
```

Usuarios de prueba:
- admin / admin123
- almacenero / almacen123
- vendedor / vendedor123

## 📦 Despliegue en Render

Este proyecto está listo para desplegar en Render.

Incluye:
- `Procfile` - configuración para ejecutar con Gunicorn
- `runtime.txt` - especifica Python 3.11
- `requirements.txt` - todas las dependencias

Para instrucciones completas de despliegue, ve a la carpeta `DOCUMENTACION_INVENTAPRO` en la raíz del proyecto.

## 📁 Estructura del proyecto

```
InventaPro/
├── apps/                 # Lógica de la aplicación
│   ├── auth/            # Autenticación
│   ├── core/            # Dashboard principal
│   ├── Productos/       # Gestión de productos
│   ├── Categorias/      # Gestión de categorías
│   ├── Proveedores/     # Gestión de proveedores
│   ├── Compras/         # Registro de compras
│   ├── Ventas/          # Registro de ventas
│   └── app.py           # Configuración de Flask
├── migrations/          # Migraciones de base de datos
├── run.py              # Archivo principal para ejecutar
├── seed.py             # Datos de prueba
├── requirements.txt    # Dependencias
├── Procfile            # Para Render
├── runtime.txt         # Versión de Python
└── .env.example        # Plantilla de variables

```

## 🔧 Tecnologías

- Flask 3.1.3
- SQLAlchemy 2.0.50
- Flask-Login
- Flask-Bcrypt
- PostgreSQL / SQLite
- Gunicorn
- Flask-Migrate

## 📝 Funcionalidades

- ✅ Autenticación de usuarios
- ✅ Gestión de productos y stock
- ✅ Gestión de categorías
- ✅ Gestión de proveedores
- ✅ Registro de compras y ventas
- ✅ Control automático de stock
- ✅ Bitácora de actividades
- ✅ Dashboard con métricas

## ⚙️ Variables de entorno

- `SECRET_KEY` - Clave secreta de Flask (auto-generada si no se proporciona)
- `DATABASE_URL` - URL de la base de datos (SQLite por defecto)

Ver [.env.example](.env.example) para una plantilla.

## 🛠️ Desarrollo

### Crear un nuevo usuario
```bash
python seed.py  # Ejecutar script de inicialización
```

### Ver logs de base de datos
En desarrollo, SQLite guarda datos en `inventapro.db`.
En producción (Render), usa PostgreSQL.

### Limpiar la base de datos
```bash
rm inventapro.db   # Eliminar archivo de SQLite
python seed.py     # Reinicializar
```

## 📞 Documentación

Para documentación completa, ve a la carpeta:
```
../DOCUMENTACION_INVENTAPRO/
```

Allí encontrarás:
- Análisis completo del proyecto
- Guía de despliegue en Render
- Comandos rápidos
- Checklist de verificación

## 📜 Licencia

Este proyecto es open source para propósitos educativos.
