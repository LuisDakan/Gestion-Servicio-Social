# Manual Test Plan — Servicio Social

## 1. Login

| # | Action | Expected Result |
|---|--------|-----------------|
| 1.1 | Navigate to `http://localhost:3001` | Login page loads with split-screen layout (gradient panel + form) |
| 1.2 | Enter empty fields and click "Ingresar" | Browser's native validation prevents submission |
| 1.3 | Enter incorrect credentials (e.g. `admin` / `wrong`) | Red error message: "Credenciales inválidas" |
| 1.4 | Enter `admin` / `admin` and click "Ingresar" | Redirected to **Admin Dashboard** at `/admin/dashboard` |
| 1.5 | Click "Cerrar sesión" | Logged out, returned to login page |
| 1.6 | Login as alumno: `123456` / `123456` | Redirected to **Alumno Dashboard** at `/alumno/dashboard` |
| 1.7 | Login as empresa: `RFC123456` / `empresa123` | Redirected to **Empresa Dashboard** at `/empresa/dashboard` |

---

## 2. Admin — Dashboard

| # | Action | Expected Result |
|---|--------|-----------------|
| 2.1 | Navigate to `/admin/dashboard` | 4 metric cards visible: Carreras, Alumnos, Empresas, Solicitudes (with numbers) |
| 2.2 | Verify "Accesos directos" section | 3 quick-link buttons: Gestionar carreras, Gestionar alumnos, Gestionar empresas |

---

## 3. Admin — Carreras CRUD

| # | Action | Expected Result |
|---|--------|-----------------|
| 3.1 | Navigate to `/admin/carreras` | Table lists all carreras with ID, Clave, Nombre columns |
| 3.2 | Click "Nueva carrera" | Modal opens with empty Clave and Nombre fields |
| 3.3 | Enter values and click "Crear" | New row appears in table. Green flash message: "Carrera creada correctamente" |
| 3.4 | Click ✏️ icon on a row | Modal opens pre-filled with that carrera's data |
| 3.5 | Modify name and click "Guardar" | Row updates. Flash: "Carrera actualizada correctamente" |
| 3.6 | Click 🗑️ icon on a row | Confirmation modal appears: "¿Eliminar ...?" |
| 3.7 | Click "Eliminar" | Row disappears from table. Flash: "Carrera eliminada correctamente" |
| 3.8 | In the delete modal, click "Cancelar" | Modal closes, row not deleted |

---

## 4. Admin — Alumnos CRUD

| # | Action | Expected Result |
|---|--------|-----------------|
| 4.1 | Navigate to `/admin/alumnos` | Table lists all alumnos with No. Cuenta, Nombre, Carrera, Teléfono |
| 4.2 | Click "Nuevo alumno" | Modal opens with fields: No. Cuenta, Nombre, Carrera (dropdown), Teléfono, Email, Contraseña |
| 4.3 | Fill in all fields, select a carrera, and click "Crear" | New row appears. Flash: "Alumno creado correctamente" |
| 4.4 | Click ✏️ on a row | Modal opens pre-filled. Password field is hidden during edit |
| 4.5 | Modify name and click "Guardar" | Row updates. Flash: "Alumno actualizado correctamente" |
| 4.6 | Click 🗑️ on a row → confirm delete | Row removed. Flash: "Alumno eliminado correctamente" |

---

## 5. Admin — Empresas CRUD

| # | Action | Expected Result |
|---|--------|-----------------|
| 5.1 | Navigate to `/admin/empresas` | Table lists all empresas with RFC, Nombre, Dirección, Contacto |
| 5.2 | Click "Nueva empresa" | Modal opens with 2-column grid: RFC, Nombre, Dirección, Contacto nombre/tel/email, Contraseña |
| 5.3 | Fill fields and click "Crear" | New row appears. Flash: "Empresa creada correctamente" |
| 5.4 | Click ✏️ → modify → "Guardar" | Row updates. Flash: "Empresa actualizada correctamente" |
| 5.5 | Click 🗑️ → confirm | Row removed. Flash: "Empresa eliminada correctamente" |

---

## 6. Alumno — Dashboard

| # | Action | Expected Result |
|---|--------|-----------------|
| 6.1 | Login as `123456` / `123456` | Header shows "Mi Panel". 4 metric cards: Vacantes abiertas, Mis postulaciones, Aceptadas, Rechazadas |
| 6.2 | Scroll down | "Postulaciones pendientes" card and "Asignaciones confirmadas" card |

---

## 7. Alumno — Vacantes (Catálogo)

