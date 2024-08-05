enum ReportType {
    FORM = 1,
    EXCEL_TABLE = 2,
    LINE_CHART = 3,
    BAR_CHART = 4
}

enum ReportFieldType {
    TEXT = 1,
    NUMBER = 2
}

interface ReportSimple {
    id: number;
    name: string;
    type: ReportType;
}

interface ReportField {
    name: string;
    type: ReportFieldType;
    field_name: string | null;
}

interface ReportFull extends ReportSimple {
    fields: ReportField[];
    data: (string | number)[][];
}

interface Page {
    path: string;
    title: string;
    description: string;
    reports: ReportSimple[];
}

export { ReportType, ReportFieldType, type ReportSimple, type ReportField, type ReportFull, type Page };