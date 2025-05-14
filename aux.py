import open3d as o3d

def export_ply_grayscale(archivo_ply, depth_map, img_gray, f, cx, cy):
    """
    Exporta el mapa de profundidad y la imagen en escala de grises a un archivo .PLY.

    Parámetros:
        archivo_ply (str): Ruta del archivo de salida .PLY.
        depth_map (numpy.ndarray): Mapa de profundidad.
        img_gray (numpy.ndarray): Imagen en escala de grises (2D).
        f (float): Distancia focal de la cámara (en píxeles).
        cx, cy (float): Coordenadas del centro óptico (en píxeles).
    """
    h, w = depth_map.shape
    with open(archivo_ply, 'w') as f_out:
        # Cabecera del archivo .PLY
        f_out.write('ply\n')
        f_out.write('format ascii 1.0\n')
        f_out.write(f'element vertex {h * w}\n')
        f_out.write('property float x\n')
        f_out.write('property float y\n')
        f_out.write('property float z\n')
        f_out.write('property uchar red\n')
        f_out.write('property uchar green\n')
        f_out.write('property uchar blue\n')
        f_out.write('end_header\n')

        for y in range(h):
            for x in range(w):
                Z = depth_map[y, x]
                if Z == 0:  # omitir píxeles con profundidad 0
                    continue

                # convertir coordenadas de píxel a coordenadas 3D
                X = (x - cx) * Z / f
                Y = (y - cy) * Z / f

                # Intensidad de gris
                intensity = img_gray[y, x]
                r = g = b = int(intensity)

                f_out.write(f'{X} {Y} {Z} {r} {g} {b}\n')

    print(f'Archivo .PLY guardado como {archivo_ply}')

def draw_geometries(geometries, note=False, **kwargs):
 
    if note:
        draw_function = o3d.visualization.draw_plotly
    else:
        draw_function = o3d.visualization.draw_geometries

    draw_function(geometries, **kwargs)