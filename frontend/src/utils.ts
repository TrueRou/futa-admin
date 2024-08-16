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

const removeCommonPrefix = (arr: any[]) => {
    const commonPrefix = arr.reduce((prefix, str) => {
        let i = 0;
        while (i < prefix.length && i < str.length && prefix[i] === str[i]) {
            i++;
        }
        return prefix.slice(0, i);
    }, arr[0]);

    console.log('commonPrefix', commonPrefix);

    return arr.map(str => str.replace(commonPrefix, ''));
}

export { deepMergeDict, removeCommonPrefix };