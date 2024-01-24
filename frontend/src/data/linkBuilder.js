import { isNullOrUndefined } from '../utils/objectUtils';

const FIELD_FILTERS_KEY = 'fieldFilters';
const NEW_FILTER_KEY = 'ff';

export function buildQueryURL(route, params) {
    let url = new URL(route);
    if (params) {
        let hasFieldFilters = params[FIELD_FILTERS_KEY] ? true : false;
        let filtersString = '';

        if (hasFieldFilters) {
            let filtersObject = params[FIELD_FILTERS_KEY];
            Object.keys(params[FIELD_FILTERS_KEY]).forEach((keyValue) => {
                filtersString += FIELD_FILTERS_KEY + '[' + keyValue + ']=' + filtersObject[keyValue] + '&';
            });

            delete params[FIELD_FILTERS_KEY];
        }

        let hasNewFilter = params[NEW_FILTER_KEY] ? true : false;
        let newFilterString = '';
        if (hasNewFilter) {
            let newFilterArray = params[NEW_FILTER_KEY];
            newFilterArray.forEach((filter, index) => {
                let fString = Object.keys(filter)
                    .map(key => key + ':' + filter[key])
                    .join(',');

                newFilterString += 'ff[' + index + ']=' + fString + '&';
            });

            delete params[NEW_FILTER_KEY];
        }

        url.search += '&' + new URLSearchParams(params).toString();
        if (hasFieldFilters) {
            url.search += '&' + filtersString;
        }
        if (hasNewFilter) {
            url.search += '&' + newFilterString;
        }
    }

    return url;
}

export function toQueryString(obj, objectName) {
    if (isNullOrUndefined(obj)) {
        return '';
    }


    return '&' +
        Object.keys(obj)
            .map(key => `${objectName}[${key}]=${isNullOrUndefined(obj[key]) ? '' : obj[key].toString()}`)
            .join('&');
}