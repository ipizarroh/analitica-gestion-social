// Crear parámetro de texto RutaCSV. Datos inventados, sin fuentes institucionales.
let
    Origen = Csv.Document(File.Contents(RutaCSV), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Cabeceras = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Cabeceras, {{"inscripcion_id", type text}, {"persona_id", type text}, {"curso", type text}, {"estado", type text}, {"registro_crm", Int64.Type}})
in
    Tipos
