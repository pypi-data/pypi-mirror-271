Nombre del Proyecto: RobinApi Framework

Descripción:
RobinApi Framework es una solución integral diseñada para facilitar la interacción eficiente con APIs de modelos de lenguaje de aprendizaje automático (LLM) y la gestión avanzada de datos vectoriales. Este framework proporciona herramientas robustas para la carga y almacenamiento de archivos en una base de datos vectorial optimizada, permitiendo a los usuarios aprovechar completamente la búsqueda y recuperación de datos basados en contenido. Además, RobinApi Framework incluye endpoints dedicados para realizar consultas complejas, permitiendo a los usuarios extraer información valiosa y realizar análisis profundos sobre los datos almacenados. Ideal para desarrolladores que buscan integrar capacidades de LLM en sus aplicaciones y gestionar grandes volúmenes de datos de manera eficiente, RobinApi Framework se destaca por su flexibilidad, escalabilidad y facilidad de uso.

Características principales:

Consumo de API de LLM: Interfaces optimizadas para la interacción con modelos de lenguaje, facilitando la integración y el manejo de respuestas en tiempo real.
Gestión de archivos en base de datos vectorial: Carga, almacenamiento y gestión eficiente de archivos con búsqueda vectorial, ideal para aplicaciones que requieren acceso rápido y preciso a grandes volúmenes de datos.
Endpoints para consultas: Funcionalidades específicas para formular preguntas y obtener respuestas basadas en los datos almacenados, soportando una amplia variedad de consultas analíticas y de búsqueda.
Alta configurabilidad y seguridad: Configuración detallada de parámetros y protocolos de seguridad avanzados para proteger la información y garantizar el rendimiento.

Project Name: RobinApi Framework

Description:
RobinApi Framework is a comprehensive solution designed to facilitate efficient interactions with machine learning language model (LLM) APIs and advanced vector data management. This framework provides robust tools for uploading and storing files in an optimized vector database, enabling users to fully leverage content-based data search and retrieval. Additionally, RobinApi Framework includes dedicated endpoints for conducting complex queries, allowing users to extract valuable information and perform in-depth analyses on stored data. Ideal for developers looking to integrate LLM capabilities into their applications and manage large volumes of data efficiently, RobinApi Framework stands out for its flexibility, scalability, and ease of use.

Key Features:

LLM API Consumption: Optimized interfaces for interacting with language models, facilitating integration and real-time response handling.
File Management in Vector Database: Efficient upload, storage, and management of files with vector search, ideal for applications requiring fast and accurate access to large data volumes.
Endpoints for Queries: Specific functionalities to ask questions and receive answers based on stored data, supporting a wide variety of analytical and search queries.
High Configurability and Security: Detailed parameter settings and advanced security protocols to protect information and ensure performance.
Ideal for:
Software developers, data scientists, and system engineers interested in integrating LLM technology and advanced vector data management into their projects.


from robin_api import RobinAIClient


client = RobinAIClient(api_key="API_KEY")

value =  [
            {
                "role": "system",
                "content": "system_prompt"
            },
            {
                "role": "user",
                "content": "hola como estas, dame un poema de 100 palabras"
            }

]

stream = client.completions.create(model="ROBIN_4", 
                            conversation = value, 
                            max_tokens = 512, stream = True, 
                            save_response = False,
                            temperature=1)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

exit()
