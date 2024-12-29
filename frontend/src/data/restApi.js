import apiCall from './apiCall.js';

const read = (url, params, token) => {
    //   url = getRouteValue(url);
    return new Promise((resolve, reject) => {

        apiCall(url, params, {}, 'GET', token)
            .then(results => {
                resolve(results);
            }).catch((error) => {
                reject(error);
            });
    });
};

const write = (url, params, bodyparams, token) => {
    return new Promise((resolve, reject) => {

        apiCall(url, params, bodyparams, 'POST', token)
            .then(results => {
                resolve(results);
            }).catch((error) => {
                reject(error);
            });
    });
};

export { read, write };