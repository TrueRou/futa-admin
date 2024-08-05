enum ReportType {
    Type1 = 1,
    Type2 = 2,
    Type3 = 3,
}

interface ReportSimple {
    id: number;
    name: string;
    type: ReportType;
}

interface ReportFull extends ReportSimple {
    fields: { name: string; type: ReportType; }[];
    data: string[][];
}

interface Page {
    path: string;
    title: string;
    description: string;
    reports: ReportSimple[];
}