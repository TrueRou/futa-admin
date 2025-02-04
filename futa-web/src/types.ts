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

interface Report {
    id: number;
    label: string;
    type: ReportType;
    linked_table: string | null;
    appendable: boolean;
}

interface ReportField {
    id: number;
    order: number;
    label: string;
    type: ReportFieldType;
    linked_field: string | null;
}

interface ReportFragment {
    id: number;
    trait: string;
    label: string;
    type: ReportFragmentType;
    extends: string;
    sql: string;
}

interface ReportMixin {
    id: number;
    ref_variable: string;
    values: string;
}

interface ReportFull extends Report {
    fields: ReportField[];
    fragments: ReportFragment[];
    mixins: ReportMixin[];
    data: (string | number)[][];
}

interface ReportAdmin extends Report {
    sql: string;
}

interface Page {
    path: string;
    name: string;
    description: string;
    reports: Report[];
}

const ReportTypeMap = {
    1: "自定义选择器",
    2: "时段选择器",
    3: "单日选择器",
    4: "月份选择器",
}

export { ReportType, ReportFieldType, ReportFragmentType, ReportTypeMap, type Report as ReportSimple, type ReportField, type ReportFragment, type ReportFull, type ReportAdmin, type Page, type ReportMixin };