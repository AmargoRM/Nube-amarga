import os
import psycopg2

conn = psycopg2.connect(os.environ["NEON_URL"])
cur = conn.cursor()
cur.execute('''
SELECT jsonb_build_object(
  'type', 'FeatureCollection',
  'features', COALESCE(jsonb_agg(
    jsonb_build_object(
      'type', 'Feature',
      'geometry', ST_AsGeoJSON(ST_Transform(geom, 4326))::jsonb,
      'properties', to_jsonb(t) - 'geom'
    )
  ), '[]'::jsonb)
)::text
FROM "Control_DA_LERM" t;
''')
geojson = cur.fetchone()[0]
os.makedirs("docs", exist_ok=True)
with open("docs/casos.geojson", "w", encoding="utf-8") as f:
    f.write(geojson)
cur.close()
conn.close()
print("GeoJSON actualizado")
