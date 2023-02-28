APIs usando el REST Framework y usamos features avanzados del Django
Admin.

Teniendo en cuenta lo anterior la prueba consiste en implementar modelos para manejar notas
de estudiantes, exámenes con sus preguntas y respuestas, y modificaciones en el django
Admin para mostrar las respuestas escogidas por un estudiante.
Se deben exponer endpoints para registrar la respuesta de un estudiante a preguntas de un
examen.


Requerimientos de Aplicación Django
1. Crear modelos de Student, Test, Question, Answer ok
2. Endpoint para identificar a un estudiante y devolver su respectivo JWT
3. Endpoint protegido para registrar las respuestas de un estudiante
4. Modificaciones al Django Admin para que un estudiante pueda ingresar al portal y solo
ver sus propias respuestas a los tests