| # | Action | Expected Result |
|---|--------|-----------------|
| 7.1 | Navigate to Vacantes in sidebar | Card grid showing all open vacancies |
| 7.2 | Verify card content | Each card shows: title, status badge (green "abierta"), truncated description, company name, location |
| 7.3 | Click "Ver detalle" on a card | Navigated to `/alumno/vacantes/:id` with full detail view |
| 7.4 | Verify detail page | Shows: title, status badge, empresa, ubicación, duración, horario, descripción, requisitos, actividades |
| 7.5 | Click "Postularme" | Navigated to `/alumno/vacantes/:id/postular` |

---

## 8. Alumno — Postular

| # | Action | Expected Result |
|---|--------|-----------------|
| 8.1 | On postular page, click "Enviar postulación" without file | Red error: "Debes seleccionar un archivo PDF." |
| 8.2 | Click the dashed upload area | File picker opens (PDF files only) |
| 8.3 | Select a PDF file | File name appears below the upload area |
| 8.4 | Click "Enviar postulación" | Loading spinner, then success card appears with confirmation code |
| 8.5 | Verify success card | Shows: green checkmark, "¡Postulación exitosa!", bold confirmation code, link to dashboard |
| 8.6 | Click "Ir al dashboard" | Dashboard now shows the application in "Postulaciones pendientes" |
| 8.7 | Verify the pending card | Shows the vacancy title, status "pendiente", and the confirmation code |

---

## 9. Empresa — Dashboard

| # | Action | Expected Result |
|---|--------|-----------------|
| 9.1 | Login as `RFC123456` / `empresa123` | 5 metric cards: Vacantes, Abiertas, Postulantes, Aceptados, Rechazados |
| 9.2 | Scroll down | "Tus vacantes" card with list + "Ver todas" link |

---

## 10. Empresa — Vacantes + Postulantes

| # | Action | Expected Result |
|---|--------|-----------------|
| 10.1 | Navigate to Vacantes | List of vacante cards with title, description, status badge, "Postulantes (N)" button |
| 10.2 | Click "Nueva vacante" | Modal opens with fields: Título, Descripción, Ubicación, Duración, Horario, Status, Requisitos, Actividades |
| 10.3 | Fill fields, click "Crear" | New vacante appears in list. Flash: "Vacante creada correctamente" |
| 10.4 | Click **Postulantes (N)** | Modal opens showing alumno name, carrera, date, carta link, status, and action buttons |
| 10.5 | Verify postulante card shows correct status | Status badge: "pendiente" (amber), "aceptada" (green), "rechazada" (red) |
| 10.6 | Click "Aceptar" on a pending postulante | Status changes to "aceptada" immediately. Flash: "Postulante aceptado" |
| 10.7 | Click "Rechazar" on a pending postulante | Status changes to "rechazada". Flash: "Postulante rechazado" |
| 10.8 | Accept a postulante | The system schedules a confirmation code assignment (APScheduler) |

---

## 11. Empresa — Vacante CRUD

| # | Action | Expected Result |
|---|--------|-----------------|
| 11.1 | Click ✏️ on a vacante | Modal opens pre-filled with all fields |
| 11.2 | Change status to "Cerrada" and save | Vacante card shows red "cerrada" badge |
| 11.3 | Click 🗑️ → confirm | Vacante removed. Flash: "Vacante eliminada correctamente" |

---

## 12. Full End-to-End Flow

| # | Action | Expected Result |
|---|--------|-----------------|
| 12.1 | **Admin** creates a carrera, a student, and an empresa | All appear in respective tables |
| 12.2 | **Empresa** creates a vacante (status: abierta) | Vacante visible in alumno catalogue |
| 12.3 | **Alumno** views vacante detail and posts with a PDF | Postulation succeeds with confirmation code |
| 12.4 | **Empresa** opens Postulantes modal and sees the application | Alumno info + carta link visible. Status: "pendiente" |
| 12.5 | **Empresa** clicks "Aceptar" | Postulante status → "aceptada" |
| 12.6 | (Wait for APScheduler) | The accepted postulante gets a confirmation code assigned automatically |
| 12.7 | **Alumno** checks dashboard | The postulation appears in "Asignaciones confirmadas" with the confirmation code |

---

## 13. Edge Cases

| # | Action | Expected Result |
|---|--------|-----------------|
| 13.1 | Navigate to `/admin/dashboard` while logged in as alumno | Redirected to `/login` (role guard) |
| 13.2 | Navigate to `/alumno/vacantes` while logged in as empresa | Redirected to `/login` (role guard) |
| 13.3 | Navigate to `/empresa/dashboard` while logged in as admin | Redirected to `/login` (role guard) |
| 13.4 | Navigate to `/nonexistent` | Redirected to `/login` |
| 13.5 | Login, then clear localStorage token manually | Next navigation redirects to login |
| 13.6 | Login as admin, then type `/alumno/dashboard` in URL | Redirected to login (role mismatch) |
