// Crear parámetro CarpetaDemo (texto) apuntando a datos_evolucion. Ejecución M pendiente.
let
    Leer = (nombre as text) as table => Table.PromoteHeaders(Csv.Document(File.Contents(CarpetaDemo & "/" & nombre & ".csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]), [PromoteAllScalars=true]),
    Matricula = Table.TransformColumnTypes(Leer("matricula"), {{"desde", type date}, {"hasta", type date}}),
    Calendario = Table.TransformColumnTypes(Leer("calendario"), {{"fecha", type date}, {"abierto_demo", type logical}}),
    Abiertos = Table.SelectRows(Calendario, each [abierto_demo] = true),
    ExpandirDias = Table.AddColumn(Matricula, "Dias", each Abiertos),
    Jornadas = Table.ExpandTableColumn(ExpandirDias, "Dias", {"fecha"}),
    Vigentes = Table.SelectRows(Jornadas, each [desde] <= [fecha] and [fecha] <= [hasta]),
    Observaciones = Table.TransformColumnTypes(Leer("asistencia"), {{"fecha", type date}}),
    Unico = if Table.RowCount(Table.Distinct(Observaciones, {"participante_id", "fecha"})) = Table.RowCount(Observaciones) then Observaciones else error "Asistencia duplicada",
    Huerfanos = Table.NestedJoin(Unico, {"participante_id", "fecha"}, Vigentes, {"participante_id", "fecha"}, "Esperada", JoinKind.LeftAnti),
    Validado = if Table.RowCount(Huerfanos) = 0 then Unico else error "Registro fuera del universo",
    Join = Table.NestedJoin(Vigentes, {"participante_id", "fecha"}, Validado, {"participante_id", "fecha"}, "Observado", JoinKind.LeftOuter),
    Estado = Table.ExpandTableColumn(Join, "Observado", {"estado"}),
    Completo = Table.ReplaceValue(Estado, null, "Sin registro", Replacer.ReplaceValue, {"estado"}),
    Resultado = Table.SelectColumns(Completo, {"participante_id", "programa_id", "fecha", "estado"})
in
    Resultado
