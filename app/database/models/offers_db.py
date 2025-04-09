# db/models/offers_db.py

from app.database.config.config import driver

def crear_oferta(
    titulo,
    empresa,
    ciudad,
    nivel_educativo,
    nivel_experiencia,
    habilidades
):
    query = """
    MERGE (v:Vacancy {title: $titulo})
    MERGE (c:Company {name: $empresa})
    MERGE (ci:City {name: $ciudad})
    MERGE (e:EducationLevel {level: $nivel_educativo})
    MERGE (x:ExperienceLevel {level: $nivel_experiencia})
    MERGE (v)-[:PUBLISHED_BY]->(c)
    MERGE (v)-[:LOCATED_IN]->(ci)
    MERGE (v)-[:REQUIRES_EDUCATION]->(e)
    MERGE (v)-[:REQUIRES_EXPERIENCE]->(x)
    WITH v
    UNWIND $habilidades AS kw
    MERGE (k:Skill {name: kw})
    MERGE (v)-[:REQUIRES_SKILL]->(k)
    RETURN v.title AS created
    """

    with driver.session() as session:
        result = session.run(query, {
            "titulo": titulo,
            "empresa": empresa,
            "ciudad": ciudad,
            "nivel_educativo": nivel_educativo,
            "nivel_experiencia": nivel_experiencia,
            "habilidades": habilidades
        })
        for record in result:
            print(f"✅ Oferta creada exitosamente: {record['created']}")
            

def get_all_vacancies():
    query = """
    MATCH (v:Vacancy)
    OPTIONAL MATCH (v)-[:PUBLISHED_BY]->(c:Company)
    OPTIONAL MATCH (v)-[:LOCATED_IN]->(ci:City)
    OPTIONAL MATCH (v)-[:REQUIRES_EDUCATION]->(e:EducationLevel)
    OPTIONAL MATCH (v)-[:REQUIRES_EXPERIENCE]->(x:ExperienceLevel)
    OPTIONAL MATCH (v)-[:REQUIRES_SKILL]->(s:Skill)
    RETURN 
        v.title AS titulo,
        c.name AS empresa,
        ci.name AS ciudad,
        e.level AS nivel_educativo,
        x.level AS nivel_experiencia,
        collect(s.name) AS habilidades
    """

    with driver.session() as session:
        result = session.run(query)
        ofertas = []
        for record in result:
            oferta = {
                "titulo": record["titulo"],
                "empresa": record["empresa"],
                "ciudad": record["ciudad"],
                "nivel_educativo": record["nivel_educativo"],
                "nivel_experiencia": record["nivel_experiencia"],
                "habilidades": record["habilidades"]
            }
            ofertas.append(oferta)
        
        print("Ofertas encontradas:")
        for o in ofertas:
            for key, value in o.items():
                print(f"{key}: {value}")
        
        return ofertas

    
# Ejemplo de prueba
if __name__ == "__main__":
    get_all_vacancies()
