from app.database.config.config import driver

def interact_with_vacancy(correo_candidato: str, titulo_vacante: str, accion: str):
    print(f"🔍 Interacción recibida: correo={correo_candidato}, titulo={titulo_vacante}, accion={accion}")
    with driver.session() as session:
        if accion == "like":
            session.run("""
                MATCH (c:Candidate {correo: $correo}), (v:Vacancy {title: $titulo})
                MERGE (c)-[r:LIKES]->(v)
            """, correo=correo_candidato, titulo=titulo_vacante)

        elif accion == "save":
            session.run("""
                MATCH (c:Candidate {correo: $correo}), (v:Vacancy {title: $titulo})
                MERGE (c)-[r:SAVES]->(v)
            """, correo=correo_candidato, titulo=titulo_vacante)

        elif accion == "share":
            session.run("""
                MATCH (c:Candidate {correo: $correo}), (v:Vacancy {title: $titulo})
                MERGE (c)-[r:SHARES]->(v)
            """, correo=correo_candidato, titulo=titulo_vacante)
        
        if accion in ["like", "save"]:
            rel = "LIKES" if accion == "like" else "SAVES"
            existing = session.run(f"""
                MATCH (c:Candidate {{correo: $correo}})-[r:{rel}]->(v:Vacancy {{title: $titulo}})
                RETURN r
            """, correo=correo_candidato, titulo=titulo_vacante)

            if existing.single():
                session.run(f"""
                    MATCH (c:Candidate {{correo: $correo}})-[r:{rel}]->(v:Vacancy {{title: $titulo}})
                    DELETE r
                """, correo=correo_candidato, titulo=titulo_vacante)
            else:
                session.run(f"""
                    MATCH (c:Candidate {{correo: $correo}}), (v:Vacancy {{title: $titulo}})
                    MERGE (c)-[:{rel}]->(v)
                """, correo=correo_candidato, titulo=titulo_vacante)
    