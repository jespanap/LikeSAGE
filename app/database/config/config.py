from neo4j import GraphDatabase

NEO4J_URI = "neo4j+s://448f9976.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "eYJbIiHYicqS4u3N7fT4rXUzucUx9S1A-iRRQkQ01yc"

driver = None

try:
    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )
    with driver.session() as session:
        result = session.run("RETURN 1 AS test")
        if result.single()["test"] == 1:
            print("✅ Conexión exitosa con la base de datos Neo4j.")
        else:
            print("⚠ Conexión establecida, pero la prueba falló.")
except Exception as e:
    print(f"❌ Error al conectar a Neo4j: {e}")