/**
  * @param {Object} value
  * @return {boolean} a boolean represents if the object is set to null or undefined
 */
export const isNullOrUndefined = (value) => {
    return (value === null || value === undefined);
};

/**
  * @param {string} value
  * @return {boolean} a boolean represents if an object value is set to 
  * null or undefined or empty string
 */
export const isStringEmpty = (value) => {
    return (value === null || value === undefined || value === '');
};


/**
  * @param {Array} value
  * @return {boolean} a boolean represents if the array is set to null, undefined or is empty
 */
export const isArrayEmpty = (value) => {
    return (isNullOrUndefined(value) || value.length === 0);
};


/**
  * @param {string} s1
  * @param {string} s2
  * @return {boolean} a boolean represents if two strings are equal
 */
export const areStringsEqualIgnoreCase = (s1, s2) => {
    if (isNullOrUndefined(s1) || isNullOrUndefined(s2)) {
        return s1 === s2;
    }
    if (typeof s1 !== 'string' || typeof s2 !== 'string') {
        return false;
    }
    return s1.toLowerCase() === s2.toLowerCase();
};

/**
  * @param {string} s1
  * @param {string} s2
  * @return {boolean} a boolean represents if two strings are equal
 */
export const stringsEqual = (s1, s2, caseSensetive) => {
    if (isNullOrUndefined(s1) || isNullOrUndefined(s2)) {
        return s1 === s2;
    }
    if (typeof s1 !== 'string' || typeof s2 !== 'string') {
        try {
            return caseSensetive ? String(s1) === String(s2)
                : String(s1).toLowerCase() === String(s2).toLowerCase();
        } catch (error) {
            console.error(error);
            return false;
        }

    }
    return caseSensetive ? s1 === s2
        : String(s1).toLowerCase() === String(s2).toLowerCase();
};

/**
  * @param {Object} object
  * @param {string} key
  * @return {any} value
 */
export function getParameterCaseInsensitive(object, key) {
    return object[Object.keys(object)
        .find(k => k.toLowerCase() === key.toLowerCase())
    ];
}

/**
  * @param {Object} object
  * @param {string} key1
  * @param {string} key2
  * @return {any} value
 */

export function searchParameterCaseInsensitive(object, key1, key2, key3) {
    return object[Object.keys(object)
        .find(k => k.toLowerCase().includes(key1.toString().toLowerCase())
            && k.toLowerCase().includes(key2.toString().toLowerCase())
            && k.toLowerCase().includes(key3.toString().toLowerCase()))
    ];
}

/**
  * @param {Object} object
  * @param {string} key
  * @return {any} value
 */
export function searchParametersCaseInsensitive(object, key) {
    return Object.keys(object)
        .filter(k => k.toLowerCase().includes(key.toString().toLowerCase()))
        .reduce((obj, key) => {
            obj[key] = object[key];
            return obj;
        }, {});
}


/**
  * @param {Array} source
  * @param {Array} destination
  * @param {number} index
 */
export function moveElementAtIndex(source, target, index) {
    let element = source.splice(index, 1);
    target.push(element[0]);
}



/**
  * @param {number} max
  * @return {number} value
 */
export function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

/**
  * @param {any} v
  * @return {boolean} result
 */
export function isFunction(v) {
    return typeof v === 'function';
}