// Crear parámetro CarpetaDemo (texto) apuntando a datos_evolucion. Ejecución M pendiente.
let
    Leer = (nombre as text) as table => Table.PromoteHeaders(Csv.Document(File.Contents(CarpetaDemo & "/" & nombre & ".csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]), [PromoteAllScalars=true]),
    Inscripciones = Table.TransformColumnTypes(Leer("inscripciones"), {{"inscripcion_id", type text}, {"persona_id", type text}, {"curso_id", type text}, {"fecha_inscripcion", type date}}),
    Estados = Table.TransformColumnTypes(Leer("seguimiento"), {{"inscripcion_id", type text}, {"corte", type date}, {"estado", type text}}),
    Cursos = Table.TransformColumnTypes(Leer("cursos"), {{"curso_id", type text}, {"fin", type date}}),
    JoinIns = Table.NestedJoin(Estados, {"inscripcion_id"}, Inscripciones, {"inscripcion_id"}, "Ins", JoinKind.LeftOuter),
    Cardinalidad = if List.AllTrue(List.Transform(JoinIns[Ins], each Table.RowCount(_) = 1)) then JoinIns else error "FK o duplicación de inscripción",
    Expandir = Table.ExpandTableColumn(Cardinalidad, "Ins", {"persona_id", "curso_id", "fecha_inscripcion"}),
    JoinCurso = Table.NestedJoin(Expandir, {"curso_id"}, Cursos, {"curso_id"}, "Curso", JoinKind.LeftOuter),
    CardinalidadCurso = if List.AllTrue(List.Transform(JoinCurso[Curso], each Table.RowCount(_) = 1)) then JoinCurso else error "FK curso",
    FinCurso = Table.ExpandTableColumn(CardinalidadCurso, "Curso", {"fin"}, {"fin_curso"}),
    Temporal = if Table.RowCount(Table.SelectRows(FinCurso, each [corte] < [fecha_inscripcion] or [fecha_inscripcion] > [fin_curso])) = 0 then FinCurso else error "Fuga temporal",
    Unico = if Table.RowCount(Table.Distinct(Temporal, {"inscripcion_id", "corte"})) = Table.RowCount(Temporal) then Temporal else error "Snapshot duplicado",
    Cerrado = Table.AddColumn(Unico, "curso_cerrado_al_corte", each [fin_curso] <= [corte], type logical)
in
    Cerrado
