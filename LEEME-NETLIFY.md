# Juega y Aprende · listo para Netlify

```
index.html                         el juego (página principal)
Juega_y_Aprende_admin.html         el administrador
netlify.toml                       configuración de Netlify
package.json                       dependencia de la función (@netlify/blobs)
netlify/functions/ranking.mjs      ranking global (reemplaza al servidor Java)
```

El ranking usa **Netlify Blobs**: no necesitas JSONBin, claves ni servidor Java.
La dirección `/api/ranking` funciona sola, igual que antes.

## Opción A (recomendada): desde GitHub

1. Sube esta carpeta a un repositorio de GitHub.
2. En Netlify: **Add new site → Import an existing project** y elige el repositorio.
3. Deja el comando de build vacío y el directorio de publicación en `.` (ya lo dice `netlify.toml`).
4. **Deploy**. Netlify instala `@netlify/blobs` y publica la función solo.

## Opción B: con la terminal (Netlify CLI)

```
npm install -g netlify-cli
cd esta-carpeta
npm install
netlify deploy --prod
```

## Opción C: arrastrar la carpeta a Netlify Drop

Publica el juego y el administrador, pero la función del ranking puede no
desplegarse con este método. Si el ranking no carga, usa la opción A o B.

## Notas

- Los cambios del administrador se guardan solo en el navegador donde se editan.
- Entrar al administrador: `/Juega_y_Aprende_admin.html` o escribir `Mielametio` como usuario en el juego.
- Reglas del ranking (iguales a las del servidor Java): un puntaje por jugador, materia y modo (el mejor), 50 mejores visibles, nombre de hasta 24 caracteres, puntaje de 1 a 1.000.000.
- Los archivos Java, `Dockerfile` e `iniciar.*` ya no hacen falta en Netlify.
