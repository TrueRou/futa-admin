enum ReportType {
    FORM = 1,
    EXCEL_TABLE = 2,
    LINE_CHART = 11,
    BAR_CHART = 12
}

enum ReportFragmentType {
    FILTER_SELECT = 1,
    FILTER_DATERANGE = 2,
    FILTER_DATEDAY = 3,
    FILTER_DATEMONTH = 4,
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
    field_pos: number;
    is_fixed: boolean;
    width: number | null;
}

interface ReportFragment {
    trait: string;
    name: string;
    type: ReportFragmentType;
    labels: string[];
    values: string[];
}

interface ReportMixin {
    ref_variable: string;
    values: Record<string, any>;
}

interface ReportFull extends ReportSimple {
    is_editable: boolean;
    updateable_fields_only: boolean;
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