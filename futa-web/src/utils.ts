const deepMergeDict = (source: Record<string, any>, mixins: Record<string, any>) => {
    for (const key in mixins) {
        if (mixins.hasOwnProperty(key)) {
            if (typeof mixins[key] === 'object' && !Array.isArray(mixins[key])) {
                source[key] = deepMergeDict(source[key] || {}, mixins[key]);
            } else if (Array.isArray(mixins[key]) && Array.isArray(source[key])) {
                source[key] = source[key].concat(mixins[key]);
            } else {
                source[key] = mixins[key];
            }
        }
    }
    return source;
}

export { deepMergeDict };