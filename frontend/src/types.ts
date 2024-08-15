enum ReportType {
    FORM = 1,
    EXCEL_TABLE = 2,
    LINE_CHART = 11,
    BAR_CHART = 12
}

enum ReportFragmentType {
    FILTER_SELECT = 1,
    FILTER_DATEPICKER = 2
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
    field_pos: number
}

interface ReportFragment {
    trait: string;
    name: string;
    type: ReportFragmentType;
    values: string[] | null;
}

interface ReportMixin {
    ref_variable: string;
    values: Record<string, any>;
}

interface ReportFull extends ReportSimple {
    fields: ReportField[];
    fragments: ReportFragment[];
    mixins: ReportMixin[];
    data: (string | number)[][];
}

interface Page {
    path: string;
    name: string;
    description: string;
    reports: ReportSimple[];
}

export { ReportType, ReportFieldType, ReportFragmentType, type ReportSimple, type ReportField, type ReportFragment, type ReportFull, type Page };